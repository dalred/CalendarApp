import json
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login as login_user, authenticate

from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login_user(request, user)
            return JsonResponse({'username': username,
                                 'password': password})
            #return HttpResponse('Authenticated successfully')
            #return HttpResponseRedirect("/")
        else:
            return JsonResponse({'error': 'Invalid login or password'})