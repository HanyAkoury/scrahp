BLUE="\e[34m"
RED="\e[31m"
GREEN="\e[32m"
YELLOW="\e[33m"
ENDCOLOR="\e[0m"

source .venv/Scripts/activate

echo -e "${BLUE}> Run Flake8 verification.${ENDCOLOR}"
poetry run flake8 scrahp
echo -e "${GREEN}... > Flake8 verification done.${ENDCOLOR}\n"

echo -e "${BLUE}> Run Mypy verification.${ENDCOLOR}"
poetry run mypy scrahp
echo -e "${GREEN}... > Mypy verification done.${ENDCOLOR}\n"

echo -e "${BLUE}> Run Black verification.${ENDCOLOR}"
poetry run black .
echo -e "${GREEN}... > Black verification done.${ENDCOLOR}\n"

echo -e "${BLUE}> Run iSort verification.${ENDCOLOR}"
poetry run isort .
echo -e "${GREEN}... > iSort verification done.${ENDCOLOR}\n"
