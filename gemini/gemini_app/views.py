from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from .models import ChatBot
from django.http import HttpResponseRedirect, JsonResponse
import google.generativeai as genai

# Create your views here.
# API Key
genai.configure(api_key = 'AIzaSyAw4Ihj-njNXeM875Bud9f3y6CyvEDt-hI')

@login_required
def ask_question(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        model = genai.GenerativeModel('gemini-pro')
        chat = model.start_chat()
        response = chat.send_message(text)
        user = request.user
        ChatBot.objects.create(text_input=text, gemini_output=response.text, user=user)
        # Extract necessary data from response
        response_data = {
            "text": response.text,  # Assuming response.text contains the relevant response data
            # Add other relevant data from response if needed
        }
        return JsonResponse({"data": response_data})
    else:
        return HttpResponseRedirect(
            reverse("chat")
        )  # Redirect to chat page for GET requests

@login_required
def chat(request):
    user = request.user
    chats = ChatBot.objects.filter(user=user)
    return render(request, "chat_bot.html", {"chats": chats})
