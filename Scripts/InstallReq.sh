#!/bin/bash -l
#SBATCH --job-name=InstallReq
#SBATCH --account=pawsey0411
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=00:03:00

echo "Installing Requirements"

source /software/projects/pawsey0411/oanwar/TestEnv/bin/activate

pip install -r /software/projects/pawsey0411/oanwar/2023-01-data-science-exercise/requirements.txt

echo "Done installing the requirements"