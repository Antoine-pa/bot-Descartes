# Bot Descartes

Mettez vous à la racine du projet.

## Installer les dépendances

Pour utiliser ce bot, il faut d'abord installer les modules python
nécessaires :

```sh
python3 -m pip install -r requirements.txt
```

## Mettre en place les variables d'environnement

Ensuite, il faut définir plusieurs variables d'environnement (on peut
utiliser un fichier `.env`).
Pour cela, clonez le fichier template :

```sh
cp ./.env_template/env ./.env
```

Remplacez ou modifiez les variables d'environnement du fichier .env :
- `TOKEN` est le token qui sera utilisé par le bot
- `GUILD` indique l'id du serveur sur lequel le bot sera activé
- `GUILD_OWNER` indique l'id des propriétaires du serveurs. Ils doivent
  être séparés par un espace dans les guillemets.
- `ROLE_FLOP` est le nom du rôle qui sera attribué à celui qui flop (voir
[ratio.py](cogs/ratio.py))
- `RATIO_STORAGE`, `FLOPS_STORAGE`, `TOURNAMENTS_STORAGE` et
`POLLS_STORAGE` indiquent les noms des fichiers utilisés pour stocker
les différentes données. Ils seront placés dans le dossier `storage/`.

les valeurs des variables doivent êtres misent entre guillemets.

## Ajouter les dossier manquants

Il faut aussi créer deux dossiers différents, au même niveau que
`main.py`: `pictures/` et `storage/` :

```sh
mkdir ./pictures ./storage
```

## Lancer le bot

Pour lancer le bot, la commande est la suivante :

```sh
python3 main.py
```