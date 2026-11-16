#!/usr/bin/env python3
"""Monta o resource pack PT-BR do Homestead e instala tudo na instância.

Uso:
    python tools/build.py --instance "<caminho da instancia>"
    python tools/build.py            # usa a env HOMESTEAD_INSTANCE
    python tools/build.py --instance "<...>" --zip-only

O que faz:
  1. copia pack-source/assets/*  -> <instancia>/resourcepacks/Homestead PTBR/assets/*
  2. junta quests/pt_*.tsv       -> assets/ftbquests/lang/pt_br.json (dentro do pack)
                                   e em config/openloader/resources/ftbquests/... (fallback)
  3. copia patchouli/patchouli_books/* -> <instancia>/patchouli_books/*
  4. gera dist/Homestead-PTBR-<versao>.zip com pack.mcmeta + assets
"""

import argparse
import io
import json
import os
import shutil
import sys
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERSION = "1.0.0"
PACK_NAME = "Homestead PTBR"


def die(msg):
    print("ERRO: " + msg)
    sys.exit(1)


def load_tsv_dir(path):
    data = {}
    if not os.path.isdir(path):
        return data
    for name in sorted(os.listdir(path)):
        if not name.endswith(".tsv"):
            continue
        with io.open(os.path.join(path, name), encoding="utf-8-sig") as f:
            for line in f:
                line = line.rstrip("\n")
                if not line or "\t" not in line:
                    continue
                k, v = line.split("\t", 1)
                k = k.strip()
                if k and v.strip():
                    data[k] = v
    return data


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instance", default=os.environ.get("HOMESTEAD_INSTANCE", ""))
    ap.add_argument("--zip-only", action="store_true", help="só gera o zip, não mexe na instância")
    args = ap.parse_args()

    mc = args.instance
    if not args.zip_only:
        if not mc:
            die("informe --instance ou defina HOMESTEAD_INSTANCE")
        if not os.path.isdir(mc):
            die("instância não encontrada: " + mc)

    staging = os.path.join(ROOT, "dist", "build")
    if os.path.isdir(staging):
        shutil.rmtree(staging)
    assets_out = os.path.join(staging, "assets")

    # 1. assets dos mods
    total = 0
    src_assets = os.path.join(ROOT, "pack-source", "assets")
    for ns in sorted(os.listdir(src_assets)):
        src = os.path.join(src_assets, ns, "lang", "pt_br.json")
        if not os.path.isfile(src):
            continue
        with io.open(src, encoding="utf-8") as f:
            data = json.load(f)
        clean = {k: v for k, v in data.items() if v.strip()}
        dst_dir = os.path.join(assets_out, ns, "lang")
        os.makedirs(dst_dir, exist_ok=True)
        with io.open(os.path.join(dst_dir, "pt_br.json"), "w", encoding="utf-8") as f:
            json.dump(clean, f, ensure_ascii=False, indent=1, sort_keys=True)
        total += len(clean)
        print("  %-22s %5d chaves" % (ns, len(clean)))

    # 2. quests
    quests = load_tsv_dir(os.path.join(ROOT, "quests"))
    if quests:
        qdir = os.path.join(assets_out, "ftbquests", "lang")
        os.makedirs(qdir, exist_ok=True)
        with io.open(os.path.join(qdir, "pt_br.json"), "w", encoding="utf-8") as f:
            json.dump(quests, f, ensure_ascii=False, indent=1, sort_keys=True)
        print("  %-22s %5d chaves" % ("ftbquests", len(quests)))
        total += len(quests)

    # 3. pack.mcmeta
    with io.open(os.path.join(staging, "pack.mcmeta"), "w", encoding="utf-8") as f:
        json.dump(
            {"pack": {"pack_format": 15, "description": "Homestead PT-BR - quests, livros e mods"}},
            f,
            ensure_ascii=False,
            indent=2,
        )
        f.write("\n")

    print("TOTAL de chaves no pack: %d" % total)

    # 4. zip
    os.makedirs(os.path.join(ROOT, "dist"), exist_ok=True)
    zip_path = os.path.join(ROOT, "dist", "Homestead-PTBR-%s.zip" % VERSION)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for base, _dirs, files in os.walk(staging):
            for name in files:
                full = os.path.join(base, name)
                z.write(full, os.path.relpath(full, staging))
    print("ZIP -> " + zip_path)

    if args.zip_only:
        return

    # 5. instala na instância
    rp_dir = os.path.join(mc, "resourcepacks")
    os.makedirs(rp_dir, exist_ok=True)
    final = os.path.join(rp_dir, PACK_NAME)
    if os.path.isdir(final):
        shutil.rmtree(final)
    shutil.copytree(staging, final)
    print("PACK -> " + final)

    if quests:
        odir = os.path.join(
            mc, "config", "openloader", "resources", "ftbquests", "assets", "ftbquests", "lang"
        )
        os.makedirs(odir, exist_ok=True)
        with io.open(os.path.join(odir, "pt_br.json"), "w", encoding="utf-8") as f:
            json.dump(quests, f, ensure_ascii=False, indent=1, sort_keys=True)
        print("QUESTS -> " + os.path.join(odir, "pt_br.json"))

    books_src = os.path.join(ROOT, "patchouli", "patchouli_books")
    if os.path.isdir(books_src):
        for book in sorted(os.listdir(books_src)):
            s = os.path.join(books_src, book)
            d = os.path.join(mc, "patchouli_books", book)
            if not os.path.isdir(s):
                continue
            shutil.copytree(s, d, dirs_exist_ok=True)
            print("LIVRO %-20s -> %s" % (book, d))


if __name__ == "__main__":
    main()
