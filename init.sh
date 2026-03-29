#!/usr/bin/env bash
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "Initializing DevDrop virtual environment..."
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

echo "Installing launcher devdrop in ~/.local/bin..."
mkdir -p ~/.local/bin

cat << 'EOF' > ~/.local/bin/devdrop
#!/usr/bin/env bash
PROJECT_DIR="DIR_PLACEHOLDER"
cd "$PROJECT_DIR"
source .venv/bin/activate
python main.py "$@"
EOF

sed -i "s|DIR_PLACEHOLDER|$DIR|g" ~/.local/bin/devdrop
chmod +x ~/.local/bin/devdrop

echo "DevDrop initialized. You can now run 'devdrop' from anywhere if ~/.local/bin is in your PATH."
