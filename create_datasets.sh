#!/bin/bash
#SBATCH --partition=cpu-6h
#SBATCH --output=log/output_%A_%a.log
#SBATCH --mail-type=END,FAIL

source venv/bin/activate

python3 -m processor.make_datasets