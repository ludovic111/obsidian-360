# OBSIDIAN-360

**Comprendre la machine. Documenter chaque preuve. Construire son avenir sous Linux.**

Laboratoire local d’analyse de la Xbox 360 de Ludovic : matériel, charge de démarrage, pilotes Linux, interface à la manette et expériences reproductibles.

## État vérifié

- ArchPOWER installé et démarré sur le disque interne de 120 Go ; swap de 2 Gio.
- Bureau IceWM personnalisé en 1280 × 720, clavier visuel et moteur de saisie testés.
- Douze fonctions PCI relevées ; GPU identifié par sa signature PCI comme famille Jasper ; six threads CPU visibles.
- **Récupération vérifiée après le gel : SSH rétabli, racine sur disque interne, bureau relancé automatiquement. Les acquisitions SMC/ANA/GPU sont sauvegardées dans ce dépôt.**
- Ni 1080p, ni démarrage indépendant du système Xbox, ni rétro-ingénierie intégrale réalisés.

## Lire et continuer

1. [État courant](docs/STATE.md) et [prochaines étapes](docs/NEXT.md).
2. [Architecture et faits établis](docs/ARCHITECTURE.md).
3. [Incidents et expériences](docs/EXPERIMENTS.md).
4. [Dossier technique détaillé](docs/rapport-initial.txt) et [chronologie historique](docs/historique-installation.txt).
5. [Mesures structurées](evidence/2026-10-01/mesures.json), [contrôleurs PCI](evidence/2026-10-01/peripheriques-pci.csv) et [sources](docs/SOURCES.md).
6. [Analyse approfondie : deux défauts mémoire reproduits, vidéo, audio et NAND](docs/DEEP-AUDIT-2026-10-01.md), [correctifs candidats](research/patches/README.md) et [tests hors console](research/tests/README.md).

## Organisation

- `evidence/` : relevés datés et sommes SHA-256 ; observations ponctuelles, pas état courant garanti.
- `desktop/` : lanceur Python à la manette et configuration vidéo fonctionnelle.
- `tools/` : accès SSH local, collecte d’inventaire et conversion des captures XWD.
- `research/archive/` : scripts historiques d’installation, conservés comme texte non exécutable.
- `research/blocked/` : sonde ayant gelé la console, pour analyse seulement.
- `.local/` : configuration d’accès ignorée par Git ; aucune clé privée versionnée.

## Accès local

```sh
./tools/ssh-xbox 'uptime'
python3 desktop/xbox_desktop.py --self-test
```

Le premier appel nécessite la configuration locale créée sur ce Mac et la clé existante hors dépôt. Il ne recherche pas d’autres machines et conserve la vérification de clé d’hôte. Le test Python ne simule pas une manette physique.

Chaque expérience doit préciser : objectif, état initial, action, preuve, résultat et récupération. Les instructions de travail sont dans [AGENTS.md](AGENTS.md).

Dépôt Git local ; aucun dépôt distant configuré et aucune publication effectuée.
