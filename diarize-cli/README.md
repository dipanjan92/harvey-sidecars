1. copy the pyannote cache to ./models as real files (and not links):

mkdir -p /Users/dipanjan/tauri/deps/pyannote-cli/models
rsync -aL ~/.cache/torch/pyannote/models--* /Users/dipanjan/tauri/deps/pyannote-cli/models/


2. test the diarize_cli.py

3. Run this from terminal:

python3 - <<'EOF'
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
#    findSystemFonts scans your system’s fonts
font_list = fm.findSystemFonts(fontpaths=None, fontext='ttf')
print(f"Scanned {len(font_list)} .ttf fonts")

#    Accessing fontManager will write the new cache files
_ = fm.fontManager

# 4) Show the newly written files
print("New cache contents:", os.listdir(cache_dir))
EOF



4. then run this:

cp -R "$(python3 -c 'import matplotlib as mpl; print(mpl.get_cachedir())')" \
      /Users/dipanjan/tauri/deps/pyannote-cli/resources


5. Run this to build the project:

rm -rf build/ dist/ diarize_cli.spec

pyinstaller --clean --onefile \
  --add-data "/Users/dipanjan/tauri/deps/pyannote-cli/models:models" \
  --add-data "/Users/dipanjan/tauri/deps/pyannote-cli/resources/.matplotlib:resources/.matplotlib" \
  --add-data "/Users/dipanjan/tauri/deps/pyannote-cli/.conda/lib/python3.11/site-packages/lightning_fabric/version.info:lightning_fabric" \
  --add-data "/Users/dipanjan/tauri/deps/pyannote-cli/.conda/lib/python3.11/site-packages/speechbrain:speechbrain" \
  --hidden-import=pyannote.audio.pipelines \
  --hidden-import=pyannote.audio.models \
  --hidden-import=pyannote.audio.models.segmentation \
  --hidden-import=pyannote.audio.models.embedding \
  diarize_cli.py


6. test the executable under ./dist:

./diarize_cli --audio ../audio.wav --output ../test-1.rttm --num_speakers 2

7. Move the files to Harvey sidecar.