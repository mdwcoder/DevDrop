#!/usr/bin/env bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

if [ ! -d ".venv" ]; then
    echo "Virtual environment not found. Please run init.sh first."
    exit 1
fi

source .venv/bin/activate
python main.py "$@"
