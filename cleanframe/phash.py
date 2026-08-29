"""64-bit Difference Hash (dHash) & Perceptual Hamming Distance Evaluator."""
from typing import List

def compute_dhash_from_grayscale_grid(grid_9x8: List[List[int]]) -> int:
    """
    Compute a 64-bit difference hash (dHash) from an 8-row by 9-column grayscale pixel matrix.
    Used to verify that spatio-temporal video perturbations shift frame hashes beyond
    automated duplicate-detection thresholds (Hamming distance >= 14 bits).
    """
    if len(grid_9x8) != 8 or any(len(row) != 9 for row in grid_9x8):
        raise ValueError("Grid must be 8 rows by 9 columns of grayscale intensities (0-255).")
    bits = 0
    for r in range(8):
        for c in range(8):
            bits = (bits << 1) | (1 if grid_9x8[r][c] > grid_9x8[r][c + 1] else 0)
    return bits

def hamming_distance_64(hash_a: int, hash_b: int) -> int:
    """Return the bit-level Hamming distance between two 64-bit perceptual hashes."""
    return bin((hash_a ^ hash_b) & ((1 << 64) - 1)).count("1")
