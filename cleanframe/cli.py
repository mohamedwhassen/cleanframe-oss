"""Command-line interface for CleanFrame-OSS."""
import argparse
import json
import subprocess
from cleanframe.sanitizer import build_ffmpeg_sanitize_cmd, generate_provenance_manifest

def main():
    parser = argparse.ArgumentParser(
        description="CleanFrame-OSS: Client-Side Video Sanitization & Anti-pHash Toolkit for At-Risk Reporters"
    )
    parser.add_argument("input", help="Path to raw input video (.mp4 / .mov)")
    parser.add_argument("output", help="Path to sanitized output video (.mp4)")
    parser.add_argument("--manifest", help="Optional path to save local SHA-256 provenance manifest JSON")
    parser.add_argument("--dry-run", action="store_true", help="Print FFmpeg pipeline without executing")
    args = parser.parse_args()

    if args.manifest:
        manifest = generate_provenance_manifest(args.input)
        with open(args.manifest, "w", encoding="utf-8") as mf:
            json.dump(manifest, mf, indent=2)

    cmd = build_ffmpeg_sanitize_cmd(args.input, args.output)
    if args.dry_run:
        print(" ".join(cmd))
        return
    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    main()
