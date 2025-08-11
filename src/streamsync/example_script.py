from __future__ import annotations

import mne

from streamsync import StreamSync, extract_audio_from_video

# load an MNE raw file
raw = mne.io.read_raw("")
cam1 = "path/to/video"
flux1 = mne.io.read_raw("")
my_events = []


subjects = ["146a", "222b"]

for subj in subjects:
    # MEG data from SQUID
    ss = StreamSync(raw, "STIM001")
    # audio from camera
    audio1 = extract_audio_from_video(cam1, channel=2)
    ss.add_stream(audio1, channel=1)
    # MEG data from FLUX
    ss.add_stream(flux1, channel=127)
    # synchronize
    result = ss.do_syncing()
    # plot (to verify good sync)
    fig = ss.plot_sync()
    fig.savefig(...)  # optional
    # add camera events to SQUID raw as Annotations
    annot = ss.add_camera_events(my_events)
    raw.set_annotations(annot)
    if result < 0.7:
        write_log_msg(f"subj {subj} had bad pulse syncing")  # noqa: F821
        continue

    # apply maxfilter
    # do ICA
