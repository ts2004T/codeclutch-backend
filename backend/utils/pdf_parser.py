"""
Utility for parsing PDF resume files.
"""
from typing import Optional
import PyPDF2
from io import BytesIO


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """
    Extract text content from a PDF file.
    
    Args:
        pdf_bytes: Raw bytes of the PDF file
        
    Returns:
        Extracted text as a string
        
    Raises:
        Exception: If PDF parsing fails
    """
    try:
        # Create a PDF reader object from bytes
        pdf_file = BytesIO(pdf_bytes)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        # Extract text from all pages
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        
        return text.strip()
    
    except Exception as e:
        raise Exception(f"Failed to parse PDF: {str(e)}")


def clean_resume_text(text: str) -> str:
    """
    Clean and normalize resume text.
    
    Args:
        text: Raw text extracted from resume
        
    Returns:
        Cleaned text
    """
    # Remove excessive whitespace
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    return '\n'.join(lines)
