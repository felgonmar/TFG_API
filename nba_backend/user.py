from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from .models import User
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


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
        # El usuario no existe
        return HttpResponse("Usuario no encontrado", status=404)

    if check_password(password, user.password_hash):
        # La contraseña es correcta
        request.session['user_id'] = user.id
        return HttpResponse("Inicio de sesión exitoso", status=200)
    else:
        # La contraseña es incorrecta
        return HttpResponse("Contraseña incorrecta", status=401)

def log_out(request):
    logout(request)
    return HttpResponse("User logged out successfully")
