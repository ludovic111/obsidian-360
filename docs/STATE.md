# État courant — 1 octobre 2026

## Récupération vérifiée

SSH est rétabli après le redémarrage physique effectué par l’utilisateur. La racine `/dev/sda1` est montée en ext4 et IceWM ainsi que le lanceur se sont relancés automatiquement. Aucun service systemd actuellement en échec. Preuve : `evidence/2026-10-01/recovery-log.txt`.

L’incident NAND reste non expliqué : la sonde de lecture a figé la machine. Aucune écriture flash envoyée, aucun dump NAND validé. Ne pas rejouer cette sonde.

## Installation déjà vérifiée avant le gel

- Racine ext4 : UUID `e9584d6f-d7ed-40ba-80a2-6834f8d91f31` ; swap 2 Gio.
- Noyau `6.18.11-xenon`, applications PowerPC 32 bits ; hostname `xbox-linux`.
- IceWM 4.0.0, Xorg 21.1.24, Python 3.14.6, Tk 8.6.16.
- Xorg `modesetting`, rendu logiciel, 1280 × 720 ; premier essai `fbdev` abandonné.
- Compte graphique `xbox`, autologin tty1 → startx → IceWM → lanceur Python.
- Manette : `/dev/input/js0` présent après redémarrage, accès ouvert par le lanceur, 4 557 événements reçus au relevé. La réussite des interactions visibles doit encore être confirmée par utilisateur.
- Pas de son : `CONFIG_SOUND` désactivé dans le noyau installé.
- Les paquets étaient entièrement installés avant le gel ; aucune transaction pacman en cours à cet instant.

## Acquisitions rapatriées

`smc-status.json`, `platform-read.log`, `ana-720p.bin`, `ana-720p.json` et `gpu-display-registers.json` ont survécu au redémarrage. Ils sont copiés dans `evidence/2026-10-01/` et leurs SHA-256 ont été comparés à ceux calculés sur la console. Le dump ANA contient exactement 1 024 octets.

## Observation résiduelle

Le journal du nouveau démarrage signale le module facultatif `pkcs8_key_parser` introuvable, demandé par `/usr/lib/modules-load.d/pkcs8.conf`. Aucun service n’est en échec au contrôle final. Aucune modification de noyau n’a été effectuée pour ce point ; à examiner séparément si une fonction cryptographique en dépend.

## Analyse approfondie suivante

Console revérifiée vivante en SSH : noyau `6.18.11-xenon`, racine interne, bureau actif, affichage 1280 × 720. Relevé dans `evidence/2026-10-01/deep-audit/`.

Deux défauts mémoire des sources de référence sont reproduits par AddressSanitizer sur le Mac : framebuffer Xenos sous-dimensionné pour les tuiles en 720p/1080p ; tampon HTTP XeLL de 512 octets pour une lecture NAND brute de 528 octets. Deux correctifs candidats et dix cas de test vérifiés, **aucun correctif déployé sur la Xbox**. Correspondance exacte des binaires installés avec ces sources encore à établir ; aucune cause démontrée du gel E10. Lire `docs/DEEP-AUDIT-2026-10-01.md`.

Le journal vivant confirme néanmoins la même taille d'allocation graphique linéaire : `0x384000` octets en 1280 × 720. Contrôle final : bureau actif, SSH accessible, aucun service en échec, uptime 22 minutes. Preuve : `deep-audit/final-console-check.txt`.

Le pilote audio historique exige un portage des API et une revue DMA/SMC avant activation. Le nouveau relevé réseau indique 100 Mbit/s duplex intégral et aucune erreur RX/TX ; il ne valide pas la stabilité prolongée.

Une interrogation du paquet installé a également signalé un trousseau public pacman absent ; `/etc/pacman.d/gnupg/pubring.gpg` n'existe pas au contrôle. Diagnostic incomplet, aucune modification de la politique de signatures. À résoudre avant une prochaine installation de paquets. Preuve : `deep-audit/package-access.txt`.

## Identification binaire et outillage rétabli

La recette exacte du paquet pointe vers `techflashYT/linux-custom@a293dd19311668900eb1eeb2f6cb01dcac54f330`. Le vmlinux récupéré et l'image de démarrage ont six sections identiques, dont tout `.text` ; leurs empreintes sont vérifiées. Ne plus attribuer sans comparaison le comportement du patch Free60 à ce binaire. Le mode graphique de la branche installée est **constant 1280 × 720**.

Neuf fonctions du noyau ont été désassemblées avec succès dans l'environnement Docker multiarchitecture. Les multiplications de la taille graphique sont confirmées dans le binaire. Un troisième défaut concerne `xenon_ipi_send_mask`, qui perd le masque des destinataires ; le chemin SMP ordinaire utilise une autre fonction correcte. Test du callback réel hors console : 256 combinaisons avant et après correction candidate. Aucun correctif déployé ; aucune cause du gel E10 démontrée. Lire `docs/BINARY-AUDIT-2026-10-01.md`.

`tools/audit-session.py` vérifie les prérequis et conserve les résultats de chaque étape, sans refaire les acquisitions. L'environnement est opérationnel ; une compilation complète PowerPC reste à réaliser.

## Accès et sauvegardes conservés

Configuration d’accès dans `.local/ssh_config`, ignorée. La clé privée reste à son emplacement original hors dépôt. Accès root par clé uniquement.

Les sauvegardes historiques sont des régions du disque interne, pas une sauvegarde de la NAND. Aucune image de flash restaurable confirmée. N’effacer aucune sauvegarde ni la récupération Linux live de la clé USB.
