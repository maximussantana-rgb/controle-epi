"""Telas de consulta, cadastro, edição e exclusão de colaboradores."""

from django.contrib import messages
from django.db.models import Q
from django.db.models.deletion import ProtectedError
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ColaboradorForm, EquipamentoForm, EmprestimoForm, EmprestimoStatusForm
from .models import Colaborador, Equipamento, Emprestimo


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
        try:
            colaborador.delete()
        except ProtectedError:
            messages.error(request, 'Este colaborador possui registros de EPI vinculados e não pode ser excluído.')
            return redirect('nucleo-inicial')
        messages.success(request, 'Colaborador excluído com sucesso!')
        return redirect('nucleo-inicial')

    return render(request, 'nucleo/forms/excluir.html', {
        'colaborador': colaborador,
    })


def equipamento_lista(request):
    busca = request.GET.get('busca', '').strip()
    equipamentos = Equipamento.objects.all()
    if busca:
        equipamentos = equipamentos.filter(Q(nome__icontains=busca) | Q(numero_ca__icontains=busca))
    return render(request, 'nucleo/equipamentos/lista.html', {
        'equipamentos': equipamentos, 'busca': busca,
        'total': Equipamento.objects.count(), 'quantidade': equipamentos.count(),
    })


def equipamento_criar(request):
    form = EquipamentoForm(request.POST or None)
    status = 200
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Equipamento cadastrado com sucesso! Você pode cadastrar outro.')
            return redirect('equipamento-criar')
        messages.error(request, 'Não foi possível cadastrar o equipamento. Confira os dados.')
        status = 400
    return render(request, 'nucleo/equipamentos/formulario.html', {
        'form': form, 'editando': False,
    }, status=status)


def equipamento_editar(request, pk):
    equipamento = get_object_or_404(Equipamento, pk=pk)
    form = EquipamentoForm(request.POST or None, instance=equipamento)
    status = 200
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Equipamento atualizado com sucesso!')
            return redirect('equipamento-lista')
        messages.error(request, 'Não foi possível atualizar o equipamento. Confira os dados.')
        status = 400
    return render(request, 'nucleo/equipamentos/formulario.html', {
        'form': form, 'editando': True, 'equipamento': equipamento,
    }, status=status)


def equipamento_excluir(request, pk):
    equipamento = get_object_or_404(Equipamento, pk=pk)
    if request.method == 'POST':
        try:
            equipamento.delete()
        except ProtectedError:
            messages.error(request, 'Este equipamento está vinculado a entregas de EPI e não pode ser excluído.')
            return redirect('equipamento-lista')
        messages.success(request, 'Equipamento excluído com sucesso!')
        return redirect('equipamento-lista')
    return render(request, 'nucleo/equipamentos/excluir.html', {'equipamento': equipamento})


def emprestimo_lista(request):
    """Consulta operacional para escolher qual empréstimo atualizar; NÃO é relatório."""
    emprestimos = Emprestimo.objects.select_related('colaborador', 'equipamento').all()
    return render(request, 'nucleo/emprestimos/lista.html', {
        'emprestimos': emprestimos, 'total': emprestimos.count(),
    })


def emprestimo_criar(request):
    form = EmprestimoForm(request.POST or None)
    status = 200
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Entrega de EPI cadastrada com sucesso!')
            return redirect('emprestimo-criar')
        messages.error(request, 'Não foi possível cadastrar a entrega. Confira os campos.')
        status = 400
    return render(request, 'nucleo/emprestimos/criar.html', {'form': form}, status=status)


def emprestimo_editar(request, pk):
    emprestimo = get_object_or_404(
        Emprestimo.objects.select_related('colaborador', 'equipamento'), pk=pk
    )
    form = EmprestimoStatusForm(request.POST or None, instance=emprestimo)
    status = 200
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Status da entrega atualizado com sucesso!')
            return redirect('emprestimo-lista')
        messages.error(request, 'Não foi possível atualizar o status. Confira os campos.')
        status = 400
    return render(request, 'nucleo/emprestimos/editar.html', {
        'emprestimo': emprestimo, 'form': form,
    }, status=status)
