from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
import whisper
from googletrans import Translator

class VoiceTranslateView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        audio = request.FILES['audio']
        source_lang = request.data.get('sourceLang', 'en')
        target_lang = request.data.get('targetLang', 'ne')  # default: Nepali

        # Load model
        model = whisper.load_model("base")

        # Save file temporarily
        with open("temp_audio.mp3", "wb+") as f:
            for chunk in audio.chunks():
                f.write(chunk)

        # Transcribe
        result = model.transcribe("temp_audio.mp3", language=source_lang)
        recognized_text = result['text']

        # Translate
        translator = Translator()
        translated = translator.translate(recognized_text, src=source_lang, dest=target_lang)

        return Response({
            "recognized_text": recognized_text,
            "translated_text": translated.text
        })
