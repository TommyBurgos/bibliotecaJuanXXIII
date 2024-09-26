
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
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('registroExitoso/',views.registroExitoso),
    path('logout/', views.signout),
    


]
