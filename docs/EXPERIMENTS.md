# Journal des expériences

| ID | Action | Résultat et preuve | Suite |
|---|---|---|---|
| E01 | Exploit Rock Band Blitz et XeLL depuis USB | Démarrage Linux observé puis SSH vérifié | Chemin de récupération à conserver |
| E02 | Installation sur Hitachi 120 Go autorisée par utilisateur | Racine `/dev/sda1` ext4 et swap 2 Gio vérifiés après démarrage réel | Ne pas rejouer le partitionnement |
| E03 | Mise à jour et installation du bureau | Service pacman terminé `Result=success` | SSH a nécessité un redémarrage local |
| E04 | Xorg fbdev | Échec `no screens found` | Remplacé par modesetting ; permissions initiales Xorg rétablies |
| E05 | Xorg modesetting, rendu logiciel | Capture 1280 × 720 vérifiée | Support 1080p manquant |
| E06 | XTest puis clics sur clavier visuel | Terminal a reçu `xbox360`, puis `123` et Entrée | Manette physique encore à confirmer |
| E07 | Demande XRandR 1920 × 1080 sur None-1 | `cannot find mode 1920x1080` | Développer et valider la programmation vidéo |
| E08 | Inventaire PCI/USB/configuration/dmesg | 12 fonctions PCI et preuves copiées sur Mac | État daté, pas télémétrie continue |
| E09 | Requêtes SMC d’état, hwmon, lecture ANA et registres vidéo ciblés | Réponses cohérentes, températures, 1 024 octets ANA, 15 registres GPU | Rapatriement vérifié en E11 |
| E10 | Lecture mmap PROT_READ de BAR1 du contrôleur flash | SSH et ping perdus, utilisateur confirme écran figé ; aucun dump validé | Sonde bloquée. Cause inconnue ; ne pas relancer. Aucun flash/effacement envoyé |
| E11 | Redémarrage utilisateur et reconnexion SSH | Racine ext4 interne, IceWM et lanceur actifs ; fichiers SMC/ANA/GPU récupérés et SHA-256 concordants | Incident E10 récupéré, cause encore inconnue |
| E12 | Lecture du diagnostic de manette après redémarrage | js0 présent, device_open=true, 4 557 événements | Utilisation visible à confirmer |
| E13 | Inventaire vivant via interfaces noyau standards | SSH, racine, bureau, températures et réseau vérifiés ; `deep-audit/runtime.json` | Aucun accès MMIO/NAND brut |
| E14 | Décodage hors ligne GPU et comparaison ANA/libxenon | Paramètres horizontaux HDMI 720p concordants ; 109/121 entrées ANA hors sentinelles identiques | Total vertical/horloge non mesurés ; six différences expliquées par écritures de constantes |
| E15 | Fonction C réelle xenos_blit dans banc ASan sur Mac | Dépassements heap en 720p/1080p reproduits ; allocation arrondie passe quatre tailles | Correctif candidat, noyau complet non compilé, non déployé |
| E16 | Gestionnaire HTTP XeLL réel avec SFCX simulé sur Mac | Dépassement stack 512/528 reproduit ; correction transmet deux pages intactes | Statut/ECC à traiter ; aucune acquisition réelle de NAND |
| E17 | Revue du pilote audio et des en-têtes Linux 6.18 | API historiques absentes, risques DMA/SMC/IRQ identifiés | Portage et compilation requis avant activation |
| E18 | Provenance du noyau et observation pacman | Paquet linux-xenon 6.18.11-1 ; avertissement trousseau public manquant | Binaire non désassemblé ; trousseau à diagnostiquer avant installation |
| E19 | Vérification finale du journal graphique sur la console | Allocation annoncée 0x384000 = 3 686 400 octets pour 720p ; bureau actif après 22 minutes | Corrobore la taille de F01, sans prouver une corruption ni la cause de E10 |

## Analyse de l’incident E10

La documentation décrit une fenêtre flash en lecture seule, sans ECC. Cela ne garantissait pas que la méthode de lecture large employée fonctionnerait sur cette combinaison matériel/noyau. Le programme a ouvert `resource1` avec O_RDONLY, utilisé PROT_READ, et ne contenait aucune commande d’effacement ou de programmation. Le gel est corrélé à cette lecture ; son mécanisme exact n’a pas été établi.

La sonde est conservée comme texte dans `research/blocked/` afin de pouvoir l’examiner. Elle ne fait pas partie des outils à exécuter. Privilégier une acquisition XeLL ou une interface matérielle documentée avec contrôle des résultats.

## Fiche pour les prochaines expériences

- Question précise et hypothèse.
- État matériel/logiciel et moyen de retour au fonctionnement.
- Action exacte et limites de durée/volume.
- Preuve conservée, hash, résultat observé.
- Incertitudes, effet sur le système, prochaine étape.
