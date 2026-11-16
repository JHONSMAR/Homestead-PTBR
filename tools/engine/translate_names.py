#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tradutor de nomes de blocos/itens (EN -> PT-BR) por glossário + concordância."""
import json, os, re, sys, zipfile, collections

W = r"C:\Users\mailo\AppData\Local\Temp\opencode\tr"
MC = r"C:\Users\mailo\AppData\Roaming\PrismLauncher\instances\Homestead - A Cozy Survival Experience\minecraft"

# genero/plural -> indice da forma
def F(m, f=None, mp=None, fp=None):
    return [m, f or m, mp or m + "s", fp or (f or m) + "s"]

COLORS = {
 "white": F("branco","branca"), "black": F("preto","preta"),
 "gray": F("cinza","cinza"), "lightgray": F("cinza-claro","cinza-clara"),
 "lightblue": F("azul-claro","azul-clara"), "red": F("vermelho","vermelha"),
 "yellow": F("amarelo","amarela"), "green": F("verde","verde"),
 "purple": F("roxo","roxa"), "magenta": F("magenta","magenta"),
 "cyan": F("ciano","ciana"), "lime": F("verde-limão","verde-limão"),
 "pink": F("rosa","rosa"), "blue": F("azul","azul"), "brown": F("marrom","marrom"),
 "orange": F("laranja","laranja"), "scarlet": F("escarlate","escarlate"),
 "verdant": F("verdejante","verdejante"), "umber": F("âmbar-escuro","âmbar-escura"),
 "dusk": F("crepuscular","crepuscular"), "golden": F("dourado","dourada"),
 "silver": F("prateado","prateada"), "copper": F("cobreado","cobreada"),
 "rose": F("rosado","rosada"), "amber": F("âmbar","âmbar"),
 "beige": F("bege","bege"), "teal": F("verde-azulado","verde-azulada"),
}

ADJS = {
 "long": F("longo","longa"), "longer": F("mais longo","mais longa"),
 "short": F("curto","curta"), "tall": F("alto","alta"),
 "large": F("grande","grande"), "small": F("pequeno","pequena"),
 "wide": F("largo","larga"), "thin": F("fino","fina"),
 "high": F("alto","alta"), "low": F("baixo","baixa"),
 "flat": F("plano","plana"), "hollow": F("oco","oca"),
 "framed": F("emoldurado","emoldurada"), "waxed": F("encerado","encerada"),
 "polished": F("polido","polida"), "oxidized": F("oxidado","oxidada"),
 "weathered": F("desgastado","desgastada"), "exposed": F("exposto","exposta"),
 "cracked": F("rachado","rachada"), "mossy": F("musgoso","musgosa"),
 "stripped": F("descascado","descascada"), "masoned": F("assentado","assentada"),
 "indented": F("entalhado","entalhada"), "tiled": F("ladrilhado","ladrilhada"),
 "riveted": F("rebitado","rebitada"), "slashed": F("cortado","cortada"),
 "folding": F("dobrável","dobrável"), "wrapped": F("revestido","revestida"),
 "basic": F("básico","básica"), "industrial": F("industrial","industrial"),
 "european": F("europeu","europeia"), "fully": F("completo","completa"),
 "static": F("estático","estática"), "charged": F("carregado","carregada"),
 "lethal": F("letal","letal"), "strong": F("forte","forte"),
 "dead": F("morto","morta"), "glowing": F("brilhante","brilhante"),
 "lit": F("aceso","acesa"), "unlit": F("apagado","apagada"),
 "hanging": F("suspenso","suspensa"), "standing": F("em pé","em pé"),
 "single": F("simples","simples"), "double": F("duplo","dupla"),
 "triple": F("triplo","tripla"), "quadruple": F("quádruplo","quádrupla"),
 "thick": F("grosso","grossa"), "smooth": F("liso","lisa"),
 "rough": F("áspero","áspera"), "carved": F("entalhado","entalhada"),
 "ornate": F("ornamentado","ornamentada"), "elegant": F("elegante","elegante"),
 "cozy": F("aconchegante","aconchegante"), "rustic": F("rústico","rústica"),
 "modern": F("moderno","moderna"), "vintage": F("vintage","vintage"),
 "pastel": F("pastel","pastel"), "neon": F("neon","neon"),
 "vertical": F("vertical","vertical"), "horizontal": F("horizontal","horizontal"),
 "diagonal": F("diagonal","diagonal"), "top": F("superior","superior"),
 "bottom": F("inferior","inferior"), "left": F("esquerdo","esquerda"),
 "right": F("direito","direita"), "middle": F("central","central"),
 "center": F("central","central"), "middle-left": F("central-esquerdo","central-esquerda"),
 "middle-right": F("central-direito","central-direita"),
 "top-left": F("superior-esquerdo","superior-esquerda"),
 "top-right": F("superior-direito","superior-direita"),
 "bottom-left": F("inferior-esquerdo","inferior-esquerda"),
 "bottom-right": F("inferior-direito","inferior-direita"),
 "down-left": F("para baixo à esquerda","para baixo à esquerda"),
 "down-right": F("para baixo à direita","para baixo à direita"),
 "up-left": F("para cima à esquerda","para cima à esquerda"),
 "up-right": F("para cima à direita","para cima à direita"),
 "inner": F("interno","interna"), "outer": F("externo","externa"),
 "upper": F("superior","superior"), "lower": F("inferior","inferior"),
 "extended": F("estendido","estendida"), "reinforced": F("reforçado","reforçada"),
 "chipped": F("lascado","lascada"), "aged": F("envelhecido","envelhecida"),
 "crude": F("cru","crua"), "raw": F("bruto","bruta"),
 "unpolished": F("não polido","não polida"), "refined": F("refinado","refinada"),
 "pure": F("puro","pura"), "heavy": F("pesado","pesada"),
 "light": F("leve","leve"), "open": F("aberto","aberta"),
 "closed": F("fechado","fechada"), "empty": F("vazio","vazia"),
 "full": F("cheio","cheia"), "half-flag": F("meia-bandeira","meia-bandeira"),
 "patterned": F("estampado","estampada"), "tattered": F("esfarrapado","esfarrapada"),
 "flowering": F("florido","florida"), "antique": F("antigo","antiga"),
 "checkered": F("xadrez","xadrez"), "lunar": F("lunar","lunar"),
 "mini": F("mini","mini"), "imperial": F("imperial","imperial"),
 "aquatic": F("aquático","aquática"), "toxic": F("tóxico","tóxica"),
 "wooden": F("de madeira","de madeira"), "giant": F("gigante","gigante"),
 "cooked": F("cozido","cozida"), "cobbled": F("de pedregulho","de pedregulho"),
 "electrical": F("elétrico","elétrica"), "radioactive": F("radioativo","radioativa"),
 "locked": F("trancado","trancada"), "cut": F("lapidado","lapidada"),
 "budding": F("em formação","em formação"), "lingering": F("persistente","persistente"),
 "mythic": F("mítico","mítica"), "sweetheart": F("Sweetheart","Sweetheart"),
 "halloween": F("de Halloween","de Halloween"), "glowing2": F("brilhante","brilhante"),
 "etching": F("gravado","gravada"), "painted": F("pintado","pintada"),
 "decorated": F("decorado","decorada"), "patterned2": F("estampado","estampada"),
 "ornamental": F("ornamental","ornamental"), "glassed": F("envidraçado","envidraçada"),
 "double2": F("duplo","dupla"), "stacked": F("empilhado","empilhada"),
 "layered": F("em camadas","em camadas"), "trimmed": F("aparado","aparada"),
 "barred": F("com grades","com grades"),
 "narrow": F("estreito","estreita"), "incomplete": F("incompleto","incompleta"),
 "hazard": F("de perigo","de perigo"), "hinged": F("dobradiço","dobradiça"),
 "sliding": F("deslizante","deslizante"), "plated": F("chapeado","chapeada"),
 "round": F("redondo","redonda"), "geometric": F("geométrico","geométrica"),
 "quilted": F("acolchoado","acolchoada"), "decorative": F("decorativo","decorativa"),
 "southern": F("sulista","sulista"), "choco": F("de chocolate","de chocolate"),
 "mint": F("de menta","de menta"), "two": F("de dois","de dois"),
 "three": F("de três","de três"), "four": F("de quatro","de quatro"),
 "one": F("de um","de um"), "unliving": F("inanimado","inanimada"),
 "cluttered": F("abarrotado","abarrotada"), "royal": F("real","real"),
 "japanese": F("japonês","japonesa"), "magic": F("mágico","mágica"),
 "linked": F("conectado","conectada"), "unlinked": F("desconectado","desconectada"),
 "cold": F("frio","fria"), "warm": F("quente","quente"),
 "squashed": F("esmagado","esmagada"), "falling": F("cainte","cainte"), "asian": F("asiático","asiática"), "blocky": F("blocado","blocada"),
}

# substantivos: (pt, genero, plural)
NOUNS = {
 "roof": ("Telhado","m",False), "block": ("Bloco","m",False),
 "slab": ("Laje","f",False), "stairs": ("Escadas","f",True),
 "wall": ("Parede","f",False), "brick": ("Tijolo","m",False),
 "bricks": ("Tijolos","m",True), "candle": ("Vela","f",False),
 "chair": ("Cadeira","f",False), "floor": ("Piso","m",False),
 "chandelier": ("Lustre","m",False), "candelabra": ("Candelabro","m",False),
 "lamp": ("Lâmpada","f",False), "tile": ("Ladrilho","m",False),
 "lantern": ("Lanterna","f",False), "fence": ("Cerca","f",False),
 "umbrella": ("Guarda-chuva","m",False), "door": ("Porta","f",False),
 "trapdoor": ("Alçapão","m",False), "curtains": ("Cortinas","f",True),
 "curtain": ("Cortina","f",False), "bed": ("Cama","f",False),
 "bench": ("Banco","m",False), "table": ("Mesa","f",False),
 "cupboard": ("Armário","m",False), "cage": ("Gaiola","f",False),
 "stand": ("Suporte","m",False), "window": ("Janela","f",False),
 "bars": ("Grades","f",True), "ore": ("Minério","m",False),
 "frame": ("Moldura","f",False), "chain": ("Corrente","f",False),
 "egg": ("Ovo","m",False), "skull": ("Crânio","m",False),
 "globe": ("Globo","m",False), "bookshelf": ("Estante de Livros","f",False),
 "shelf": ("Prateleira","f",False), "pillow": ("Travesseiro","m",False),
 "plushie": ("Pelúcia","f",False), "helmet": ("Capacete","m",False),
 "torch": ("Tocha","f",False), "glass": ("Vidro","m",False),
 "gate": ("Portão","m",False), "pillar": ("Pilar","m",False),
 "chimney": ("Chaminé","f",False), "lattice": ("Treliça","f",False),
 "trellis": ("Treliça","f",False), "armchair": ("Poltrona","f",False),
 "futon": ("Futon","m",False), "switch": ("Interruptor","m",False),
 "stack": ("Pilha","f",False), "panel": ("Painel","m",False),
 "plate": ("Prato","m",False), "sheet": ("Folha","f",False),
 "shard": ("Fragmento","m",False), "sill": ("Peitoril","m",False),
 "placard": ("Placa","f",False), "shield": ("Escudo","m",False),
 "fan": ("Ventilador","m",False), "decal": ("Decalque","m",False),
 "box": ("Caixa","f",False), "button": ("Botão","m",False),
 "coin": ("Moeda","f",False), "pot": ("Vaso","m",False),
 "vase": ("Vaso","m",False), "plant": ("Planta","f",False),
 "flower": ("Flor","f",False), "leaves": ("Folhas","f",True),
 "planks": ("Tábuas","f",True), "log": ("Tronco","m",False),
 "sapling": ("Muda","f",False), "seedling": ("Muda","f",False),
 "bucket": ("Balde","m",False), "crate": ("Caixote","m",False),
 "barrel": ("Barril","m",False), "chest": ("Baú","m",False),
 "sign": ("Placa","f",False), "carpet": ("Tapete","m",False),
 "rug": ("Tapete","m",False), "painting": ("Pintura","f",False),
 "picture": ("Quadro","m",False), "mirror": ("Espelho","m",False),
 "clock": ("Relógio","m",False), "bell": ("Sino","m",False),
 "ladder": ("Escada","f",False), "rail": ("Trilho","m",False),
 "track": ("Trilho","m",False), "buffer": ("Para-choque","m",False),
 "boiler": ("Caldeira","f",False), "smokebox": ("Caixa de Fumaça","f",False),
 "locometal": ("Locometal","m",False), "casing": ("Revestimento","m",False),
 "station": ("Estação","f",False), "platform": ("Plataforma","f",False),
 "cart": ("Carrinho","m",False), "wagon": ("Vagão","m",False),
 "train": ("Trem","m",False), "coupler": ("Engate","m",False),
 "whistle": ("Apito","m",False), "semaphore": ("Semáforo","m",False),
 "tank": ("Tanque","m",False), "hopper": ("Funil","m",False),
 "crane": ("Guindaste","m",False), "trunk": ("Baú","m",False),
 "cabinet": ("Armário","m",False), "sink": ("Pia","f",False),
 "stove": ("Fogão","m",False), "oven": ("Forno","m",False),
 "fireplace": ("Lareira","f",False), "counter": ("Balcão","m",False),
 "countertop": ("Bancada","f",False), "desk": ("Escrivaninha","f",False),
 "stool": ("Banquinho","m",False), "sofa": ("Sofá","m",False),
 "couch": ("Sofá","m",False), "drawer": ("Gaveta","f",False),
 "shelf2": ("Prateleira","f",False), "hook": ("Gancho","m",False),
 "rack": ("Prateleira","f",False), "pole": ("Poste","m",False),
 "post": ("Poste","m",False), "beam": ("Viga","f",False),
 "board": ("Tábua","f",False), "panel2": ("Painel","m",False),
 "banner": ("Estandarte","m",False), "flag": ("Bandeira","f",False),
 "carpet2": ("Tapete","m",False), "drape": ("Cortina","f",False),
 "valance": ("Sanefa","f",False), "canopy": ("Dossel","m",False),
 "awning": ("Toldo","m",False), "mill": ("Moinho","m",False),
 "well": ("Poço","m",False), "fountain": ("Fonte","f",False),
 "pond": ("Lago","m",False), "path": ("Caminho","m",False),
 "road": ("Estrada","f",False), "bridge": ("Ponte","f",False),
 "dock": ("Cais","m",False), "barrier": ("Barreira","f",False),
 "mosaic": ("Mosaico","m",False), "triangle": ("Triângulo","m",False),
 "triangles": ("Triângulos","m",True), "quarter": ("Quarto","m",False),
 "half": ("Metade","f",False), "third": ("Terço","m",False),
 "stripe": ("Faixa","f",False), "stripes": ("Faixas","f",True),
 "gradient": ("Gradiente","m",False), "border": ("Borda","f",False),
 "bordure": ("Bordadura","f",False), "corner": ("Canto","m",False),
 "circle": ("Círculo","m",False), "square": ("Quadrado","m",False),
 "rhombus": ("Losango","m",False), "cross": ("Cruz","f",False),
 "chevron": ("Chevron","m",False), "arrow": ("Seta","f",False),
 "sunburst": ("Raio de Sol","m",False), "splash": ("Respingo","m",False),
 "pattern": ("Padrão","m",False), "top2": ("Topo","m",False),
 "pane": ("Painel","m",False), "handle": ("Puxador","m",False),
 "knob": ("Maçaneta","f",False), "hinge": ("Dobradiça","f",False),
 "knocker": ("Aldrava","f",False), "mailbox": ("Caixa de Correio","f",False),
 "lantern2": ("Lanterna","f",False), "candleholder": ("Castiçal","m",False),
 "holder": ("Suporte","m",False), "tray": ("Bandeja","f",False),
 "bowl": ("Tigela","f",False), "cup": ("Xícara","f",False),
 "mug": ("Caneca","f",False), "jug": ("Jarra","f",False),
 "bottle": ("Garrafa","f",False), "jar": ("Pote","m",False),
 "can": ("Lata","f",False), "kettle": ("Chaleira","f",False),
 "sack": ("Saco","m",False), "bag": ("Bolsa","f",False),
 "basket": ("Cesta","f",False), "book": ("Livro","m",False),
 "books": ("Livros","m",True), "scroll": ("Pergaminho","m",False),
 "map": ("Mapa","m",False), "candle2": ("Vela","f",False),
 "incense": ("Incenso","m",False), "burner": ("Queimador","m",False),
 "censer": ("Turíbulo","m",False), "vial": ("Frasco","m",False),
 "crystal": ("Cristal","m",False), "gem": ("Gema","f",False),
 "ingot": ("Barra","f",False), "nugget": ("Pepita","f",False),
 "coil": ("Bobina","f",False), "wire": ("Fio","m",False),
 "pipe": ("Cano","m",False), "valve": ("Válvula","f",False),
 "gauge": ("Medidor","m",False), "dial": ("Mostrador","m",False),
 "gear": ("Engrenagem","f",False), "cog": ("Engrenagem","f",False),
 "wheel": ("Roda","f",False), "axle": ("Eixo","m",False),
 "spring": ("Mola","f",False), "piston": ("Pistão","m",False),
 "pump": ("Bomba","f",False), "motor": ("Motor","m",False),
 "engine": ("Motor","m",False), "chimney2": ("Chaminé","f",False),
 "skylight": ("Claraboia","f",False), "dormer": ("Água-furtada","f",False),
 "shutter": ("Postigo","m",False), "shutters": ("Postigos","m",True),
 "blind": ("Persiana","f",False), "blinds": ("Persianas","f",True),
 "lamp2": ("Lâmpada","f",False), "sconce": ("Arandela","f",False),
 "pendant": ("Pingente","m",False), "garland": ("Guirlanda","f",False),
 "wreath": ("Coroa de Flores","f",False), "ornament": ("Ornamento","m",False),
 "decoration": ("Decoração","f",False), "decor": ("Decoração","f",False),
 "trim": ("Acabamento","m",False), "molding": ("Moldura","f",False),
 "cornice": ("Cornija","f",False), "railing": ("Corrimão","m",False),
 "handrail": ("Corrimão","m",False), "balustrade": ("Balustrada","f",False),
 "column": ("Coluna","f",False), "arch": ("Arco","m",False),
 "portal": ("Portal","m",False), "gateway": ("Portão","m",False),
}


EXTRA = {
 "pagoda": ("Pagode","m",False), "kitchen": ("Cozinha","f",False),
 "detail": ("Detalhe","m",False), "shoji": ("Shoji","m",False),
 "koi": ("Koi","m",False), "katana": ("Katana","f",False),
 "fish": ("Peixe","m",False), "beam": ("Viga","f",False),
 "sail": ("Vela","f",False), "rope": ("Corda","f",False),
 "twigs": ("Gravetos","m",True), "spawn": ("Spawn","m",False),
 "fencegate": ("Portão de Cerca","m",False), "bunkbed": ("Beliche","m",False),
 "windowpane": ("Caixilho","m",False), "countertop": ("Bancada","f",False),
 "wallcupboard": ("Armário de Parede","m",False),
 "ground": ("Chão","m",False), "ceiling": ("Teto","m",False),
 "arch": ("Arco","m",False), "post": ("Poste","m",False),
 "pole": ("Poste","m",False), "hoop": ("Argola","f",False),
 "ring": ("Anel","m",False), "sconce": ("Arandela","f",False),
 "lamppost": ("Poste de Luz","m",False), "streetlamp": ("Poste de Luz","m",False),
 "fountain": ("Fonte","f",False), "windchime": ("Sino de Vento","m",False),
 "windchimes": ("Sinos de Vento","m",True), "grill": ("Grelha","f",False),
 "shutter": ("Postigo","m",False), "shutters": ("Postigos","m",True),
 "blinds": ("Persianas","f",True), "wallpaper": ("Papel de Parede","m",False),
 "tiles": ("Ladrilhos","m",True), "mat": ("Capacho","m",False),
 "sticks": ("Gravetos","m",True), "blocks": ("Blocos","m",True),
 "eggs": ("Ovos","m",True), "shelves": ("Prateleiras","f",True),
 "jars": ("Potes","m",True), "jam": ("Geleia","f",False),
 "picnic": ("Piquenique","m",False), "sewing": ("Costura","f",False),
 "sketchbook": ("Caderno de Esboços","m",False), "bunny": ("Coelhinho","m",False),
 "cardboard": ("Papelão","m",False), "flair": ("Estilo","m",False),
 "piece": ("Peça","f",False), "glow": ("Brilho","m",False),
 "confectionary": ("Doceria","f",False), "dorado": ("Dourado","m",False),
 "luphie": ("Luphie","m",False), "entity": ("Entidade","f",False),
 "windows": ("Janelas","f",True), "doors": ("Portas","f",True),
 "ladders": ("Escadas","f",True), "end": ("Extremidade","f",False),
 "cap": ("Tampa","f",False), "alloy": ("Liga","f",False),
 "ironcoin": ("Moeda de Ferro","f",False), "brasscoin": ("Moeda de Latão","f",False),
 "coppercoin": ("Moeda de Cobre","f",False), "goldcoin": ("Moeda de Ouro","f",False),
 "zinccoin": ("Moeda de Zinco","f",False), "netheritecoin": ("Moeda de Netherita","f",False),
 "bud": ("Broto","m",False), "aura": ("Aura","f",False),
 "reaction": ("Reação","f",False), "share": ("Partilha","f",False),
 "field": ("Campo","m",False), "miasma": ("Miasma","m",False),
 "blood": ("Sangue","m",False), "thirst": ("Sede","f",False),
 "damage": ("Dano","m",False), "deflection": ("Deflexão","f",False),
 "arcane": ("Arcano","m",False), "bomb": ("Bomba","f",False),
 "freeze": ("Congelamento","m",False), "incubation": ("Incubação","f",False),
 "cluster": ("Aglomerado","m",False), "medium": ("Médio","m",False),
 "vulnerability": ("Vulnerabilidade","f",False), "meltdown": ("Fusão","f",False),
 "shimmer": ("Vislumbre","m",False), "pouch": ("Bolsa","f",False),
 "mushrooms": ("Cogumelos","m",True), "chorus": ("Coro","m",False),
 "pads": ("Almofadas","f",True), "pile": ("Monte","m",False),
 "kiln": ("Forno","m",False), "fungi": ("Fungos","m",True),
 "sculk": ("Sculk","m",False), "fox": ("Raposa","f",False),
 "seahorse": ("Cavalo-marinho","m",False), "newt": ("Tritão","m",False),
 "apple": ("Maçã","f",False), "pumpkin": ("Abóbora","f",False),
 "carrot": ("Cenoura","f",False), "pine": ("Pinho","m",False),
 "olive": ("Oliva","f",False), "chartreuse": ("Chartreuse","m",False),
 "limestone": ("Calcário","m",False), "maroon": ("Vinho","m",False),
 "ochrum": ("Ocre","m",False), "scorchia": ("Escória","f",False),
 "turquoise": ("Turquesa","f",False), "vermilion": ("Vermelhão","m",False),
 "sea": ("Mar","m",False), "tuff": ("Tufo","m",False),
 "rung": ("Degrau","m",False), "pane": ("Painel","m",False),
 "louver": ("Veneziana","f",False), "slats": ("Ripas","f",True),
 "grille": ("Grade","f",False), "vent": ("Respiro","m",False),
 "dial2": ("Mostrador","m",False), "lever": ("Alavanca","f",False),
 "crank": ("Manivela","f",False), "wheel2": ("Roda","f",False),
 "cab": ("Cabine","f",False), "cabin": ("Cabine","f",False),
 "roof2": ("Telhado","m",False), "headlamp": ("Farol","m",False),
 "lamp3": ("Lanterna","f",False), "coupling": ("Engate","m",False),
 "plow": ("Arado","m",False), "snowplow": ("Arado de Neve","m",False),

 "extension": ("Extensão","f",False), "connector": ("Conector","m",False),
 "railing": ("Corrimão","m",False), "fencepost": ("Poste de Cerca","m",False),
 "gable": ("Oitão","m",False), "eave": ("Beirada","f",False),
 "eaves": ("Beiradas","f",True), "ridge": ("Cumeeira","f",False),
 "valley": ("Calha","f",False), "hip": ("Água","f",False),
 "sleeper": ("Dormente","m",False), "railtie": ("Travessa","f",False),
}
NOUNS.update({k: v for k, v in EXTRA.items() if k not in NOUNS})


EXTRA2 = {
 "catwalk": ("Passarela","f",False), "facade": ("Fachada","f",False),
 "hull": ("Casco","m",False), "mesh": ("Malha","f",False),
 "overlay": ("Sobreposição","f",False), "wedge": ("Cunha","f",False),
 "support": ("Apoio","m",False), "sheetmetal": ("Chapa Metálica","f",False),
 "primrose": ("Prímula","f",False), "watermelon": ("Melancia","f",False),
 "mushroom": ("Cogumelo","m",False), "briefcase": ("Maleta","f",False),
 "barrens": ("Ermos","m",True), "rifts": ("Fendas","f",True),
 "caves": ("Cavernas","f",True), "bulletin": ("Mural","m",False),
 "bee": ("Abelha","f",False), "observatory": ("Observatório","m",False),
 "row": ("Fileira","f",False), "puzzle": ("Quebra-cabeça","m",False),
 "strawberry": ("Morango","m",False), "lemon": ("Limão","m",False),
 "cat": ("Gato","m",False), "darkwood": ("Madeira Escura","f",False),
 "soul": ("Alma","f",False), "food": ("Comida","f",False),
 "pressure": ("Pressão","f",False), "kiwi": ("Quivi","m",False),
 "ghost": ("Fantasma","m",False), "thorn": ("Espinho","m",False),
 "cocoa": ("Cacau","m",False), "passion": ("Maracujá","m",False),
 "anchor": ("Âncora","f",False), "sulphur": ("Enxofre","m",False),
 "bird": ("Pássaro","m",False), "emperor": ("Imperador","m",False),
 "penguin": ("Pinguim","m",False), "berry": ("Baga","f",False),
 "lily": ("Lírio","m",False), "pad": ("Almofada","f",False),
 "beer": ("Cerveja","f",False), "butterfly": ("Borboleta","f",False),
 "eel": ("Enguia","f",False), "tatami": ("Tatame","m",False),
 "cobblestone": ("Pedregulho","m",False), "fluid": ("Fluido","m",False),
 "flow": ("Fluxo","m",False), "entry": ("Entrada","f",False),
 "warning": ("Aviso","m",False), "potion": ("Poção","f",False),
 "upgrades": ("Melhorias","f",True), "necoium": ("Necônio","m",False),
 "platinum": ("Platina","f",False), "nether": ("Nether","m",False),
 "brickwall": ("Parede de Tijolos","f",False), "brickstairs": ("Escadas de Tijolo","f",True),
 "brickwall2": ("Parede de Tijolos","f",False), "tileblock": ("Bloco de Ladrilho","m",False),
 "floortile": ("Ladrilho de Piso","m",False), "walltile": ("Ladrilho de Parede","m",False),
 "rooftile": ("Telha","f",False), "shingle": ("Telha","f",False),
 "shingles": ("Telhas","f",True), "gutter": ("Calha","f",False),
 "downspout": ("Condutor de Água","m",False), "flashing": ("Rufo","m",False),
 "soffit": ("Sofito","m",False), "fascia": ("Testeira","f",False),
 "balcony": ("Sacada","f",False), "porch": ("Varanda","f",False),
 "veranda": ("Varanda","f",False), "patio": ("Pátio","m",False),
 "pergola": ("Pérgola","f",False), "gazebo": ("Caramanchão","m",False),
 "shed": ("Galpão","m",False), "barn": ("Celeiro","m",False),
 "coop": ("Galinheiro","m",False), "pen": ("Curral","m",False),
 "stable": ("Estábulo","m",False), "hutch": ("Coelheira","f",False),
 "trough": ("Cocho","m",False), "feeder": ("Comedouro","m",False),
 "sign2": ("Placa","f",False), "letter": ("Letra","f",False),
 "letters": ("Letras","f",True), "number": ("Número","m",False),
 "numbers": ("Números","m",True), "label": ("Etiqueta","f",False),
 "board2": ("Quadro","m",False), "chalkboard": ("Lousa","f",False),
 "noteboard": ("Mural de Recados","m",False), "pinboard": ("Mural","m",False),
 "corkboard": ("Mural de Cortiça","m",False), "whiteboard": ("Lousa Branca","f",False),
}
NOUNS.update({k: v for k, v in EXTRA2.items() if k not in NOUNS})

MATERIAL_HINT = {"paper","wood","stone","iron","gold","copper","silver","onyx","jade",
 "topaz","ruby","sapphire","citrine","peridot","aquamarine","ametrine","pearl","coral",
 "prismarine","quartz","amethyst","slate","schist","mud","clay","bamboo","cork","brick"}

# materiais que funcionam como "de X" (substantivo)
MATERIAL_NOUNS = {
 "paper": ("Papel","m"), "wood": ("Madeira","f"), "stone": ("Pedra","f"),
 "iron": ("Ferro","m"), "gold": ("Ouro","m"), "copper": ("Cobre","m"),
 "silver": ("Prata","f"), "onyx": ("Ônix","m"), "jade": ("Jade","m"),
 "topaz": ("Topázio","m"), "ruby": ("Rubi","m"), "sapphire": ("Safira","f"),
 "citrine": ("Citrino","m"), "peridot": ("Peridoto","m"),
 "aquamarine": ("Aquamarina","f"), "ametrine": ("Ametrina","f"),
 "pearl": ("Pérola","f"), "coral": ("Coral","m"), "prismarine": ("Prismarinho","m"),
 "quartz": ("Quartzo","m"), "amethyst": ("Ametista","f"), "slate": ("Ardósia","f"),
 "schist": ("Xisto","m"), "mud": ("Lama","f"), "clay": ("Argila","f"),
 "bamboo": ("Bambu","m"), "cork": ("Cortiça","f"), "snow": ("Neve","f"),
 "ice": ("Gelo","m"), "bone": ("Osso","m"), "leather": ("Couro","m"),
 "wool": ("Lã","f"), "hay": ("Feno","m"), "straw": ("Palha","f"),
 "sand": ("Areia","f"), "sandstone": ("Arenito","m"), "dripstone": ("Estalactite","f"),
 "tuff": ("Tufo","m"), "calcite": ("Calcita","f"), "basalt": ("Basalto","m"),
 "blackstone": ("Pedra-negra","f"), "deepslate": ("Ardósia","f"),
 "andesite": ("Andesito","m"), "diorite": ("Diorito","m"), "granite": ("Granito","m"),
 "marble": ("Mármore","m"), "brass": ("Latão","m"), "zinc": ("Zinco","m"),
 "tin": ("Estanho","m"), "bronze": ("Bronze","m"), "steel": ("Aço","m"),
 "glass": ("Vidro","m"), "crystal": ("Cristal","m"), "obsidian": ("Obsidiana","f"),
 "flint": ("Sílex","m"), "coal": ("Carvão","m"), "redstone": ("Redstone","m"),
 "glowstone": ("Pedra Luminosa","f"), "netherite": ("Netherita","f"),
 "diamond": ("Diamante","m"), "emerald": ("Esmeralda","f"), "lapis": ("Lápis","m"),
}

WOODS = {
 "oak": "Carvalho", "spruce": "Pinheiro", "birch": "Bétula", "jungle": "Madeira da Selva",
 "acacia": "Acácia", "darkoak": "Carvalho Escuro", "mangrove": "Mangue",
 "cherry": "Cerejeira", "bamboo": "Bambu", "crimson": "Carmesim", "warped": "Distorcida",
 "redwood": "Sequoia", "sakura": "Sakura", "maple": "Bordo", "palm": "Palmeira",
 "willow": "Salgueiro", "cedar": "Cedro", "fir": "Abeto", "ash": "Freixo",
 "elm": "Olmo", "beech": "Faia", "poplar": "Álamo", "sequoia": "Sequoia",
}

MULTI = ["light gray","light blue","dark oak","dark oak wood","half-gradient",
 "top-left","top-right","bottom-left","bottom-right","down-left","down-right",
 "up-left","up-right","middle-left","middle-right","half-flag","no detail"]

DROP = {"a","an","the","of","s","and","with","to","no","in","on","for"}

def norm(s):
    s = s.lower()
    for m in sorted(MULTI, key=len, reverse=True):
        s = s.replace(m, m.replace(" ", ""))
    return s.replace("-", "")

def agree(forms, gender, plural):
    idx = (0 if gender == "m" else 1) + (2 if plural else 0)
    return forms[idx]

def tr_phrase(text, gender=None, plural=False, depth=0):
    """Traduz uma frase nominal. gender/plural = do substantivo cabeça externo."""
    if depth > 3: return None
    raw = text.strip()
    if not raw: return ""
    # parenteses
    m = re.match(r"^(.*?)\s*\((.*)\)\s*$", raw)
    tail = ""
    if m:
        inner = tr_phrase(m.group(2), depth=depth+1) or m.group(2)
        raw, tail = m.group(1), f" ({inner})"
    # "X of Y"
    mo = re.search(r"\s+of\s+", raw, re.I)
    if mo:
        left, right = raw[:mo.start()], raw[mo.end():]
        l = tr_phrase(left, depth=depth+1)
        r = tr_phrase(right, depth=depth+1)
        if l and r:
            return f"{l} de {r[0].lower()+r[1:]}{tail}"
    toks = norm(raw).split()
    head_tok, head_len = None, 0
    for n in (3,2,1):
        if len(toks) >= n:
            cand = "".join(toks[-n:])
            if cand in NOUNS:
                head_tok, head_len = cand, n
                break
    mods = toks[:len(toks)-head_len] if head_tok else toks

    if not head_tok:
        for i, t in enumerate(toks):
            if t in NOUNS:
                head_tok, head_len = t, 1
                mods = toks[:i] + toks[i+1:]
                break

    if not head_tok:
        if len(toks) == 1 and toks[0] in MATERIAL_NOUNS:
            mp, mg = MATERIAL_NOUNS[toks[0]]
            return mp + tail
        if len(toks) == 1:
            t = toks[0]
            if t in WOODS: return WOODS[t] + tail
            if t in COLORS: return agree(COLORS[t], gender or "m", plural).capitalize() + tail
            if t in ADJS: return agree(ADJS[t], gender or "m", plural).capitalize() + tail
            if t in NOUNS: return NOUNS[t][0] + tail
        if toks and toks[0] == "no" and len(toks) > 1:
            rest = tr_phrase(" ".join(toks[1:]), depth=depth+1)
            if rest: return "Sem " + rest[0].lower() + rest[1:] + tail
        return None

    hp, hg, hpl = NOUNS[head_tok]
    col, mats, adjs, unknown = [], [], [], []
    for t in mods:
        if t in COLORS: col.append(t)
        elif t in MATERIAL_NOUNS: mats.append(t)
        elif t in WOODS: mats.append(("wood", WOODS[t]))
        elif t in ADJS: adjs.append(t)
        elif t in NOUNS: mats.append(("noun", NOUNS[t][0]))
        elif t in DROP: continue
        else: unknown.append(t)

    parts = [hp]
    if mats:
        seq = []
        for mt in reversed(mats):
            if isinstance(mt, tuple): seq.append(mt[1])
            else:
                mp, mg = MATERIAL_NOUNS[mt]
                seq.append(mp)
        parts.append("de " + " de ".join(seq).lower())
    for c in col:
        parts.append(agree(COLORS[c], hg, hpl))
    def adj_rank(t):
        if t in ("top","bottom","left","right","middle","center","inner","outer","upper","lower",
                 "top-left","top-right","bottom-left","bottom-right","middle-left","middle-right",
                 "up-left","up-right","down-left","down-right","vertical","horizontal","diagonal"):
            return 1
        if t in ("long","longer","short","tall","high","low","large","small","wide","thin","thick"):
            return 2
        return 0
    for a in sorted(adjs, key=adj_rank):
        parts.append(agree(ADJS[a], hg, hpl))
    out = " ".join(p for p in parts if p)
    if unknown:
        out += " [" + " ".join(unknown) + "]"
    return out + tail

def translate_value(v):
    if not isinstance(v, str): return v
    s = v.strip()
    if not s: return v
    if "\n" in s or len(s) > 90:  # texto longo: nao mexe
        return v
    t = tr_phrase(s)
    if not t: return v
    return t[0].upper() + t[1:]

def load_namespace(ns):
    for jar in os.listdir(os.path.join(MC, "mods")):
        if not jar.endswith(".jar"): continue
        try:
            with zipfile.ZipFile(os.path.join(MC, "mods", jar)) as z:
                name = f"assets/{ns}/lang/en_us.json"
                if name in z.namelist():
                    return json.loads(z.read(name).decode("utf-8-sig"))
        except Exception:
            pass
    return None

def run(ns, only_prefixes=None, limit=None):
    en = load_namespace(ns)
    if not en: print(f"[!] {ns}: en_us nao encontrado"); return
    out, unmapped, done = {}, collections.Counter(), 0
    for k, v in en.items():
        if only_prefixes and not any(k.startswith(p) for p in only_prefixes):
            continue
        t = translate_value(v)
        if t != v and "[" not in t:
            out[k] = t; done += 1
        else:
            for w in re.findall(r"\[(.*?)\]", t): unmapped.update(w.split())
    os.makedirs(os.path.join(W, "out"), exist_ok=True)
    with open(os.path.join(W, "out", ns + ".json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1, sort_keys=True)
    print(f"{ns}: total={len(en)} traduzidos={done} ({done*100//max(1,len(en))}%)")
    print("   palavras nao mapeadas:", ", ".join(f"{w}({c})" for w, c in unmapped.most_common(25)) or "-")

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        args = ["fetzisasiandeco"]
    for a in args:
        run(a)

# ---------------- expansao 5 (gaps: railways, umbrellas, mythicupgrades, luphie, lamps)
NOUNS.update({
 "sword": ("Espada","f",False), "swords": ("Espadas","f",True),
 "pickaxe": ("Picareta","f",False), "pickaxes": ("Picaretas","f",True),
 "axe": ("Machado","m",False), "axes": ("Machados","m",True),
 "shovel": ("Pá","f",False), "shovels": ("Pás","f",True),
 "hoe": ("Enxada","f",False), "hoes": ("Enxadas","f",True),
 "chestplate": ("Peitoral","m",False), "leggings": ("Perneiras","f",True),
 "boots": ("Botas","f",True), "armor": ("Armadura","f",False),
 "tool": ("Ferramenta","f",False), "tools": ("Ferramentas","f",True),
 "paint": ("Tinta","f",False), "pitcher": ("Jarra","f",False),
 "pitchers": ("Jarras","f",True), "flywheel": ("Volante","m",False),
 "headstock": ("Cabeçote","m",False), "smokestack": ("Chaminé","f",False),
 "smokestacks": ("Chaminés","f",True), "bogey": ("Bogey","m",False),
 "bogeys": ("Bogeys","m",True), "axles": ("Eixos","m",True),
 "tender": ("Tender","m",False), "handcar": ("Draisiana","f",False),
 "cap": ("Boné","m",False), "conductor": ("Condutor","m",False),
 "conductors": ("Condutores","m",True), "lens": ("Lente","f",False),
 "signal": ("Sinal","m",False), "office": ("Escritório","m",False),
 "planter": ("Jardineira","f",False), "terrarium": ("Terrário","m",False),
 "terrariums": ("Terrários","m",True), "nightstand": ("Criado-mudo","m",False),
 "endtable": ("Mesinha","f",False), "fridge": ("Geladeira","f",False),
 "radio": ("Rádio","m",False), "bicycle": ("Bicicleta","f",False),
 "machine": ("Máquina","f",False), "spool": ("Carretel","m",False),
 "thread": ("Linha","f",False), "cube": ("Cubo","m",False),
 "pyramid": ("Pirâmide","f",False), "wardrobe": ("Guarda-roupa","m",False),
 "poster": ("Pôster","m",False), "papers": ("Papéis","m",True),
 "codex": ("Códice","m",False), "library": ("Biblioteca","f",False),
 "creeper": ("Creeper","m",False), "thing": ("Coisa","f",False),
 "snout": ("Focinho","m",False), "flag": ("Bandeira","f",False),
 "ham": ("Presunto","m",False), "croissant": ("Croissant","m",False),
 "cake": ("Bolo","m",False), "safe": ("Cofre","m",False),
 "cans": ("Latas","f",True), "wine": ("Vinho","m",False),
 "towel": ("Toalha","f",False), "dish": ("Prato","m",False),
 "supplies": ("Suprimentos","m",True), "clutter": ("Tralhas","f",True),
 "stained": ("Vitral","m",False), "glass2": ("Vidro","m",False),
 "mermaid": ("Sereia","f",False), "heart": ("Coração","m",False),
 "seat": ("Assento","m",False), "bee": ("Abelha","f",False),
 "goldfish": ("Peixinho Dourado","m",False), "frog": ("Sapo","m",False),
 "bunny": ("Coelhinho","m",False), "cat": ("Gato","m",False),
 "hamster": ("Hamster","m",False), "fox": ("Raposa","f",False),
 "fountain2": ("Fonte","f",False), "teapot": ("Bule","m",False),
 "teacup": ("Xícara de Chá","f",False), "kettle2": ("Chaleira","f",False),
})

ADJS.update({
 "smoked": F("defumado","defumada"), "enchanted": F("encantado","encantada"),
 "streamlined": F("aerodinâmico","aerodinâmica"), "capped": F("com tampa","com tampa"),
 "bound": F("vinculado","vinculada"), "potted": F("em vaso","em vaso"),
 "trailing": F("rebocado","rebocada"), "invisible": F("invisível","invisível"),
 "manual": F("manual","manual"), "classic": F("clássico","clássica"),
 "retro": F("retrô","retrô"), "cute": F("fofo","fofa"),
 "lovely": F("adorável","adorável"), "gothic": F("gótico","gótica"),
 "steampunk": F("steampunk","steampunk"), "traditional": F("tradicional","tradicional"),
 "angry": F("zangado","zangada"), "worn": F("desgastado","desgastada"),
 "scattered": F("espalhado","espalhada"), "drying": F("secando","secando"),
 "mini2": F("mini","mini"), "filled": F("cheio","cheia"),
 "tieless": F("sem dormente","sem dormente"), "standard": F("padrão","padrão"),
 "normal": F("normal","normal"), "special": F("especial","especial"),
 "quintuple": F("quíntuplo","quíntupla"), "double3": F("duplo","dupla"),
 "medium": F("médio","média"), "large2": F("grande","grande"),
 "empty2": F("vazio","vazia"), "old": F("velho","velha"),
 "aromatic": F("aromático","aromática"), "arromantic": F("arromântico","arromântica"),
 "aromantic": F("arromântico","arromântica"), "asexual": F("assexual","assexual"),
 "bisexual": F("bissexual","bissexual"), "genderfluid": F("gênero-fluido","gênero-fluida"),
 "intersex": F("intersexo","intersexo"), "lesbian": F("lésbico","lésbica"),
 "mlm": F("MLM","MLM"), "pansexual": F("pansexual","pansexual"),
 "transgender": F("transgênero","transgênero"), "pride": F("do Orgulho","do Orgulho"),
 "nonbinary": F("não-binário","não-binária"),
})

MATERIAL_NOUNS.update({
 "gumball": ("Chiclete","m"), "jam": ("Geleia","f"), "tea": ("Chá","m"),
 "cotton": ("Algodão","m"), "candy": ("Doce","m"), "chocolate": ("Chocolate","m"),
 "honey": ("Mel","m"), "mushroom": ("Cogumelo","m"), "flower": ("Flor","f"),
 "spirit": ("Espírito","m"), "phantom": ("Fantasma","m"), "ender": ("Ender","m"),
 "monorail": ("Monotrilho","m"), "rubber": ("Borracha","f"),
})

WOODS.update({
 "aspen": "Álamo", "jacaranda": "Jacarandá", "mahogany": "Mogno", "cypress": "Cipreste",
 "azalea": "Azaleia", "empyreal": "Empíreo", "hellbark": "Casca-do-Inferno",
 "umbran": "Umbrã", "bluebright": "Bluebright", "frostbright": "Frostbright",
 "starlit": "Estrelado", "baobab": "Baobá", "bulbis": "Bulbis", "cika": "Cika",
 "ebony": "Ébano", "embur": "Embur", "ether": "Éter", "holly": "Azevinho",
 "imparius": "Imparius", "lament": "Lamento", "nightshade": "Beladona",
 "eucalyptus": "Eucalipto", "skyris": "Skyris", "sythian": "Sythian",
 "zelkova": "Zelkova", "rubber": "Seringueira", "wisteria": "Glicínia",
 "ashen": "Ashen", "trumpet": "Trombeta", "blackwood": "Pau-negro",
 "chestnut": "Castanheiro", "douglas": "Douglas", "hickory": "Hickory",
 "kapok": "Sumaúma", "rosewood": "Pau-rosa", "sycamore": "Sicômoro",
 "minewood": "Minewood", "sortingwood": "Sortingwood", "timewood": "Timewood",
 "transwood": "Transwood", "twilight": "Twilight", "sugi": "Sugi", "ghaf": "Ghaf",
 "joshua": "Joshua", "palo": "Palo", "verde": "Verde", "edified": "Edificado",
})

MULTI += ["train track", "record player", "palo verde", "book ends", "love seat",
          "end table", "stained glass", "gumball machine", "table lamp"]
NOUNS.update({
 "traintrack": ("Trilho","m",False), "recordplayer": ("Toca-discos","m",False),
 "love seat": ("Sofá","m",False), "loveseat": ("Sofá","m",False),
 "bookends": ("Fins de Livro","m",True), "endtable2": ("Mesinha","f",False),
 "stainedglass": ("Vitral","m",False), "gumballmachine": ("Máquina de Chiclete","f",False),
 "tablelamp": ("Abajur","m",False),
})

NOUNS.update({
 "diagonal": ("Diagonal","f",False), "halfgradient": ("Meio-gradiente","m",False),
 "halfflag": ("Meia-bandeira","f",False), "nightlight": ("Luz Noturna","f",False),
 "glowshroom": ("Cogumelo Brilhante","m",False),
 "coalburner": ("Queimador de Carvão","m",False),
 "oilburner": ("Queimador de Óleo","m",False),
 "woodburner": ("Queimador de Madeira","m",False),
 "schist": ("Xisto","m",False), "guster": ("Guster","m",False),
 "unknown": ("Desconhecido","m",False), "umbrellas": ("Guarda-chuvas","m",True),
 "pattern": ("Estampa","f",False), "patterns": ("Estampas","f",True),
 "cabinet": ("Armário","m",False), "painting": ("Pintura","f",False),
 "switches": ("Interruptores","m",True), "semicolon": ("Ponto e vírgula","m",False),
})
ADJS.update({
 "bottomleft": F("inferior-esquerdo","inferior-esquerda"),
 "bottomright": F("inferior-direito","inferior-direita"),
 "topleft": F("superior-esquerdo","superior-esquerda"),
 "topright": F("superior-direito","superior-direita"),
 "conductor's": F("do condutor","do condutor"),
 "copycat": F("de imitação","de imitação"), "china": F("de porcelana","de porcelana"),
 "tarrey": F("de Tarrey","de Tarrey"), "night": F("noturna","noturna"),
 "create": F("Create","Create"), "styled": F("estilizado","estilizada"),
})
MULTI += ["night light", "night sky", "glow shroom"]

ADJS.update({
 "middleleft": F("central-esquerdo","central-esquerda"),
 "middleright": F("central-direito","central-direita"),
 "upleft": F("para cima à esquerda","para cima à esquerda"),
 "upright": F("para cima à direita","para cima à direita"),
 "downleft": F("para baixo à esquerda","para baixo à esquerda"),
 "downright": F("para baixo à direita","para baixo à direita"),
 "halfgradient": F("meio-gradiente","meio-gradiente"),
 "halfflag": F("meia-bandeira","meia-bandeira"),
 "nonbinary": F("não-binário","não-binária"),
})

NOUNS.update({
 "crossing": ("Cruzamento","m",False), "radial": ("Radial","m",False),
 "interface": ("Interface","f",False), "caboose": ("Furgão","m",False),
 "radiator": ("Radiador","m",False), "yoke": ("Forquilha","f",False),
 "gauge": ("Bitola","f",False), "mono": ("Mono","m",False),
 "collision": ("Colisão","f",False), "coupling": ("Engate","m",False),
 "screwlink": ("Screwlink","m",False), "knuckle": ("Knuckle","m",False),
 "workbench": ("Bancada de Trabalho","f",False),
 "minecart": ("Carrinho de Mina","m",False), "jukebox": ("Jukebox","m",False),
 "buffer": ("Para-choque","m",False), "bzzt": ("Bzzt","m",False),
})
ADJS.update({
 "big": F("grande","grande"), "generic": F("genérico","genérica"),
 "radial": F("radial","radial"), "deco": F("decorativo","decorativa"),
 "portable": F("portátil","portátil"), "mono": F("mono","mono"),
 "comically": F("cômico","cômica"), "scotch": F("Scotch","Scotch"),
 "inverted": F("invertido","invertida"),
})
MATERIAL_NOUNS.update({"fuel": ("Combustível","m")})
WOODS.update({"paloverde": "Palo Verde", "rainboweucalyptus": "Eucalipto Arco-Íris",
              "witchhazel": "Hamamélis"})

MULTI += ["rainbow eucalyptus", "witch hazel", "screwlink coupler", "knuckle coupler",
          "big buffer", "fuel tank", "fuel interface", "caboose smokestack",
          "casing collision", "conductor whistle", "track casing"]

NOUNS.update({
 "wood": ("Madeira","f",False), "moon": ("Lua","f",False), "bush": ("Arbusto","m",False),
 "balm": ("Bálsamo","m",False), "honeycomb": ("Favo de Mel","m",False),
 "string": ("Cordão","m",False), "sandwich": ("Sanduíche","m",False),
 "sandwiches": ("Sanduíches","m",True), "bottles": ("Garrafas","f",True),
 "mugs": ("Canecas","f",True), "sheet": ("Folha","f",False),
 "inventory": ("Inventário","m",False), "cactus": ("Cacto","m",False),
 "set": ("Conjunto","m",False), "birdhouse": ("Casa de Pássaro","f",False),
 "star": ("Estrela","f",False), "flooring": ("Piso","m",False),
 "blueberry": ("Mirtilo","m",False), "muffin": ("Muffin","m",False),
 "cobweb": ("Teia","f",False), "tv": ("TV","f",False), "cafe": ("Café","m",False),
 "tablecloth": ("Toalha de Mesa","f",False), "jackolantern": ("Abóbora de Halloween","f",False),
 "seltzer": ("Seltzer","m",False), "index": ("Índice","m",False),
 "card": ("Ficha","f",False), "row": ("Fileira","f",False),
})
ADJS.update({
 "luphie": F("de Luphie","de Luphie"), "rover's": F("do Rover","do Rover"),
 "floral": F("floral","floral"), "striped": F("listrado","listrada"),
 "havana": F("de Havana","de Havana"), "ancient": F("antigo","antiga"),
 "mango": F("de manga","de manga"), "souther": F("sulista","sulista"),
 "dynasty": F("dinástico","dinástica"), "rubik's": F("de Rubik's","de Rubik's"),
 "hannish": F("de Hannish","de Hannish"), "art": F("de arte","de arte"),
 "general": F("geral","geral"), "tarrey town": F("de Tarrey Town","de Tarrey Town"),
 "destroying": F("destruidor","destruidora"),
})
COLORS.update({"fuschia": F("fúcsia","fúcsia"), "periwinkle": F("pervinca","pervinca"),
               "lavender": F("lavanda","lavanda")})
MULTI += ["tarrey town", "jack o' lantern", "box of paint", "card index"]
MATERIAL_NOUNS.update({"honeycomb": ("Favo de Mel","m"), "mango": ("Manga","f")})
