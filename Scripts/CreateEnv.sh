#!/bin/bash -l
#SBATCH --job-name=CreateEnv
#SBATCH --partition=work
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=00:02:00

echo "Creating ENV"
python3 -m TestEnv /software/projects/pawsey0411/oanwar/

cd /software/projects/pawsey0411/oanwar/2023-01-data-science-exercise

source TestEnv/bin/activate
pip install -r requirements.txt

echo "Done creating 'TestEnv' ENV"