from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from .models import User
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json

#delete this if we want to deploy in prod
@csrf_exempt
def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name', '')
        last_name = request.POST.get('last_name', '')
        full_name = name + ' ' + last_name
        password = request.POST.get('password')
        user = User(full_name=full_name, email=email, name=name, last_name=last_name, password_hash=password)
        user.save()
        return HttpResponse("User registered successfully")
    else:
        return HttpResponse("Invalid request")

@csrf_exempt
def login(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')

        try:
            body = json.loads(body_unicode)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        email = body.get('email') 
        password = body.get('password')

        user = User.objects.filter(email=email).first()
        if user is None:
            return JsonResponse({'error':"User not found"}, status=404)

        if check_password(password, user.password_hash):
            request.session['user_id'] = user.id
            user_data = {
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'last_name': user.last_name,
                'full_name': user.full_name
            }
            return JsonResponse({'Response':"Successfully logged in", 'status':200, 'user': user_data}, status=200)
        else:
            return JsonResponse({'error':"Wrong password"}, status=401)
    return JsonResponse({'error': 'Invalid method'}, status=400)

    
def log_out(request):
    logout(request)
    return HttpResponse("User logged out successfully")

#
@csrf_exempt
def get_user_data(request):
    if(request.user.id):
        user = request.user
        user_data = {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'last_name': user.last_name,
            'full_name': user.full_name
        }
        return JsonResponse(user_data)
    else:
        return JsonResponse({'error': 'No user is logged in'}, status=400)
        
def get_user_by_id(id):
    user = User.objects.get(id=id)
    if(user is not None):
        user_data = {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'last_name': user.last_name,
            'full_name': user.full_name
        }
        return JsonResponse(user_data, status=200)
    return JsonResponse('Not found', status= 404)
    
