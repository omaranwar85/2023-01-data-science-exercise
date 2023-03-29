#!/bin/bash -l
#SBATCH --job-name=ICRAR_excer_Job
#SBATCH --partition=work
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=00:02:00

source /software/projects/pawsey0411/oanwar/TestEnv/bin/activate
echo "Environment activated"

echo "Loading Modules"
module load python/3.9.15
module load numpy/1.21.5
module load pandas/1.4.4
module load python_dateutil/2.8.2
module load scipy/1.9.1
echo "Modules loaded"

echo "Generating figures"
cd $MYSCRATCH
python3 /software/projects/pawsey0411/oanwar/2023-01-data-science-exercise/tests/exercise_functions_test.py