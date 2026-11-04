# CleanFrame-OSS (`v0.4.2`)

**Client-Side Media Sanitization, Container Metadata Stripping & Perceptual Hash (pHash/dHash) Obfuscation Toolkit**

## Overview
Independent journalists and human rights researchers face two technical vectors when publishing mobile video evidence:
1. **Deep Container & Hardware Fingerprinting:** Mobile OS muxers (iOS QuickTime `.mov` and Android `.mp4`) embed persistent device atoms, GPS coordinates, creation timestamps, and hardware encoder quantization signatures that survive surface-level EXIF tag removal.
2. **Perceptual Hash (`pHash` / `dHash` / `MD5`) Blocklisting:** Automated filters compute perceptual frame hashes to throttle or cross-reference re-uploaded whistleblower footage.

**CleanFrame-OSS** runs 100% offline on the user's device (`FFmpeg` CLI) to:
- Strip all container metadata, chapters, and hardware encoder signatures via `+bitexact` bitstream re-encoding.
- Apply calibrated, human-imperceptible spatio-temporal perturbations (Lanczos micro-crop/scale, color-matrix micro-shift, and audio sample-rate normalization) that shift 64-bit `pHash/dHash` Hamming distances beyond duplicate detection thresholds while preserving visual evidentiary integrity.
- Optionally generate a local **SHA-256 Chain-of-Custody Provenance Manifest** prior to sanitization.

## Usage

```bash
python3 -m cleanframe.cli raw_clip.mov sanitized_output.mp4 --manifest provenance.json
```

## License
MIT License.
