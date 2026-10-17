"""Rotas do cadastro de colaboradores."""
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='nucleo-inicial'),
    # Mantidas as URLs já existentes para não quebrar o projeto original.
    path('criar', views.tela_criar, name='nucleo-criar'),
    path('salvar', views.salvar, name='nucleo-salvar'),
    path('editar/<int:pk>/', views.tela_editar, name='nucleo-editar'),
    path('excluir/<int:pk>/', views.tela_excluir, name='nucleo-excluir'),
]
