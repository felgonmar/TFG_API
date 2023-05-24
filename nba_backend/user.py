from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from .models import User
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

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
    email = request.POST.get('email')
    password = request.POST.get('password')
    
    user = User.objects.filter(email=email).first()
    if user is None:
       
        return HttpResponse("User not found", status=404)

    if check_password(password, user.password_hash):
        
        request.session['user_id'] = user.id
        return HttpResponse("Successfully logged in", status=200)
    else:
        
        return HttpResponse("Wrong password", status=401)

def log_out(request):
    logout(request)
    return HttpResponse("User logged out successfully")

@login_required
def get_user_data(request):
    user = request.user
    user_data = {
        'id': user.id,
        'email': user.email,
        'name': user.name,
        'last_name': user.last_name,
        'full_name': user.full_name
    }
    return JsonResponse(user_data)
