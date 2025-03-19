import openai
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render

openai_client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)  # Nuevo cliente OpenAI

def chatbot_view(request):
    return render(request, "chatbot.html")

def get_response(request):
    if request.method == "GET":
        user_message = request.GET.get("message", "")

        try:
            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": "Eres un chatbot experto en programación en Python."},
                          {"role": "user", "content": user_message}]
            )
            bot_response = response.choices[0].message.content
        except Exception as e:
            bot_response = f"Error en la respuesta: {str(e)}"

        return JsonResponse({"response": bot_response})
