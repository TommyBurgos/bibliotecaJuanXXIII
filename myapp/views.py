# from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.csrf import ensure_csrf_cookie
from .inventory_services import prestar_libro, devolver_libro
from django.utils.timezone import now, timedelta
from django.middleware.csrf import rotate_token
from .models import Libro, HistorialInventario, Inventario
from django.db.models import Q
from user.models import User
from .forms import LibroForm
import re


# Create your views here.
def hello(request):
    return render(request,"index.html")

@ensure_csrf_cookie
def vistaLogin(request):
    print("Me meti aca?")
    #if request.method != "POST":
    #    print("Ocurrio un post")
    #    return redirect('custom_login')  # Redirige a la vista de autenticación
    return render(request, 'login.html')
    


def vistaRegistro(request):
    return render(request,"registro.html")

def registroExitoso(request):
    print(request.POST)
    print(request.POST['password'] == request.POST['confirmPassword'])
    user = request.POST['idNumber']        
    usuario = User.objects.filter(Q(username=user))
    print('ps1 ->'+request.POST['password'])
    print('ps2 ->'+request.POST['confirmPassword'])
    print('usuario //'+ request.POST['idNumber'])
    if request.POST['password'] == request.POST['confirmPassword']:
        try:
            password = request.POST.get('password')
            confirmPassword = request.POST.get('confirmPassword')
            idNumber = request.POST.get('idNumber')
            email = request.POST.get('email')
            print("Apenas ingrese")

            # print(user.rol_id)
            idNumber = request.POST['idNumber']
            print(len(idNumber))
            print(len(password) < 8)
            print("Valor de verdad")
            print(re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', password))
            if password != confirmPassword or len(password) < 8 or not re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', password):
                print("Entre al primer error")
                errorP = 'La contraseña debe tener al menos 8 caracteres y contener una combinación de letras y números'
                print(errorP)
            # Validar email
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                errorEmail = 'El formato del correo electrónico no es válido'
                print("Entre al segundo error")

            # Validar idNumber
            if len(idNumber) != 10:
                errorCedula = 'El número de cédula debe tener exactamente 10 caracteres'
                print("Entre al tercer error")
            if 'errorP' in locals() or 'errorEmail' in locals() or 'errorCedula' in locals():
                print("Entre al cuarto error")
                return render(request, 'registro.html', {
                    'errorP': errorP if 'errorP' in locals() else None,
                    'errorEmail': errorEmail if 'errorEmail' in locals() else None,
                    'errorCedula': errorCedula if 'errorCedula' in locals() else None,
                    'formData': {
                        'idNumber': idNumber,
                        'firstName': request.POST.get('firstName'),
                        'lastName': request.POST.get('lastName'),
                        'email': email,                        
                        'birthdate': request.POST.get('birthdate'),
                        'city': request.POST.get('city'),
                        'address': request.POST.get('address'),
                    }
                })
            print("Antes de crear el usuario")
            user = User.objects.create_user(username=request.POST['idNumber'],
                                            password=request.POST['password'],
                                            first_name=request.POST['firstName'],
                                            last_name=request.POST['lastName'],
                                            email=request.POST['email'],                                            
                                            nacimiento=request.POST['birthdate'],                                            
                                            ciudad=request.POST['city'],
                                            direccion=request.POST['address'],
                                            rol_id=2)
            print("Casi guardo")
            user.save()
            print("Guarde el usuario")
            #paciente = Paciente.objects.create(estado_id=1, idDispositivo_id=1, idUsuario_id=user.id)
            print("Cree el paciente")
            #paciente.save()
            login(request, user)
            print("Se guardo correctamente")
            print(user.rol_id)
            return vistaLogin(request)
        except:
            print("no se pudo")
            
            return render(request, 'registro.html', {
                    'errorP': errorP if 'errorP' in locals() else None,
                    'errorEmail': errorEmail if 'errorEmail' in locals() else None,
                    'errorCedula': errorCedula if 'errorCedula' in locals() else None,
                    'formData': {
                        'idNumber': idNumber,
                        'firstName': request.POST.get('firstName'),
                        'lastName': request.POST.get('lastName'),
                        'email': email,                        
                        'birthdate': request.POST.get('birthdate'),
                        'city': request.POST.get('city'),
                        'address': request.POST.get('address'),
                    }
                })
    return HttpResponse('Contraseñas no coinciden')


def custom_login(request):
    print("entre a la funcion custom")
    if request.method == "POST":  
        print("Estoy en post")      
        user = authenticate(request, username=request.POST['idNumber'], password= request.POST
        ['password'])
        print("Ya autentique el usuario")
        if user is not None:
            login(request, user)
            print("Loguie al usuario")
            rol = user.rol_id  # Asignar rol después de la autenticación   
            print(rol)         
            if rol == 1:
                print("Ingrese al rol 1")
                return redirect('dashboard-adm')
            elif rol == 2:
                return redirect('student_dashboard')
        else:
            # Manejar error de autenticación
            return render(request, 'login.html', {'error': 'Credenciales inválidas'})
    return redirect('login')


#PROOOOOBANDO

#CIERRE DE PRUEB

def redireccionLogin(request):
    if request.method == "POST": 
        return redirect('login') 


@login_required
def admin_dashboard(request):
    #Datos usuario actual
    user = request.user
    imgPerfil=user.picture
    # 1. Cantidad de usuarios cuyo rol es igual a 2
    cantidad_usuarios_rol_2 = User.objects.filter(rol__id=2).count()
    
    # 2. Cantidad de libros registrados
    cantidad_libros = Libro.objects.count()

    # 3. Lista de la cantidad de estudiantes registrados en la última semana
    ultima_semana = now() - timedelta(days=7)
    estudiantes_ultima_semana = User.objects.filter(rol__id=2, date_joined__gte=ultima_semana)

    # Pasar los datos al contexto
    context = {
        'cantidad_usuarios_rol_2': cantidad_usuarios_rol_2,
        'cantidad_libros': cantidad_libros,
        'estudiantes_ultima_semana': estudiantes_ultima_semana,
        'imgPerfil': imgPerfil,
        'usuario':user.username
    }    
    return render(request, 'vistaAdmin/index.html', context)


@login_required
def student_dashboard(request):
    # Código de la vista del estudiante
    return render(request, 'estudiante/index.html')

def signout(request):
    logout(request)
    rotate_token(request)  # Gira el token CSRF para la nueva sesión
    return redirect('login')

@login_required
def vistaRegistroLibro(request):
    libros = Libro.objects.all()
    libros_con_inventario = []
    user=request.user
    imgPerfil=user.picture
    for libro in libros:
        try:
            inventario = Inventario.objects.get(libro=libro)
        except Inventario.DoesNotExist:
            inventario = None
        libros_con_inventario.append({
            'libro': libro,
            'inventario': inventario
        })

    if request.method == 'POST':
        form = LibroForm(request.POST, request.FILES)  # Asegúrate de manejar archivos correctamente
        if form.is_valid():
            try:
                # Guarda el nuevo libro a través del formulario
                form.save()
                print("Se guardó correctamente")
                return render(request, 'vistaAdmin/registroLibro.html', {'form': LibroForm(), 'libros': libros})
            except Exception as e:
                print(f"No se pudo guardar el libro. Error: {e}")
                return HttpResponse(f"Error al guardar el libro: {e}")
        else:
            print("Formulario no válido")
            print(form.errors)
            return render(request, 'vistaAdmin/registroLibro.html', {'form': form, 'libros': libros})
    
    return render(request, 'vistaAdmin/registroLibro.html', {
        'form': LibroForm(),
        'libros': libros,
        'libros_con_inventario': libros_con_inventario,
        'imgPerfil': imgPerfil,
        'usuario':user.username
    })



# Vista para ver el historial
def ver_historial(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    historial = HistorialInventario.objects.filter(libro=libro).order_by('-fecha_cambio')
    return render(request, 'historial_libro.html', {'libro': libro, 'historial': historial})

def vistaActualizarLibro(request):    
    return render(request,"vistaAdmin/actualizarLibro.html")

def vistaEliminarLibro(request):    
    return render(request,"vistaAdmin/eliminarLibro.html")