.DEFAULT_GOAL := help

run: ## run the application using uvicorn 
	poetry run uvicorn main:app --host 0.0.0.0 --port 8000 --reload


migrate:
	alembic revision --autogenerate -m $(MIGRATION)

migrate-apply:
	alembic upgrade head