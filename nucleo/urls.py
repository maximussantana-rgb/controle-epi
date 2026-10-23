"""Rotas do sistema de gerenciamento de EPIs."""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='nucleo-inicial'),
    # Mantém as URLs da etapa anterior para links já existentes.
    path('criar', views.tela_criar, name='nucleo-criar'),
    path('salvar', views.salvar, name='nucleo-salvar'),
    path('editar/<int:pk>/', views.tela_editar, name='nucleo-editar'),
    path('excluir/<int:pk>/', views.tela_excluir, name='nucleo-excluir'),
    path('equipamentos/', views.equipamento_lista, name='equipamento-lista'),
    path('equipamentos/novo/', views.equipamento_criar, name='equipamento-criar'),
    path('equipamentos/<int:pk>/editar/', views.equipamento_editar, name='equipamento-editar'),
    path('equipamentos/<int:pk>/excluir/', views.equipamento_excluir, name='equipamento-excluir'),
    path('emprestimos/', views.emprestimo_lista, name='emprestimo-lista'),
    path('emprestimos/novo/', views.emprestimo_criar, name='emprestimo-criar'),
    path('emprestimos/<int:pk>/editar/', views.emprestimo_editar, name='emprestimo-editar'),
]
