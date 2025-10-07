#!/usr/bin/env python3
"""
CLI tool for offline PyAnnote Speaker Diarization (v3.1), packaged with PyInstaller.
Assumes model snapshots are bundled in the `models/` directory and
Matplotlib font cache is bundled in `resources/.matplotlib` beside the executable.
"""
import os
import sys

# === Configure Matplotlib to use bundled font cache ===
# Determine base path: sys._MEIPASS for PyInstaller onefile, script dir otherwise
def _get_resource_root():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(__file__)

# Point MPLCONFIGDIR to the embedded .matplotlib folder
base_path = _get_resource_root()
mpl_cache = os.path.join(base_path, 'resources', '.matplotlib')
os.environ['MPLCONFIGDIR'] = mpl_cache

# === Dependencies ===
import argparse
import torch
from pyannote.audio import Pipeline


def get_model_cache():
    """
    Determine the path to the bundled `models` folder.
    When running as a PyInstaller onefile executable, resources are unpacked to sys._MEIPASS.
    Otherwise, use the script's `models/` directory alongside it.
    """
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, 'models')
    return os.path.join(os.path.dirname(__file__), 'models')


def main():
    parser = argparse.ArgumentParser(
        description="Offline Speaker Diarization CLI using pyannote.audio v3.1"
    )
    parser.add_argument(
        "--audio", required=True,
        help="Path to input audio file (e.g., WAV)"
    )
    parser.add_argument(
        "--output", default="output.rttm",
        help="Path to output RTTM file (default: output.rttm)"
    )
    parser.add_argument(
        "--num_speakers", type=int,
        help="Specify the exact number of speakers"
    )
    parser.add_argument(
        "--min_speakers", type=int,
        help="Minimum number of speakers"
    )
    parser.add_argument(
        "--max_speakers", type=int,
        help="Maximum number of speakers"
    )
    args = parser.parse_args()

    # Force HF Hub fully offline
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["HF_HUB_DISABLE_IMPLICIT_TOKEN"] = "1"

    # Locate bundled models cache
    model_cache = get_model_cache()
    if not os.path.isdir(model_cache):
        sys.exit(f"Error: bundled models directory not found at {model_cache}")

    # Load the diarization pipeline from local cache
    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1",
        use_auth_token=False,
        cache_dir=model_cache
    )
    device = torch.device("cpu")
    pipeline.to(device)

    # Build optional diarization parameters
    kwargs = {}
    if args.num_speakers is not None:
        kwargs["num_speakers"] = args.num_speakers
    if args.min_speakers is not None:
        kwargs["min_speakers"] = args.min_speakers
    if args.max_speakers is not None:
        kwargs["max_speakers"] = args.max_speakers

    # Run diarization and write output to RTTM
    diarization = pipeline(args.audio, **kwargs)
    with open(args.output, "w") as f:
        diarization.write_rttm(f)

    print(f"Finished diarization. Result saved to {args.output}")


if __name__ == "__main__":
    main()
