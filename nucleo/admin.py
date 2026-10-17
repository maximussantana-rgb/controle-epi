from django.contrib import admin

from .models import Colaborador


@admin.register(Colaborador)
class ColaboradorAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'telefone')
    search_fields = ('nome', 'telefone')
