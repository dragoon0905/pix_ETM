#!/bin/bash

#SBATCH --job-name=train_pix_rio
#SBATCH --gres=gpu:1
#SBATCH -o ./slurm/gta52rio_labnode3.out
#SBATCH --time=24:00:00

#cp -r /data/dataset/GTA5  /local_datasets/GTA5
#cp -r /data/dataset/SYNTHIA  /local_datasets/SYNTHIA
#cp -r /data/dataset/NTHU_Datasets  /local_datasets/NTHU_Datasets

source /data/seunan/init.sh
conda activate torch38gpu

HYDRA_FULL_ERROR=1 python main_crosscity.py --config-name=gta5_crosscity lam_aug=0.10 name=gta52rio_baseline_node3


#rm -rf /local_datasets/GTA5
#rm -rf /local_datasets/SYNTHIA
#rm -rf /local_datasets/NTHU_Datasets