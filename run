#!/bin/zsh

VENV_DIR=${1:-venv}

echo "Creating virtual environment in ./${VENV_DIR} ..."

python3 -m venv $VENV_DIR

if [[ $? -ne 0 ]]; then
  echo "Failed to create virtual environment."
  exit 1
fi

echo "Activating virtual environment..."
source $VENV_DIR/bin/activate

echo "Installing dependencies..."
pip install --upgrade pip
pip install discord.py python-dotenv

echo "Setup complete! Virtual environment '$VENV_DIR' is active."
echo "Running bot..."
python bot.py
