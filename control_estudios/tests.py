from django.test import TestCase

from control_estudios.models import Curso


class CursoTests(TestCase):
    """En esta clase van todas las pruebas del modelo Curso."""

    def test_creacion_curso(self):
        # Caso de uso esperado
        nuevo_curso = Curso(nombre="Titulo", comision=1000)
        nuevo_curso.save()

        # Compruebo que el curso fue creado y la data fue guardada correctamente
        self.assertEqual(Curso.objects.count(), 1)
        self.assertEqual(nuevo_curso.nombre, "Titulo")
        self.assertEqual(nuevo_curso.comision, 1000)

    def test_curso_str(self):
        nuevo_curso = Curso(nombre="Python", comision=20000)
        nuevo_curso.save()

        # Compruebo que el método __str__ funciona como se espera
        self.assertEqual(nuevo_curso.__str__(), "Python (20000)")
