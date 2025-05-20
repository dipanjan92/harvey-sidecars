Usage:

cd /Users/dipanjan/tauri/deps/harvey-sidecars
chmod +x init-folders.sh
./init-folders.sh


# From your repo root
find . -type d \( -path "./ffmpeg" -o -path "./pandoc" -o -path "./markitdown" -o -path "./whisper-cpp" -o -path "./diarize-cli" \) \
  -exec touch {}/.gitkeep \;

find . -type d \
  -path "./ffmpeg/*" \
  -o -path "./pandoc/*" \
  -o -path "./markitdown/*" \
  -o -path "./whisper-cpp/*" \
  -o -path "./diarize-cli/*" \
  | while read dir; do
      touch "${dir}/.gitkeep"
    done


2. Setup workflows for ffmpeg

mkdir -p .github/workflows
cat > .github/workflows/update-ffmpeg.yml << 'EOF'
# (we’ll fill this in next)
EOF




This will yield exactly:

harvey-sidecars/
├── ffmpeg
│   ├── macos-arm64
│   ├── macos-x86_64
│   └── windows-x86_64
├── pandoc
│   ├── macos-arm64
│   ├── macos-x86_64
│   └── windows-x86_64
├── markitdown
│   ├── macos-arm64
│   ├── macos-x86_64
│   └── windows-x86_64
├── whisper-cpp
│   ├── macos-arm64
│   ├── macos-x86_64
│   └── windows-x86_64
└── diarize-cli
    ├── macos-arm64
    ├── macos-x86_64
    └── windows-x86_64