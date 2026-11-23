#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later
"""Repackage strict ARM64 AOT runtime with optional newly linked NGS2 sound host.

Reuses the verified 0.1.69 strict ARM64 native host and renderer. Repackages
only the updated launcher/scripts plus the hash-verified GameHub DD Turnip.
When --audio-probe is supplied, replace ONLY the freshly linked native host: 
all rendering/AOT/driver binaries remain from the already ABI-verified baseline.
"""
from __future__ import annotations
import argparse
import hashlib
import io
import json
from pathlib import Path
from vendor_turnip import embed_verified_turnip, LIB_SHA256
import subprocess
import tarfile
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[3]
EXPECTED_BASE = "0.1.69-aot-ux"
RELEASE = "0.2.0"
ROOTPATHS = {
    "sotcport/run-sotc-bionic.sh": ROOT / "ports/sotc/android/run-sotc-bionic.sh",
    "sotcport/scripts/sotc_prepare_game.py": ROOT / "ports/sotc/android/prepare_game.py",
    "sotcport/scripts/bachata_perf.py": ROOT / "ports/sotc/android/bachata_perf.py",
}
# fxdisplay and fxio are already provided by the launcher source-set's
# tools/android/bridges. Duplicating them in apk-jni makes Gradle's
# :app:mergeReleaseJniLibFolders fail even when the bytes are identical.
JNI_LIBS = {"libbbrecomp.so", "libgow3present.so"}


def dynamic_symbols(binary: Path, defined: bool) -> set[str]:
    cmd = ["nm", "-D", "--defined-only" if defined else "--undefined-only", str(binary)]
    output = subprocess.check_output(cmd, text=True)
    result: set[str] = set()
    for line in output.splitlines():
        columns = line.split()
        if len(columns) < 2:
            continue
        if defined and columns[-2].upper() not in ("T", "D", "R", "B", "W", "V"):
            continue
        if not defined and columns[-2] != "U":
            continue
        result.add(columns[-1].split("@")[0])
    return result


def repack(base_apk: Path, asset_dir: Path, jni_root: Path, driver_zip: Path,
           audio_probe: Path | None = None) -> None:
    new_host = None
    if audio_probe is not None:
        new_host = audio_probe.read_bytes()
        if not new_host.startswith(b"\x7fELF") or len(new_host) < 1000000:
            raise ValueError("New NGS2 host must be a real ARM64 ELF executable")
        dynamic = dynamic_symbols(audio_probe, True)
        if not {"runtime_ngs2_resolve", "runtime_audio_resolve", "runtime_memory_clamp_gap_hits"}.issubset(dynamic):
            raise ValueError("Compiled host lacks NGS2 mixer or mandatory exported ABIs")
        if b"NGS2: built-in mixer" not in new_host:
            raise ValueError("NGS2 host does not contain the upstream software mixer")
        print("PASS native NGS2 host: "+hashlib.sha256(new_host).hexdigest())
    # The repository release is downloaded by CI. Require the exact known ZIP
    # and ELF hashes; do not add a fallback or an unidentified Turnip version.
    with tempfile.TemporaryDirectory() as driver_tmp:
        stage = Path(driver_tmp)
        if not embed_verified_turnip(stage, driver_zip):
            raise ValueError("Required GameHub DD Turnip ZIP not available")
        bundled = {p.relative_to(stage).as_posix(): p.read_bytes()
                   for p in stage.rglob("*") if p.is_file()}
    if not any(path.endswith("/gamehub-dd/libvulkan_freedreno.so") for path in bundled):
        raise ValueError("Verified GameHub DD Turnip ELF missing")
    asset_dir.mkdir(parents=True, exist_ok=True)
    jni_root.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(base_apk) as apk:
        if apk.testzip() is not None:
            raise ValueError("0.1.68 base APK ZIP CRC check failed")
        old = apk.read("assets/runtime.payload")
        if hashlib.sha256(old).hexdigest() != apk.read("assets/runtime.sha256").decode().strip():
            raise ValueError("Base runtime checksum mismatch")
        with tarfile.open(fileobj=io.BytesIO(old), mode="r:gz") as original:
            original_members = original.getmembers()
            if set(ROOTPATHS) - {m.name for m in original_members}:
                raise ValueError("Base runtime does not contain required SotC shell script")
            manifest_file = original.extractfile("runtime-manifest.json")
            if manifest_file is None:
                raise ValueError("Missing runtime manifest")
            manifest = json.loads(manifest_file.read())
            if manifest.get("version") != EXPECTED_BASE or manifest.get("aot_mode") != "strict":
                raise ValueError("Not the approved strict native AOT 0.1.68 runtime")

            # The only valid SotC GPU driver is bundled GameHub DD 26.3.
            # Do not retain any incompatible generic Turnip packages.
            manifest.pop("adreno7xx_driver", None)
            manifest["driver"] = {
                "id": "gamehub-dd-26.3",
                "name": "Turnip GameHub DD 26.3 GMEM/PWR_MAX",
                "archive_sha256": "8255659cc205110e0fa89f2d364292b86fe563a2cedafbc41915bead5a611ecb",
                "library_sha256": "4f242a453496ab27fc29be950d632edbae494dcc0c9b7d56c37c7ebdffe42df9",
                "bundled": True,
                "runtime_validation": "mandatory",
            }
            manifest["gamehub_dd_turnip_bundled"] = True
            manifest["version"] = RELEASE
            manifest["runtime_name"] = "sotc-daedalus-aot-0.2.0"
            if new_host is not None:
                manifest["audio_engine"] = {
                    "id": "ngs2-software-mixer",
                    "upstream": "AjncSystem/ShadowOfTheColossus-PC v0.76.2",
                    "host_sha256": hashlib.sha256(new_host).hexdigest(),
                    "aot_guest_calls": True,
                    "fifo_pcm": "s16-stereo-48000"
                }
            manifest_bytes = (json.dumps(manifest, indent=2, ensure_ascii=False)+"\n").encode()
            stream = io.BytesIO()
            with tarfile.open(fileobj=stream, mode="w:gz", format=tarfile.GNU_FORMAT) as modified:
                for entry in original_members:
                    if entry.name.startswith(("sotcport/arm64/drivers/gen8",
                                              "sotcport/arm64/drivers/adreno7xx",
                                              "sotcport/arm64/drivers/gamehub-dd")):
                        continue
                    if entry.name == "runtime-manifest.json":
                        payload = manifest_bytes
                    elif entry.name in ROOTPATHS:
                        payload = ROOTPATHS[entry.name].read_bytes()
                    elif entry.name == "sotcport/arm64/bin/sotc-probe" and new_host is not None:
                        payload = new_host
                    elif entry.isfile():
                        infile = original.extractfile(entry)
                        if infile is None:
                            raise ValueError("Missing archived entry: " + entry.name)
                        payload = infile.read()
                    else:
                        modified.addfile(entry)
                        continue
                    entry.size = len(payload)
                    modified.addfile(entry, io.BytesIO(payload))
                for name, payload in bundled.items():
                    info = tarfile.TarInfo(name)
                    info.size = len(payload)
                    info.mode = 0o644
                    modified.addfile(info, io.BytesIO(payload))
            new_payload = stream.getvalue()
        (asset_dir / "runtime.payload").write_bytes(new_payload)
        (asset_dir / "runtime.sha256").write_text(hashlib.sha256(new_payload).hexdigest()+"\n")
        (asset_dir / "THIRD_PARTY_LICENSES.txt").write_bytes(apk.read("assets/THIRD_PARTY_LICENSES.txt"))
        available = set()
        for member in apk.namelist():
            if member.startswith("lib/arm64-v8a/"):
                name = member.rsplit("/", 1)[-1]
                if name in JNI_LIBS:
                    target = jni_root / "arm64-v8a" / name
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(apk.read(member))
                    available.add(name)
        if available != JNI_LIBS:
            raise ValueError("Missing JNI libraries: " + repr(sorted(JNI_LIBS - available)))

    # Compare the EXACT two ELFs inside the repackaged payload. This prevents
    # 0.1.66's C++ ABI and 0.1.67's runtime_memory_clamp_gap_hits dlopen failures.
    with tempfile.TemporaryDirectory() as temp:
        with tarfile.open(fileobj=io.BytesIO(new_payload), mode="r:gz") as tar:
            host = Path(temp) / "sotc-probe"
            gpu = Path(temp) / "libbbgpu.so"
            host.write_bytes(tar.extractfile("sotcport/arm64/bin/sotc-probe").read())
            gpu.write_bytes(tar.extractfile("sotcport/arm64/lib/libbbgpu.so").read())
        host_exports = dynamic_symbols(host, True)
        gpu_imports = dynamic_symbols(gpu, False)
        runtime_imports = {symbol for symbol in gpu_imports if symbol.startswith("runtime_")}
        missing = runtime_imports - host_exports
        if missing:
            raise ValueError("Repackaged renderer cannot dlopen; missing host ABI: " + str(sorted(missing)))
        bad_cpp = [sym for sym in gpu_imports if sym.startswith(("_ZN6Vulkan", "_ZN6AmdGpu", "_ZN9VideoCore"))]
        if bad_cpp:
            raise ValueError("Unresolved internal renderer ABI: " + str(bad_cpp))
        if "runtime_memory_clamp_gap_hits" not in host_exports:
            raise ValueError("Regression: host still missing gap cache counter")
        if new_host is not None and "runtime_ngs2_resolve" not in host_exports:
            raise ValueError("New Android host lost the NGS2 mixer export")
        print(f"PASS ABI {len(runtime_imports)} runtime imports from EXACT repackaged host; no internal C++ missing")

    with tarfile.open(fileobj=io.BytesIO(new_payload), mode="r:gz") as verify:
        name = "sotcport/arm64/drivers/gamehub-dd/libvulkan_freedreno.so"
        actual = hashlib.sha256(verify.extractfile(name).read()).hexdigest()
        if actual != LIB_SHA256:
            raise ValueError("Wrong GameHub driver ELF SHA256 in final runtime payload")
        for old in ("gen8", "adreno7xx"):
            if any(f"/drivers/{old}/" in n for n in verify.getnames()):
                raise ValueError(f"Old {old} driver survived repack")
    print("PASS 0.2.0: verified NGS2 sound host if supplied; AOT/render/driver invariant")
    print(f"Runtime payload: {len(new_payload)} bytes, SHA256 {hashlib.sha256(new_payload).hexdigest()}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-apk", type=Path, required=True)
    parser.add_argument("--assets", type=Path, default=ROOT / "out/android-release/assets")
    parser.add_argument("--jni", type=Path, default=ROOT / "out/bionic/apk-jni")
    parser.add_argument("--gamehub-zip", type=Path, required=True)
    parser.add_argument("--audio-probe", type=Path, default=None,
                        help="Newly built ARM64 host with real upstream NGS2 software mixer")
    args = parser.parse_args()
    repack(args.base_apk, args.assets, args.jni, args.gamehub_zip, args.audio_probe)
