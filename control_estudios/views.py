from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from control_estudios.forms import cursoFormulario
from control_estudios.models import Estudiante, curso


@login_required
def listar_estudiantes(request):
    # No usado
    contexto = {
        "profesor": "Pedro",
        "estudiantes": Estudiante.objects.all(),
    }
    http_response = render(
        request=request,
        template_name='control_estudios/lista_estudiantes.html',
        context=contexto,
    )
    return http_response


def listar_cursos(request):
    # Data de pruebas, más adelante la llenaremos con nuestros cursos de verdad
    contexto = {
        "cursos": curso.objects.all(),
    }
    http_response = render(
        request=request,
        template_name='control_estudios/lista_cursos.html',
        context=contexto,
    )
    return http_response


def crear_curso_version_1(request):
    if request.method == "POST":
        # Guardado de datos
        data = request.POST  # request.POST es un diccionario

        # creo un curso en memoria RAM
        curso = curso(nombre=data['nombre'], comision=data['comision'])

        # .save lo guarda en la base de datos
        curso.save()

        # Redirecciono al usuario a la lista de cursos
        url_exitosa = reverse('lista_cursos')
        return redirect(url_exitosa)
    else:  # GET
        # Descargar formulario inicial
        http_response = render(
            request=request,
            template_name='control_estudios/formulario_curso_a_mano.html',
        )
        return http_response


@login_required
def crear_curso(request):
    if request.method == "POST":
        # Guardado de datos
        # Creo un objeto formulario con la data que envio el usuario
        formulario = cursoFormulario(request.POST)

        if formulario.is_valid():
            data = formulario.cleaned_data  # es un diccionario
            nombre = data["nombre"]
            comision = data["comision"]
            # creo un curso en memoria RAM
            nuevo_curso = curso(nombre=nombre, comision=comision, creador=request.user)
            # Lo guardan en la Base de datos
            nuevo_curso.save()

            # Redirecciono al usuario a la lista de cursos
            url_exitosa = reverse('lista_cursos')  # estudios/cursos/
            return redirect(url_exitosa)
    else:  # GET
        # Descargar formulario inicial
        formulario = cursoFormulario()
    http_response = render(
        request=request,
        template_name='control_estudios/formulario_curso.html',
        context={'formulario': formulario}
    )
    return http_response


def buscar_cursos(request):
    if request.method == "POST":
        data = request.POST
        busqueda = data["busqueda"]
        # Filtro simple
        # cursos = curso.objects.filter(comision__contains=busqueda)
        # Ejemplo filtro avanzado
        cursos = curso.objects.filter(
            Q(nombre__icontains=busqueda) | Q(comision__contains=busqueda)
        )

        contexto = {
            "cursos": cursos,
        }
        http_response = render(
            request=request,
            template_name='control_estudios/lista_cursos.html',
            context=contexto,
        )
        return http_response


@login_required
def eliminar_curso(request, id):
    # obtienes el curso de la base de datos
    curso_eliminar = curso.objects.get(id=id)
    if request.method == "POST":
        # borra el curso de la base de datos
        curso_eliminar.delete()
        # redireccionamos a la URL exitosa
        url_exitosa = reverse('lista_cursos')
        return redirect(url_exitosa)


@login_required
def editar_curso(request, id):
    curso_editar = curso.objects.get(id=id)
    if request.method == "POST":
        formulario = cursoFormulario(request.POST)

        if formulario.is_valid():
            data = formulario.cleaned_data
            curso_editar.nombre = data['nombre']
            curso_editar.comision = data['comision']
            curso_editar.save()

            url_exitosa = reverse('lista_cursos')
            return redirect(url_exitosa)
    else:  # GET
        # Obtener datos actuales del curso_editar y prellenar el formulario
        inicial = {
            'nombre': curso_editar.nombre,
            'comision': curso_editar.comision,
        }
        formulario = cursoFormulario(initial=inicial)
        
    return render(
        request=request,
        template_name='control_estudios/formulario_curso.html',
        context={'formulario': formulario},
    )
    
# Vistas de estudiantes (basadas en clases)
class EstudianteListView(LoginRequiredMixin, ListView):
    model = Estudiante
    template_name = 'control_estudios/lista_estudiantes.html'


class EstudianteCreateView(LoginRequiredMixin, CreateView):
    model = Estudiante
    fields = ('apellido', 'nombre', 'email', 'dni')
    success_url = reverse_lazy('lista_estudiantes')

    # Así se guarda la info del creador en vistas basadas en clase
    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        # Agregamos la información del creador
        self.object.creador = self.request.user
        self.object.save()
        return super().form_valid(form)


class EstudianteDetailView(LoginRequiredMixin, DetailView):
    model = Estudiante
    success_url = reverse_lazy('lista_estudiantes')


class EstudianteUpdateView(LoginRequiredMixin, UpdateView):
    model = Estudiante
    fields = ('apellido', 'nombre', 'email', 'dni')
    success_url = reverse_lazy('lista_estudiantes')


class EstudianteDeleteView(LoginRequiredMixin, DeleteView):
    model = Estudiante
    success_url = reverse_lazy('lista_estudiantes')
    