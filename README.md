# Bot Descartes

Bot Discord pour le serveur de la prépa MP2I du Lycée Descartes.

## Utilisation

Pour utiliser ce bot, il faut d'abord installer les modules python
nécessaires :

```sh
python3 -m pip install requirements.txt
```

Ensuite, il faut définir plusieurs variables d'environnement (on peut
utiliser un fichier `.env`):
- `TOKEN` est le token qui sera utilisé par le bot
- `GUILD` indique le serveur sur lequel le bot sera activé
- `GUILD_OWNER` indique les propriétaires du serveurs. Ils doivent
  être séparés par un espace.
- `ROLE_FLOP` est le rôle qui sera attribué à celui qui flop (voir
[ratio.py](cogs/ratio.py)
- `RATIO_STORAGE`, `FLOPS_STORAGE`, `TOURNAMENTS_STORAGE` et
`POLLS_STORAGE` indiquent les noms des fichiers utilisés pour stocker
les différentes données. Ils seront placés dans le dossier `storage/`.

Il faut aussi créer deux dossiers différents, au même niveau que
`main.py`: `pictures/` et `storage/`.

## TODO

- [ ] Système de hot unload/reload/deload de modules
- [ ] Migrer le système de JSON vers du SQL
- [ ] Solveur d'équations

## Contribuer

Voir [CONTRIBUTING.md](CONTRIBUTING.md).