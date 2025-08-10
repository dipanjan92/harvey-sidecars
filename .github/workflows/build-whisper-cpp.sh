#!/bin/bash
set -ex

# Script to build whisper.cpp, accepting the toolchain directory as an argument

if [ -z "$1" ]; then
  echo "Error: Toolchain directory must be provided as the first argument."
  exit 1
fi

TOOLCHAIN_DIR=$1
CMAKE_OPTS=$2

export PKG_CONFIG_PATH="${TOOLCHAIN_DIR}/aarch64-none-linux-gnu/lib/pkgconfig"

rm -rf whisper.cpp/build
mkdir -p whisper.cpp/build
cd whisper.cpp/build

CMAKE_ARGS="-DCMAKE_BUILD_TYPE=Release -DBUILD_SHARED_LIBS=OFF -DWHISPER_SDL2=ON"

cmake .. ${CMAKE_ARGS} \
  -DCMAKE_C_COMPILER="${TOOLCHAIN_DIR}/bin/aarch64-none-linux-gnu-gcc" \
  -DCMAKE_CXX_COMPILER="${TOOLCHAIN_DIR}/bin/aarch64-none-linux-gnu-g++" \
  ${CMAKE_OPTS}

cmake --build . --config Release

