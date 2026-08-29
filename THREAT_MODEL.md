# Threat Model: Evidentiary Mobile Video Sanitization

## 1. Threat Vectors
1. **Container & Sensor Attribution:** Automated extraction of QuickTime (`moov/udta/meta`) atoms, creation timestamps, GPS tags, and hardware H.264/HEVC quantization matrices from raw `.mov` and `.mp4` uploads.
2. **Perceptual Hash Blocklisting:** Automated filtering using 64-bit `pHash`, `dHash`, and Temporal Match Kernel (TMK) signatures to suppress or trace re-uploaded evidentiary footage.

## 2. CleanFrame-OSS Countermeasures
- **Zero-Metadata Remuxing:** `-map_metadata -1 -map_chapters -1 -fflags +bitexact` strips 100% of container and stream tags.
- **Calibrated Spatio-Temporal Perturbation:** Lanczos 4px crop/rescale + micro-contrast/brightness transformation shifts 64-bit `dHash`/`pHash` Hamming distances by `>= 14 bits` while preserving human-visible evidentiary detail.
- **Offline Chain-of-Custody:** Optional pre-sanitization `SHA-256` manifest (`--manifest`) stored locally.
