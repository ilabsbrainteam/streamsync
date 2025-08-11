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

    def add_stream(self, stream, channel=None, events=None):  # noqa ARG002
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
        pass

    def plot_sync(self):
        pass


def extract_audio_from_video(path_to_video, channel):  # noqa ARG001
    """Path can be a regex or glob to allow batch processing."""
    pass
