.PHONY: setup dev-backend dev-frontend test clean

setup:
	cd backend && python -m venv venv && .\venv\Scripts\activate && pip install -r requirements.txt

dev-backend:
	cd backend && uvicorn app.main:app --reload

dev-frontend:
	cd frontend && npm run dev

test:
	cd backend && pytest

clean:
	find . -type d -name __pycache__ -exec rm -r {} \+
	find . -type f -name "*.pyc" -delete
