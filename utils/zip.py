import os

from tqdm import tqdm
from shutil import make_archive
from typing import List


def zip_directory(zip_path: str, root_dir: str):
    """Creates a zip file in `zip_path` with the content of `root_dir`. 
    Do not include '.zip' in `zip_path`"""
    make_archive(zip_path, 'zip', os.path.dirname(root_dir),
                 os.path.basename(root_dir))


def zip_patient_dirs(patient_dirs: List[str], zip_dest_dir: str):
    """Zip all the directories inside `patient_dirs`. If you do not want
    to upload all the patients inside  """
    patients_stream = tqdm(patient_dirs)
    for patient_dir in patients_stream:
        patient_id = os.path.basename(patient_dir)
        patients_stream.set_description(
            f"Zipping the content of patient {patient_id}")
        zip_path_dest = os.path.join(zip_dest_dir, patient_id)
        zip_directory(zip_path_dest, patient_dir)