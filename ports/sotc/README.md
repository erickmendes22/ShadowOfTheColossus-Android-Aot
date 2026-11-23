# Shadow of the Colossus — Android port

> **Documentação atual:** [README principal (Português)](../../README.md) · [English](../../README.en.md) · [Créditos](../../CREDITS.md)

A implementação Android **0.2.0** é um port experimental com **CPU ARM64 AOT nativa, sem FEX e sem TSO**, carregador Bionic, renderização Vulkan/AHardwareBuffer e driver Turnip GameHub DD integrado. Não é mais o protótipo *preboot* descrito nas primeiras versões deste arquivo.

## Código Android

- [Preparação do jogo, runtime e compilador AOT](android/)
- [Workflow do APK](../../.github/workflows/sotc-021-apk.yml)
- [Testes de integridade e validação obrigatória](../../AGENTS.md)
- [Port original para PC: AjncSystem/ShadowOfTheColossus-PC](https://github.com/AjncSystem/ShadowOfTheColossus-PC)

As edições reconhecidas na versão atual são **CUSA08809 (EU 1.00)** e **CUSA08034 (US 1.00)**. Os patches são aplicados apenas após a verificação do executável compatível.

### Sobre referências antigas a FEX

O port teve fases iniciais de pesquisa com FEX. Parte da árvore de código e dos namespaces Android preserva essa origem por compatibilidade histórica e atribuição de licença. O **APK atual não inclui o runtime FEX**; o próprio manifesto do runtime informa `fex_runtime_included: false`.

Referências a FEX no histórico do projeto ou nos arquivos de licenças **não representam dependência ativa de execução do jogo**. Não exclua licenças e créditos dos componentes dos quais o port foi derivado.

Nenhum arquivo do jogo, chave de descriptografia ou firmware proprietário é distribuído.
