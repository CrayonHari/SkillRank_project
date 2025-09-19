import os
import re
import json
import streamlit as st
import pdfplumber
from db import Document, SessionLocal
from dotenv import load_dotenv
import google.generativeai as genai
import pandas as pd

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Streamlit App Title
st.set_page_config(page_title="LLM Document Analyzer", layout="wide")
st.title("LLM Document Analyzer with Gemini")

# File Upload Section
uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file is not None:
    st.success("✅ PDF uploaded successfully!")
    
    # Extract text from PDF
    text_content = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            text_content += page.extract_text() or ""
    
    if text_content.strip():        
        st.subheader("Extracted Text from PDF")
        st.text_area("Scroll to view document text", text_content, height=400)
        # Document Classification with Gemini
        st.subheader("Document Classification")
        candidate_labels = ["invoice", "contract", "report"]
        
        with st.spinner("Classifying with Gemini..."):
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            prompt = f"""
        Classify the following document into one of these categories: {candidate_labels}.
        Respond in this format: <category_name>, <confidence_percent_as_number>

        Document text: {text_content}
        """
            
            response = model.generate_content(prompt)
            output = response.text.strip()

            # Split the output into category and confidence
            try:
                predicted_type, confidence = [x.strip() for x in output.split(",")]
                confidence = float(confidence)  # convert to number
            except:
                predicted_type = output
                confidence = None

            st.write(f"Predicted type: **{predicted_type.upper()}**")
            if confidence is not None:
                # st.progress(int(confidence))

                st.write(f"Confidence: **{confidence:.2f}%**")
        
        # Missing Fields & Improvement Recommendations
        st.subheader("Detailed Missing Fields Analysis & Recommendations")
        
        # Define required fields for different document types
        required_map = {
            "invoice": [
                {"field": "invoice_number", "critical": True},
                {"field": "amount", "critical": True},
                {"field": "due_date", "critical": True},
                {"field": "tax", "critical": False},
                {"field": "bill_to", "critical": True},
                {"field": "bill_from", "critical": True},
            ],
            "contract": [
                {"field": "party_1", "critical": True},
                {"field": "party_2", "critical": True},
                {"field": "signature", "critical": True},
                {"field": "date", "critical": True},
                {"field": "payment_terms", "critical": False},
            ],
        }
        
        fields_to_check = required_map.get(predicted_type, [])
        
        if fields_to_check:
            with st.spinner("Asking Gemini to check required fields and provide improvement recommendations..."):
                check_prompt = f"""
                The document type is {predicted_type}.
                Required fields with priority (critical or optional): {fields_to_check}.
                
                For each field, return a JSON array of objects with:
                - "field": field name
                - "status": either "PRESENT" or "MISSING"
                - "value": extracted text if present, empty if missing
                - "priority": "critical" or "optional"
                - "recommendation": specific suggestion to complete or improve this field
                
                Document text: {text_content}
                """
                
                check_response = model.generate_content(check_prompt)
                
                # Safe JSON parsing
                raw_text = check_response.text.strip()
                match = re.search(r'\[.*\]', raw_text, re.DOTALL)
                
                if match:
                    improvement_report = json.loads(match.group())
                else:
                    st.error("Could not parse Gemini JSON. Showing raw output:")
                    st.text(raw_text)
                    improvement_report = []
                
                # Display table with critical missing highlight
                if improvement_report:
                    df = pd.DataFrame(improvement_report)
                    
                    def highlight_critical(row):
                        if row['status'] == 'MISSING' and row['priority'] == 'critical':
                            return ['background-color: #ff9999'] * len(row)
                        return [''] * len(row)
                    
                    st.dataframe(df.style.apply(highlight_critical, axis=1))
                    
                    # Download option
                    st.download_button(
                        "Download Checklist",
                        json.dumps(improvement_report, indent=2),
                        file_name=f"{uploaded_file.name}_report.json"
                    )
                    
                    # Save to Database
                    session = SessionLocal()
                    new_doc = Document(
                        filename=uploaded_file.name,
                        content=text_content,
                        predicted_type=predicted_type,
                        field_report=improvement_report,
                        improvement_report=improvement_report
                    )
                    session.add(new_doc)
                    session.commit()
                    session.close()
                    
                    st.success(f"Document '{uploaded_file.name}' saved with detailed reports in database.")
                else:
                    st.warning("Gemini returned no valid JSON. Please check raw output above.")
        else:
            st.warning("No required field rules defined for this document type.")
    else:
        st.error("No extractable text found in this PDF. It might be scanned or image-based.")
