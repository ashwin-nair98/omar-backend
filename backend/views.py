from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from .watson_assistant.conversation import Conversation
from pprint import pprint

# Create your views here.
@csrf_exempt
def get(request):
    if request.method == 'POST':
        conversation = Conversation()
        if 'context' in request.POST:
            context = request.POST['context']
        else:
            context = {}
        # pprint(context)
        message= request.POST['msg']

        response_data = conversation.message(message, context)
        response_message = response_data['text']
        response_context = response_data['context']
        return JsonResponse({
            'text': response_message,
            'context': response_context
            })

def initialize(request):
    if request.method == 'GET':
        conversation = Conversation()
        response_data = conversation.start()
        response_message = response_data['text']
        response_context = response_data['context']
        return JsonResponse({
            'text': response_message,
            'context': response_context
            })