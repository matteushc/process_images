#!/usr/bin/env bash
set -euo pipefail

# Create virtualenv in .venv if it doesn't exist. Prefer `virtualenv` if available, fallback to `python3 -m venv`.
if [ ! -d ".venv" ]; then
	if command -v virtualenv >/dev/null 2>&1; then
		virtualenv .venv
	else
		python3 -m venv .venv
	fi
fi

# If a Python virtualenv exists in .venv, activate it for the run
if [ -f ".venv/bin/activate" ]; then
	# shellcheck disable=SC1091
	source .venv/bin/activate
    pip install -r requirements.txt
fi

mkdir -p ./encartes/
mkdir -p ./images/removed/
mkdir -p ./images/produtos/
mkdir -p ./images/produtos_produtos_filtrados/

echo "1) Downloading encarte (PDF)..."
python3 download_encarte.py

echo "2) Extracting images from PDF..."
python3 extract_image_from_pdf.py

echo "3) Removing background color from extracted images..."
python3 remove_background_color.py

echo "4) Detecting contours and saving product crops..."
python3 detect_image.py

echo "5) Filtering product crops with OCR..."
python3 read_image.py

echo "Pipeline finished."
