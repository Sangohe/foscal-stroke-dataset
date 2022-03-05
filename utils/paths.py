import os

from glob import glob
from typing import List, Optional, Union


def is_patient_dir_in_ignore_list(patient_dir: str, ignore_list: List[str]):
    """Utility function to tell if a path needs to be discarded"""
    for id_to_ignore in ignore_list:
        if id_to_ignore in os.path.basename(patient_dir):
            return True
    return False


def get_patients_dirs(src_dir: str,
                      ignore_patients: Optional[List[str]] = None,
                      ignore_from_patient: Optional[Union[int, str]] = None,
                      ignore_until_patient: Optional[Union[int, str]] = None):
    """Get a list of all the patients inside one of the directories of the
    FOSCAL database. If you want to filter out some patients use kwargs:
        
        patients = ['ACV-001', 'ACV-002', 'ACV-003', 'ACV-004']
        `ignore_patients`: to be specific about which patients to drop,
            e.g. 'ACV-001', 'ACV-003' -> patients = ['ACV-002', 'ACV-004']
        `ignore_from_patient`: drop all the patients from this id until
        the last one
            e.g. from 3 or '003' -> patients = ['ACV-001', 'ACV-002']
        `ignore_until_patient`: drop all the patients from begginning 
        until this id
            e.g. until 3 or '003' -> patients = ['ACV-003', 'ACV-004']
    """
    patient_dirs = sorted(glob(os.path.join(src_dir, '*')))
    patient_dirs = [d for d in patient_dirs if os.path.isdir(d)]

    patients_to_ignore = []
    if ignore_patients is not None:
        patients_to_ignore = ignore_patients
    elif ignore_from_patient is not None:
        if isinstance(ignore_from_patient, str):
            ignore_from_patient = int(ignore_from_patient)
        patients_to_ignore = [
            f'{i:03d}' for i in range(ignore_from_patient,
                                      len(patient_dirs) + 1)
        ]
    elif ignore_until_patient is not None:
        if isinstance(ignore_until_patient, str):
            ignore_until_patient = int(ignore_until_patient)
        patients_to_ignore = [
            f'{i:03d}' for i in range(ignore_until_patient + 1)
        ]

    # Drop the patient dirs inside patients_to_ignore.
    if patients_to_ignore:
        patient_dirs = [
            d for d in patient_dirs
            if not is_patient_dir_in_ignore_list(d, patients_to_ignore)
        ]

    return patient_dirs