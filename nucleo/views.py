"""Telas de consulta, cadastro, edição e exclusão de colaboradores."""

from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ColaboradorForm
from .models import Colaborador


def home(request):
    """Lista e pesquisa; todas as consultas vêm do banco SQLite."""
    busca = request.GET.get('busca', '').strip()
    colaboradores = Colaborador.objects.all().order_by('nome', 'id')

    if busca:
        colaboradores = colaboradores.filter(
            Q(nome__icontains=busca) | Q(telefone__icontains=busca)
        )

    return render(request, 'nucleo/index.html', {
        'colaboradores': colaboradores,
        'busca': busca,
        'total_colaboradores': Colaborador.objects.count(),
        'quantidade_encontrada': colaboradores.count(),
    })


def tela_criar(request):
    """Exibe o formulário de um novo colaborador."""
    return render(request, 'nucleo/forms/criar.html', {
        'form': ColaboradorForm(),
    })


def salvar(request):
    """Grava um novo colaborador. Não permite gravação via GET."""
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    form = ColaboradorForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Colaborador cadastrado com sucesso! Você pode cadastrar outro colaborador.')
        return redirect('nucleo-criar')

    messages.error(request, 'Não foi possível cadastrar o colaborador. Confira os campos informados.')
    return render(request, 'nucleo/forms/criar.html', {'form': form}, status=400)


def tela_editar(request, pk):
    """Atualiza o mesmo registro, mantendo seu ID e os demais dados."""
    colaborador = get_object_or_404(Colaborador, pk=pk)
    if request.method == 'POST':
        form = ColaboradorForm(request.POST, instance=colaborador)
        if form.is_valid():
            form.save()
            messages.success(request, 'Colaborador atualizado com sucesso!')
            return redirect('nucleo-inicial')
        messages.error(request, 'Não foi possível atualizar o colaborador. Confira os campos informados.')
        status = 400
    else:
        form = ColaboradorForm(instance=colaborador)
        status = 200

    return render(request, 'nucleo/forms/editar.html', {
        'form': form,
        'colaborador': colaborador,
    }, status=status)


def tela_excluir(request, pk):
    """Mostra a confirmação e exclui somente mediante POST com CSRF."""
    colaborador = get_object_or_404(Colaborador, pk=pk)
    if request.method == 'POST':
        colaborador.delete()
        messages.success(request, 'Colaborador excluído com sucesso!')
        return redirect('nucleo-inicial')

    return render(request, 'nucleo/forms/excluir.html', {
        'colaborador': colaborador,
    })
