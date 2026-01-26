.PHONY: execute autoflake pre-commit

execute:
	uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload

autoflake:
	autoflake --in-place --remove-all-unused-imports --remove-unused-variables --expand-star-imports --recursive app/

pre-commit: autoflake
	pre-commit run --all-files
