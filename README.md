# LLM Document Analyzer

## Overview
LLM Document Analyzer is a Streamlit web application that intelligently analyzes business documents. It can:

- Detect document type (contract, invoice, or report)  
- Identify missing critical and optional fields  
- Provide actionable improvement recommendations  
- Store document analysis results in a database for future reference  

This project uses PDF text extraction, SQLite database, and Gemini LLM API for classification and field analysis.

---

## Demo / Deployed Site
You can access the live application here:  
[**LLM Document Analyzer on Streamlit Cloud**](https://skillrankproject-uuhg2dr4uuxfr8tymxlwka.streamlit.app/)

---

## Features
1. **Document Upload & Processing**  
   - Upload PDF documents via web interface  
   - Extract and display text content  

2. **LLM Document Classification**  
   - Automatically identifies document type using Gemini API  
   - Displays detected type with confidence score  

3. **Missing Fields Analysis & Recommendations**  
   - Detects missing required fields based on document type  
   - Highlights critical missing fields  
   - Provides improvement checklist  
   - Option to download the JSON report  

4. **Database Integration**  
   - Stores uploaded documents and analysis reports in SQLite  

---

## Installation & Running Locally

1. **Clone the repository**  

```bash
git clone https://github.com/CrayonHari/LLM-Document-Analyzer.git
cd LLM-Document-Analyzer

![WhatsApp Image 2025-09-19 at 10 18 31_3dcda80f](https://github.com/user-attachments/assets/b4b5dd69-6301-4962-abe6-cf9e88487c6f)

