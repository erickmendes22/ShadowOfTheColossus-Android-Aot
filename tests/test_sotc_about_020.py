#!/usr/bin/env python3
"""Guard native-AOT credits in the SotC Android 0.2.0 About screen."""
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
def read(path):return (ROOT / path).read_text(encoding="utf-8")

class SotcAboutCredits020(unittest.TestCase):
    def test_no_fexdroid_as_active_ui_component(self):
        ui=read("android-launcher/app/src/main/java/com/gow3/android/ui/SotcScreen.kt")
        about=ui.split('else -> {',1)[-1]
        self.assertNotIn('SotcCreditLink(ctx,"fexdroid"',about)
        self.assertNotIn('"https://github.com/cobrabm12/fexdroid"',about)
        self.assertIn('"shadPS4"',about)
        self.assertIn('"Pink-shadPS4"',about)
        self.assertNotIn('"shadPS4 / Pink-shadPS4"',about)
        self.assertIn('CREDITS.md',about)
        self.assertIn('compilação AOT ARM64 nativa',about)
    def test_historical_credits_and_runtime_policy_preserved(self):
        credits=read("CREDITS.md")
        self.assertIn("cobrabm12/fexdroid",credits)
        self.assertIn("sem FEX",credits)
        launcher=read("ports/sotc/android/run-sotc-bionic.sh")
        self.assertIn("NO-FEX NO-TSO",launcher)
        self.assertIn("gamehub-dd",launcher)
    def test_same_version_and_package(self):
        gradle=read("android-launcher/app/build.gradle.kts")
        self.assertIn('applicationId = "com.sotc.android.daedalus"',gradle)
        self.assertIn('versionName = "0.2.0"',gradle)
        self.assertIn('versionCode = 20000',gradle)
        self.assertNotIn('versionName = "0.2.1"',gradle)

if __name__ == "__main__":unittest.main()
