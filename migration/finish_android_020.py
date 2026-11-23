#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later
"""Apply checked 0.2.0 Android changes after importing the 0.1.74 source tree."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def replace(path,old,new):
    p=ROOT/path
    s=p.read_text()
    n=s.count(old)
    if n != 1: raise RuntimeError(f"{path}: expected one match, got {n}: {old[:80]!r}")
    p.write_text(s.replace(old,new))

ui="android-launcher/app/src/main/java/com/gow3/android/ui/SotcScreen.kt"
replace(ui, 'modifier=Modifier.fillMaxWidth().aspectRatio(1.9f)\n            .clip(RoundedCornerShape(15.dp)),\n        contentScale=ContentScale.Crop,',
    'modifier=Modifier.fillMaxWidth().height(142.dp)\n            .clip(RoundedCornerShape(15.dp)),\n        contentScale=ContentScale.Fit,')
replace(ui,"CUSA08809 (EU 1.01) e CUSA08034 (US 1.00)","CUSA08809 (EU 1.00) e CUSA08034 (US 1.00)")
replace(ui,"CUSA08809 (EU 1.01) and CUSA08034 (US 1.00)","CUSA08809 (EU 1.00) and CUSA08034 (US 1.00)")
replace(ui,"https://github.com/erickmendes22/gow3_android_daedalus_fork/tree/sotc-apk-integration",
    "https://github.com/erickmendes22/ShadowOfTheColossus-Android-Aot")
replace(ui,'Text("YouTube: @daedalusemulator",color=SotcPalette.secondary)',
'''Text("YouTube: @daedalusemulator",color=SotcPalette.secondary)
                    Text(if(pt) "CRÉDITOS" else "CREDITS",
                        color=SotcPalette.accent,fontWeight=FontWeight.Bold)
                    Text(if(pt)
                        "Port original para PC: AjncSystem e colaboradores. Base do carregador: bloodborne_pc (Supermedo, deadinside28 e forks). Renderizador Vulkan: shadPS4, Pink-shadPS4 e colaboradores. AOT ARM64 e infraestrutura Android: trabalhos de ducvd89/Bloodborne-Android, ferramentas bb-recomp, fexdroid e comunidade. Driver: Mesa/Turnip e DD/GameHub. Adaptação Android/Daedalus: erickmendes22."
                        else "Original PC port: AjncSystem and contributors. Loader foundation: bloodborne_pc (Supermedo, deadinside28 and forks). Vulkan renderer: shadPS4, Pink-shadPS4 and contributors. ARM64 AOT and Android infrastructure: ducvd89/Bloodborne-Android, bb-recomp tools, fexdroid and community. Driver: Mesa/Turnip and DD/GameHub. Android/Daedalus adaptation: erickmendes22.",
                        color=SotcPalette.secondary,fontSize=12.sp)
                    Text(if(pt) "Licença GPL-2.0-ou-posterior e licenças de terceiros em CREDITS.md. Sem arquivos do jogo."
                         else "GPL-2.0-or-later and third-party notices in CREDITS.md. No game files included.",
                        color=SotcPalette.secondary,fontSize=11.sp)''')
replace("ports/sotc/android/prepare_game.py","'CUSA08809':'EU 1.01'","'CUSA08809':'EU 1.00'")
replace("android-launcher/app/build.gradle.kts",
    'versionCode = 10074\n                versionName = "0.1.74-video-aot-hud-icons"',
    'versionCode = 20000\n                versionName = "0.2.0"')
replace("android-launcher/app/build.gradle.kts",
    'manifestPlaceholders["appLabel"] = "Shadow of the Colossus"',
    'manifestPlaceholders["appLabel"] = "Shadow of the Colossus Android"')
src=ROOT/"ports/sotc/android/repack_sotc_074.py"
pack=src.read_text().replace("0.1.74-video-aot-hud-icons","0.2.0").replace("0.1.74","0.2.0")
(ROOT/"ports/sotc/android/repack_sotc_020.py").write_text(pack)
assert 'RELEASE = "0.2.0"' in pack
assert "AjncSystem e colaboradores" in (ROOT/ui).read_text()
assert "EU 1.01" not in (ROOT/ui).read_text()
assert "ContentScale.Fit" in (ROOT/ui).read_text()
assert 'versionCode = 20000' in (ROOT/"android-launcher/app/build.gradle.kts").read_text()
# Make new-fork GitHub Actions self-contained and replace obsolete release labels.
source_workflow=ROOT/".github/workflows/sotc-074-fast-apk.yml"
if not source_workflow.is_file():
    raise RuntimeError("Expected last known good incremental 0.1.74 workflow")
w=source_workflow.read_text()
w=w.replace("name: SotC 0.1.74 Display AOT HUD Icons APK (incremental)",
            "name: Shadow of the Colossus Android 0.2.0 incremental APK")
w=w.replace("feature/sotc-074-display-aot-icons-hud","feature/android-aot-0.2.0, main")
w=w.replace("sotc-074-fast-apk.yml","sotc-020-apk.yml")
w=w.replace("sotc-074-gamehub-bundle","sotc-020-gamehub-bundle")
w=w.replace("sotc-074-badging","sotc-020-badging")
w=w.replace("repack_sotc_074","repack_sotc_020")
w=w.replace("test_sotc_ux_074.py","test_sotc_ux_020.py")
w=w.replace("0.1.74-video-aot-hud-icons","0.2.0")
w=w.replace("0.1.74","0.2.0")
w=w.replace("10074","20000")
w=w.replace("          run-id: 45076980313",
            "          run-id: 45076980313\n          repository: erickmendes22/gow3_android_daedalus_fork")
(ROOT/".github/workflows/sotc-020-apk.yml").write_text(w)
assert "repack_sotc_020.py" in w
assert "versionName = " not in w or "0.2.0" in w
# Retain source-drift tests but bind expectations to the 0.2.0 UI and version.
oldtest=(ROOT/"tests/test_sotc_ux_074.py").read_text()
newtest=(oldtest.replace("Sotc074","Sotc020")
    .replace("0.1.74","0.2.0")
    .replace("10074","20000")
    .replace("0.2.0-video-aot-hud-icons","0.2.0")
    .replace('manifestPlaceholders["appLabel"] = "Shadow of the Colossus"',
             'manifestPlaceholders["appLabel"] = "Shadow of the Colossus Android"')
    .replace("ContentScale.Crop","ContentScale.Fit"))
(ROOT/"tests/test_sotc_ux_020.py").write_text(newtest)
assert 'versionName = "0.2.0"' in newtest
assert (ROOT/"LICENSE").is_file()
assert (ROOT/"AGENTS.md").is_file()
print("PASS Android AOT 0.2.0 metadata, both CUSA 1.00, compact original artwork and credits")
