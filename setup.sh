set -e

python3 -m pip install --upgrade pip
pip install -r python_requirements.txt

Rscript r_requirements.R
