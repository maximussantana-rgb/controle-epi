# Controle de EPI — Sistema Django

Atividade de Desenvolvimento de Sistemas: gerenciamento de **colaboradores**, **equipamentos de proteção individual (EPIs)** e **empréstimos / fornecimentos** de EPI.

## Funcionalidades desta entrega

- **Tela base:** menu lateral presente em todas as telas; nome e imagem ilustrativa de perfil fixos (não implementa autenticação, conforme enunciado).
- **Colaboradores:** criar, listar, pesquisar por nome/telefone, editar e excluir com confirmação. Mostra sucesso/falha; cadastro mantém o formulário aberto após salvar.
- **Equipamentos:** criar, listar/pesquisar, editar e excluir com confirmação. Campos: nome obrigatório, número do CA opcional e descrição opcional. Mostra sucesso/falha; cadastro permanece na mesma tela.
- **Empréstimo de EPI:** entrega vinculada a colaborador e equipamento por chaves estrangeiras (ForeignKey). Data/hora de entrega preenchida automaticamente. Armazena previsão de devolução, data efetiva, observação e status.
- **Status:** Emprestado, Fornecido, Devolvido, Danificado e Perdido. Ao criar, só é permitido Emprestado ou Fornecido. Ao atualizar, as cinco opções aparecem. Dados originais da entrega (colaborador, equipamento e datas iniciais) são exibidos em modo somente leitura e **não podem ser alterados pelo envio de um POST forjado**.
- **Regras de data:** em *Emprestado*, previsão obrigatória e posterior ao momento atual; em *Fornecido*, data prevista é opcional porque o fornecimento é definitivo. Se preenchida, também precisa ser futura. Para *Devolvido* ou *Danificado*, data efetiva é obrigatória; para *Perdido*, pode ficar vazia. Campos de devolução só são exibidos nos três estados finais e são limpos ao voltar para Emprestado/Fornecido.
- **Persistência:** SQLite local. Os registros sobrevivem a parar/reiniciar o servidor. Para preservar o histórico, colaboradores e equipamentos com entregas relacionadas não podem ser excluídos (on_delete=PROTECT).
- **Relatórios:** **não implementados**, conforme a observação do enunciado (ficam para outra aula). A lista simples de entregas serve só para encontrar um registro e atualizar o status.

## Executar no VS Code (Windows / PowerShell)

Abra **a pasta `epi` contendo `manage.py`**:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
py manage.py migrate
py manage.py runserver
```

Acesse **http://127.0.0.1:8000/**.

> Se o PowerShell bloquear a ativação do ambiente, não é preciso mudar a política do Windows: rode `.\.venv\Scripts\python.exe -m pip install -r requirements.txt` e `.\.venv\Scripts\python.exe manage.py migrate` e `.\.venv\Scripts\python.exe manage.py runserver`.

### Importante se você já tinha colaboradores cadastrados

**Não apague o `db.sqlite3` da sua pasta de trabalho!** Copie os arquivos novos por cima dos antigos e execute `py manage.py migrate`. A migração `nucleo/migrations/0002_equipamento_emprestimo.py` cria as duas novas tabelas **sem apagar os colaboradores existentes**. Faça um backup do `db.sqlite3` antes de atualizar, por segurança.

Para testar a persistência, cadastre equipamento, registre um empréstimo, encerre o servidor com `Ctrl+C`, rode `py manage.py runserver` novamente e confira os registros. Depois atualize um status e repita o processo.

## Testes automatizados

```powershell
py manage.py test nucleo
py manage.py check
py manage.py makemigrations --check --dry-run
```

Os testes do Django usam um banco temporário e não afetam o banco local. No ambiente em que o pacote foi preparado, Django não pôde ser instalado por falta de acesso ao índice de pacotes; **execute estes comandos localmente e só entregue após validar os resultados**.

## Arquivos importantes

- `nucleo/models.py` — `Colaborador`, `Equipamento` e `Emprestimo`.
- `nucleo/forms.py` — validações e restrições dos formulários.
- `nucleo/views.py` — regras das telas e mensagens.
- `nucleo/urls.py` — rotas.
- `nucleo/migrations/0002_equipamento_emprestimo.py` — novas tabelas SQLite.
- `nucleo/templates/nucleo/` — HTML de todas as telas e template base.
- `nucleo/static/css/style.css`, `nucleo/static/js/emprestimo.js` — interface e exibição condicional.
- `nucleo/tests.py` — testes de CRUD, datas e segurança dos campos de edição.

## Enviar atualização ao GitHub

Se já configurou o repositório `maximussantana-rgb/controle-epi`, **não use `git init` nem `git remote add` novamente**. Na pasta onde o Git já está inicializado:

```powershell
git status
git add .
git commit -m "Implementa CRUD de equipamentos e emprestimos de EPI"
git push origin main
```

O arquivo `db.sqlite3`, o ambiente virtual `.venv`, arquivos `.env` e cache Python estão no `.gitignore` e não devem ser publicados com dados reais. Se o banco estiver versionado de antes, remova apenas do índice Git (`git rm --cached db.sqlite3`), sem apagar o arquivo local.

## Docker (opcional)

O `Dockerfile` monta o Python e executa o servidor Django; `compose.yaml` define um volume persistente para SQLite. Se tiver Docker Desktop instalado, execute `docker compose up --build` na pasta do projeto. O banco do Docker é independente do SQLite usado localmente. Não use `docker compose down -v` se quiser manter os dados no volume.

## Observações

Este projeto é uma atividade didática. Não há login e a foto de perfil é uma **ilustração estática**; substitua o arquivo `nucleo/static/img/perfil-usuario.svg` por uma foto autorizada, se desejar. Para publicar em produção são necessários controle de acesso, HTTPS, configurações seguras de chave/DEBUG/ALLOWED_HOSTS e servidor adequado (não usar `runserver` em produção).
