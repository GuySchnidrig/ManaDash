# ManaDash

# install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# install Quarto separately
sudo apt update
sudo apt install quarto

# setup
cd ManaDash
uv sync
source .venv/bin/activate
cd website
quarto preview

