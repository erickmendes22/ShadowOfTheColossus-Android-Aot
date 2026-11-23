#!/usr/bin/env bash
# Rebuild ONLY the SotC native ARM64 host with the real NGS2 software mixer.
# Pin the same FFmpeg and NDK ABI as the validated 0.1.69 Bionic host.
set -Eeuo pipefail
trap 'echo "NGS2 host build failed at line $LINENO: $BASH_COMMAND" >&2' ERR
cd "$(dirname "$0")/../../.."
base_apk="${1:?Usage: build_ngs2_audio_host.sh BASE_APK OUT_ELF}"
output="${2:?Usage: build_ngs2_audio_host.sh BASE_APK OUT_ELF}"
ndk="${GOW3_NDK:-${ANDROID_NDK_HOME:?Set GOW3_NDK or ANDROID_NDK_HOME}}"
api=30
llvm="$ndk/toolchains/llvm/prebuilt/linux-x86_64"
cc="$llvm/bin/aarch64-linux-android${api}-clang"
workspace="$PWD/out/sotc-audio-host"
prefix="$workspace/prefix"
mkdir -p "$workspace/lib" "$workspace/objects" "$workspace/atrac9" "$prefix"
test -x "$cc"
python3 - "$base_apk" "$workspace/lib" <<'PY'
from pathlib import Path
import io,tarfile,zipfile,sys
apk=Path(sys.argv[1]); dest=Path(sys.argv[2])
with zipfile.ZipFile(apk) as archive:
    with tarfile.open(fileobj=io.BytesIO(archive.read('assets/runtime.payload')),mode='r:gz') as bundle:
        for name in ('libgow3cpu.so','libgow3gpu.so','libbbgpu.so','libc++_shared.so'):
            p='sotcport/arm64/lib/'+name
            item=bundle.extractfile(p)
            if item is None:raise RuntimeError('Missing pinned runtime dependency '+p)
            (dest/name).write_bytes(item.read())
PY
# LibAtrac9 sources are in an upstream git submodule, never redistribute game files.
if [[ ! -f third_party/LibAtrac9/C/src/libatrac9.h ]]; then
  git submodule update --init --depth=1 third_party/LibAtrac9
fi
test -f third_party/LibAtrac9/C/src/libatrac9.h || {
  echo 'LibAtrac9 submodule not available' >&2; exit 2;
}
# Reuse the pinned FFmpeg 7.1.5 build if the audio-host cache exists.
if [[ ! -f "$prefix/lib/libavcodec.a" || ! -f "$prefix/lib/libavformat.a" ]]; then
    mkdir -p "$workspace/ffmpeg"
    curl -fL --retry 6 --retry-all-errors --retry-delay 4 --connect-timeout 30 \
      'https://ffmpeg.org/releases/ffmpeg-7.1.5.tar.xz' -o "$workspace/ffmpeg-7.1.5.tar.xz"
    tar -xJf "$workspace/ffmpeg-7.1.5.tar.xz" -C "$workspace/ffmpeg" --strip-components=1
    mkdir -p "$workspace/ffbuild"
    pushd "$workspace/ffbuild" >/dev/null
    "$workspace/ffmpeg/configure" --prefix="$prefix" \
      --enable-cross-compile --target-os=android --arch=aarch64 \
      --cc="$cc" --cxx="$llvm/bin/aarch64-linux-android${api}-clang++" \
      --ar="$llvm/bin/llvm-ar" --ranlib="$llvm/bin/llvm-ranlib" \
      --strip="$llvm/bin/llvm-strip" --nm="$llvm/bin/llvm-nm" \
      --enable-static --disable-shared --enable-pic --extra-cflags=-fvisibility=hidden \
      --disable-programs --disable-doc --disable-debug --disable-avdevice \
      --disable-avfilter --disable-network --disable-autodetect \
      --disable-mediacodec --disable-jni
    make -j "${GOW3_JOBS:-2}"
    make install
    popd >/dev/null
fi
for source in third_party/LibAtrac9/C/src/*.c; do
    "$cc" -std=c99 -O2 -w -fPIC -c "$source" -o "$workspace/atrac9/$(basename "${source%.c}").o"
done
"$llvm/bin/llvm-ar" rcs "$workspace/libatrac9.a" "$workspace"/atrac9/*.o
objects=()
for source in src/probe.c src/runtime*.c src/vulkan_smoke.c \
    ports/sotc/android/lowmem.c ports/sotc/android/gpu_bridge.c; do
    obj="$workspace/objects/$(basename "${source%.c}").o"
    "$cc" -std=c11 -O2 -g -Wall -Wextra -Werror -pthread -I"$prefix/include" -I. -Isrc \
      -fPIE -c "$source" -o "$obj"
    objects+=("$obj")
done
mkdir -p "$(dirname "$output")"
"$cc" "${objects[@]}" "$workspace/libatrac9.a" \
  "$prefix/lib/libavformat.a" "$prefix/lib/libavcodec.a" \
  "$prefix/lib/libswscale.a" "$prefix/lib/libswresample.a" "$prefix/lib/libavutil.a" \
  -L"$workspace/lib" -lgow3gpu -lgow3cpu -lc++_shared \
  -lm -ldl -pthread \
  -Wl,--exclude-libs,libavcodec.a:libavformat.a:libavutil.a:libswscale.a:libswresample.a \
  -rdynamic -pie -Wl,-rpath,'$ORIGIN/../lib' -o "$output"
"$llvm/bin/llvm-nm" -D --defined-only "$output" | grep -F ' runtime_ngs2_resolve'
"$llvm/bin/llvm-nm" -D --defined-only "$output" | grep -F ' runtime_memory_clamp_gap_hits'
"$llvm/bin/llvm-readelf" -h "$output" | grep -F 'AArch64'
echo "PASS: upstream NGS2 mixer linked into native AOT host; original GPU untouched."
