up:
	docker compose up --build

backend-dev:
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

frontend-dev:
	cd frontend && npm run dev

migrate:
	cd backend && alembic upgrade head

test-backend:
	cd backend && pytest -q

test-frontend:
	cd frontend && npm run test
