build:
	@echo Building instances
	@docker-compose -f docker-compose.dev.yml build

start:
	@echo Starting instances
	@docker-compose -f docker-compose.dev.yml up -d

stop:
	@echo Shutting down instances
	@docker-compose down

restart:
	@echo Shutting down instances
	@docker-compose down
	@echo Starting instances
	@docker-compose -f docker-compose.dev.yml up -d --build

status:
	@echo Checking application status
	@docker ps -a

test:
	@echo Runing tests
	@docker-compose exec api sh -c "cd ../ && pytest"

migrations:
	@echo Making database migrations
	@docker-compose exec api python manage.py makemigrations

migrate:
	@echo Making database migrations
	@docker-compose exec api python manage.py migrate

lint:
	@echo Checking codebase for errors, styling issues and complexity
	@docker-compose exec api flake8 /app/src /app/tests

create_certs:
	@echo Generating certificates
	@cd certs; mkcert -cert-file cert.pem -key-file key.pem localhost 127.0.0.1