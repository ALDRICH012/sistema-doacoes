# Sistema de Doações

Sistema de gerenciamento de doações desenvolvido em Django.

## Funcionalidades

- Cadastro de doadores
- Registro de doações
- Busca de doadores
- Relatórios e estatísticas
- Interface responsiva

## Requisitos

- Python 3.8+
- Django 4.2+
- PostgreSQL

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/sistema-doacoes.git
cd sistema-doacoes
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

5. Execute as migrações:
```bash
python manage.py migrate
```

6. Inicie o servidor:
```bash
python manage.py runserver
```

## Configuração do Banco de Dados

O projeto usa PostgreSQL. Configure as seguintes variáveis de ambiente:

```
DB_NAME=nome_do_banco
DB_USER=usuario
DB_PASSWORD=senha
DB_HOST=localhost
DB_PORT=5432
```

## Estrutura do Projeto

```
sistema-doacoes/
├── doacoes/              # Aplicação principal
│   ├── models.py        # Modelos de dados
│   ├── views.py         # Views
│   ├── forms.py         # Formulários
│   └── urls.py          # URLs
├── templates/           # Templates HTML
├── static/             # Arquivos estáticos
├── media/              # Arquivos de mídia
└── manage.py           # Script de gerenciamento
```

## Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Faça commit das suas alterações (`git commit -m 'Adiciona nova feature'`)
4. Faça push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes. 