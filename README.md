# VideoPlay

VideoPlay é uma plataforma de streaming de vídeos com funcionalidades de cursos e playlists, desenvolvida em Django.

## 📋 Requisitos

### Método Tradicional
- Python 3.10+
- Django 5.2
- SQLite (padrão) ou outro banco de dados compatível

### Método com Docker
- Docker
- Docker Compose

## 🚀 Configuração Inicial

### Método com Docker (Recomendado)

A maneira mais fácil de executar o projeto é usando Docker:

```bash
# Construir e iniciar os contêineres
docker-compose up -d

# Criar um superusuário
docker-compose exec web python manage.py createsuperuser
```

Acesse o site em [http://localhost:8000/](http://localhost:8000/)

### Método Tradicional

Siga estas etapas para configurar o ambiente de desenvolvimento tradicional:

#### 1. Clone o repositório

```bash
git clone [URL do repositório]
cd VideoPlay
```

#### 2. Configure o ambiente virtual

```bash
# Criar o ambiente virtual
python -m venv venv

# Ativar o ambiente virtual
# No Windows:
.\venv\Scripts\activate

# No macOS/Linux:
source venv/bin/activate
```

#### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

#### 4. Configuração do banco de dados

```bash
# Crie as tabelas no banco de dados
python manage.py migrate

# Crie um superusuário para acessar o admin
python manage.py createsuperuser
```

#### 5. Execute o servidor de desenvolvimento

```bash
python manage.py runserver
```

Acesse o site em [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## 🔑 Acesso ao Painel Administrativo

1. Acesse [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
2. Faça login com as credenciais do superusuário criado anteriormente

## 📋 Funcionalidades Principais

### Gerenciamento de Vídeos
- Upload de vídeos
- Categorização
- Controle de visualizações
- Thumbnails personalizados

### Cursos e Playlists
- Crie cursos para organizar vídeos em sequência
- Defina a ordem dos vídeos dentro de um curso
- Navegação entre vídeos sequenciais

## 🏗️ Estrutura do Projeto

### Principais Apps
- `core`: Funcionalidades básicas e homepage
- `videos`: Gerenciamento de vídeos e cursos
- `accounts`: Gerenciamento de usuários

### Modelos Principais
- `Video`: Armazena informações e arquivos de vídeo
- `VideoCategory`: Categorias para organizar vídeos
- `Course`: Cursos com coleções de vídeos
- `CourseVideo`: Associação entre cursos e vídeos com ordem

## 💻 Desenvolvimento

### Arquivos Estáticos e Media
- Arquivos estáticos (CSS, JS) estão em `/static/`
- Uploads de mídia são armazenados em `/media/`

### Templates
Os templates estão organizados em:
- `/templates/` - Templates base
- `/templates/videos/` - Templates específicos para vídeos
- `/templates/accounts/` - Templates de autenticação

### Configurações de Media
As configurações de mídia (onde vídeos e thumbnails são armazenados) estão em `settings.py`:
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

## ⚠️ Notas Importantes

### Ambiente de Produção
Para configuração de produção:
1. Desative o `DEBUG` em `settings.py`
2. Configure uma chave secreta segura
3. Configure um servidor adequado (como Gunicorn + Nginx)
4. Para armazenamento de arquivos grandes, considere configurar AWS S3 (já há suporte no código)

### S3 Storage (Opcional)
Para usar o AWS S3 para armazenamento de vídeos:
1. Descomente e configure as configurações S3 em `settings.py`
2. Instale `boto3`: `pip install boto3`

## 🔄 Fluxo de Trabalho Recomendado

1. Crie categorias de vídeos
2. Faça upload dos vídeos
3. Crie cursos e organize os vídeos em sequência
4. Personalize a interface se necessário

## 🐞 Solução de Problemas Comuns

- **Erro ao fazer upload de vídeos grandes**: Verifique as configurações de tamanho máximo de upload no seu servidor.
- **Problemas de reprodução**: Verifique os formatos compatíveis (MP4 é recomendado).
- **Erros de CORS**: Se estiver usando S3, configure corretamente as permissões CORS.
- **Erros com Docker**: Verifique se as portas não estão sendo usadas por outros serviços.

## 📝 Logs e Depuração

Para visualizar logs no Docker:
```bash
docker-compose logs -f web
```

Para acessar o shell no contêiner:
```bash
docker-compose exec web bash
```

Para acessar o shell Django:
```bash
# Método tradicional
python manage.py shell

# Com Docker
docker-compose exec web python manage.py shell
```

---

Este projeto foi desenvolvido com Django e está sob licença [inserir licença]. 