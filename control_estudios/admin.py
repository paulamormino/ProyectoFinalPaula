from django.contrib import admin

from control_estudios.models import Estudiante, Profesor, curso, Entregable

admin.site.register(Estudiante)
admin.site.register(Profesor)
admin.site.register(curso)
admin.site.register(Entregable)
