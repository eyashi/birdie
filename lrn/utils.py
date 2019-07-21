# for any repeatedly used utility files

import os
import csv

import pathlib
import psutil
import random


def check_data_drive(drive_name):
    # validates that the drive is present, returns the drive name if it is. Not that cool.
    if drive_name in [i.device for i in psutil.disk_partitions()]:
        return drive_name
    else:
        return False


def generate_subset_of_data(
    data_drive_path, num_samples=10, output_path="samples", generate_new_subset=False
):

    if os.path.isfile(
        os.path.join(output_path, "{}-selected-samples.txt".format(num_samples))
    ):
        if not generate_new_subset:
            return

    sample_pool = []
    collected_samples = []

    # make the sample pool of all available audio files
    for fold in os.listdir(data_drive_path):
        d1 = os.path.join(data_drive_path, fold)
        try:
            if os.path.isdir(d1):
                for f in os.listdir(d1):
                    d2 = os.path.join(d1, f)
                    if os.path.isdir(d2):
                        sample_pool += [os.path.join(d2, i) for i in os.listdir(d2)]
        except:
            pass

    if num_samples == "all":
        with open(
            os.path.join(output_path, "{}-selected-samples.txt".format(num_samples)),
            "w",
        ) as f:
            for i in sample_pool:
                f.write(i + "\n")
    else:
        while len(collected_samples) < num_samples:
            idx = random.randint(0, len(sample_pool) - 1)
            collected_samples.append(sample_pool[idx])

        with open(
            os.path.join(output_path, "{}-selected-samples.txt".format(num_samples)),
            "w",
        ) as f:
            for i in collected_samples:
                f.write(i + "\n")


if __name__ == "__main__":
    generate_subset_of_data("E:\\", 50)

