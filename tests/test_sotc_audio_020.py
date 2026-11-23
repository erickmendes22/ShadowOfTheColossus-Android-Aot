#!/usr/bin/env python3
"""Fail-closed checks for the SotC Android built-in sound mixer."""
import unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def get(p):return (R/p).read_text()
class NativeAudio020(unittest.TestCase):
    def test_real_ngs2_registered_over_silent_fallback(self):
        main=get("src/runtime.c")
        self.assertIn("runtime_ngs2_resolve(legacy)",main)
        self.assertLess(main.index("runtime_ngs2_resolve(legacy)"),main.index("runtime_sotc_resolve(name)"))
        old=get("src/runtime_sotc.c")
        self.assertIn("#ifndef __ANDROID__",old)
        self.assertIn('#endif /* real mixer must win on Android */',old)
        ngs=get("src/runtime_ngs2.c")
        self.assertIn('NGS2: built-in mixer',ngs)
        self.assertIn('sceNgs2SystemRender',ngs)
        self.assertIn('sceNgs2VoiceControl',ngs)
        self.assertIn('sceNgs2VoiceGetStateFlags',ngs)
        self.assertIn('WAVE_ATRAC9',ngs)
        self.assertIn('WAVE_VAG',ngs)
    def test_guest_callbacks_are_arm64_aot_safe(self):
        s=get("src/runtime_ngs2.c")
        self.assertEqual(s.count("guest_cpu_call("),4)
        self.assertIn('#if defined(__aarch64__)',s)
        self.assertIn('old_fpcr',s)
        self.assertIn('#if defined(__SSE__)',s)
        self.assertIn('#include "guest_cpu.h"',s)
    def test_verified_native_host_replaces_only_host(self):
        p=get("ports/sotc/android/repack_sotc_021.py")
        self.assertIn('--audio-probe',p)
        self.assertIn('runtime_ngs2_resolve',p)
        self.assertIn('elif entry.name == "sotcport/arm64/bin/sotc-probe" and new_host is not None:',p)
        self.assertIn('runtime_imports - host_exports',p)
        self.assertIn('RELEASE = "0.2.0"',p)
        build=get('ports/sotc/android/build_ngs2_audio_host.sh')
        self.assertIn('src/runtime*.c',build)
        self.assertIn('libavcodec.a',build)
        self.assertIn('libgow3gpu.so',build)
        self.assertNotIn('build_cpu.sh',build)
        self.assertNotIn('build_gpu.sh',build)
    def test_preserve_apk_package_and_audio_bridge(self):
        s=get("android-launcher/app/build.gradle.kts")
        self.assertIn('versionCode = 20000',s)
        self.assertIn('versionName = "0.2.0"',s)
        self.assertIn('applicationId = "com.sotc.android.daedalus"',s)
        self.assertIn('GOW3_AUDIO_FIFO',get('ports/sotc/android/run-sotc-bionic.sh'))
        self.assertIn('AudioTrack',get('android-launcher/app/src/main/java/ro/cobrabm/fexdroid/AudioBridge.java'))
if __name__=="__main__":unittest.main()
