#!/usr/bin/env python3
"""Shadow of the Colossus 0.2.0 UI/source drift and AOT validity gates."""
from pathlib import Path
import re, unittest
ROOT=Path(__file__).resolve().parents[1]
def src(name): return (ROOT/name).read_text()
class Sotc021(unittest.TestCase):
    def test_artwork_icon_and_name(self):
        art=(ROOT/"android-launcher/app/src/main/res/drawable-nodpi/sotc_art.webp").read_bytes()
        self.assertEqual(art[:4],b"RIFF")
        self.assertEqual(art[8:12],b"WEBP")
        import hashlib
        self.assertEqual(hashlib.sha256(art).hexdigest(),"d4a491aa0ac7c1c0d6c202006ee3d58d9e236df74e73b1558e3513e2ad1afe41")
        manifest=src("android-launcher/app/src/main/AndroidManifest.xml")
        self.assertIn('android:roundIcon="${appIcon}"',manifest)
        gradle=src("android-launcher/app/build.gradle.kts")
        self.assertIn('manifestPlaceholders["appIcon"] = "@mipmap/sotc_launcher"',gradle)
        self.assertIn('manifestPlaceholders["appLabel"] = "Shadow of the Colossus Android"',gradle)
        self.assertIn("versionCode = 20000",gradle)
        self.assertIn('versionName = "0.2.0"',gradle)
        adaptive=src("android-launcher/app/src/main/res/mipmap-anydpi-v26/sotc_launcher.xml")
        self.assertIn('@drawable/sotc_art',adaptive)
        home=src("android-launcher/app/src/main/java/com/gow3/android/ui/SotcScreen.kt")
        self.assertIn('R.drawable.sotc_art',home)
        self.assertIn('ContentScale.Fit',home)
        self.assertNotIn('SotcGameArtwork(gameDir)',"")
    def test_in_game_video_and_patch_menu(self):
        game=src("android-launcher/app/src/main/java/ro/cobrabm/fexdroid/GameActivity.java")
        main=src("android-launcher/app/src/main/java/com/gow3/android/MainActivity.kt")
        present=src("android-launcher/app/src/main/java/ro/cobrabm/fexdroid/Gow3Present.java")
        driver=src("tools/android/bionic/present/gow3present.c")
        store=src("android-launcher/app/src/main/java/ro/cobrabm/fexdroid/SotcSettingsStore.java")
        for token in ("chooseSotcResolution","chooseSotcPatches","chooseSotcFullscreen",
                      "chooseSotcHud","confirmSotcRestart",
                      "restartSotcWithAot","sotc_apply_restart",
                      "Gow3Present.setFullscreen(fill)","fitSurface(screen.getWidth(),screen.getHeight())"):
            self.assertIn(token,game)
        self.assertIn('onNewIntent(intent: Intent)',main)
        self.assertIn('handleSotcGameRestart(intent)',main)
        self.assertIn('sotcAotBuilder.ensureReadyThen',main)
        self.assertIn('public static synchronized void setFullscreen(boolean fullscreen)',present)
        self.assertIn('gow3_display_size(w, h, width, height, S.fullscreen',driver)
        self.assertIn('StandardCopyOption.ATOMIC_MOVE',store)
        self.assertIn('sotc_bachata_bloom',game)
        self.assertIn('sotc_af16',game)
        self.assertIn('sotc_hud_mode',game)
        self.assertNotIn("Change game patches in the launcher's Patches tab.",game)

    def test_banner_and_clickable_credits(self):
        screen=src("android-launcher/app/src/main/java/com/gow3/android/ui/SotcScreen.kt")
        self.assertIn("val bannerHeight=if(landscape) 230.dp else 208.dp",screen)
        self.assertIn("contentScale=ContentScale.Crop",screen)
        self.assertIn("contentScale=ContentScale.Fit",screen)
        self.assertIn("private fun SotcCreditLink",screen)
        self.assertGreaterEqual(screen.count("SotcCreditLink(ctx"),7)
        self.assertIn("CRÉDITOS E COMPONENTES",screen)
        self.assertIn("LICENÇAS E ATRIBUIÇÕES",screen)
        readme=src("README.md")
        for project in ("AjncSystem/ShadowOfTheColossus-PC",
                        "Supermedo/bloodborne_pc","shadps4-emu/shadPS4",
                        "luizgustavs/Pink-shadPS4","ducvd89/Bloodborne-Android",
                        "cobrabm12/fexdroid","erickmendes22/WinlatorComponents"):
            self.assertIn("https://github.com/"+project,readme)

    def test_render_sizes_match_AOT_and_game(self):
        ui=src("android-launcher/app/src/main/java/com/gow3/android/ui/SotcScreen.kt")
        aot=src("android-launcher/app/src/main/java/com/gow3/android/data/SotcAotBuildManager.kt")
        game=src("android-launcher/app/src/main/java/ro/cobrabm/fexdroid/GameActivity.java")
        for choice,target in (("540p","960x540"),("360p","640x360")):
            self.assertIn('"'+choice+'" to ',ui)
            self.assertIn('"'+choice+'" -> "'+target+'"',aot)
            self.assertIn('case "'+choice+'": env.put("SOTC_RENDER","'+target+'")',game)
        self.assertIn('"sotc_resolution"',ui)
        self.assertIn('android_fullscreen',ui)
        self.assertIn('sotc_hud_mode',ui)
        self.assertIn('Gow3Present.start(holder,BASE+"/present.sock","1".equals(setting("android_fullscreen")))',game)
    def test_live_hud_modes_with_real_metrics_only(self):
        s=src("android-launcher/app/src/main/java/ro/cobrabm/fexdroid/GameActivity.java")
        for mode in ['"off".equals(mode)','"fps".equals(mode)','HudPresentation.text("fps"','HudPresentation.text("full"']:
            self.assertIn(mode,s)
        sampler=src("android-launcher/app/src/main/java/ro/cobrabm/fexdroid/SotcLoadSampler.java")
        self.assertIn("/proc/stat",sampler)
        self.assertIn("/sys/class/kgsl/kgsl-3d0/gpubusy",sampler)
        self.assertIn("Double.NaN",sampler)
        self.assertIn("busyTime<=totalTime",sampler)
        self.assertIn("N/A",src("android-launcher/app/src/main/java/ro/cobrabm/fexdroid/HudPresentation.java"))
    def test_aot_keeps_old_verified_code_when_apk_updates(self):
        install=src("android-launcher/app/src/main/java/ro/cobrabm/fexdroid/RuntimeInstaller.java")
        self.assertIn('preserveUserData(files, stage)',install)
        self.assertIn('AOT code cache not preserved on runtime update',install)
        self.assertIn('sotcport/user/aot/libSotcAot.so',install)
        script=src("ports/sotc/android/run-sotc-bionic.sh")
        self.assertIn('if [ "$sotc_mode" = verify ]; then',script)
        self.assertIn('SOTC_AOT_VERIFIED: current profile',script)
        self.assertIn('SOTC_AOT_VERIFIED: reused compiled patch profile',script)
        manager=src("android-launcher/app/src/main/java/com/gow3/android/data/SotcAotBuildManager.kt")
        self.assertIn('if (execute("verify") == 0)',manager)
        self.assertIn('if (!ready)',manager)
        verifier=src("ports/sotc/android/aot/select_local_aot.py")
        self.assertIn('patch_sha256',verifier)
        self.assertIn('compiler_version',verifier)
        self.assertIn('original_boot_sha256',verifier)
    def test_translation_and_two_cusa_ids(self):
        ui=src("android-launcher/app/src/main/java/com/gow3/android/ui/SotcScreen.kt")
        about=ui.split('else -> {',1)[-1]
        self.assertNotIn('SotcAction("Português")',about)
        self.assertIn('"DADOS SALVOS"',about)
        nav=src("android-launcher/app/src/main/java/com/gow3/android/ui/LauncherScreen.kt")
        self.assertIn('"INÍCIO"',nav)
        self.assertIn('"SOBRE"',nav)
        patch=src("ports/sotc/android/bachata_perf.py")
        self.assertIn('"CUSA08809", "CUSA08034"',patch)
        self.assertIn('digest != EBOOT_SHA256',patch)
if __name__=="__main__": unittest.main()
