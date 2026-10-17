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
