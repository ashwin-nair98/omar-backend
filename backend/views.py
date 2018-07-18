from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

# Create your views here.
@csrf_exempt
def get(request):
    if request.method == 'POST':
        print(request.session.session_key)
        return JsonResponse({'text': 'Success'})