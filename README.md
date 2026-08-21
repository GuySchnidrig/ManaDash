# ManaDash


# Linux
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


# Windows
# install uv (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# install Quarto
$env:Path += ";$env:USERPROFILE\.local\bin"
$env:Path += ";C:\Program Files\Quarto\bin"

# setup
uv sync
.venv\Scripts\activate
cd website
quarto preview