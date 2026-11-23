# Shadow of the Colossus Android — Daedalus AOT 0.2.0

[English](README.en.md) · [Créditos completos](CREDITS.md) · [Licença GPL-2.0-or-later](LICENSE)

Port **experimental para Android ARM64** mantido por **[erickmendes22 / Daedalus Emulator](https://www.youtube.com/@daedalusemulator)**, derivado do port de PC **[AjncSystem/ShadowOfTheColossus-PC](https://github.com/AjncSystem/ShadowOfTheColossus-PC)** e do trabalho de seus colaboradores e de outros projetos abertos.

> **Não contém jogo, PKGs, arquivos da Sony, chaves nem dumps.** Use sua cópia própria de Shadow of the Colossus (PS4). Projeto não afiliado à Sony Interactive Entertainment ou Bluepoint Games.

## Recursos da versão 0.2.0

- **Edições no port Android:** CUSA08809 (**EU 1.00**) e CUSA08034 (**US 1.00**), com verificação de hash e bytes do executável antes de aplicar patches. Executáveis diferentes não são aceitos automaticamente.
- **CPU:** ARM64 AOT nativo, sem FEX e sem TSO; compilação no aparelho, reutilização de perfis válidos após atualização e recompilação somente quando a validação exigir.
- **GPU:** Vulkan Bionic/AHardwareBuffer; apenas a **Turnip GameHub DD 26.3** integrada e verificada por SHA-256.
- **Vídeo:** resolução interna 720p, 540p ou 360p, saída 720p, opção de preencher a tela. Arte da página inicial com altura limitada e sem ampliação desproporcional.
- **HUD:** FPS + CPU/GPU quando houver medidores disponíveis, somente FPS ou desativada.
- **Controles:** touch personalizável e controle físico; ajuste de layout e sensibilidade.
- **Instalação e saves:** PKG base em subpasta automática, seleção de pasta do jogo, exportação/importação de saves e exportação de logs.
- **Idiomas:** português brasileiro e inglês no launcher; idioma do jogo depende dos arquivos disponíveis.

## Instalação

1. Baixe um APK **assinado** em [Releases](https://github.com/erickmendes22/ShadowOfTheColossus-Android-Aot/releases), quando publicado.
2. Para atualizar por cima, o certificado de assinatura precisa ser **idêntico**. Não desinstale se quiser preservar dados e compilações.
3. Escolha a pasta do jogo que contém **eboot.bin** e **sce_sys/param.sfo**, ou instale seu próprio PKG base.
4. Na primeira execução, compile o código ARM64 AOT. Perfis anteriores são reutilizados após verificação; alterar jogo, resolução ou patches pode exigir recompilação.

Nenhum FPS ou compatibilidade total é garantido; o desempenho depende do dispositivo e da GPU.

## Código e compilação

Fontes: **android-launcher/**, **ports/sotc/android/**, **src/**, **gpu/** e **cpu/**. O workflow para APK é **.github/workflows/sotc-020-apk.yml**. É obrigatória a validação de ABI dos ELFs ARM64 por **ports/sotc/android/verify_sotc_link.py**. A chave privada da assinatura **não está no repositório**.

## Créditos e licença

Este é um **port derivado**, não uma obra reescrita independentemente. Créditos a **AjncSystem e colaboradores**, **bloodborne_pc (Supermedo, deadinside28 e forks)**, **shadPS4 e Pink-shadPS4**, **ducvd89/Bloodborne-Android e bb-recomp**, **fexdroid** e **Mesa/Turnip + DD/GameHub**, além da adaptação Android por **erickmendes22**.

Veja [CREDITS.md](CREDITS.md), [LICENSE](LICENSE) e **android-launcher/app/src/main/assets/THIRD_PARTY_LICENSES.txt**. Código derivado GPL-2.0-or-later onde aplicável; demais componentes preservam suas licenças.

[Issues](https://github.com/erickmendes22/ShadowOfTheColossus-Android-Aot/issues) · [@daedalusemulator](https://www.youtube.com/@daedalusemulator)
