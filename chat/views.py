from django.shortcuts import render

# Create your views here.
def chat_interface(request):
    return render(request, 'bot/interface.html', {})