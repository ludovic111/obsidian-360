# Correctifs candidats — non déployés

Ces deux diffs sont des résultats d'analyse. Ils ne constituent ni un noyau bootable ni un XeLL reconstruit. Aucun n'a été appliqué au système de la Xbox.

- `0001-xenos-pad-tiled-framebuffer.patch` : taille d'allocation arrondie aux macro-tuiles 32 × 32. Base : `xenos.c` ajouté par le patch Linux 6.18-xenon0.30, commit `498bbe1910f707ceba0535276d75a3e6ad0b7df4` du dépôt Free60Project/linux-kernel-xbox360.
- `0002-xell-allocate-physical-page.patch` : tampon dimensionné pour les 528 octets de la page NAND brute. Base : Free60Project/xell-reloaded, commit `a36ed6b7dae940e47e472a20fd14b0616ddc8cef`.

Les dix cas du banc AddressSanitizer passent : les trois erreurs attendues sont reproduites dans les sources originales ; les variantes corrigées et les contrôles sans dépassement terminent normalement. Les interfaces matérielles sont simulées. Le pilote graphique n'est pas compilé comme module Linux complet ; XeLL n'est pas compilé comme chargeur PowerPC complet.

Avant déploiement : retrouver les sources et options exactes des binaires installés, compiler sur la cible PowerPC appropriée, revoir le cycle de vie mémoire et les erreurs, préparer une entrée de démarrage USB distincte et conserver le chemin de récupération actuel. Le défaut HTTP ne valide ni les statuts SFCX, ni les ECC, ni les blocs défectueux.

Ne pas appliquer ces diffs aux archives de preuves. Aucun flash NAND requis pour le test graphique envisagé.
