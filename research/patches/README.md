# Correctifs candidats — non déployés

Ces quatre diffs sont des résultats d'analyse. Les correctifs Linux 0001, 0003 et 0004 ont été compilés ensemble dans un vmlinux candidat ; celui-ci n'a pas démarré sur la console. XeLL n'a pas été reconstruit. Aucun correctif n'a été appliqué au système de la Xbox.

- `0001-xenos-pad-tiled-framebuffer.patch` : taille d'allocation arrondie aux macro-tuiles 32 × 32. Base : `xenos.c` ajouté par le patch Linux 6.18-xenon0.30, commit `498bbe1910f707ceba0535276d75a3e6ad0b7df4` du dépôt Free60Project/linux-kernel-xbox360.
- `0002-xell-allocate-physical-page.patch` : tampon dimensionné pour les 528 octets de la page NAND brute. Base : Free60Project/xell-reloaded, commit `a36ed6b7dae940e47e472a20fd14b0616ddc8cef`.
- `0003-xenon-preserve-ipi-target-mask.patch` : corrige l'ordre masque/décalage dans le callback IPI. Base : techflashYT/linux-custom, commit `a293dd19311668900eb1eeb2f6cb01dcac54f330`. 256 combinaisons testées par variante avec MMIO simulée ; le chemin SMP ordinaire appelle une autre fonction.
- `0004-xenon-bound-smc-reply-cache.patch` : borne la recherche dans le cache SMC à ses treize entrées. Même base linux-custom ; quatre cas ASan vérifient l'original et le candidat, sans messages envoyés au matériel.

Les dix cas du premier banc AddressSanitizer passent : les trois erreurs attendues sont reproduites dans les sources originales ; les variantes corrigées et les contrôles sans dépassement terminent normalement. Les interfaces matérielles sont simulées. Le pilote graphique a ensuite été compilé dans le vmlinux candidat complet avec LLVM 16 ; XeLL n'est pas compilé comme chargeur PowerPC complet. Les preuves de cette compilation sont dans `evidence/2026-10-01/kernel-build/` ; un avertissement du pilote LED reste à corriger.

Avant déploiement : terminer la revue des erreurs et du cycle de vie mémoire, produire et vérifier les modules et le conditionnement de démarrage, préparer une entrée USB distincte et conserver le chemin de récupération actuel. La source du noyau installé est identifiée ; le candidat LLVM ne reproduit pas bit à bit son build GCC. Le défaut HTTP ne valide ni les statuts SFCX, ni les ECC, ni les blocs défectueux.

Ne pas appliquer ces diffs aux archives de preuves. Aucun flash NAND requis pour le test graphique envisagé.
