# Journal chronologique

Horodatages en UTC. Les expériences antérieures E01–E38 sont décrites dans EXPERIMENTS avec leurs preuves datées ; ne pas inventer d'horodatage de manipulation lorsqu'il n'a pas été enregistré.

## 2026-10-01 — 21:45:47 — E38

- Objectif : identifier le noyau réellement démarré après sélection utilisateur.
- Action : SSH, état du bureau, udev, journal graphique et interfaces standard.
- Observation : obsidian4, racine interne, Xorg/IceWM actifs, allocation 0x398000, zéro service en échec.
- Résultat : premier démarrage candidat confirmé.
- Interprétation : activation effective du correctif graphique ; pas de preuve de stabilité prolongée ni de cause du gel antérieur.
- Suite : établir une référence de performances sans changer la configuration.

## 2026-10-01 — 21:50:15 — E39

- Objectif : mesurer boot, mémoire, topologie et deux charges userspace courtes.
- Action : collect-baseline.py avec trois échantillons puis collect-boot-detail.py.
- Observation : cible graphique à 34,1 s, 118,5 Mio disponibles au premier relevé, SHA-256 médian 22,553 Mio/s ; deux analyses systemd expirées.
- Résultat : référence conservée et suivi ciblé réussi ; /proc/slabinfo absent, erreur initiale conservée puis interface rendue facultative.
- Interprétation : référence d'un démarrage ; la copie Python ne mesure pas la RAM brute, la cible graphique ne mesure pas le bureau visible.
- Suite : décomposer le démarrage et la mémoire ; comparer toute optimisation future à une méthode équivalente.

## 2026-10-01 — révision d'objectif pendant E39

- Objectif : intégrer le texte de référence actualisé sans perdre l'historique.
- Action : conserver les deux versions détaillées, leurs empreintes et une carte des inconnues.
- Observation : ajout de l'analyse des jeux, de la modernisation, de l'autonomie nocturne et d'une autorisation GitHub publique conditionnée à l'audit.
- Résultat : OBJECTIVE, RESEARCH-MAP et BLOCKED mis à jour.
- Interprétation : la publication n'autorise pas l'envoi des données confidentielles ni de l'ancien historique privé.
- Suite : export public contrôlé, licence et instructions reproductibles. Aucun reboot demandé à l'utilisateur absent.

## 2026-10-01 — 22:01 UTC — E40

- Objectif : publier le projet autorisé sans exporter l'historique privé.
- Action : export textuel à sélection explicite, contrôle des empreintes, recherche de secrets/identifiants, compilation syntaxique des scripts Python, nouveau Git avec identité de projet, audit des objets atteignables puis création/push GitHub.
- Observation : première revue trouve l'adresse MAC dans deux relevés ; ajout d'une règle bloquante et masquage dans les dérivés. Originaux locaux intacts. Attributions amont distinguées des données personnelles de l'opérateur.
- Résultat : 187 fichiers publics, 17 chemins exclus de la sélection initiale ; premier commit f9da49e sans parent. L'API GitHub confirme visibilité publique et arbre identique à l'export contrôlé.
- Interprétation : publication de connaissances/outils et de preuves sélectionnées, pas distribution de firmware ou de jeux. Le scanner de motifs n'est pas une preuve universelle d'absence de secrets.
- Suite : maintenir les deux historiques séparés, actualiser les exports après audit, poursuivre les mesures et l'analyse de formats avec échantillons synthétiques en attendant des supports légitimes accessibles.
