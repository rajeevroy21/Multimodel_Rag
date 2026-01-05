# Google's Gemini Bot

**Gemini Bot** is a powerful AI assistant powered by **Google's Gemini models**, featuring a **Django** backend and a **Streamlit** frontend. It allows users to converse with a chatbot, analyze images, and chat with PDF documents using RAG (Retrieval-Augmented Generation).

## Features
- **Conversational Chatbot**: Chat with Gemini using custom system prompts.
- **Image Analysis**: Upload images and ask questions about them using the `gemini-2.5-flash` model.
- **PDF Chat**: Upload PDFs and ask questions about their content. Uses `text-embedding-004` for embeddings and FAISS for vector search.

---

## Project Structure
The project is divided into two main parts:
1.  **Backend (`Gemini-Bot-backend`)**: A Django REST Framework API that handles the logic for text, image, and PDF processing.
2.  **Frontend (`Gemini-Bot-main`)**: A Streamlit application that provides a user-friendly interface to interact with the backend APIs.

---

## Setup Instructions

### Prerequisites
- Python 3.10 or higher (Tested with Python 3.13)
- A Google Gemini API Key (Get it from [Google AI Studio](https://aistudio.google.com/))

### 1. Backend Setup
1.  Navigate to the backend directory:
    ```bash
    cd Gemini-Bot-backend
    ```

2.  Create and activate a virtual environment:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4.  Configure Environment Variables:
    - Create a `.env` file in the `Gemini-Bot-backend` directory.
    - Add your Gemini API Key:
      ```env
      GEMINI_API_KEY=your_actual_api_key_here
      ```
    - (Optional) Configure model names if needed (defaults are set in code):
      ```env
      GEMINI_VISION_MODEL=models/gemini-2.5-flash
      GEMINI_TEXT_MODEL=models/gemini-2.5-flash
      ```

5.  Run Migrations and Start Server:
    ```bash
    python manage.py migrate
    python manage.py runserver 8001
    ```
    The backend will run at `http://localhost:8001`.

### 2. Frontend Setup
1.  Open a new terminal and navigate to the frontend directory:
    ```bash
    cd Gemini-Bot-main
    ```

2.  Create and activate a virtual environment:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4.  Run the Streamlit App:
    ```bash
    streamlit run app.py
    ```
    The app will open in your browser (usually at `http://localhost:8501`).

---

## Usage Guide

1.  **Converse with Chatbot**: Select this option to have a general conversation. You can set a "System Prompt" to define the bot's persona.
2.  **Image-Bot**: Upload an image (JPG, PNG, WEBP) and ask questions about it.
3.  **Chat with PDF**: Upload a PDF document. Once uploaded, you can ask specific questions about the content of the PDF.

## Troubleshooting

-   **500 Errors / Quota Exceeded**: If you encounter errors related to quotas (especially in PDF Chat), it means the API key has hit the rate limit for the embedding model. Wait a minute and try again.
-   **Model Not Found**: Ensure you are using supported models. This project uses `gemini-2.5-flash` and `text-embedding-004`.

## Technologies Used
-   **Python**
-   **Django & Django REST Framework**
-   **Streamlit**
-   **Google Gemini API** (`google-genai`, `langchain-google-genai`)
-   **LangChain**
-   **FAISS** (Vector Store)
-   **PDFPlumber** (PDF Text Extraction)
