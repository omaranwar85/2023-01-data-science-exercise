#!/bin/bash -l
#SBATCH --job-name=CreateEnv
#SBATCH --partition=work
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=00:01:00

echo "Creating ENV"

module load python/3.9.15
python3 -m venv /software/projects/pawsey0411/oanwar/TestEnv

cd /software/projects/pawsey0411/oanwar

source TestEnv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "Done creating 'TestEnv' ENV"