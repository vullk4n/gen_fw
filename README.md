# Gen FW - Gerador de Framework HAL

Este repositório contém um gerador de framework HAL (Hardware Abstraction Layer) para Android, que converte listas de FQNs (Fully Qualified Names) de interfaces HIDL e AIDL em arquivos de configuração XML compatíveis com o sistema Android.

## 📋 Descrição

O `genfwkona.py` é um script Python que processa uma lista de interfaces HAL (HIDL e AIDL) e gera configurações XML padronizadas para uso em builds AOSP (Android Open Source Project). O script suporta tanto interfaces HIDL quanto AIDL e pode mesclar múltiplas versões e instâncias de interfaces.

## 🚀 Funcionalidades

- **Suporte a HIDL e AIDL**: Processa ambos os tipos de interfaces HAL
- **Mesclagem de versões**: Combina automaticamente diferentes versões da mesma interface
- **Múltiplas instâncias**: Suporta múltiplas instâncias de uma mesma interface
- **Validação de entrada**: Verifica e valida o formato dos FQNs de entrada
- **Geração XML**: Produz saída XML compatível com o framework Android

## 📦 Uso em Builds AOSP

Este gerador é especialmente útil para:
- Configuração de HALs em builds AOSP
- Geração automática de arquivos de configuração
- Padronização de interfaces HAL
- Integração com sistemas de build Android

