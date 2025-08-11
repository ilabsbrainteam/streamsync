from __future__ import annotations

import importlib.metadata

import streamsync as m


def test_version():
    assert importlib.metadata.version("ilabs_streamsync") == m.__version__
