from django import forms

class cursoFormulario(forms.Form):
    nombre = forms.CharField(required=True, max_length=64)
    comision = forms.CharField(required=True, max_length=400)
