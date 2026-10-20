from django.urls import path

from . import views

urlpatterns = [
    path("", views.lista_tareas, name="lista_tareas"),
    path("tareas/<int:tarea_id>/completar/", views.completar_tarea, name="completar_tarea"),
    path("tareas/<int:tarea_id>/eliminar/", views.eliminar_tarea, name="eliminar_tarea"),
    path("salud/", views.salud, name="salud"),
]
