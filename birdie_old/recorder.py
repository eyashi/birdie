import os
import sys
from datetime import datetime
import librosa
import numpy as np
import logging

import sounddevice as sd

import constants

"""
This class will allow you to record continuous clips using the default
audio device of your computer. Set some constants in constants.py and
run to start collecting audio data. Yay.
"""


class Recorder:
    def __init__(self, sr=constants.REC_SAMPLE_RATE):
        self.sr = sr
        if not os.path.isdir(constants.DEFAULT_RECORDING_DIR):
            os.mkdir(constants.DEFAULT_RECORDING_DIR)

    def make_clip(
        self,
        clip_duration=10,
        output_format="npy",
        output_dir=constants.DEFAULT_RECORDING_DIR,
    ):
        """
        Makes a single recording.
        Returns the size of the recorded file.
        """

        clip_time_stamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        raw_rec = sd.rec(int(clip_duration * self.sr), samplerate=self.sr, channels=1)
        sd.wait()

        # remove extra axis brought along with recording. not sure what it's doing there.
        rec_clean = np.squeeze(raw_rec)

        if output_format == "npy":
            out_path = os.path.join(output_dir, clip_time_stamp + ".npy")
            np.save(out_path, rec_clean)

        elif output_format == "wav":
            out_path = os.path.join(output_dir, clip_time_stamp + ".wav")
            librosa.output.write_wav(out_path, rec_clean, self.sr)

        else:
            raise NotImplementedError("This output format is not supported.")

        return rec_clean.nbytes / 1000000

    def start_recording(
        self,
        clip_duration=10,
        output_format="npy",
        output_dir=constants.DEFAULT_RECORDING_DIR,
        end_time=None,
        data_limit=None,
    ):
        """
        Start a recording loop.
        Specify the end time to stop at a particular date and time. (Datetime type)
        Specify a data limit to stop when the exported data exceeds a limit. (Megabytes)
        """
        # validate end time
        if end_time:
            if end_time < datetime.now():
                raise ValueError("End date provided is already in the past.")

        data_generated = 0
        recording_count = 0

        while 1:
            try:
                if data_limit:
                    if data_generated > data_limit:
                        print("Data limit reached, stopping recording.")
                        break

                if end_time:
                    if datetime.now() > end_time:
                        print("End time reached, stopping recording.")
                        break

                file_size = self.make_clip(clip_duration, output_format, output_dir)

                data_generated += file_size
                recording_count += 1

            except KeyboardInterrupt:
                break

        # print recording summary
        print("Recorded {} Mb of data.".format(data_generated))
        print("Created {} recordings".format(recording_count))


if __name__ == "__main__":
    # TODO: make this take command line arguments
    r = Recorder()
    # r.start_recording(output_format="wav", data_limit=5)
    r.start_recording()
