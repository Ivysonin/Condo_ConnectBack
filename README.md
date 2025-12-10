# **CondoConnect - API**

API para gestão de **usuários**, **avisos** e **chamados** do condomínio.
Desenvolvida em **Flask**, com autenticação via **Flask-Login**, validações com **Marshmallow**, ORM **SQLAlchemy** e migrações com **Flask-Migrate**.

---

## 🚀 **Funcionalidades Principais**

### 🔐 **Autenticação**

* Login e logout com Flask-Login
* Senha criptografada com Werkzeug
* Permissões baseadas no tipo de usuário:

  * **morador** – restrito
  * **sindico** – acesso administrativo

---

## 👤 **Usuários**

### Morador:

* Criar conta
* Autenticar
* Editar perfil (nome, email, telefone, bloco/apto e senha)
* Ver apenas os próprios chamados
* Ver avisos ativos

### Síndico:

* Tudo que o morador pode
* Listar todos os usuários do sistema
* Criar, editar e desativar avisos
* Alterar o status de qualquer chamado

---

## 🔔 **Avisos**

* Criados apenas por síndicos
* Editáveis por 5 minutos após criados
* Quando desativados → deixam de aparecer
* Moradores só visualizam os avisos ativos

---

## 🛠 **Chamados**

### Morador:

* Criar chamados
* Ver detalhes do próprio chamado
* Ver apenas chamados com status **aberto** ou **andamento** (os concluídos somem para moradores)

### Síndico:

* Ver todos os chamados
* Alterar status para:

  * `aberto`
  * `andamento`
  * `concluido`

---

## 🧩 **Permissões Resumidas**

| Ação              | Morador     | Síndico   |
| ----------------- | ----------- | --------- |
| Ver avisos ativos | ✔           | ✔         |
| Criar aviso       | ✖           | ✔         |
| Editar aviso      | ✖           | ✔ (5 min) |
| Remover aviso     | ✖           | ✔         |
| Criar chamado     | ✔           | ✔         |
| Ver chamados      | Apenas dele | Todos     |
| Alterar status    | ✖           | ✔         |
| Listar usuários   | ✖           | ✔         |

---

## 🗂 **Tecnologias Utilizadas**

* Python
* Flask
* Flask-Login
* SQLAlchemy
* Marshmallow
* Flask-Migrate

---

## 🧱 **Estrutura do Projeto**

```
app/
 ├── controllers/
 │   ├── adm_controller.py
 │   ├── auth_controller.py
 │   ├── aviso_controller.py
 │   ├── chamado_controller.py
 │   └── user_controller.py
 ├── models/
 │   ├── aviso_model.py
 │   ├── chamado_model.py
 │   └── user_model.py
 ├── schemas/
 │   ├── aviso_schema.py
 │   ├── chamado_schema.py
 │   └── user_schema.py
 ├── services/
 │   ├── auth_service.py
 │   ├── aviso_service.py
 │   ├── chamado_service.py
 │   └── user_service.py
 ├── __init__.py
 ├── config.py
 └── ...
```

---

## 🔌 **Como Rodar o Projeto**

### 1. Criar ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux
venv\Scripts\activate     # Windows
```

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

### 3. Configurar variáveis de ambiente

Crie um `.env`:

```
FLASK_ENV=development
SECRET_KEY=uma_senha_segura
DATABASE_URL=sqlite:///data.db
```

### 4. Inicializar o banco

```bash
flask db init
flask db migrate
flask db upgrade
```

### 5. Executar o servidor

```bash
flask run
```

---

## 📌 **Endpoints disponíveis**

### 🔐 Autenticação

| Método | URL            | Descrição          |
| ------ | -------------- | ------------------ |
| POST   | /auth/login    | Login do usuário   |
| POST   | /auth/logout   | Logout do usuário  |

---

### 👤 Usuário

| Método | URL             | Descrição              |
| ------ | --------------- | ---------------------- |
| POST   | /users/register | Cadastra novo usuário  |
| GET    | /users/perfil   | Informações do usuário |
| PUT    | /users/perfil   | Atualiza informações   |

---

### 👤 Administração (Síndico)

| Método | URL             | Descrição                |
| ------ | -------------   | ------------------------ |
| GET    | /admin/usuarios | Listar todos os usuários |

---

### 🔔 Avisos

| Método | URL          | Descrição                 |
| ------ | ------------ | ------------------------- |
| GET    | /avisos      | Listar avisos ativos      |
| POST   | /avisos      | Criar aviso (síndico)     |
| PUT    | /avisos/{id} | Editar aviso (síndico)    |
| DELETE | /avisos/{id} | Desativar aviso (síndico) |

---

### 🛠 Chamados

| Método | URL           | Descrição                                    |
| ------ | ------------- | -------------------------------------------- |
| GET    | /chamado      | Listar chamados (regras por tipo de usuário) |
| GET    | /chamado/{id} | Detalhes de um chamado                       |
| POST   | /chamado      | Criar chamado                                |
| PATCH  | /chamado/{id} | Alterar status (somente síndico)             |

---

## 📄 Licença

Este projeto está licenciado sob os termos da [Licença MIT](./LICENSE), com cláusula adicional de atribuição.
