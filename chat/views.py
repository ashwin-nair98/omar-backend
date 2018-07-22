from django.shortcuts import render

# Create your views here.
def chat_interface(request):
    return render(request, 'bot/interface.html', {})

def home(request):
    return render(request, 'bot/home.html', {})

def interface_arabic(request):
    return render(request, 'bot/interface_arabic.html', {})

def interface_english(request):
    return render(request, 'bot/interface_english.html', {})
