from django.test import TestCase

from control_estudios.models import curso


class cursoTests(TestCase):
    """En esta clase van todas las pruebas del modelo curso."""

    def test_creacion_curso(self):
        # caso uso esperado
        curso = curso(nombre="Titulo", comision=1000)
        curso.save()

        # Compruebo que el curso fue creado y la data fue guardad correctamente
        self.assertEqual(curso.objects.count(), 1)
        self.assertEqual(curso.nombre, "Titulo")
        self.assertEqual(curso.comision, 1000)

    def test_curso_str(self):
        curso = curso(nombre="Python", comision=20000)
        curso.save()

        # Compruebo el str funciona como se desea
        self.assertEqual(curso.__str__(), "Python (20000)")
