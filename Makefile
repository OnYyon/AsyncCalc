all: install run
install:
	uv sync
run:
	uv run uvicorn src.api.utils.handlers:app --port 8000 --host 0.0.0.0
dev:
	uv run uvicorn src.api.utils.handlers:app --port 8000 --host 0.0.0.0 --reload