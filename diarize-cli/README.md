# diarize-cli

This tool is a command-line interface for performing speaker diarization using pyannote.audio.
It's intended to be built into an executable using PyInstaller for distribution as a sidecar with applications like Harvey.

## Prerequisites & Setup

These instructions are a guideline for developers. Paths may need to be adjusted for your environment.

1.  **Populate Pyannote Models Cache:**
    The tool expects Pyannote's pre-trained models to be available. You need to copy your Pyannote model cache (typically from `~/.cache/torch/pyannote/models--*`) to a local `./models` directory relative to where you are building `diarize-cli`. Ensure that actual files are copied, not symbolic links.

    ```bash
    # Example: Replace <path_to_your_project>/diarize-cli/ with the actual path
    mkdir -p ./models
    rsync -aL ~/.cache/torch/pyannote/models--* ./models/
    ```

2.  **Prepare Matplotlib Font Cache:**
    Matplotlib requires a font cache. The following steps help ensure it's correctly generated and then copied to a local `./resources` directory for packaging.

    *   Run this Python script in your terminal to refresh Matplotlib's font cache:
        ```python
        import os
        import matplotlib as mpl
        from matplotlib import font_manager as fm

        # 1) Locate cache directory
        cache_dir = mpl.get_cachedir()
        print("Matplotlib cache directory:", cache_dir)

        # 2) Remove old cache files if they exist
        for fname in ("fontList.json", "fontList.py3k.cache"):
            p = os.path.join(cache_dir, fname)
            if os.path.exists(p):
                os.remove(p)
                print("Removed old cache file:", p)

        # 3) Trigger a full font scan & cache write
        font_list = fm.findSystemFonts(fontpaths=None, fontext='ttf')
        print(f"Scanned {len(font_list)} .ttf fonts")
        _ = fm.fontManager # Accessing fontManager writes the new cache

        # 4) Show the newly written files
        print("New cache contents:", os.listdir(cache_dir))
        ```

    *   Then, copy the generated Matplotlib cache directory to `./resources`:
        ```bash
        # Example: Replace <path_to_your_project>/diarize-cli/ with the actual path
        # The Python command below gets the cache directory path for Matplotlib
        cp -R "$(python3 -c 'import matplotlib as mpl; print(mpl.get_cachedir())')" ./resources/matplotlib_cache
        # Note: The PyInstaller command below expects it at ./resources/.matplotlib
        # You might need to rename or adjust paths accordingly, e.g.:
        # mv ./resources/matplotlib_cache ./resources/.matplotlib
        ```
        *Self-correction during thought process: The original path was `resources/.matplotlib`. The copy command should reflect that, or the PyInstaller command should be updated. I will assume the PyInstaller command is the source of truth and the user wants it at `resources/.matplotlib`.*
        Adjust the copy command if your PyInstaller expects a different target path like `resources/.matplotlib`. A safer approach for the copy might be:
        ```bash
        MPL_CACHE_DIR=$(python3 -c 'import matplotlib as mpl; print(mpl.get_cachedir())')
        mkdir -p ./resources/.matplotlib
        cp -R "${MPL_CACHE_DIR}/"* ./resources/.matplotlib/
        ```


## Build Instructions

The following command uses PyInstaller to build the `diarize_cli.py` script into a single executable. Adjust paths for `--add-data` if your model cache, resources, or Python environment differ.

*   The paths like `/Users/dipanjan/tauri/deps/pyannote-cli/.conda/lib/python3.11/site-packages/` are specific to a Conda environment. You'll need to find the equivalent paths for `lightning_fabric/version.info` and the `speechbrain` package in your own Python environment if you are not using a similar Conda setup.

```bash
# Clean previous builds
rm -rf build/ dist/ diarize_cli.spec

# Run PyInstaller
# Replace placeholder paths like <path_to_your_project_root>/diarize-cli/
# and <path_to_your_conda_env_site_packages>/ if needed.
# It's generally better to run this from the diarize-cli directory.

pyinstaller --clean --onefile \
  --add-data "./models:models" \
  --add-data "./resources/.matplotlib:resources/.matplotlib" \
  --add-data "<path_to_conda_env_site_packages>/lightning_fabric/version.info:lightning_fabric" \
  --add-data "<path_to_conda_env_site_packages>/speechbrain:speechbrain" \
  --hidden-import=pyannote.audio.pipelines \
  --hidden-import=pyannote.audio.models \
  --hidden-import=pyannote.audio.models.segmentation \
  --hidden-import=pyannote.audio.models.embedding \
  diarize_cli.py
```
*Note: `<path_to_conda_env_site_packages>` should be replaced with the actual path to the `site-packages` directory of the Python environment where `lightning_fabric` and `speechbrain` are installed.*


## Testing

After a successful build, the executable will be located in the `dist/` directory.

```bash
# Example: Run from the diarize-cli directory
./dist/diarize_cli --audio ../audio.wav --output ../test-1.rttm --num_speakers 2
```
*(Ensure `../audio.wav` points to a valid audio file for testing.)*

## Deployment

The built executable (e.g., `dist/diarize_cli`) is then ready to be moved to the target application's sidecar directory (e.g., for Harvey).

## Credits & License

This tool relies heavily on the work of the `pyannote.audio` team. Please cite their work if you use this tool or `pyannote.audio` in your research:

```bibtex
@inproceedings{Plaquet23,
  author={Alexis Plaquet and Hervé Bredin},
  title={{Powerset multi-class cross entropy loss for neural speaker diarization}},
  year=2023,
  booktitle={Proc. INTERSPEECH 2023},
}

@inproceedings{Bredin23,
  author={Hervé Bredin},
  title={{pyannote.audio 2.1 speaker diarization pipeline: principle, benchmark, and recipe}},
  year=2023,
  booktitle={Proc. INTERSPEECH 2023},
}
```

The `diarize-cli` specific code is licensed under the MIT license, as detailed in the `LICENSE` file in this directory. The underlying `pyannote.audio` library also uses the MIT License (Copyright (c) 2020 CNRS).
