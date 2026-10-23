from django.db import models
from django.utils import timezone

class Colaborador(models.Model):
    nome = models.CharField(max_length=30, null=False, blank=False)
    telefone = models.CharField(max_length=30)

    def __str__(self):
        return self.nome


class Equipamento(models.Model):
    """EPI que pode ser entregue a um colaborador."""

    nome = models.CharField('Nome do EPI', max_length=100)
    numero_ca = models.CharField('Número do CA', max_length=30, blank=True)
    descricao = models.TextField('Descrição', blank=True)

    class Meta:
        ordering = ['nome', 'pk']
        verbose_name = 'Equipamento'
        verbose_name_plural = 'Equipamentos'

    def __str__(self):
        return self.nome


class Emprestimo(models.Model):
    """Histórico persistido de entrega de EPI; FKs impedem exclusão acidental."""

    class Status(models.TextChoices):
        EMPRESTADO = 'emprestado', 'Emprestado'
        FORNECIDO = 'fornecido', 'Fornecido'
        DEVOLVIDO = 'devolvido', 'Devolvido'
        DANIFICADO = 'danificado', 'Danificado'
        PERDIDO = 'perdido', 'Perdido'

    colaborador = models.ForeignKey(
        Colaborador, on_delete=models.PROTECT, related_name='emprestimos'
    )
    equipamento = models.ForeignKey(
        Equipamento, on_delete=models.PROTECT, related_name='emprestimos'
    )
    data_entrega = models.DateTimeField('Data do empréstimo', default=timezone.now, editable=False)
    data_prevista_devolucao = models.DateTimeField('Data prevista para devolução', null=True, blank=True)
    data_devolucao = models.DateTimeField('Data da devolução', null=True, blank=True)
    observacao_devolucao = models.TextField('Observação na devolução', blank=True)
    status = models.CharField('Status', max_length=12, choices=Status.choices, default=Status.EMPRESTADO)

    class Meta:
        ordering = ['-data_entrega', '-pk']
        verbose_name = 'Empréstimo de EPI'
        verbose_name_plural = 'Empréstimos de EPI'

    def __str__(self):
        return f'{self.equipamento} — {self.colaborador} ({self.get_status_display()})'
