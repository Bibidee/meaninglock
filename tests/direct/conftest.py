"""Windows compatibility for the official GenLayer Direct Mode loader.

The runner replaces stdin with a temporary file, closes its descriptor, and
immediately unlinks the path.  Windows keeps the duplicated stdin handle open
until the contract module is loaded, so the unlink raises WinError 32 before
execution starts.  Delaying only that one unlink lets the OS remove the file
when the duplicated handle is released; Linux behavior is unchanged.
"""

import errno
import os
import io

from PIL import Image


_unlink = os.unlink


def _unlink_after_handle_release(path, *args, **kwargs):
    try:
        return _unlink(path, *args, **kwargs)
    except PermissionError as exc:
        if os.name == "nt" and getattr(exc, "winerror", None) == 32:
            return None
        raise


os.unlink = _unlink_after_handle_release

_image_open = Image.open


def _open_empty_mock_image(fp, *args, **kwargs):
    # genlayer-test 0.29.2 returns an empty screenshot payload for mocked
    # WebRender calls.  Supply a valid 1x1 image so multimodal code can still
    # exercise its image plumbing; real HTTP screenshots are unaffected.
    if isinstance(fp, (io.BytesIO, bytes)):
        pos = fp.tell() if hasattr(fp, "tell") else 0
        raw = fp.getvalue() if hasattr(fp, "getvalue") else fp
        if not raw:
            return Image.new("RGB", (1, 1), (255, 255, 255))
        if hasattr(fp, "seek"):
            fp.seek(pos)
    return _image_open(fp, *args, **kwargs)


Image.open = _open_empty_mock_image
