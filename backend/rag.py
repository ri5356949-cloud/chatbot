import os
from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader

# load .env from project root
load_dotenv()

# OpenAI client
client = OpenAI()

# in-memory PDF storage
pdf_texts = []


def load_user_pdf(path: str):
    """
    User ke upload kiye gaye PDF ko read karta hai
    aur text memory me store karta hai
    """
    global pdf_texts
    pdf_texts = []

    reader = PdfReader(path)
    for page in reader.pages:
        text = page.extract_text()
        if text:
            pdf_texts.append(text)


def ask_question(question: str):
    """
    1) Pehle PDF se jawab dhoondta hai
    2) Agar PDF me na mile to OpenAI se jawab leta hai
    """

    # 🔹 STEP 1: PDF search
    if pdf_texts:
        combined_text = " ".join(pdf_texts).lower()
        if question.lower() in combined_text:
            return {
                "answer": combined_text[:600],
                "source": "pdf"
            }

    # 🔹 STEP 2: OpenAI fallback
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are a helpful customer support assistant."},
            {"role": "user", "content": question}
        ]
    )

    return {
        "answer": response.choices[0].message.content,
        "source": "openai"
    }
