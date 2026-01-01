# Gemini-HF-FastAPI
# FastAI-Gemini-Chat

A **FastAPI-based AI Chat System** integrating **Google Gemini** and **Hugging Face LLaMA** models.  
Users can register, login, and interact with either Gemini or Hugging Face endpoints securely using tokens.

---

## Features

- User registration and login with token-based authentication
- Chat with **Google Gemini API**
- Chat with **Hugging Face LLaMA 3.3 (Router API)**
- SQLite database for user management
- Environment variables for secure API keys
- FastAPI auto-generated **Swagger docs** for easy API testing

---

## Project Structure

FastAI-Gemini-Chat/
│
├─ main.py # FastAPI application entry point
├─ database.py # Database connection and session
├─ models.py # SQLAlchemy ORM models
├─ requirements.txt # Project dependencies
├─ user.db # SQLite database
├─ .env # Environment variables for API keys
├─ myenv/ # Python virtual environment
├─ FastAPI_Gemini_HuggingFace_Documentation.docx
└─ README.md




API Endpoints
Endpoint	Method	Description
/register	POST	Register a new user
/login	POST	Login and receive a token
/chat/gemini	POST	Chat with Google Gemini (requires token header)
/chat/huggingface	POST	Chat with Hugging Face LLaMA (requires token header)
/	GET	Root endpoint (welcome message)
