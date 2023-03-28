#!/bin/bash -l
#SBATCH --job-name=ICRAR_excer_Job
#SBATCH --partition=work
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=00:02:00

echo "Starting program"
cd /software/projects/pawsey0411/oanwar/2023-01-data-science-exercise/tests
python3 exercise_functions_test.py