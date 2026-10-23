"""Testes do CRUD de colaboradores (banco de testes isolado pelo Django)."""

from django.test import TestCase
from django.urls import reverse

from .models import Colaborador


class ColaboradorCRUDTests(TestCase):
    def test_criar_e_listar_colaborador(self):
        resposta = self.client.post(reverse('nucleo-salvar'), {
            'nome': '  Ana Souza  ',
            'telefone': '(71) 99999-9999',
        }, follow=True)
        self.assertRedirects(resposta, reverse('nucleo-criar'))
        self.assertContains(resposta, 'Colaborador cadastrado com sucesso!')
        self.assertTrue(Colaborador.objects.filter(
            nome='Ana Souza', telefone='(71) 99999-9999'
        ).exists())
        self.assertContains(self.client.get(reverse('nucleo-inicial')), 'Ana Souza')

    def test_editar_mantem_mesmo_registro(self):
        colaborador = Colaborador.objects.create(nome='Carlos', telefone='1111')
        self.client.post(reverse('nucleo-editar', args=[colaborador.pk]), {
            'nome': 'Carlos Silva', 'telefone': '2222',
        })
        colaborador.refresh_from_db()
        self.assertEqual(colaborador.nome, 'Carlos Silva')
        self.assertEqual(colaborador.telefone, '2222')
        self.assertEqual(Colaborador.objects.count(), 1)

    def test_excluir_exige_post_e_remove_do_banco(self):
        colaborador = Colaborador.objects.create(nome='Maria', telefone='3333')
        url = reverse('nucleo-excluir', args=[colaborador.pk])
        self.client.get(url)  # Apenas tela de confirmação
        self.assertTrue(Colaborador.objects.filter(pk=colaborador.pk).exists())
        resposta = self.client.post(url)
        self.assertRedirects(resposta, reverse('nucleo-inicial'))
        self.assertFalse(Colaborador.objects.filter(pk=colaborador.pk).exists())

    def test_pesquisar_por_nome_e_telefone(self):
        Colaborador.objects.create(nome='Beatriz', telefone='12345678')
        Colaborador.objects.create(nome='Renato', telefone='99999999')
        for busca in ['Bea', '1234']:
            resposta = self.client.get(reverse('nucleo-inicial'), {'busca': busca})
            self.assertContains(resposta, 'Beatriz')
            self.assertNotContains(resposta, 'Renato')

    def test_nao_salvar_campos_vazios(self):
        resposta = self.client.post(reverse('nucleo-salvar'), {
            'nome': '   ', 'telefone': '',
        })
        self.assertEqual(resposta.status_code, 400)
        self.assertEqual(Colaborador.objects.count(), 0)
        self.assertContains(resposta, 'Não foi possível cadastrar o colaborador', status_code=400)

    def test_salvar_nao_aceita_get(self):
        self.assertEqual(self.client.get(reverse('nucleo-salvar')).status_code, 405)

    def test_colaborador_inexistente_retorna_404(self):
        self.assertEqual(self.client.get(reverse('nucleo-editar', args=[99999])).status_code, 404)
        self.assertEqual(self.client.get(reverse('nucleo-excluir', args=[99999])).status_code, 404)

    def test_edicao_invalida_nao_altera_banco(self):
        colaborador = Colaborador.objects.create(nome='Lucas', telefone='5555')
        resposta = self.client.post(reverse('nucleo-editar', args=[colaborador.pk]), {
            'nome': ' ', 'telefone': '',
        })
        self.assertEqual(resposta.status_code, 400)
        colaborador.refresh_from_db()
        self.assertEqual(colaborador.nome, 'Lucas')

    def test_apos_cadastro_continua_com_formulario_novo(self):
        resposta = self.client.post(reverse('nucleo-salvar'), {
            'nome': 'Novo Colaborador', 'telefone': '71900000000',
        }, follow=True)
        self.assertEqual(resposta.resolver_match.url_name, 'nucleo-criar')
        self.assertContains(resposta, 'Novo colaborador')
        self.assertNotContains(resposta, 'value="Novo Colaborador"')
        self.assertEqual(Colaborador.objects.count(), 1)

    def test_tela_editar_preenche_os_dados_atuais(self):
        colaborador = Colaborador.objects.create(nome='Nina', telefone='7122223333')
        resposta = self.client.get(reverse('nucleo-editar', args=[colaborador.pk]))
        self.assertContains(resposta, 'value="Nina"')
        self.assertContains(resposta, 'value="7122223333"')


from datetime import timedelta

from django.utils import timezone

from .models import Emprestimo, Equipamento


def futura(dias=2):
    return timezone.localtime(timezone.now() + timedelta(days=dias)).strftime('%Y-%m-%dT%H:%M')


def passada(dias=2):
    return timezone.localtime(timezone.now() - timedelta(days=dias)).strftime('%Y-%m-%dT%H:%M')


class EquipamentoCRUDTests(TestCase):
    def test_cadastrar_continua_no_formulario_e_persiste(self):
        resposta = self.client.post(reverse('equipamento-criar'), {
            'nome': 'Óculos de proteção', 'numero_ca': '12345', 'descricao': 'Lente transparente',
        }, follow=True)
        self.assertRedirects(resposta, reverse('equipamento-criar'))
        self.assertContains(resposta, 'Equipamento cadastrado com sucesso!')
        self.assertTrue(Equipamento.objects.filter(nome='Óculos de proteção').exists())
        self.assertContains(self.client.get(reverse('equipamento-lista')), 'Óculos de proteção')
        self.assertNotContains(resposta, 'value="Óculos de proteção"')

    def test_editar_mantem_registro(self):
        equipamento = Equipamento.objects.create(nome='Luva de raspa')
        resposta = self.client.post(reverse('equipamento-editar', args=[equipamento.pk]), {
            'nome': 'Luva de segurança', 'numero_ca': '998877', 'descricao': 'Tamanho M',
        })
        self.assertRedirects(resposta, reverse('equipamento-lista'))
        equipamento.refresh_from_db()
        self.assertEqual(equipamento.nome, 'Luva de segurança')
        self.assertEqual(equipamento.numero_ca, '998877')
        self.assertEqual(Equipamento.objects.count(), 1)

    def test_excluir_somente_quando_confirmado(self):
        equipamento = Equipamento.objects.create(nome='Protetor auricular')
        url = reverse('equipamento-excluir', args=[equipamento.pk])
        self.assertContains(self.client.get(url), 'Deseja excluir este equipamento?')
        self.assertTrue(Equipamento.objects.filter(pk=equipamento.pk).exists())
        self.assertRedirects(self.client.post(url), reverse('equipamento-lista'))
        self.assertFalse(Equipamento.objects.filter(pk=equipamento.pk).exists())

    def test_cadastro_invalido_exibe_falha(self):
        resposta = self.client.post(reverse('equipamento-criar'), {'nome': '  '})
        self.assertEqual(resposta.status_code, 400)
        self.assertContains(resposta, 'Não foi possível cadastrar o equipamento', status_code=400)
        self.assertEqual(Equipamento.objects.count(), 0)

    def test_busca_por_nome(self):
        Equipamento.objects.create(nome='Capacete')
        Equipamento.objects.create(nome='Bota')
        resp = self.client.get(reverse('equipamento-lista'), {'busca': 'capac'})
        self.assertContains(resp, 'Capacete')
        self.assertNotContains(resp, '<strong>Bota</strong>')


class EmprestimoTests(TestCase):
    def setUp(self):
        self.colaborador = Colaborador.objects.create(nome='Ana', telefone='12345678')
        self.outro_colaborador = Colaborador.objects.create(nome='Luiz', telefone='22222222')
        self.equipamento = Equipamento.objects.create(nome='Capacete')
        self.outro_equipamento = Equipamento.objects.create(nome='Bota')

    def dados(self, **overrides):
        dados = {
            'colaborador': self.colaborador.pk,
            'equipamento': self.equipamento.pk,
            'status': 'emprestado',
            'data_prevista_devolucao': futura(),
        }
        dados.update(overrides)
        return dados

    def criar(self, **overrides):
        return self.client.post(reverse('emprestimo-criar'), self.dados(**overrides))

    def test_emprestimo_criado_com_chaves_estrangeiras_e_dados_persistidos(self):
        resposta = self.criar()
        self.assertRedirects(resposta, reverse('emprestimo-criar'))
        registro = Emprestimo.objects.get()
        self.assertEqual(registro.colaborador, self.colaborador)
        self.assertEqual(registro.equipamento, self.equipamento)
        self.assertEqual(registro.status, Emprestimo.Status.EMPRESTADO)
        self.assertIsNotNone(registro.data_entrega)
        self.assertIsNotNone(registro.data_prevista_devolucao)
        self.assertContains(self.client.get(reverse('emprestimo-lista')), 'Capacete')

    def test_so_duas_opcoes_no_cadastro_e_post_fraudado_nao_funciona(self):
        resposta = self.client.get(reverse('emprestimo-criar'))
        self.assertContains(resposta, '<option value="emprestado"')
        self.assertContains(resposta, '<option value="fornecido"')
        self.assertNotContains(resposta, '<option value="devolvido"')
        resposta = self.criar(status='devolvido')
        self.assertEqual(resposta.status_code, 400)
        self.assertEqual(Emprestimo.objects.count(), 0)

    def test_data_prevista_passada_ou_ausente_rejeitada(self):
        for data in [passada(), '']:
            resposta = self.criar(data_prevista_devolucao=data)
            self.assertEqual(resposta.status_code, 400)
        self.assertEqual(Emprestimo.objects.count(), 0)

    def test_fornecimento_definitivo_nao_exige_data_prevista(self):
        resposta = self.criar(status='fornecido', data_prevista_devolucao='')
        self.assertRedirects(resposta, reverse('emprestimo-criar'))
        registro = Emprestimo.objects.get()
        self.assertIsNone(registro.data_prevista_devolucao)

    def test_editar_nao_permite_mudar_fk_nem_datas_originais(self):
        self.criar()
        registro = Emprestimo.objects.get()
        data_entrega = registro.data_entrega
        prevista = registro.data_prevista_devolucao
        resposta = self.client.post(reverse('emprestimo-editar', args=[registro.pk]), {
            'status': 'devolvido', 'data_devolucao': timezone.localtime(timezone.now()).strftime('%Y-%m-%dT%H:%M'),
            'observacao_devolucao': 'Retornou em bom estado',
            'colaborador': self.outro_colaborador.pk,
            'equipamento': self.outro_equipamento.pk,
            'data_entrega': passada(10),
            'data_prevista_devolucao': futura(10),
        })
        self.assertRedirects(resposta, reverse('emprestimo-lista'))
        registro.refresh_from_db()
        self.assertEqual(registro.status, 'devolvido')
        self.assertEqual(registro.colaborador_id, self.colaborador.pk)
        self.assertEqual(registro.equipamento_id, self.equipamento.pk)
        self.assertEqual(registro.data_entrega, data_entrega)
        self.assertEqual(registro.data_prevista_devolucao, prevista)
        self.assertEqual(registro.observacao_devolucao, 'Retornou em bom estado')

    def test_devolvido_ou_danificado_exige_data_efetiva(self):
        self.criar()
        registro = Emprestimo.objects.get()
        for status in ['devolvido', 'danificado']:
            resposta = self.client.post(reverse('emprestimo-editar', args=[registro.pk]), {
                'status': status, 'data_devolucao': '', 'observacao_devolucao': 'teste',
            })
            self.assertEqual(resposta.status_code, 400)
        registro.refresh_from_db()
        self.assertEqual(registro.status, 'emprestado')

    def test_perdido_pode_ficar_sem_data_devolucao(self):
        self.criar()
        registro = Emprestimo.objects.get()
        resposta = self.client.post(reverse('emprestimo-editar', args=[registro.pk]), {
            'status': 'perdido', 'data_devolucao': '', 'observacao_devolucao': 'Extraviado na obra',
        })
        self.assertRedirects(resposta, reverse('emprestimo-lista'))
        registro.refresh_from_db()
        self.assertEqual(registro.status, 'perdido')
        self.assertIsNone(registro.data_devolucao)
        self.assertEqual(registro.observacao_devolucao, 'Extraviado na obra')

    def test_dados_de_devolucao_sao_limpos_ao_voltar_para_emprestado(self):
        self.criar()
        registro = Emprestimo.objects.get()
        registro.status = 'perdido'
        registro.observacao_devolucao = 'Perdeu'
        registro.save()
        self.client.post(reverse('emprestimo-editar', args=[registro.pk]), {'status': 'emprestado'})
        registro.refresh_from_db()
        self.assertEqual(registro.status, 'emprestado')
        self.assertEqual(registro.observacao_devolucao, '')
        self.assertIsNone(registro.data_devolucao)

    def test_protecao_contra_exclusao_de_colaborador_e_equipamento_com_entrega(self):
        self.criar()
        resp_col = self.client.post(reverse('nucleo-excluir', args=[self.colaborador.pk]), follow=True)
        resp_epi = self.client.post(reverse('equipamento-excluir', args=[self.equipamento.pk]), follow=True)
        self.assertContains(resp_col, 'não pode ser excluído')
        self.assertContains(resp_epi, 'não pode ser excluído')
        self.assertTrue(Colaborador.objects.filter(pk=self.colaborador.pk).exists())
        self.assertTrue(Equipamento.objects.filter(pk=self.equipamento.pk).exists())

    def test_layout_base_exibe_usuario_e_menus(self):
        resposta = self.client.get(reverse('emprestimo-lista'))
        self.assertContains(resposta, 'Maximus Santana')
        self.assertContains(resposta, 'Cadastrar equipamento')
        self.assertContains(resposta, 'Registrar empréstimo')
        self.assertNotContains(resposta, 'Relatórios')
