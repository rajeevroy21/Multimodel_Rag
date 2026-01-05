from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.sessions.backends.db import SessionStore
from rest_framework.decorators import api_view
import google.generativeai as genai
from rest_framework.response import Response
from decouple import config
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os

# keyVaultName = os.environ["GEMINIKEY"]
# vault_url = f"https://{keyVaultName}.vault.azure.net"
# credential = DefaultAzureCredential()
# client = SecretClient(vault_url=vault_url, credential=credential)
# api_key = client.get_secret("$GEMINI_API_KEY").value

API_KEY = config("GEMINI_API_KEY", default=None)
# API_KEY = os.environ["GEMINI_API_KEY"]

_gemini_model = None


def _get_api_key():
    return config("GEMINI_API_KEY", default=None)


def _get_text_model_name():
    return config("GEMINI_TEXT_MODEL", default="models/gemini-flash-latest")


def _get_gemini_model():
    global _gemini_model
    if _gemini_model is None:
        api_key = _get_api_key()
        if not api_key:
            raise ValueError("GEMINI_API_KEY not configured")
        genai.configure(api_key=api_key)
        _gemini_model = genai.GenerativeModel(_get_text_model_name())
    return _gemini_model

hist_dict = {}
dialogue_dict = {}

@api_view(['POST'])
def generate_text(request):
    if request.method == 'POST':
        try:
            gemini_model = _get_gemini_model()
            session_id = request.data.get('session_id')
            system_prompt = request.data.get('system_prompt', '')
            prompt = request.data.get('prompt')

            if session_id not in hist_dict:
                hist_dict[session_id] = []
            
            chat = gemini_model.start_chat(history=hist_dict[session_id])
            response = chat.send_message([system_prompt,
                                          prompt],
                                          stream=True)
            response.resolve()

            hist_dict[session_id] = chat.history
            
            return Response({"generated_text": response.text})
        except ValueError as e:
            print(e)
            return Response({"generated_text": str(e)}, status=500)
        except Exception as e:
            print(e)
            return Response({"generated_text": "Something went wrong. Please try again later."})
