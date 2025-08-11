from __future__ import annotations

import os

import matplotlib.pyplot as plt
import mne
import numpy as np
from numpy.typing import ArrayLike

type Stream = mne.io.BaseRaw | ArrayLike
type Channel = str | int
type PathLike = str | bytes | os.PathLike


class StreamSync:
    """Synchronize two data streams.

    Inputs: `mne.io.Raw` files, audio files (TODO which formats?),
    and additional camera events.

    Outputs: `mne.Annotations` object created from the camera events and
    time-warped to the timescale of the `Raw`.
    """

    def __init__(self, reference_object: Stream, pulse_channel: Channel) -> None:
        self.ref_stream: ArrayLike = reference_object.get_chan(pulse_channel)
        self.sfreq: float = reference_object.info["sfreq"]  # Hz
        self.streams: list[Stream] = []

    def add_camera_events(self, events: ArrayLike) -> mne.Annotations:  # noqa: ARG002
        return mne.Annotations([], [], [])

    def add_stream(
        self,
        stream: Stream,
        channel: Channel,
        events: ArrayLike | None = None,  # noqa: ARG002
    ) -> StreamSync:
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
        return self

    def _extract_pulse_sequence_from_stream(
        self,
        stream: Stream,  # noqa: ARG002
        channel: Channel,  # noqa: ARG002
    ) -> ArrayLike:
        # TODO triage based on input type (e.g., if it's a Raw, pull out a stim chan,
        # if it's audio, just add it as-is)
        return np.array([])  # fake return

    def do_syncing(self) -> float:
        """Synchronize all streams with the reference stream."""
        # TODO (waves hands) do the hard part.
        # TODO spit out a report of correlation/association between all pairs of streams
        return 0.0

    def plot_sync(self) -> plt.figure.Figure:
        return plt.figure.Figure()


def extract_audio_from_video(path_to_video: PathLike, channel: Channel) -> ArrayLike:  # noqa: ARG001
    """Path can be a regex or glob to allow batch processing."""
    return np.array([])  # fake return
