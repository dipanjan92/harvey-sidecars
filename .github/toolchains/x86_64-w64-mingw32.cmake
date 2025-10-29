# This file is adapted from the following source:
# https://github.com/dvhh/ffmpeg-wos-arm64-build/blob/main/aarch64-w64-mingw32.cmake
#
# Use with CMAKE_TOOLCHAIN_FILE
# See: https://cmake.org/cmake/help/book/mastering-cmake/chapter/Cross%20Compiling%20With%20CMake.html
# See: https://bitbucket.org/multicoreware/x265_git/wiki/CrossCompile

# The name of the target operating system
set(CMAKE_SYSTEM_NAME Windows)

# Which compilers to use for C and C++
set(CMAKE_C_COMPILER   x86_64-w64-mingw32-gcc)
set(CMAKE_CXX_COMPILER x86_64-w64-mingw32-g++)
set(CMAKE_RC_COMPILER x86_64-w64-mingw32-windres)

# Adjust the default behavior of the FIND_XXX() commands:
# Search programs in the host environment
set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)

# Search headers and libraries in the target environment
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
