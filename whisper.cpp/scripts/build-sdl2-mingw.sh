#!/bin/bash
set -ex

# This script is designed to be run inside the mstorsjo/llvm-mingw container
# It downloads and builds SDL2 for the specified target architecture.

TARGET_HOST=$1
INSTALL_PREFIX=$2

if [ -z "$TARGET_HOST" ] || [ -z "$INSTALL_PREFIX" ]; then
  echo "Usage: $0 <target-host> <install-prefix>"
  echo "Example: $0 x86_64-w64-mingw32 /path/to/install"
  exit 1
fi

SDL2_VERSION="2.30.5"
echo "Building SDL2 from source for ${TARGET_HOST}..."

curl -sL "https://github.com/libsdl-org/SDL/releases/download/release-${SDL2_VERSION}/SDL2-${SDL2_VERSION}.tar.gz" | tar xz
cd "SDL2-${SDL2_VERSION}"

# Configure and build
./configure \
  --host=${TARGET_HOST} \
  --prefix=${INSTALL_PREFIX} \
  --enable-static \
  --disable-shared \
  --disable-video-x11

make -j$(nproc)
make install
