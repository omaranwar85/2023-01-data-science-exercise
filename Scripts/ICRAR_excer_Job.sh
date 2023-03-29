#!/bin/bash -l
#SBATCH --job-name=ICRAR_excer_Job
#SBATCH --partition=work
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=00:02:00

echo "Creating ENV"

module load python/3.9.15
python3 -m venv /software/projects/pawsey0411/oanwar/TestEnv

pip install --upgrade pip

echo "Done creating 'TestEnv' ENV"

source /software/projects/pawsey0411/oanwar/TestEnv/bin/activate
echo "Environment activated"

echo "Loading Modules"
module load numpy/1.21.5
module load pandas/1.4.4
module load python_dateutil/2.8.2
module load scipy/1.9.1
echo "Modules loaded"

echo "Generating clean files"
cd $MYSCRATCH

export PYTHONPATH=${/software/projects/pawsey0411/oanwar/2023-01-data-science-exercise/src
python3 /software/projects/pawsey0411/oanwar/2023-01-data-science-exercise/tests/exercise_functions_test.py

deactivate