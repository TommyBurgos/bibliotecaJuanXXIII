
from django.urls import path
from . import views

urlpatterns = [    
    path('', views.hello),
    path('login/', views.vistaLogin, name='login'),
    path('autenticado/', views.custom_login, name='custom_login'),
    path('registro/',views.vistaRegistro),
    path('dashboard-adm/', views.admin_dashboard, name='dashboard-adm'),
    path('dashboard-adm/registroLibros/', views.vistaRegistroLibro, name='registroLibros'),
    path('dashboard-adm/actualizarLibros/', views.vistaActualizarLibro, name='actualizarLibros'),
    path('dashboard-adm/eliminarLibros/', views.vistaEliminarLibro, name='eliminarLibros'),
    path('dashboard-adm/verLibrosDigitales/', views.lista_libros_digitales, name='ver_libro_digital'),
    path('dashboard-adm/detalleUsuarios/', views.detalleUsuarios, name='ver_libro_digital'),
    path('dashboard-adm/verLibrosDigitales/<int:libro_id>/', views.ver_libro_digital, name='ver_libro_digital'),

    path('dashboard-adm/revisarSolicitudes/', views.vistaAdminRevisarSolicitudes, name='adminRevisarSolicitudes'),
    
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('registroExitoso/',views.registroExitoso),
    path('student_dashboard/solicitarLibro/',views.vistaSolicitarLibro, name='solicitarLibro'),
    path('student_dashboard/solicitarLibro/<int:libro_id>',views.solicitar_libro),
    path('student_dashboard/misLecturas/',views.vistaMisLecturas),
    path('student_dashboard/misLibrosLeidos/',views.vistaLibrosLeidos),
    path('student_dashboard/solicitudesRealizadas/',views.vistaSolicitudesRealizadas),
    path('student_dashboard/misFavoritos/',views.vistaFavoritos),
    path('student_dashboard/verLibrosDigitales/', views.lista_libros_digitales_Estudiante, name='ver_libro_digital'),
    path('student_dashboard/verLibrosDigitales/<int:libro_id>/', views.ver_libro_digital_Estudiante, name='ver_libro_digital'),
    path('logout/', views.signout),
    


]
