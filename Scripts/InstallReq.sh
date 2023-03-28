#!/bin/bash -l
#SBATCH --job-name=InstallReq
#SBATCH --account=pawsey0411
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=00:01:00

echo "Installing Requirements"

cd /software/projects/pawsey0411/oanwar

source TestEnv/bin/activate
pip install --upgrade pip

cd /CreateEnv.sh
pip install -r requirements.txt

echo "Done installing the requirements"