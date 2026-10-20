from django.test import TestCase
from django.urls import reverse

from .models import Tarea


class TareaModelTests(TestCase):
    def test_crear_tarea(self):
        tarea = Tarea.objects.create(titulo="Escribir reporte")
        self.assertEqual(str(tarea), "Escribir reporte")
        self.assertFalse(tarea.completada)

    def test_orden_por_fecha_reciente_primero(self):
        primera = Tarea.objects.create(titulo="Primera")
        segunda = Tarea.objects.create(titulo="Segunda")
        tareas = list(Tarea.objects.all())
        self.assertEqual(tareas[0], segunda)
        self.assertEqual(tareas[1], primera)


class TareaViewTests(TestCase):
    def test_lista_tareas_responde_200(self):
        response = self.client.get(reverse("lista_tareas"))
        self.assertEqual(response.status_code, 200)

    def test_crear_tarea_via_formulario(self):
        response = self.client.post(reverse("lista_tareas"), {"titulo": "Revisar PR"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Tarea.objects.filter(titulo="Revisar PR").exists())

    def test_completar_tarea(self):
        tarea = Tarea.objects.create(titulo="Pendiente")
        self.client.get(reverse("completar_tarea", args=[tarea.id]))
        tarea.refresh_from_db()
        self.assertTrue(tarea.completada)

    def test_eliminar_tarea(self):
        tarea = Tarea.objects.create(titulo="Para borrar")
        self.client.get(reverse("eliminar_tarea", args=[tarea.id]))
        self.assertFalse(Tarea.objects.filter(id=tarea.id).exists())

    def test_endpoint_salud(self):
        response = self.client.get(reverse("salud"))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"status": "ok", "app": "django-cicd-practica"})
