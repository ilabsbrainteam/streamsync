from __future__ import annotations

import os
import subprocess


class StreamSync:
    """Synchronize two data streams.

    Inputs: `mne.io.Raw` files, audio files (TODO which formats?),
    and additional camera events.

    Outputs: `mne.Annotations` object created from the camera events and
    time-warped to the timescale of the `Raw`.
    """

    def __init__(self, reference_object, pulse_channel):
        self.ref_stream = reference_object.get_chan(pulse_channel)
        self.sfreq = reference_object.info["sfreq"]  # Hz
        self.streams = []

    def add_stream(self, stream, channel=None, events=None):
        """Add a new ``Raw`` or video stream, optionally with events.

        stream : Raw | wav
            An audio or FIF stream.
        channel : str | int | None
            Which channel of `stream` contains the sync pulse sequence.
        events : array-like | None
            Events associated with the stream. TODO: should they be integer sample
            numbers? Timestamps? Do we support both?
        """
        pulses = self._extract_pulse_sequence_from_stream(stream, channel=channel)
        self.streams.append(pulses)

    def _extract_pulse_sequence_from_stream(self, stream, channel):
        # TODO triage based on input type (e.g., if it's a Raw, pull out a stim chan,
        # if it's audio, just add it as-is)
        pass

    def do_syncing(self):
        """Synchronize all streams with the reference stream."""
        # TODO (waves hands) do the hard part.
        # TODO spit out a report of correlation/association between all pairs of streams

    def plot_sync(self):
        pass


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
        Exception if filename is taken in output_dir
    """
    audio_codecout = 'pcm_s16le'
    audio_suffix = '_16bit'
    audio_file = os.path.basename(path_to_video) + audio_suffix + '.wav'
    if not os.path.exists(path_to_video):
        raise ValueError('Path provided cannot be found.')
    if os.path.exists(os.path.join(output_dir, audio_file)):
        raise Exception("Audio already exists for " + path_to_video + " in output directory " + output_dir)

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
    pipe = subprocess.run(command, timeout=50)

    if pipe.returncode==0:
        print('Audio extraction was successful for ' + path_to_video)
        output_path = os.path.join(output_dir, audio_file)
        os.renames(audio_file, output_path)
    else:
        print("Audio extraction unsuccessful for " + path_to_video)