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


from django.utils import timezone

from .models import Emprestimo, Equipamento


class EquipamentoForm(forms.ModelForm):
    class Meta:
        model = Equipamento
        fields = ['nome', 'numero_ca', 'descricao']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: Capacete de segurança'}),
            'numero_ca': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Certificado de Aprovação (se aplicável)'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Tamanho, material, observações...'}),
        }

    def clean_nome(self):
        nome = self.cleaned_data['nome'].strip()
        if not nome:
            raise forms.ValidationError('Informe o nome do equipamento.')
        return nome


class EmprestimoForm(forms.ModelForm):
    """Novo registro: status restrito e data futura validada no servidor."""

    status = forms.ChoiceField(
        label='Status',
        choices=[(Emprestimo.Status.EMPRESTADO, 'Emprestado'),
                 (Emprestimo.Status.FORNECIDO, 'Fornecido')],
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Emprestimo
        fields = ['colaborador', 'equipamento', 'status', 'data_prevista_devolucao']
        widgets = {
            'colaborador': forms.Select(attrs={'class': 'form-control'}),
            'equipamento': forms.Select(attrs={'class': 'form-control'}),
            'data_prevista_devolucao': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M', attrs={'class': 'form-control', 'type': 'datetime-local'}
            ),
        }
        labels = {'data_prevista_devolucao': 'Data prevista para devolução'}
        help_texts = {
            'data_prevista_devolucao': 'Obrigatória para empréstimos temporários. Não se aplica a fornecimentos definitivos.'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['colaborador'].queryset = Colaborador.objects.order_by('nome')
        self.fields['equipamento'].queryset = Equipamento.objects.order_by('nome')
        self.fields['colaborador'].empty_label = 'Selecione um colaborador'
        self.fields['equipamento'].empty_label = 'Selecione um equipamento'
        self.fields['data_prevista_devolucao'].input_formats = ['%Y-%m-%dT%H:%M', '%Y-%m-%dT%H:%M:%S']

    def clean(self):
        cleaned = super().clean()
        prevista = cleaned.get('data_prevista_devolucao')
        if cleaned.get('status') == Emprestimo.Status.EMPRESTADO and not prevista:
            self.add_error('data_prevista_devolucao', 'Informe a data prevista de devolução para um empréstimo.')
        if prevista and prevista <= timezone.now():
            self.add_error('data_prevista_devolucao', 'A data prevista precisa ser posterior à data e hora atuais.')
        return cleaned


class EmprestimoStatusForm(forms.ModelForm):
    """O ModelForm não expõe FK nem datas originais: POST forjado é ignorado."""

    class Meta:
        model = Emprestimo
        fields = ['status', 'data_devolucao', 'observacao_devolucao']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control', 'data-status-emprestimo': 'true'}),
            'data_devolucao': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M', attrs={'class': 'form-control', 'type': 'datetime-local'}
            ),
            'observacao_devolucao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4,
                                                          'placeholder': 'Condição do EPI ou motivo da perda...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['data_devolucao'].input_formats = ['%Y-%m-%dT%H:%M', '%Y-%m-%dT%H:%M:%S']

    def clean(self):
        cleaned = super().clean()
        status = cleaned.get('status')
        data = cleaned.get('data_devolucao')
        if status in (Emprestimo.Status.DEVOLVIDO, Emprestimo.Status.DANIFICADO):
            if not data:
                self.add_error('data_devolucao', 'Informe a data efetiva da devolução.')
        if data:
            if data > timezone.now():
                self.add_error('data_devolucao', 'A data de devolução não pode estar no futuro.')
            # A interface recebe minutos, enquanto a entrega tem segundos/microssegundos.
            # Compare na mesma precisão para aceitar devoluções no minuto da entrega.
            if (self.instance.pk and
                data.replace(second=0, microsecond=0) <
                    self.instance.data_entrega.replace(second=0, microsecond=0)):
                self.add_error('data_devolucao', 'A devolução não pode ser anterior à entrega.')
        if status in (Emprestimo.Status.EMPRESTADO, Emprestimo.Status.FORNECIDO):
            cleaned['data_devolucao'] = None
            cleaned['observacao_devolucao'] = ''
        return cleaned
