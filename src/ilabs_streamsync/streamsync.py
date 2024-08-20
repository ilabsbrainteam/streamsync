from __future__ import annotations

import os
import pathlib
import subprocess

import matplotlib.pyplot as plt
import numpy as np
from scipy.io.wavfile import read as wavread


class StreamSync:
    """Synchronize two data streams.

    Inputs: `mne.io.Raw` files, audio files (TODO which formats?),
    and additional camera events.

    Outputs: `mne.Annotations` object created from the camera events and
    time-warped to the timescale of the `Raw`.
    """

    def __init__(self, reference_object, pulse_channel):
        # self.ref_stream = reference_object.get_chan(pulse_channel)
        self.ref_stream = None
        # self.sfreq = reference_object.info["sfreq"]  # Hz
        self.sfreq = 0
        self.streams = [] #  of (filename, srate, Pulses, Data)

    def add_stream(self, stream, channel=None, events=None):
        """Add a new ``Raw`` or video stream, optionally with events.
        stream : str
            File path to an audio or FIF stream.
        channel : str | int | None
            Which channel of `stream` contains the sync pulse sequence.
        events : array-like | None
            Events associated with the stream. TODO: should they be integer sample
            numbers? Timestamps? Do we support both?
        """
        srate, pulses, data = self._extract_data_from_stream(stream, channel=channel)
        self.streams.append((stream, srate, pulses, data))

    def _extract_data_from_stream(self, stream, channel):
        """Extracts pulses and raw data from stream provided."""
        ext = pathlib.Path(stream).suffix
        if ext == ".fif":
            return self._extract_data__from_raw(stream, channel)
        if ext == ".wav":
            return self._extract_data_from_wav(stream, channel)
        raise TypeError("Stream provided was of unsupported format. Please provide a fif or wav file.")
            

    def _extract_data__from_raw(self, stream, channel):
        pass

    def _extract_data_from_wav(self, stream, channel):
        "Returns tuple of (pulse channel, audio channel) from stereo file."
        srate, wav_signal = wavread(stream)
        return (srate, wav_signal[:,channel], wav_signal[:,1-channel])

    def do_syncing(self):
        """Synchronize all streams with the reference stream."""
        # TODO (waves hands) do the hard part.
        # TODO spit out a report of correlation/association between all pairs of streams

    def plot_sync_pulses(self, tmin=0, tmax=float('inf')):
        # TODO Plot the raw file on the first plot.
        fig, axset = plt.subplots(len(self.streams)+1, 1, figsize = [8,6]) #show individual channels seperately, and the 0th plot is the combination of these. 
        for i, stream in enumerate(self.streams):
            npts = len(stream[2])
            tt = np.arange(npts) / stream[1]
            idx = np.where((tt>=tmin) & (tt<tmax))
            axset[i+1].plot(tt[idx], stream[2][idx].T)
            axset[i+1].set_title(pathlib.Path(stream[0]).name)
            # Make label equal to simply the cam number
        plt.show()

def extract_audio_from_video(path_to_video, output_dir):
    """Extracts audio from path provided.

    path_to_video: str
        Path to audio file
        TODO allow path_to_video to take regex?
    output_dir: str
        Path to directory where extracted audio should be sent

    Effects:
        Creates output directory if non-existent. For each video found, creates
        a file with the associated audio labeled the same way.

    Raises:
        ValueException if video path does not exist, 
        Exception if filename is taken in output_dir
    """
    audio_codecout = 'pcm_s16le'
    audio_suffix = '_16bit'
    p = pathlib.Path(path_to_video)
    audio_file = p.stem + audio_suffix + '.wav'
    if not p.exists():
        raise ValueError('Path provided cannot be found.')
    if pathlib.PurePath.joinpath(pathlib.Path(output_dir), pathlib.Path(audio_file)).exists():
        raise Exception(f"Audio already exists for {path_to_video} in output directory.")

    command = ['ffmpeg',
        '-acodec', 'pcm_s24le',       # force little-endian format (req'd for Linux)
        '-i', path_to_video,
        '-map', '0:a',                # audio only (per DM)
#         '-af', 'highpass=f=0.1',
        '-acodec', audio_codecout,
        '-ac', '2',                   # no longer mono output, so setting to "2"
        '-y', '-vn',                  # overwrite output file without asking; no video
        '-loglevel', 'error',
        audio_file]
    pipe = subprocess.run(command, timeout=50, check=False)

    if pipe.returncode==0:
        print(f'Audio extraction was successful for {path_to_video}')
        output_path = pathlib.PurePath.joinpath(pathlib.Path(output_dir), pathlib.Path(audio_file))
        os.renames(audio_file, output_path)
    else:
        print(f"Audio extraction unsuccessful for {path_to_video}")