# Lobbyzinha

Plataforma web para jogadores de CS2 encontrarem times e times encontrarem jogadores no cenário competitivo brasileiro.

**Alunos:**
- Breno do Patrocínio Raisch — 2110039
- João Pedro de Oliveira Andrade Paiva — 2110569

---

## Escopo

Lobbyzinha é um site de recrutamento para o cenário competitivo de Counter Strike. Jogadores criam perfis com suas informações de nível (Faceit, Gamers Club), funções in-game e disponibilidade. Times são criados por donos que podem recrutar jogadores via convite ou aceitar pedidos de entrada. A plataforma conecta os dois lados de forma organizada, com dashboards individuais e controle de acesso por tipo de usuário.

**Funcionalidades implementadas:**

- Cadastro e login de usuários --> Sem restrições para tamanho de string e caracteres para usuários e senhas. Há verificação de duplicidade para email
- Perfil de jogador com foto de perfil, banner, funções, níveis e redes sociais
- Criação, edição e exclusão de times
- Sistema de convites (dono convida jogador)
- Sistema de pedidos de entrada (jogador pede para entrar no time)
- Dashboard com convites recebidos, convites enviados e pedidos de entrada pendentes
- Kick de membros pelo dono do time
- Saída voluntária do time pelo jogador
- Lista de jogadores disponíveis com status "Looking for team"
- Lista de times com busca por nome
- Página de perfil pública de cada jogador
- Página de detalhe de cada time
- Visões diferentes para dono de time, membro e visitante
- Painel de administração Django com gerenciamento de jogadores e times

---

## Tecnologias

- Python 3.12 + Django 4.2
- HTML e CSS (sem JavaScript)
- SQLite
- Docker

---

## Como rodar com Docker

**Pré-requisitos:** Docker e Docker Compose instalados.

**1. Clone o repositório:**
```bash
git clone https://github.com/JPPaiva17/INF1047_G1.git
cd INF1047_G1
```

**2. Crie o arquivo `.env` na raiz do projeto:**
```
DJANGO_SECRET_KEY=sua-chave-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=*
```

**3. Suba o container:**
```bash
docker-compose up --build
```

As migrations e o collectstatic rodam automaticamente. Acesse http://localhost:8000

**Para criar um superusuário (opcional):**
```bash
docker exec -it prog_web python manage.py createsuperuser
```

---

## Como rodar localmente (sem Docker)

**1. Clone o repositório e crie um ambiente virtual:**
```bash
git clone https://github.com/JPPaiva17/INF1047_G1.git
cd INF1047_G1
python -m venv venv
venv\Scripts\activate  # Windows
```

**2. Instale as dependências:**
```bash
pip install -r requirements.txt
```

**3. Crie o arquivo `.env` na raiz do projeto:**
```
DJANGO_SECRET_KEY=sua-chave-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=*
```

**4. Aplique as migrations e rode:**
```bash
python manage.py migrate
python manage.py runserver
```

**5. Acesse:** http://localhost:8000

---

## Deploy no Railway

**1.** Crie uma conta em https://railway.app e conecte com o GitHub.

**2.** Crie um novo projeto → **Deploy from GitHub repo** → selecione `INF1047_G1`.

**3.** Em **Variables**, adicione:
```
DJANGO_SECRET_KEY=sua-chave-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=*
```

**4.** Em **Settings** → **Networking** → **Generate Domain**.

O Railway detecta o Dockerfile automaticamente. As migrations e o collectstatic rodam sozinhos no startup.

---

## Manual do Usuário

### Registro e Login
- Acesse `/players/register/` para criar uma conta com username, email e senha
- Faça login em `/players/login/`
- Cada usuário tem um perfil de jogador criado automaticamente

### Perfil do Jogador
- Acesse **My Profile** na sidebar para ver seu perfil público
- Clique em **Edit Profile** para editar avatar, banner, bio, níveis de Faceit e Gamers Club, roles e redes sociais
- Marque ou desmarque **Looking for team** para aparecer ou não na lista de jogadores

### Times

**Criar um time:**
- Acesse **Teams** na sidebar e clique em **Create Team**
- Preencha nome, descrição, requisitos mínimos e informações de recrutamento
- Apenas jogadores que não estão em nenhum time podem criar um

**Gerenciar um time (dono):**
- Acesse **Manage Team** na sidebar
- Edite as informações do time, aceite ou recuse pedidos de entrada, cancele convites enviados, defina seu próprio role no time e remova membros

**Entrar em um time:**
- Na página de um time com recrutamento aberto, selecione um role e clique em **Request to Join**
- Aguarde o dono aceitar ou recusar no dashboard dele

**Sair de um time:**
- No Dashboard, no card **Meu Time**, clique no botão de saída

### Convites
- Donos de time podem convidar jogadores pela lista de **Players**
- Jogadores recebem os convites no **Dashboard** e podem aceitar ou recusar

### Admin
- Acesse `/admin/` com uma conta superusuário
- É possível gerenciar usuários, jogadores e membros de times diretamente pelo painel

---

## O que funcionou

- Cadastro, login e logout de usuários
- CRUD completo de times (criar, visualizar, editar, deletar)
- CRUD de perfil de jogador
- Sistema de convites e pedidos de entrada com aceite/recusa
- Kick de membros e saída voluntária do time
- Notificações internas
- Visões diferenciadas por tipo de usuário (dono, membro, visitante)
- Lista de jogadores com status de disponibilidade
- Busca de times por nome
- Painel admin com gerenciamento de jogadores e membros
- Deploy via Docker

## O que não funcionou

- Integração automática com Gamers Club e Faceit: a ideia era buscar o nível do jogador automaticamente via web scraping a partir do username, mas não foi implementada. Os níveis são inseridos manualmente pelo próprio jogador no perfil.
