ENV_ACTIVATE=$(grep ENV_ACTIVATE .env | cut -d '=' -f2)
source $ENV_ACTIVATE && python -m pytest -v tests