import os
import shutil
import random

# Make directories
dataset_dir = os.environ.get('BODY_DATASET_DIR')
try:
  os.mkdir(f'{dataset_dir}/camera/training')
  os.mkdir(f'{dataset_dir}/camera/validation')
  os.mkdir(f'{dataset_dir}/log/training')
  os.mkdir(f'{dataset_dir}/log/validation')
except:
  print('training/validation directories already exist')

file_list = os.listdir(f'{dataset_dir}/camera')
# Filter out directories
file_list = [file for idx, file in enumerate(file_list) if os.path.isfile(os.path.join(f'{dataset_dir}/camera/', file))]    
print(f"{len(file_list)} files")

random.shuffle(file_list)
valid_ratio = 0.2

for idx, file in enumerate(file_list):
  if ((idx/len(file_list)) > (1-valid_ratio)):
    shutil.move(f"{dataset_dir}/camera/{file}", f"{dataset_dir}/camera/validation/{file}")
    shutil.move(f"{dataset_dir}/log/{file}", f"{dataset_dir}/log/validation/{file}")
  else:
    shutil.move(f"{dataset_dir}/camera/{file}", f"{dataset_dir}/camera/training/{file}")
    shutil.move(f"{dataset_dir}/log/{file}", f"{dataset_dir}/log/training/{file}")
