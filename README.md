# Homestead · A Cozy Survival Experience — Tradução PT-BR

Tradução brasileira do modpack **Homestead — A Cozy Survival Experience** (Fabric 1.20.1): quests do FTB Quests, os três livros do Patchouli e os textos/nomes de oito mods que os packs comunitários não cobriam.

**[⬇ Baixar a versão mais recente](../../releases/latest)** · [Como instalar](#instalação) · [Cobertura](#cobertura)

## Cobertura

| Parte | Chaves traduzidas | Status |
| --- | --- | --- |
| Quests (FTB Quests, 27 capítulos) | 2.530 / 2.530 | 100% |
| Livros Patchouli (`homestead`, `welcome`, `roots_take_hold`) | 8 arquivos | 100% |
| Mods (8 namespaces) | 10.753 / 10.753 | 100% |

Namespaces cobertos: `railways` (Steam 'n' Rails), `fetzisasiandeco`, `umbrellas`, `clutter`, `luphieclutteredmod`, `mythicupgrades`, `decorativelamps`, `createdeco`.

No jogo, o FTB Quests exibe **2.499** dessas chaves: as 31 restantes são linhas vazias também no original em inglês (o jogo usa o fallback).

---

## Instalação

São três coisas: o **pack de recursos** (mods + quests), os **livros Patchouli** e o **idioma do jogo**. A opção rápida faz tudo de uma vez.

### Opção 1 — script (faz tudo)

Precisa de [Python 3](https://www.python.org/downloads/). No PowerShell, dentro desta pasta:

```powershell
git clone https://github.com/JHONSMAR/Homestead-PTBR.git
cd Homestead-PTBR
python tools/build.py --instance "C:\caminho\da\instancia\minecraft"
```

Isso instala o pack em `resourcepacks/Homestead PTBR`, as quests em `config/openloader/resources/...` e os livros em `patchouli_books/`, e ainda gera o zip em `dist/`.

### Opção 2 — manual

**1. Baixe o zip da release**

Vá em [Releases](../../releases/latest) e baixe `Homestead-PTBR-1.0.0.zip`. **Não extraia**.

**2. Coloque em `resourcepacks`**

Minecraft fechado. Copie o zip para a pasta `resourcepacks` da instância:

| Launcher | Caminho |
| --- | --- |
| PrismLauncher | `%APPDATA%\PrismLauncher\instances\Homestead - A Cozy Survival Experience\minecraft\resourcepacks\` |
| CurseForge | `%USERPROFILE%\curseforge\minecraft\Instances\Homestead - A Cozy Survival Experience\resourcepacks\` |
| Modrinth App | `%APPDATA%\com.modrinth.theseus\profiles\Homestead - A Cozy Survival Experience\resourcepacks\` |
| MultiMC | `%APPDATA%\MultiMC\instances\Homestead - A Cozy Survival Experience\.minecraft\resourcepacks\` |

**3. Ative o pack**

Abra o jogo em *Opções → Pacotes de Recursos* e ative **Homestead PTBR**. Ele deve ficar **acima** de `The Brazilian Project` e `Traducao PTBR CurseForge` — assim as traduções deste repo têm prioridade sobre as comunitárias nos pontos onde as duas mexem.

**4. Deixe o jogo em português**

*Opções → Idioma → Português (Brasil)*. Sem isso o Minecraft continua carregando os textos em inglês, por mais packs ativos que existam.

**5. Livros Patchouli (opcional, só se quiser os livros em PT)**

O Patchouli não lê resource packs, então os livros são instalados à parte. Pegue a pasta `patchouli/patchouli_books/` deste repositório e copie cada `pt_br` para dentro da instância, mantendo a estrutura:

```
<instância>/patchouli_books/homestead/pt_br/
<instância>/patchouli_books/welcome/pt_br/
<instância>/patchouli_books/roots_take_hold/pt_br/
```

Os arquivos `en_us` que já existem na instância não devem ser tocados — o Patchouli escolhe a língua pelo `pt_br` ao lado.

**6. Quests (só se não aparecerem traduzidas)**

Se você instalou só o zip e as quests continuarem em inglês, extraia do próprio zip o arquivo `assets/ftbquests/lang/pt_br.json` e coloque em:

```
<instância>/config/openloader/resources/ftbquests/assets/ftbquests/lang/pt_br.json
```

### Conferindo se funcionou

- Itens do Steam 'n' Rails, Umbrellas, Clutter etc. com nome e tooltip em português;
- Primeira aba de quests com títulos como *Começando*, *Pão e Manteiga* em vez de *Beginning Game*, *Bread and Butter*;
- Livro de boas-vindas abrindo em português.

### Atualizar

Baixe o zip novo da release, substitua o antigo em `resourcepacks` e mantenha ele ativo. Os `pt_br.json` são substituídos inteiros, sem merge.

### Desinstalar

Remova o zip/pasta `Homestead PTBR` de `resourcepacks` e as pastas `pt_br` de `patchouli_books`. Nada é escrito em `mods/` nem em `config/ftbquests/`.

---

## Estrutura do repositório

```
quests/            pt_<capítulo>.tsv — chave<TAB>texto, um por capítulo
patchouli/         traduções dos livros (pt_br)
pack-source/       assets/<namespace>/lang/pt_br.json
tools/build.py     monta o pack, instala na instância e gera o zip
tools/check_quests.py   valida contagem de chaves dos TSVs
tools/engine/      gerador usado na produção (glossário + valores manuais)
```

`tools/engine/` é o pipeline que gerou os `pt_br.json`: `translate_names.py` compõe nomes de itens a partir de um glossário e `manual_values*.json` guarda as traduções revisadas à mão. Os caminhos dentro dele são absolutos e apontam para a máquina onde a tradução foi feita — serve como referência e histórico, não como instalador.

## Convenções da tradução

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
