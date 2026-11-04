from cleanframe.phash import compute_dhash_from_grayscale_grid, hamming_distance_64
from cleanframe.sanitizer import build_ffmpeg_sanitize_cmd

def test_dhash_and_hamming():
    grid1 = [[(r * 20 + c * 10) % 256 for c in range(9)] for r in range(8)]
    grid2 = [[(255 - (r * 20 + c * 10)) % 256 for c in range(9)] for r in range(8)]
    h1 = compute_dhash_from_grayscale_grid(grid1)
    h2 = compute_dhash_from_grayscale_grid(grid2)
    dist = hamming_distance_64(h1, h2)
    assert dist > 30

def test_ffmpeg_pipeline_flags():
    cmd = build_ffmpeg_sanitize_cmd("raw.mov", "clean.mp4")
    assert "-map_metadata" in cmd
    assert "-1" in cmd
    assert "+bitexact" in cmd
    assert "crop=iw-4:ih-4:2:2,scale=iw:ih:flags=lanczos,eq=contrast=1.008:brightness=0.003:saturation=1.005,noise=alls=1:allf=t" in cmd
