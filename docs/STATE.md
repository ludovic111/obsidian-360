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

## Accès et sauvegardes

Configuration d’accès dans `.local/ssh_config`, ignorée. La clé privée reste à son emplacement original hors dépôt. Accès root par clé uniquement.

Les sauvegardes historiques sont des régions du disque interne, pas une sauvegarde de la NAND. Aucune image de flash restaurable confirmée. N’effacer aucune sauvegarde ni la récupération Linux live de la clé USB.
