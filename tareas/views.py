from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import Tarea


def lista_tareas(request):
    if request.method == "POST":
        titulo = request.POST.get("titulo", "").strip()
        descripcion = request.POST.get("descripcion", "").strip()
        if titulo:
            Tarea.objects.create(titulo=titulo, descripcion=descripcion)
        return redirect("lista_tareas")

    tareas = Tarea.objects.all()
    contexto = {
        "tareas": tareas,
        "total": tareas.count(),
        "pendientes": tareas.filter(completada=False).count(),
    }
    return render(request, "tareas/lista.html", contexto)


def completar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)
    tarea.completada = not tarea.completada
    tarea.save()
    return redirect("lista_tareas")


def eliminar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)
    tarea.delete()
    return redirect("lista_tareas")


def salud(request):
    """Endpoint simple de healthcheck para validar el despliegue en Docker."""
    return JsonResponse({"status": "ok", "app": "django-cicd-practica"})
