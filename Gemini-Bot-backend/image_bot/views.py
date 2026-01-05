from rest_framework.decorators import api_view
import google.generativeai as genai
from rest_framework.response import Response
from PIL import Image
from decouple import config
import os

API_KEY = config("GEMINI_API_KEY", default=None)
# API_KEY = os.environ["GEMINI_API_KEY"]

# Model Initialization
_vision_model = None


def _get_api_key():
    return config("GEMINI_API_KEY", default=None)


import traceback

def _get_vision_model_name():
    return config("GEMINI_VISION_MODEL", default="models/gemini-2.5-flash")

def _get_vision_model():
    global _vision_model
    if _vision_model is None:
        api_key = _get_api_key()
        if not api_key:
            raise ValueError("GEMINI_API_KEY not configured")
        genai.configure(api_key=api_key)
        _vision_model = genai.GenerativeModel(_get_vision_model_name())
    return _vision_model

@api_view(['POST'])
def image_bot(request):
    if request.method == 'POST':
        try:
            session_id = request.data.get('session_id')
            system_prompt = request.data.get('system_prompt', '')
            prompt = request.data.get('prompt')
            image = request.data.get('image')

            os.makedirs('image_bot/images/', exist_ok=True)
            image_path = f"image_bot/images/{session_id}.png"
            with open(image_path, 'wb') as f:
                for chunk in image.chunks():
                    f.write(chunk)

            img = Image.open(image_path)
            
            model = _get_vision_model()
            
            content = []
            if system_prompt:
                content.append(system_prompt)
            if prompt:
                content.append(prompt)
            content.append(img)
            
            response = model.generate_content(content)
            # Check if response was blocked or invalid
            if not response.parts:
                 print(f"Response blocked or empty. Feedback: {response.prompt_feedback}")
                 return Response({'generated_text': "Error: The response was blocked by safety filters."})
                 
            text = response.text
            
            img.close() # Close image before deleting
            if os.path.exists(image_path):
                os.remove(image_path)

            return Response({'generated_text': text})
        except Exception as e:
            print(f"Error in image_bot: {e}")
            traceback.print_exc()
            if hasattr(e, 'response'):
                print(f"Response feedback: {e.response.prompt_feedback}")
            return Response({"generated_text": "Something went wrong. Please try again later. Error: " + str(e)}, status=200)