from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import *
from django.views.decorators.csrf import csrf_exempt
from django.utils.datastructures import MultiValueDictKeyError
import time

from nodesk_server import settings

def ping(request) :
    return HttpResponse(time.strftime("%c"))

@csrf_exempt
def login(request):
    response = HttpResponse()
    try:
        if request.method == 'GET':
            username = request.GET['username']
            password = request.GET['password']
        elif request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
#    except MultiValueDictKeyError as e:
    except:
        username = ""
        password = ""

    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
        else:
            response.status_code = 401
            response.reason_phrase = "User disabled"
    else:
        response.status_code = 401
        response.reason_phrase = "User or/and Password incorrect"
    return response

def logout(request):
    auth_logout(request)
    return HttpResponse()
