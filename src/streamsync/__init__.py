"""
Copyright (c) 2024 Daniel McCloy. All rights reserved.

ilabs_streamsync: General-purpose tool for syncing data sources via pulse sequences.
"""

from __future__ import annotations

# from ._version import version as __version__
from .streamsync import StreamSync, extract_audio_from_video

__all__ = ["__version__", "StreamSync", "extract_audio_from_video"]
