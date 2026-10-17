"""Formulário de cadastro e edição de colaboradores."""

from django import forms

from .models import Colaborador


class ColaboradorForm(forms.ModelForm):
    class Meta:
        model = Colaborador
        fields = ['nome', 'telefone']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome completo do colaborador',
                'autocomplete': 'name',
                'autofocus': True,
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(71) 99999-9999',
                'autocomplete': 'tel',
                'inputmode': 'tel',
            }),
        }
        labels = {'nome': 'Nome completo', 'telefone': 'Telefone'}

    def clean_nome(self):
        nome = self.cleaned_data['nome'].strip()
        if not nome:
            raise forms.ValidationError('Informe o nome do colaborador.')
        return nome

    def clean_telefone(self):
        telefone = self.cleaned_data['telefone'].strip()
        if not telefone:
            raise forms.ValidationError('Informe um telefone.')
        return telefone
