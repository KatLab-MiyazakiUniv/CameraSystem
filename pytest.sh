#bash

set -eu
cd source
PYTHONPATH=. poetry run pytest --cov=. --cov=block_bingo --cov=bluetooth --cov=detection_number --cov=detection_block --cov=decision_points --cov-branch
