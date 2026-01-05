# 🚀 Google’s Gemini Bot — Multi-Modal AI Assistant ✅

> ✅ A powerful AI assistant built using Google’s Gemini models, featuring a Django REST backend and an interactive Streamlit frontend.

Gemini Bot enables:
✅ Natural conversations  
✅ Image understanding  
✅ PDF-based question answering using RAG (Retrieval-Augmented Generation)

--------------------------------------------------

## ✨ Key Highlights ✅

✅ Powered by Google Gemini LLMs  
✅ Multi-modal support (Text + Image + PDF)  
✅ Clean backend–frontend architecture  
✅ Real-world AI deployment example  
✅ Scalable and extensible design  

--------------------------------------------------

## 🧠 Features Overview ✅

🤖 Conversational Chatbot  
✅ Chat naturally with Gemini  
✅ Custom system prompts to define behavior  
✅ Suitable for assistants, tutors, and domain bots  

🖼️ Image Analysis Bot  
✅ Upload images (JPG, PNG, WEBP)  
✅ Ask questions about image content  
✅ Uses gemini-2.5-flash vision model  

📄 Chat with PDF (RAG)  
✅ Upload PDF documents  
✅ Automatic text extraction  
✅ Embeddings via text-embedding-004  
✅ Semantic search using FAISS  
✅ Accurate, context-aware answers  

--------------------------------------------------

## 🏗️ Project Architecture (Short) ✅

Gemini Bot follows a **client–server architecture** with clear separation between UI and AI logic.

User  
→ Streamlit Frontend (UI)  
→ Django REST Backend (Business Logic)  
→ Google Gemini Models & RAG Pipeline  
→ Response back to User  

### Components
- **Frontend (Streamlit)**  
  Handles user interaction, file uploads, and API calls.

- **Backend (Django + DRF)**  
  Manages text chat, image analysis, and PDF-based RAG logic.

- **AI Layer**  
  - Gemini `gemini-2.5-flash` for text & image understanding  
  - `text-embedding-004` + FAISS for PDF semantic search

This architecture is **modular, scalable, and production-ready** 🚀


--------------------------------------------------

## ⚙️ Setup Instructions ✅

🔹 Prerequisites  
✅ Python 3.10+ (Tested with Python 3.13)  
✅ Google Gemini API Key  
➡ https://aistudio.google.com/

--------------------------------------------------

## 🔧 Backend Setup ✅

Step 1: Navigate to backend
cd Gemini-Bot-backend

Step 2: Create & activate virtual environment
python3 -m venv .venv  
source .venv/bin/activate  
(Windows: .venv\Scripts\activate)

Step 3: Install dependencies
pip install -r requirements.txt

Step 4: Create .env file
GEMINI_API_KEY=your_actual_api_key_here  
GEMINI_TEXT_MODEL=models/gemini-2.5-flash  
GEMINI_VISION_MODEL=models/gemini-2.5-flash  

Step 5: Run backend server
python manage.py migrate  
python manage.py runserver 8001  

Backend URL:
http://localhost:8001

--------------------------------------------------

## 🎨 Frontend Setup ✅

Step 1: Navigate to frontend
cd Gemini-Bot-main

Step 2: Create & activate virtual environment
python3 -m venv .venv  
source .venv/bin/activate  
(Windows: .venv\Scripts\activate)

Step 3: Install dependencies
pip install -r requirements.txt

Step 4: Run Streamlit app
streamlit run app.py

Frontend URL:
http://localhost:8501

--------------------------------------------------

## 🧪 How to Use ✅

✅ Chatbot Mode  
- Start general conversation  
- Set system prompt (example: You are a coding mentor)

✅ Image Bot  
- Upload an image  
- Ask questions about objects or text  

✅ Chat with PDF  
- Upload PDF  
- Ask document-specific questions  

--------------------------------------------------

## 🛠️ Troubleshooting ✅

❗ Quota / Rate limit exceeded  
- Happens mainly during PDF embeddings  
- Wait briefly and retry  

❗ Model not found error  
- Ensure these models are enabled:
  - gemini-2.5-flash
  - text-embedding-004

--------------------------------------------------

## 🧰 Tech Stack ✅

✅ Python  
✅ Django & Django REST Framework  
✅ Streamlit  
✅ Google Gemini API  
✅ LangChain  
✅ FAISS (Vector Store)  
✅ PDFPlumber  

--------------------------------------------------

## 🌟 Future Enhancements ✅

☑️ Authentication & chat history  
☑️ Multi-PDF support  
☑️ Streaming responses  
☑️ UI enhancements  
☑️ Cloud deployment (AWS / GCP)

--------------------------------------------------

## 🙌 Final Note ✅

This project demonstrates production-ready AI engineering using:
✅ Large Language Models  
✅ RAG pipelines  
✅ REST APIs  
✅ Modern UI frameworks  

Perfect for learning, interviews, and real-world AI applications 🚀
