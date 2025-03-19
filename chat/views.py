from asyncio import Task
from django.forms import BaseForm
import openai # type: ignore
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

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


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST) # type: ignore
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm() # type: ignore
    return render(request, 'registration/register.html', {'form': form})

def create_task(request):
    if request.method == 'POST':
        form = BaseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = BaseForm()
    return render(request, 'tasks/create_task.html', {'form': form})

# Vista para editar una tarea
def edit_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        form = BaseForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = BaseForm(instance=task)
    return render(request, 'tasks/edit_task.html', {'form': form})