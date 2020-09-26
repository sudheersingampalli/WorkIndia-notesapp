from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Notesmodel

def home(request):

    return render(request,'notesapp/home.html');

@csrf_exempt
def user(request):

    '''
    View to Create a user
    :param request:
    :return:
    : curl command : curl -H 'Content-Type: application/json' -d '{"username": "sudheer","password":"sudheer"}'
    -X POST http://127.0.0.1:8000/notesapp/user
    '''
    received_json_data= json.loads(request.body.decode('utf-8'))
    if request.method == 'POST':
        try:
            received_json_data = json.loads(request.body.decode('utf-8'))
            user = User.objects.get(username=received_json_data.get('username'))
            messages.warning(request, "Username already exists")
            return JsonResponse('User already exists',safe=False)
        except User.DoesNotExist:
            user = User.objects.create_user(received_json_data["username"], password=received_json_data["password"])
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            response = {'status': 'account created'}
            return JsonResponse(response,safe=False)
    else:
        response = {'status': 'Please do a POST  request'}
        return JsonResponse(response,safe=False)

@csrf_exempt
def auth(request):
    '''
    View to authenticate and login a user
    :param request:
    :return:
    : curl : curl -H 'Content-Type: application/json' -d '{"username": "sudheer3","password":"sudheer"}'
    -X POST http://127.0.0.1:8000/notesapp/auth
    '''
    received_json_data = json.loads(request.body.decode('utf-8'))
    if request.method == 'POST':
        user = authenticate(username=received_json_data.get('username', None),
                            password=received_json_data.get('password', None))
        if user is not None:
            login(request, user)
            user = User.objects.get(username=received_json_data.get('username', None))
            user_id = user.id
            response = {'status': 'Success', 'userId': user_id}
            return JsonResponse(response,safe=False)
        else:
            response = {'status': 'Incorrect username password'}
            return JsonResponse(response,safe=False)


@csrf_exempt
def listnotes(request, user_id=None):
    '''
    list all the notes of the user
    :param request:
    :return:
    :curl: curl -H 'Content-Type: application/json' -X GET http://127.0.0.1:8000/notesapp/sites/list/<userId>
    '''
    if request.method == 'GET':
        print('parameters -->', user_id)
        listofnotes = Notesmodel.objects.filter(user_id=user_id).values('description')
        return JsonResponse(list(listofnotes), safe=False)
    else:
        response = {"status": "Use GET method"}
        return JsonResponse(response, safe=False)


@csrf_exempt
def sites(request, user_id=None):
    '''
    save notes to the DB for a user
    :param request:
    :return:
    :curl: curl -H 'Content-Type: application/json' -d '{"description":"Sudheer is here"}'
    -X POST http://127.0.0.1:8000/notesapp/sites/<userId>
    '''
    if request.method == 'POST':
        received_json_data = json.loads(request.body.decode('utf-8'))
        note = Notesmodel()
        user = User.objects.get(id=user_id)
        note.user_id = user
        note.description = received_json_data.get("description")
        try:
            note.save()
        except:
            response = {'status' : 'Something failed'}
        else:
            response = {'status': 'success'}
    else:
        response = {'status': 'Use GET method'}
    return JsonResponse(response, safe=False)
