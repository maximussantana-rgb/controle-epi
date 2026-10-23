# Migração da etapa de equipamentos e empréstimos.
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('nucleo', '0001_initial')]

    operations = [
        migrations.CreateModel(
            name='Equipamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, verbose_name='Nome do EPI')),
                ('numero_ca', models.CharField(blank=True, max_length=30, verbose_name='Número do CA')),
                ('descricao', models.TextField(blank=True, verbose_name='Descrição')),
            ],
            options={'verbose_name': 'Equipamento', 'verbose_name_plural': 'Equipamentos', 'ordering': ['nome', 'pk']},
        ),
        migrations.CreateModel(
            name='Emprestimo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_entrega', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Data do empréstimo')),
                ('data_prevista_devolucao', models.DateTimeField(blank=True, null=True, verbose_name='Data prevista para devolução')),
                ('data_devolucao', models.DateTimeField(blank=True, null=True, verbose_name='Data da devolução')),
                ('observacao_devolucao', models.TextField(blank=True, verbose_name='Observação na devolução')),
                ('status', models.CharField(choices=[('emprestado', 'Emprestado'), ('fornecido', 'Fornecido'), ('devolvido', 'Devolvido'), ('danificado', 'Danificado'), ('perdido', 'Perdido')], default='emprestado', max_length=12, verbose_name='Status')),
                ('colaborador', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='emprestimos', to='nucleo.colaborador')),
                ('equipamento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='emprestimos', to='nucleo.equipamento')),
            ],
            options={'verbose_name': 'Empréstimo de EPI', 'verbose_name_plural': 'Empréstimos de EPI', 'ordering': ['-data_entrega', '-pk']},
        ),
    ]
