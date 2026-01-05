# AgentWall Makefile
# Quick commands for development
# Domain: agentwall.io

.PHONY: help install up down logs test clean

# Default target
help:
	@echo "🛡️  AgentWall - Development Commands"
	@echo "    agentwall.io"
	@echo ""
	@echo "Setup:"
	@echo "  make install    Install dependencies"
	@echo "  make setup      Setup environment (.env file)"
	@echo ""
	@echo "Docker:"
	@echo "  make up         Start all services"
	@echo "  make down       Stop all services"
	@echo "  make restart    Restart all services"
	@echo "  make logs       View logs (all services)"
	@echo "  make logs-api   View FastAPI logs"
	@echo ""
	@echo "Development:"
	@echo "  make test       Run tests"
	@echo "  make test-cov   Run tests with coverage"
	@echo "  make lint       Run linters"
	@echo "  make format     Format code"
	@echo ""
	@echo "Database:"
	@echo "  make db-init    Initialize ClickHouse schema"
	@echo "  make db-query   Open ClickHouse client"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean      Clean temporary files"
	@echo "  make reset      Reset all data (WARNING: destructive)"

# Setup
install:
	@echo "📦 Installing dependencies..."
	cd fastapi && pip install -r requirements.txt

setup:
	@echo "⚙️  Setting up environment..."
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "✅ Created .env file. Please edit it with your values."; \
	else \
		echo "⚠️  .env file already exists. Skipping."; \
	fi

# Docker
up:
	@echo "🚀 Starting AgentFirewall..."
	docker-compose up -d
	@echo "✅ Services started!"
	@echo ""
	@echo "FastAPI:    http://localhost:8000"
	@echo "ClickHouse: http://localhost:8123"
	@echo "Redis:      localhost:6379"

down:
	@echo "🛑 Stopping AgentFirewall..."
	docker-compose down

restart:
	@echo "🔄 Restarting AgentFirewall..."
	docker-compose restart

logs:
	docker-compose logs -f

logs-api:
	docker-compose logs -f fastapi

# Development
test:
	@echo "🧪 Running tests..."
	cd fastapi && pytest tests/ -v

test-cov:
	@echo "🧪 Running tests with coverage..."
	cd fastapi && pytest tests/ -v --cov=. --cov-report=html
	@echo "📊 Coverage report: fastapi/htmlcov/index.html"

lint:
	@echo "🔍 Running linters..."
	cd fastapi && ruff check .
	cd fastapi && mypy .

format:
	@echo "✨ Formatting code..."
	cd fastapi && black .
	cd fastapi && ruff check --fix .

# Database
db-init:
	@echo "🗄️  Initializing ClickHouse schema..."
	docker-compose exec clickhouse clickhouse-client --multiquery < clickhouse/init/01-create-database.sql
	@echo "✅ Schema initialized!"

db-query:
	@echo "🗄️  Opening ClickHouse client..."
	docker-compose exec clickhouse clickhouse-client --database=agentfirewall

# Cleanup
clean:
	@echo "🧹 Cleaning temporary files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "✅ Cleaned!"

reset:
	@echo "⚠️  WARNING: This will delete all data!"
	@read -p "Are you sure? (yes/no): " confirm; \
	if [ "$$confirm" = "yes" ]; then \
		docker-compose down -v; \
		echo "✅ All data deleted!"; \
	else \
		echo "❌ Cancelled."; \
	fi

# Quick start
quickstart: setup up
	@echo ""
	@echo "🎉 AgentWall is ready!"
	@echo "   agentwall.io"
	@echo ""
	@echo "Next steps:"
	@echo "1. Edit .env file with your OpenAI API key"
	@echo "2. Run: make restart"
	@echo "3. Test: curl http://localhost:8000"
	@echo ""
	@echo "Documentation: http://localhost:8000/docs"
