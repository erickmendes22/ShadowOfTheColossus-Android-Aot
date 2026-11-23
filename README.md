# Shadow of the Colossus Android — Daedalus AOT 0.2.0

[English](README.en.md) · [Créditos completos](CREDITS.md) · [Licença GPL-2.0-or-later](LICENSE)

Port **experimental para Android ARM64** mantido por **[erickmendes22 / Daedalus Emulator](https://www.youtube.com/@daedalusemulator)**, derivado do port de PC **[AjncSystem/ShadowOfTheColossus-PC](https://github.com/AjncSystem/ShadowOfTheColossus-PC)** e do trabalho de seus colaboradores e de outros projetos abertos.

> **Não contém jogo, PKGs, arquivos da Sony, chaves nem dumps.** Use sua cópia própria de Shadow of the Colossus (PS4). Projeto não afiliado à Sony Interactive Entertainment ou Bluepoint Games.

## Recursos da versão 0.2.0

- **Edições no port Android:** CUSA08809 (**EU 1.00**) e CUSA08034 (**US 1.00**), com verificação de hash e bytes do executável antes de aplicar patches. Executáveis diferentes não são aceitos automaticamente.
- **CPU:** ARM64 AOT nativo, sem FEX e sem TSO; compilação no aparelho, reutilização de perfis válidos após atualização e recompilação somente quando a validação exigir.
- **GPU:** Vulkan Bionic/AHardwareBuffer; apenas a **Turnip GameHub DD 26.3** integrada e verificada por SHA-256.
- **Vídeo:** resolução interna 720p, 540p ou 360p, saída 720p, opção de preencher a tela. Arte original exibida em banner que ocupa a largura disponível, preservando o pôster completo.
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

O port Android é uma adaptação derivada das implementações abaixo. Os autores originais mantêm seus direitos e atribuições:

- **[AjncSystem / ShadowOfTheColossus-PC](https://github.com/AjncSystem/ShadowOfTheColossus-PC)** — base original do port para PC e comunidade de colaboradores.
- **[bloodborne_pc — Supermedo, deadinside28 e forks](https://github.com/Supermedo/bloodborne_pc)** — carregador e arquitetura de runtime.
- **[shadPS4](https://github.com/shadps4-emu/shadPS4)** e **[Pink-shadPS4 — luizgustavs](https://github.com/luizgustavs/Pink-shadPS4)** — tradução gráfica e correções Vulkan.
- **[ducvd89 / Bloodborne-Android](https://github.com/ducvd89/Bloodborne-Android)** e **[ferramentas de recompilação](https://github.com/ducvd89/Bloodborne-android-rebuild-tool)** — referências da infraestrutura Bionic e AOT ARM64.
- **[cobrabm12 / fexdroid](https://github.com/cobrabm12/fexdroid)** — interfaces, controles e pontes de apresentação Android; a execução do jogo usa AOT ARM64 sem FEX.
- **[Mesa / Turnip](https://gitlab.freedesktop.org/mesa/mesa)**, **[Droid-Deck / Drivers](https://github.com/Droid-Deck/Drivers)** e **[WinlatorComponents — GameHub DD](https://github.com/erickmendes22/WinlatorComponents)** — driver Vulkan e integração.
- **[erickmendes22 / Daedalus Emulator](https://github.com/erickmendes22/ShadowOfTheColossus-Android-Aot)** — adaptação e manutenção do aplicativo Android.

Os demais colaboradores e avisos estão em **[CREDITS.md](CREDITS.md)** e **[THIRD_PARTY_LICENSES.txt](android-launcher/app/src/main/assets/THIRD_PARTY_LICENSES.txt)**. Licença de código derivado **[GPL-2.0-or-later](LICENSE)** onde aplicável; os componentes de terceiros preservam suas licenças.

## Melhorias 0.2.0

A tela inicial exibe a arte original em um banner responsivo, sem cortar o pôster principal. A aba Sobre reúne créditos organizados com links. No menu durante o jogo, a resolução e os patches podem ser alterados com reinício e verificação AOT; a tela cheia e os modos de HUD podem ser alterados imediatamente, sem reiniciar.

[Issues](https://github.com/erickmendes22/ShadowOfTheColossus-Android-Aot/issues) · [@daedalusemulator](https://www.youtube.com/@daedalusemulator)
