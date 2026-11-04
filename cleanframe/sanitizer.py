"""FFmpeg Bitstream Sanitization, Container Atom Stripping & Provenance Manifest Engine."""
import hashlib
import json
import os
import subprocess
import datetime
from typing import Dict, List

def build_ffmpeg_sanitize_cmd(
    input_path: str,
    output_path: str,
    crf: int = 19,
    perturb_phash: bool = True,
) -> List[str]:
    """
    Construct the deterministic client-side FFmpeg pipeline that:
    1. Strips all EXIF, XMP, Apple QuickTime atoms, GPS tags, and chapter markers (-map_metadata -1).
    2. Applies sub-perceptible Lanczos crop/scale + micro-contrast/saturation shift to break pHash/MD5 blocklists.
    3. Re-encodes clean H.264/AAC bitstreams with bitexact flags.
    """
    vf = (
        "crop=iw-4:ih-4:2:2,scale=iw:ih:flags=lanczos,"
        "eq=contrast=1.008:brightness=0.003:saturation=1.005,noise=alls=1:allf=t"
        if perturb_phash
        else "scale=iw:ih"
    )
    af = "asetrate=44100*1.001,aresample=44100,volume=1.002" if perturb_phash else "anull"
    return [
        "ffmpeg", "-y", "-i", input_path,
        "-map_metadata", "-1",
        "-map_chapters", "-1",
        "-vf", vf,
        "-af", af,
        "-c:v", "libx264", "-preset", "medium", "-crf", str(crf), "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "160k",
        "-fflags", "+bitexact", "-flags:v", "+bitexact", "-flags:a", "+bitexact",
        "-movflags", "+faststart",
        output_path,
    ]

def generate_provenance_manifest(file_path: str) -> Dict[str, str]:
    """Generate an offline SHA-256 chain-of-custody verification manifest prior to sanitization."""
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return {
        "tool": "CleanFrame-OSS v0.4.2",
        "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "original_filename": os.path.basename(file_path),
        "original_size_bytes": str(os.path.getsize(file_path)),
        "original_sha256": h.hexdigest(),
    }
