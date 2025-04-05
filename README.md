<div align="center">

![Image](https://github.com/user-attachments/assets/6ec3c160-a607-42ec-97b9-c47a604bbd68)

<h1>Open WebUI with PostgreSQL</h1>

<a href="README_JP.md"><img src="https://img.shields.io/badge/ドキュメント-日本語-white.svg" alt="JA doc"/></a>
<a href="README.md"><img src="https://img.shields.io/badge/english-document-white.svg" alt="EN doc"></a>

<img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL"/>
<img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker"/>
<img src="https://img.shields.io/badge/OpenWebUI-FF6B6B?style=for-the-badge&logo=html5&logoColor=white" alt="Open WebUI"/>

</div>

This setup runs Open WebUI connected to a PostgreSQL database using Docker Compose.

## 🔧 Components

- **PostgreSQL**: Database server for storing Open WebUI data
- **Ollama**: Local Large Language Model server
- **Open WebUI**: Web interface for interacting with Ollama models

## 🚀 Getting Started

1. Make sure Docker and Docker Compose are installed on your system.
2. Customize the environment variables in `docker-compose.yml` if needed.
3. Run the following command to start all services:

```bash
docker-compose up -d
```

4. Access Open WebUI by navigating to http://localhost:3000 in your browser.

## ⚙️ Configuration

### PostgreSQL

- Default user: `openwebui`
- Default password: `openwebui`
- Default database: `openwebui`
- Port: `5432` (accessible from host)

You can modify these settings in the `docker-compose.yml` file. If you change any of these settings after the first run, you may need to delete the volume to apply the changes:

```bash
docker-compose down
docker volume rm open-webui-postgres_postgres-data
docker-compose up -d
```

### 🔒 Security

For production environments, it's recommended to:

1. Change the default PostgreSQL username and password
2. Replace the `WEBUI_SECRET_KEY` with a secure random string
3. Consider using a `.env` file for sensitive configuration values

## 📦 Volumes

- `postgres-data`: Stores PostgreSQL database files
- `ollama-data`: Stores Ollama models and configurations
- `open-webui-data`: Stores Open WebUI data not in the database

## 🛠️ Initialization Scripts

The `init-scripts` directory contains SQL scripts that are automatically executed when the PostgreSQL container is first created:

- `01-init.sql`: Creates the required PostgreSQL extensions like `uuid-ossp`

You can add additional initialization scripts to this directory if you need to pre-configure your database.

## 🔍 Troubleshooting

- If Open WebUI cannot connect to PostgreSQL, check the `DATABASE_URL` environment variable.
- For PostgreSQL connection issues, you can connect directly to the database:

```bash
docker exec -it postgres psql -U openwebui -d openwebui
```

- To view logs:

```bash
docker-compose logs -f
