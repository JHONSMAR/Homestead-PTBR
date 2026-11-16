# Homestead · A Cozy Survival Experience — Tradução PT-BR

Tradução brasileira do modpack **Homestead — A Cozy Survival Experience** (Fabric 1.20.1): quests do FTB Quests, os três livros do Patchouli e os textos/nomes de oito mods que os packs comunitários não cobriam.

## Cobertura

| Parte | Chaves traduzidas | Status |
| --- | --- | --- |
| Quests (FTB Quests, 27 capítulos) | 2.530 / 2.530 | 100% |
| Livros Patchouli (`homestead`, `welcome`, `roots_take_hold`) | 8 arquivos | 100% |
| Mods (8 namespaces) | 10.753 / 10.753 | 100% |

Namespaces cobertos: `railways` (Steam 'n' Rails), `fetzisasiandeco`, `umbrellas`, `clutter`, `luphieclutteredmod`, `mythicupgrades`, `decorativelamps`, `createdeco`.

No jogo, o FTB Quests exibe **2.499** dessas chaves: as 31 restantes são linhas vazias também no original em inglês (o jogo usa o fallback).

## Instalação

1. Feche o Minecraft.
2. Copie a pasta `Homestead PTBR` para `<instância>/resourcepacks/` (ou use o zip da [release](../../releases) sem extrair).
3. Ative o pack em *Opções → Pacotes de Recursos*, **acima** de `The Brazilian Project` e `Traducao PTBR CurseForge`.
4. Se as quests aparecerem em inglês, confirme que `config/openloader/resources/ftbquests/assets/ftbquests/lang/pt_br.json` existe — ele é gerado junto com o pack.

Para instalar tudo de uma vez (pack + quests + livros):

```powershell
python tools/build.py --instance "C:\caminho\da\instancia\minecraft"
```

O script também gera `dist/Homestead-PTBR-1.0.0.zip` para distribuição.

## Estrutura

```
quests/            pt_<capítulo>.tsv — chave<TAB>texto, um por capítulo
patchouli/         traduções dos livros (pt_br)
pack-source/       assets/<namespace>/lang/pt_br.json
tools/build.py     monta o pack, instala na instância e gera o zip
tools/check_quests.py   valida contagem de chaves dos TSVs
```

## Convenções

- Nomes de itens e blocos de mods ficam **em inglês** (Skillet, Keg, Backpack, Ruby, Topaz); títulos, subtítulos e prosa são traduzidos.
- Trocadilhos foram recriados em português em vez de traduzidos ao pé da letra.
- `%%` e `%s` / `%1$s` são preservados exatamente como no original.
- Códigos de formatação (`§a`, `§l`, `§r`) são mantidos.

## Créditos

- Modpack: **CozyCord** — [Homestead — A Cozy Survival Experience](https://www.curseforge.com/minecraft/modpacks/homestead-a-cozy-survival-experience).
- Base de termos e revisão: **The Brazilian Project 1.5.2** e **Traducao PTBR CurseForge 0.0.41**.
- Mods traduzidos aqui: Create, Steam 'n' Rails, Fetzi's Asian Deco, Umbrellas, Clutter, Luphie's Cluttered Mod, Mythic Upgrades, Decorative Lamps, Create Deco.

Este repositório contém **apenas os textos da tradução** — nenhum jar ou asset original dos mods é redistribuído.

## Licença

- Textos da tradução: [CC BY-SA 4.0](LICENSE) — use, adapte e republique citando os créditos acima.
- Scripts em `tools/`: [MIT](LICENSE-MIT).
