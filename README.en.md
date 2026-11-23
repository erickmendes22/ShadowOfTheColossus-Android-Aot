# Shadow of the Colossus Android — Daedalus AOT 0.2.0

[Português (Brasil)](README.pt-BR.md) · [Credits](CREDITS.md) · [GPL-2.0-or-later](LICENSE)

**Experimental ARM64 Android port** maintained by **[erickmendes22 / Daedalus Emulator](https://www.youtube.com/@daedalusemulator)**, derived from **[AjncSystem/ShadowOfTheColossus-PC](https://github.com/AjncSystem/ShadowOfTheColossus-PC)** and its community. It is not a new independently rewritten game port.

> No game files, PKGs, Sony content or keys are included. Bring your own PS4 game dump. This project is unaffiliated with Sony Interactive Entertainment or Bluepoint Games.

**0.2.0 features:** CUSA08809 (**EU 1.00**) and CUSA08034 (**US 1.00**) with strict executable/patch validation; native ARM64 ahead-of-time CPU compilation without FEX/TSO; matching compiled profiles preserved across app updates; Vulkan Bionic and AHardwareBuffer; exclusively the bundled, SHA-256-verified GameHub DD 26.3 Turnip; 720p/540p/360p internal rendering at 720p output; fill screen; FPS-only/full/hidden HUD (real CPU/GPU readings when available); adjustable touch/physical controllers, base PKG installation into a new folder, import/export saves and logs, Portuguese and English interface, and a responsive full-width artwork banner with intact uncropped poster.

**Install:** use a signed APK from [Releases](https://github.com/erickmendes22/ShadowOfTheColossus-Android-Aot/releases), when published. Updating over the previous version requires the same signing certificate. Select your own extracted game directory with **eboot.bin** and **sce_sys/param.sfo**, or install the base PKG; compile the ARM64 AOT code once on the device. Subsequent launches verify and reuse compatible AOT profiles.

**Source and build:** **android-launcher/** and **ports/sotc/android/** plus CPU/GPU/native sources. See **.github/workflows/sotc-020-apk.yml**; strict ARM64 host/renderer ABI checking is mandatory. The APK signing private key is not included in this public repository.

**Credits:** [AjncSystem / ShadowOfTheColossus-PC](https://github.com/AjncSystem/ShadowOfTheColossus-PC), [bloodborne_pc](https://github.com/Supermedo/bloodborne_pc), [shadPS4](https://github.com/shadps4-emu/shadPS4), [Pink-shadPS4](https://github.com/luizgustavs/Pink-shadPS4), [ducvd89/Bloodborne-Android](https://github.com/ducvd89/Bloodborne-Android), [fexdroid](https://github.com/cobrabm12/fexdroid), [Mesa/Turnip](https://gitlab.freedesktop.org/mesa/mesa), [Droid-Deck Drivers](https://github.com/Droid-Deck/Drivers), [WinlatorComponents / GameHub DD](https://github.com/erickmendes22/WinlatorComponents), and [Daedalus Android](https://github.com/erickmendes22/ShadowOfTheColossus-Android-Aot). See **[CREDITS.md](CREDITS.md)** for individual contributors and complete attributions.

**License:** GPL-2.0-or-later where applicable; third-party software retains its own notices. See [LICENSE](LICENSE) and **android-launcher/app/src/main/assets/THIRD_PARTY_LICENSES.txt**.

**0.2.0 changes:** in-game resolution and patch options with a verified AOT restart; fullscreen and FPS HUD choices without a restart; improved wide artwork banner and structured About page with working upstream links.
