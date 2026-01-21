.PHONY: execute

execute:
	uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload

pre-commit:
	pre-commit run --all-files
