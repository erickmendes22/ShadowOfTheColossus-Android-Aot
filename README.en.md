# Shadow of the Colossus Android — Daedalus AOT 0.2.0

[Português (Brasil)](README.pt-BR.md) · [Credits](CREDITS.md) · [GPL-2.0-or-later](LICENSE)

**Experimental ARM64 Android port** maintained by **[erickmendes22 / Daedalus Emulator](https://www.youtube.com/@daedalusemulator)**, derived from **[AjncSystem/ShadowOfTheColossus-PC](https://github.com/AjncSystem/ShadowOfTheColossus-PC)** and its community. It is not a new independently rewritten game port.

> No game files, PKGs, Sony content or keys are included. Bring your own PS4 game dump. This project is unaffiliated with Sony Interactive Entertainment or Bluepoint Games.

**0.2.0 features:** CUSA08809 (**EU 1.00**) and CUSA08034 (**US 1.00**) with strict executable/patch validation; native ARM64 ahead-of-time CPU compilation without FEX/TSO; matching compiled profiles preserved across app updates; Vulkan Bionic and AHardwareBuffer; exclusively the bundled, SHA-256-verified GameHub DD 26.3 Turnip; 720p/540p/360p internal rendering at 720p output; fill screen; FPS-only/full/hidden HUD (real CPU/GPU readings when available); adjustable touch/physical controllers, base PKG installation into a new folder, import/export saves and logs, Portuguese and English interface, and a compact uncropped main artwork image.

**Install:** use a signed APK from [Releases](https://github.com/erickmendes22/ShadowOfTheColossus-Android-Aot/releases), when published. Updating over the previous version requires the same signing certificate. Select your own extracted game directory with **eboot.bin** and **sce_sys/param.sfo**, or install the base PKG; compile the ARM64 AOT code once on the device. Subsequent launches verify and reuse compatible AOT profiles.

**Source and build:** **android-launcher/** and **ports/sotc/android/** plus CPU/GPU/native sources. See **.github/workflows/sotc-020-apk.yml**; strict ARM64 host/renderer ABI checking is mandatory. The APK signing private key is not included in this public repository.

**Credits:** [CREDITS.md](CREDITS.md) documents AjncSystem and contributors, bloodborne_pc, shadPS4/Pink-shadPS4, ducvd89/Bloodborne-Android and bb-recomp, fexdroid, Mesa/Turnip and Daedalus Android adaptation.

**License:** GPL-2.0-or-later where applicable; third-party software retains its own notices. See [LICENSE](LICENSE) and **android-launcher/app/src/main/assets/THIRD_PARTY_LICENSES.txt**.
