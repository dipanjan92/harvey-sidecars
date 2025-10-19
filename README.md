# Harvey Sidecars

This project builds the necessary executables as sidecars to distribute along with the [Harvey app](https://github.com/Ethnomethodology/harvey). 

Harvey is a desktop transcription application that uses [whisper.cpp](https://github.com/ggerganov/whisper.cpp) for transcription and [FFmpeg](https://github.com/FFmpeg/FFmpeg) for manipulating media formats.

**Note:** The `ffmpeg/aarch64-w64-mingw32.cmake` file is adapted from the `dvhh/ffmpeg-wos-arm64-build` repository (https://github.com/dvhh/ffmpeg-wos-arm64-build). It is used to configure the `x265` build process for cross-compilation to Windows ARM64 within the `llvm-mingw` environment.
