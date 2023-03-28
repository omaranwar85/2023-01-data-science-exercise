#!/bin/bash -l
#SBATCH --job-name=ICRAR_excer_Job
#SBATCH --partition=work
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=00:02:00

echo "Creating ENV"
python3 -m ICRAR_excer_Job /software/projects/pawsey0411/oanwar/

cd /software/projects/pawsey0411/oanwar/2023-01-data-science-exercise

pip install -r requirements.txt

echo "Done creating 'ICRAR_excer_Job' ENV"