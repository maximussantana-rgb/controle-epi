# Controle de EPI — CRUD de Colaboradores

Projeto Django baseado no código inicial `epi.rar`, com interface inspirada no wireframe da atividade.

## Funcionalidades implementadas

- **Cadastrar** colaboradores com nome e telefone (validação de campos obrigatórios), com mensagem de sucesso ou erro. Após cadastrar, o usuário **permanece na tela de cadastro** com formulário limpo.
- **Listar** colaboradores cadastrados, com ID, nome, telefone e ações.
- **Pesquisar** por nome ou telefone.
- **Editar** os dados do colaborador sem alterar seu ID.
- **Excluir** com tela de confirmação. A exclusão só acontece ao confirmar pelo botão.
- **Persistência no SQLite**: os dados são gravados no arquivo `db.sqlite3` e continuam após parar e reiniciar o servidor.
- CSRF nos formulários, mensagens de sucesso e páginas 404 para registros inexistentes.

Esta entrega apresenta apenas os menus **Listar colaboradores** e **Cadastrar colaborador**. As telas de equipamentos, empréstimos e relatórios não fazem parte do escopo de implementação desta etapa.

## Executar no Windows (PowerShell ou terminal do VS Code)

Abra um terminal na **pasta `epi` que contém `manage.py`**.

```powershell
py -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
py manage.py migrate
py manage.py runserver
```

Acesse **http://127.0.0.1:8000/**.

No Linux ou macOS, ative o ambiente com `source .venv/bin/activate` e use `python` no lugar de `py`.

**Importante:** O banco SQLite (`db.sqlite3`) é gerado localmente após `py manage.py migrate` e não acompanha a versão para GitHub, para evitar publicar dados pessoais. O arquivo `db.sqlite3` está no `.gitignore`. Depois de criá-lo, não apague esse arquivo se desejar manter os registros; reiniciar o servidor não apaga os dados.

## Conferir persistência (item da avaliação)

1. Rode o servidor com `py manage.py runserver`.
2. Crie um colaborador. Confira a mensagem de sucesso e se continua na tela de cadastro. Clique em **Ver colaboradores** para conferir nome e telefone na lista.
3. Encerre o servidor com **Ctrl+C**, execute o comando novamente e confira que o colaborador continua cadastrado.
4. Edite o nome/telefone desse colaborador e salve. Reinicie o servidor e confira as alterações.
5. Exclua o colaborador confirmando na tela. Reinicie o servidor e confira que ele continua ausente.

**Por quê funciona?** No Django, `form.save()` (cadastro e edição) e `colaborador.delete()` (exclusão) executam operações no SQLite definido em `epi/settings.py`. Isso grava os dados no disco, em vez de armazenar a lista apenas na memória da aplicação.

## Testes automatizados

```powershell
py manage.py test nucleo
```

Os testes usam um banco temporário isolado. A avaliação após reiniciar está descrita acima para você conferir manualmente com seu banco real.

## Arquivos principais

- `nucleo/models.py` — modelo `Colaborador` existente (nome e telefone).
- `nucleo/forms.py` — validação de cadastro e edição.
- `nucleo/views.py` — lógica de CRUD e pesquisa.
- `nucleo/urls.py` — URLs de navegação e operações.
- `nucleo/templates/nucleo/` — telas HTML com template base.
- `nucleo/static/css/style.css` — visual e responsividade.
- `db.sqlite3` — banco local gerado automaticamente com `migrate` (não versionado no GitHub).
- `Dockerfile` e `compose.yaml` — exemplo de execução local com Docker e volume persistente.

## Observações

A chave de desenvolvimento e `DEBUG=True` são do projeto base. Antes de publicar o sistema na internet, configure chave secreta via ambiente, `DEBUG=False`, `ALLOWED_HOSTS`, usuários/permissões e HTTPS.


## Controle de versão: entregar pelo GitHub

Execute no terminal **dentro da pasta `epi`**, onde fica `manage.py`:

```powershell
git init
git add .
git commit -m "Implementa CRUD de colaboradores com persistencia SQLite"
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git
git push -u origin main
```

Antes de `git remote add origin`, crie um repositório **vazio** no GitHub, sem inicializar com README ou `.gitignore`, e substitua o endereço acima pelo endereço real do seu repositório. O Git pode solicitar que você configure seu nome e email e que faça login no GitHub. Em atualizações futuras, use `git add .`, `git commit -m "mensagem"` e `git push`.

Para conferir os arquivos que serão publicados, execute `git status`. **Não publique** seu banco SQLite com dados pessoais, senhas, `.env` ou sua pasta `.venv`.

## Pesquisa sobre Dockerfile (opcional na Etapa 2)

O `Dockerfile` descreve uma imagem com **Python 3.12**, instala as dependências via `requirements.txt`, copia o projeto e configura a execução do Django. O arquivo `compose.yaml` permite executar o serviço e monta um **volume Docker** para os dados do SQLite. Sem volume, recriar o contêiner poderia fazer perder o banco gerado dentro dele.

Instale o Docker Desktop e, na pasta do projeto, rode:

```powershell
docker compose up --build
```

Acesse http://127.0.0.1:8000/. Para parar, use Ctrl+C ou `docker compose down`. **Não execute `docker compose down -v`** se quiser preservar os cadastros, pois o `-v` apaga o volume do banco.

O ambiente Docker usa o SQLite **no volume** `/app/data/db.sqlite3` (configurado por `SQLITE_PATH`), separado do `db.sqlite3` local. Isso é uma demonstração para a atividade: o servidor `runserver` não é adequado para disponibilizar o sistema na internet; em produção, é preciso configurar servidor web, autenticação, segurança e infraestrutura apropriados.
