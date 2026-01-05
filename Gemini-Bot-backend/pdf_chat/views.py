from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_classic.chains.question_answering import load_qa_chain
from langchain_core.prompts import PromptTemplate
from decouple import config
import google.generativeai as genai
import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
import pdfplumber
import shutil

API_KEY = config("GEMINI_API_KEY", default=None)
# API_KEY = os.environ["GEMINI_API_KEY"]


def _get_api_key():
    return config("GEMINI_API_KEY", default=None)


def _get_pdf_chat_model_name():
    return config("GEMINI_TEXT_MODEL", default="models/gemini-2.5-flash")

@api_view(['POST'])
def pdf_chat(request):
    if request.method == 'POST':
        try:
            api_key = _get_api_key()
            if not api_key:
                return Response({"generated_text": "GEMINI_API_KEY not configured"}, status=500)

            genai.configure(api_key=api_key)
            session_id = request.data.get('session_id')
            pdf = request.data.get('pdf')
            prompt = request.data.get('prompt')

            if not pdf:
                return Response({"generated_text": "No PDF uploaded"}, status=400)

            # Save PDF to temp file for safe processing
            os.makedirs('pdf_chat/pdfs/', exist_ok=True)
            pdf_path = f"pdf_chat/pdfs/{session_id}.pdf"
            with open(pdf_path, 'wb') as f:
                for chunk in pdf.chunks():
                    f.write(chunk)

            text = ""
            # Parsing PDF and saving text
            with pdfplumber.open(pdf_path) as pd:
                for page_number in range(len(pd.pages)):
                    page = pd.pages[page_number]
                    if page:
                        extracted = page.extract_text()
                        if extracted:
                            text += extracted
            
            # Clean up PDF file
            if os.path.exists(pdf_path):
                os.remove(pdf_path)

            if not text:
                return Response({"generated_text": "Could not extract text from the PDF."}, status=400)

            # Splitting the text extracted from text got from PDF
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
            text_chunks = text_splitter.split_text(text)

            if not text_chunks:
                return Response({"generated_text": "PDF text is empty after splitting."}, status=400)

            # Create Vector Embedding of text
            # Use text-embedding-004 which is newer and might have better availability/limits
            embeddings = GoogleGenerativeAIEmbeddings(google_api_key=api_key, model="models/text-embedding-004")
            vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)

            # Store embeddings locally
            os.makedirs('pdf_chat/embeddings/', exist_ok=True)
            vector_store.save_local(f'pdf_chat/embeddings/{session_id}_index')

            # Load saved embeddings
            user_embeddings = FAISS.load_local(f'pdf_chat/embeddings/{session_id}_index', embeddings, allow_dangerous_deserialization=True)

            # Perform similarity search between user prompt and pdf uploaded
            docs = user_embeddings.similarity_search(prompt)

            # Prompt template to ask questions to PDF
            prompt_template = '''
                              Answer question as detailed as possible from the provided context, make sure to provide all the details.
                              If the answer is not in provided context, just say "your question's answer is not available in the PDF provided", do not provide the wrong answer\n\n
                              Context: \n{context}?\n
                              Question: \n{question}\n

                              Answer:
                              '''
            
            # Langchain model declaration
            model = ChatGoogleGenerativeAI(model=_get_pdf_chat_model_name(), temperature=0.5, google_api_key=api_key)
            prompting = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
            chain = load_qa_chain(model, chain_type="stuff", prompt=prompting)
            
            # Storing model answer
            response = chain({"input_documents": docs, "question": prompt}, return_only_outputs=True)

            # Delete embeddings after QA
            shutil.rmtree(f'pdf_chat/embeddings/{session_id}_index', ignore_errors=True)

            return Response({"generated_text": response['output_text']})
        
        except Exception as e:
            print(f"Error in pdf_chat: {e}")
            import traceback
            traceback.print_exc()
            return Response({"generated_text": f"An error occurred: {str(e)}"}, status=200)
