import nltk
from nltk.tokenize import word_tokenize
from difflib import get_close_matches

nltk.download('punkt')

def get_response(request):
    if request.method == "GET":
        user_message = request.GET.get("message", "").lower()
        user_tokens = word_tokenize(user_message)

        # Obtener todas las preguntas en la base de datos
        all_questions = [pregunta.texto.lower() for pregunta in Pregunta.objects.all()]
        
        # Buscar coincidencias cercanas con la pregunta del usuario
        best_match = get_close_matches(user_message, all_questions, n=1, cutoff=0.6)
        
        if best_match:
            pregunta = Pregunta.objects.get(texto__iexact=best_match[0])
            respuesta = Respuesta.objects.filter(pregunta=pregunta).first()
            bot_response = respuesta.texto if respuesta else "No encontré una respuesta exacta."
        else:
            bot_response = "No sé la respuesta, pero puedes enseñarme nuevas preguntas."

        return JsonResponse({"response": bot_response})
