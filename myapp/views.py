# from django.shortcuts import render
from datetime import timezone
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.csrf import ensure_csrf_cookie
from .inventory_services import prestar_libro, devolver_libro
from django.http import FileResponse
from django.utils.timezone import now, timedelta
from django.middleware.csrf import rotate_token
from .models import Libro, HistorialInventario, Inventario, SolicitudLibro, LibroDigital
from django.contrib import messages
from django.db.models import Q
from user.models import User
from .forms import LibroForm
import re


def lista_libros_digitales(request):
    libros = LibroDigital.objects.all()
    user=request.user
    imgPerfil=user.picture
    return render(request, 'vistaAdmin/lista_libros_digitales.html', {
        'libros': libros,
        'imgPerfil': imgPerfil,        
        'usuario':user.username
        })

def ver_libro_digital(request, libro_id):
    libro = get_object_or_404(LibroDigital, pk=libro_id)
    response = FileResponse(open(libro.archivo_pdf.path, 'rb'), content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{libro.titulo}.pdf"'
    return response

def lista_libros_digitales_Estudiante(request):
    libros = LibroDigital.objects.all()
    user=request.user
    imgPerfil=user.picture
    return render(request, 'vistaAdmin/lista_libros_digitales.html', 
                  {'libros': libros,
                   'imgPerfil': imgPerfil,        
                    'usuario':user.username})

def ver_libro_digital_Estudiante(request, libro_id):
    libro = get_object_or_404(LibroDigital, pk=libro_id)
    user=request.user
    imgPerfil=user.picture
    response = FileResponse(open(libro.archivo_pdf.path, 'rb'), content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{libro.titulo}.pdf"'
    return response



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
    total_solicitudes = SolicitudLibro.objects.count()
    

    # 1. Cantidad de usuarios cuyo rol es igual a 2
    cantidad_usuarios_rol_2 = User.objects.filter(rol__id=2).count()
    
    # 2. Cantidad de libros registrados
    cantidad_libros = Libro.objects.count()

    # 3. Lista de la cantidad de estudiantes registrados en la última semana
    ultima_semana = now() - timedelta(days=7)
    estudiantes_ultima_semana = User.objects.filter(rol__id=2, date_joined__gte=ultima_semana)
    diaActual=now()

    ultimas3semanas = now() - timedelta(days=28)
    histoSolicitud=SolicitudLibro.objects.filter(fecha_solicitud__gte=ultimas3semanas)
    histoSolicitudes_ultimaS=SolicitudLibro.objects.filter(fecha_solicitud__gte=ultima_semana).count
    print(f"Aqui van las solicitudes {histoSolicitud}")
    # Pasar los datos al contexto
    context = {
        'cantidad_usuarios_rol_2': cantidad_usuarios_rol_2,
        'cantidad_libros': cantidad_libros,
        'estudiantes_ultima_semana': estudiantes_ultima_semana,
        'imgPerfil': imgPerfil,
        'ultima_semana':ultima_semana,
        'diaActual':diaActual,
        'total_solicitudes': total_solicitudes,
        'usuario':user.username,
        'histoSolicitud':histoSolicitud,
        'histoSolicitudes_ultimaS':histoSolicitudes_ultimaS
    }    
    return render(request, 'vistaAdmin/index.html', context)

def detalleUsuarios(request):
    user = request.user
    busqueda = request.GET.get("buscar")
    usuarios = User.objects.all().order_by('-date_joined')
    if busqueda:
        usuarios = User.objects.filter(Q(username=busqueda)
                                       | Q(first_name=busqueda)
                                       | Q(last_name=busqueda)
                                       | Q(email=busqueda)
                                       | Q(ciudad=busqueda)).distinct()
        print("entre al if de busqueda")
    print("LISTADO DE USUARIOS")
    print(usuarios)
    if request.method == 'POST':
        try:
            script_js = f"""
            alert("Usuario Creado correctamente")
            """
            context = {'script_js': script_js}
            print("Apenas ingrese")
            user = User.objects.create_user(username=request.POST['idNumber'],
                                            password=request.POST['password'],
                                            first_name=request.POST['firstName'],
                                            last_name=request.POST['lastName'],
                                            email=request.POST['email'],     
                                            nacimiento=request.POST['birthdate'],
                                            ciudad=request.POST['city'],
                                            direccion=request.POST['address'],
                                            rol_id=request.POST['userRole'])
            print("Casi guardo")
            rol_id=request.POST['userRole']
            user.save()
            # doctor=Medico.objects.create(estado_id=1, idDispositivo_id=1,idUsuario_id=user.id)
            # doctor.save()
            print("Se guardo correctamente")
            print(user.rol_id)
            
            return render(request, 'vistaAdmin/detalleUsuarios.html', {'context': context, 'usuarios': usuarios})
        except:
            print("no se pudo")
            return HttpResponse('Usuario ya existe')
    return render(request, 'vistaAdmin/detalleUsuarios.html', {'usuarios': usuarios})




@login_required
def student_dashboard(request):
    #Datos usuario actual
    user = request.user
    imgPerfil=user.picture
    # Código de la vista del estudiante
    return render(request, 'estudiante/index.html',{
        'imgPerfil': imgPerfil,
    })

def signout(request):
    logout(request)
    rotate_token(request)  # Gira el token CSRF para la nueva sesión
    return redirect('login')

@login_required
def vistaRegistroLibro(request):
    libros = Libro.objects.all()
    print("estos son los libros")
    print(libros)
    libros_con_inventario = []
    print("inventario")
    print(libros_con_inventario)
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

@login_required
def vistaAdminRevisarSolicitudes(request):
    solicitudesPendientes = SolicitudLibro.objects.filter(estado='pendiente')
    print("aqui viene el for de solicitudes")
    user=request.user
    imgPerfil=user.picture
    for soli in solicitudesPendientes:
        print(soli.id)
    print(solicitudesPendientes)
     # Obtener todas las solicitudes de libros
    solicitudes = SolicitudLibro.objects.select_related('estudiante', 'libro').all()
    # Enviar las solicitudes a la plantilla
    context = {
        'solicitudes': solicitudes,
        'usuario':user.username,
        'imgPerfil': imgPerfil
    }
    if request.method == "POST":
        solicitud_id = request.POST.get('solicitud_id')
        accion = request.POST.get('nuevo_estado')  # 'aceptar' o 'rechazar'
        print("esta es la accion gg")
        print(accion)

        # Obtén la solicitud
        solicitud = get_object_or_404(SolicitudLibro, id=solicitud_id)
        print(solicitud)

        # Obtén el inventario del libro solicitado
        inventario = Inventario.objects.filter(libro=solicitud.libro).first()
        print(inventario)
        print(not inventario)

        if not inventario:
            # Maneja el caso en que no se haya registrado un inventario para ese libro
            messages.error(request, "No se ha encontrado un inventario para este libro.")
            return redirect('dashboard-adm')  # Cambia esto por la vista correspondiente
        print("opciones")
        print(accion == 'aprobada')
        print(accion == 'rechazada')
        print(inventario.cantActual)
        print("previo al if")
        if accion == 'aprobada':
            print("dentro del primer if")
            print(inventario.cantActual)
            # Verifica si hay stock disponible
            if inventario.cantActual > 0:
                print("ingrese a este if")
                # Disminuye la cantidad de libros en el inventario
                inventario.cantActual -= 1
                print(inventario.cantActual)
                inventario.save()

                # Actualiza el estado de la solicitud a 'aceptada'
                solicitud.estado = 'aprobada'
                solicitud.save()

                messages.success(request, "Solicitud aceptada y libro asignado.")
            else:
                messages.error(request, "No hay suficiente stock para aceptar esta solicitud.")
        elif accion == 'rechazada':
            # Actualiza el estado de la solicitud a 'rechazada'
            solicitud.estado = 'rechazada'
            solicitud.save()

            messages.success(request, "Solicitud rechazada.")   
        return render(request,'vistaAdmin/revisarSolicitudes.html',context) 
    
    
    print("SOLICITUDES")    
    print(solicitudesPendientes)
    return render(request,'vistaAdmin/revisarSolicitudes.html',context)


def gestionCambioSolicitud(request,solicitud_id):
    solicitud_id = request.POST.get('solicitud_id')
    print(solicitud_id)
    accion = request.POST.get('nuevo_estado')  # 'aceptar' o 'rechazar'
    print("la accion")
    print(accion)

    # Obtén la solicitud
    solicitud = get_object_or_404(SolicitudLibro, id=solicitud_id)

    # Obtén el inventario del libro solicitado
    inventario = Inventario.objects.filter(libro=solicitud.libro).first()
    print(inventario)

    if not inventario:
        print("Entre al not del inventario")
        # Maneja el caso en que no se haya registrado un inventario para ese libro
        messages.error(request, "No se ha encontrado un inventario para este libro.")
        return redirect('dashboard-adm')  # Cambia esto por la vista correspondiente
    print(accion == 'aceptar')
    if accion == 'aprobada':
        print("Verifica si hay stock disponible")
        if inventario.cantActual > 0:
            aceptar_solicitud(request,solicitud_id)    
    elif accion == 'rechazada':
        rechazar_solicitud(request,solicitud_id)
    return redirect('dashboard-adm')  # Cambia esto por la vista correspondiente

def aceptar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudLibro, id=solicitud_id)
    inventario = Inventario.objects.filter(libro=solicitud.libro).first()
    print("esta es la solicitud")
    print(solicitud)
    if inventario.cantActual > 0:
        inventario.cantActual -= 1
        inventario.save()
        # Actualiza el estado de la solicitud a 'aceptada'
        solicitud.estado = 'aceptada'
        solicitud.save()
        messages.success(request, "Solicitud aceptada y libro asignado.")

        return redirect('adminRevisarSolicitudes')
    else:
        return HttpResponse("No hay suficientes copias disponibles")

def rechazar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudLibro, id=solicitud_id)
    solicitud.estado = 'rechazada'
    solicitud.fecha_respuesta = timezone.now()
    solicitud.save()
    return redirect('adminRevisarSolicitudes')


# Vista para ver el historial
def ver_historial(request, libro_id):
    user = request.user
    imgPerfil=user.picture
    libro = get_object_or_404(Libro, id=libro_id)
    historial = HistorialInventario.objects.filter(libro=libro).order_by('-fecha_cambio')
    return render(request, 'historial_libro.html', {'libro': libro, 'imgPerfil': imgPerfil, 'historial': historial})

@login_required
def vistaActualizarLibro(request):
    user = request.user
    imgPerfil=user.picture 
    return render(request,"vistaAdmin/actualizarLibro.html",{
        'imgPerfil': imgPerfil,
        'usuario':user.username,
    } )

@login_required
def vistaEliminarLibro(request):    
    user = request.user
    imgPerfil=user.picture 
    return render(request,"vistaAdmin/eliminarLibro.html", {'imgPerfil': imgPerfil, 'usuario':user.username})


#VISTA DEL ESTUDIANTE
@login_required
def vistaSolicitarLibro(request):
    user = request.user
    imgPerfil=user.picture 
    libros = Libro.objects.all()
    print("estos son los libros")
    print(libros)
    libros_con_inventario = []
    print(libros_con_inventario)
    user=request.user
    imgPerfil=user.picture
    for libro in libros:
        try:
            inventario = Inventario.objects.get(libro=libro)
        except Inventario.DoesNotExist:
            inventario = None
        if inventario!= None:
            libros_con_inventario.append({
                'libro': libro,
                'inventario': inventario
            })
    print(libros_con_inventario)
    return render(request, "estudiante/solicitarLibro.html",{        
        'libros': libros,
        'libros_con_inventario': libros_con_inventario,
        'imgPerfil': imgPerfil,
        'usuario':user.username
    })
@login_required
def solicitar_libro(request, libro_id):
    user = request.user
    imgPerfil=user.picture 
    libro = get_object_or_404(Libro, id=libro_id)
    estudiante = request.user
    SolicitudLibro.objects.create(estudiante=estudiante, libro=libro)
    return redirect('solicitarLibro')  # Redireccionar a una página adecuada

@login_required
def vistaMisLecturas(request):
    user = request.user
    imgPerfil=user.picture 
    return render(request, "estudiante/misLecturas.html",{'imgPerfil': imgPerfil})

@login_required
def vistaLibrosLeidos(request):
    user = request.user
    imgPerfil=user.picture 
    return render(request, "estudiante/librosLeidos.html",{'imgPerfil': imgPerfil})

@login_required
def vistaSolicitudesRealizadas(request):
    user = request.user
    imgPerfil=user.picture 
    estudiante = request.user
    solicitudes = SolicitudLibro.objects.filter(estudiante=estudiante).order_by('-fecha_solicitud')
    return render(request, "estudiante/soliRealizadas.html",{
        'imgPerfil': imgPerfil, 'solicitudes': solicitudes})

@login_required
def vistaFavoritos(request):
    user = request.user
    imgPerfil=user.picture 
    return render(request, "estudiante/favoritos.html",{'imgPerfil': imgPerfil})

