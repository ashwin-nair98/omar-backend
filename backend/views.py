from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .watson_assistant.conversation import Conversation, Conversation_Arabic
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
        message= request.POST['msg']
        response_data = conversation.message(message, context)
        response_message = response_data['text']
        response_context = response_data['context']
        return JsonResponse({
            'text': response_message.split('^split'),
            'context': response_context
            })
@csrf_exempt
def initialize(request):
    if request.method == 'GET':
        conversation = Conversation()
        response_data = conversation.start()
        response_message = response_data['text']
        response_context = response_data['context']
        if(request.GET['latitude'] and request.GET['longitude']):
            lat = request.GET['latitude']
            lon = request.GET['longitude']
            response_context['latlong'] = str(lat) + ',' + str(lon)
        elif request.GET['navigator'] is 'NOT_FOUND':
            response_context['latlong'] = '25.095863,55.157950'
        return JsonResponse({
            'text': response_message,
            'context': response_context
            })

@csrf_exempt
def arabic_get(request):
    if request.method == 'POST':
        conversation = Conversation_Arabic()
        if 'context' in request.POST:
            context = request.POST['context']
        else:
            context = {}
        message= request.POST['msg']
        response_data = conversation.message(message, context)
        response_message = response_data['text']
        response_context = response_data['context']
        return JsonResponse({
            'text': response_message.split("^سبلت"),
            'context': response_context
            })


@csrf_exempt
def arabic_initialize(request):
    if request.method == 'GET':
        conversation = Conversation_Arabic()
        response_data = conversation.start()
        response_message = response_data['text']
        response_context = response_data['context']
        if(request.GET['latitude'] and request.GET['longitude']):
            lat = request.GET['latitude']
            lon = request.GET['longitude']
            response_context['latlong'] = str(lat) + ',' + str(lon)
        elif request.GET['navigator'] is 'NOT_FOUND':
            response_context['latlong'] = '25.095863,55.157950'
        return JsonResponse({
            'text': response_message,
            'context': response_context
            })
