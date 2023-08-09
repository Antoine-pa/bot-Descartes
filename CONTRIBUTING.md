# Contribuer

## Conventions de nommage

Le projet suit les conventions [PEP8](https://peps.python.org/pep-0008).

En résumé: les classes doivent être nommées en PascalCase et tous les
autres symboles doivent être en snake_case.

La fonction asynchrone correspondant à une commande doit être nommée
`{commande}_command`.

## Ajouter un `Cog`

- Choisir le nom de la catégorie du `Cog` (snake_case).
- Créer le dossier `core/src/bot_descartes/engine/cogs/{nom}`.
- Créer le fichier `core/src/bot_descartes/engine/cogs/{nom}/{nom}_commands.py`.
- Créer la classe `{Nom}Cog` dans `{nom}_commands.py`.
- Créer le fichier `core/src/bot_descartes/engine/cogs/{nom}/__init__.py`.
- Y écrire
```py
from .{nom}_commands import {Nom}Cog
from .{nom} import {Nom}Cog
```
- Instancier le `Cog` et l'ajouter au bot dans
  `core/src/bot_descartes/engine/bot.py` dans la méthode `setup_hook`.

## Contenu d'un `Cog`

Un `Cog` doit avoir pour attribut l'instance du bot, et il doit
contenir une commande ou un évennement.

Il faut créer les évennements dans
`core/src/bot_descartes/engine/cogs/events/event.py` et se réferer à
[la documentation de la bibliothèque discord.py](https://discordpy.readthedocs.io/en/stable/api.html#event-reference)
pour plus de détails.

Pour la création d'une commande, se référer aux `Cog` existants et à
[la documentation](https://discordpy.readthedocs.io/en/stable/ext/commands/cogs.html).

Pour l'utilisation de composants Discord (boutons, menus déroulants,
entrée textuelle), voir l'exemple dans
`core/src/bot_descartes/engine/cogs/tournaments/tournaments_commands.py`
et se référer à
[la documentation](https://docs.discord4py.dev/en/latest/).

Ajouter un dossier `pictures` si on veut stocker des images.

Ajouter le chemin du dossier du `Cog` en attribut de la classe `Tools`
de `core/src/bot_descartes/engine/utils/tools.py`

Y ajouter un chemin pour les images si applicable.

Pour créer une boucle, il faut
- Créer le fichier de la boucle dans
`core/src/bot_descartes/engine/loops/`.
- Se référer à `core/src/bot_descartes/engine/loops/ratios.py`

Lors de la création d'une commande "à risques" pour les serveurs, se
référer aux vérifications des commandes d'administration
(`core/src/bot_descartes/engine/admin/administration_commands.py`).

## Sauvegarde de données

La sauvegarde des données utilise temporairement le format JSON.

Pour utiliser un fichier JSON:
- Créer le fichier dans le dossier du `Cog` qui l'utilisera.
- Ajouter un attribut dans `core/src/bot_descartes/utils/Tools` avec
le chemin vers le dossier du `Cog` (voir les attributs existants pour
exemple).
- Ajouter un atribut `data_{fichier}` au `Cog` utilisant le fichier et
y affecter le retour de
```py
self.bot.tools.load_json(self.bot.tools.path_{Cog}+"{fichier}.json")
```

## Contribution par git

- Installez [git](https://git-scm.com)
- Créez vous un compte sur [GitHub](https://github.com)
  pour contribuer.
- Forkez [le dépôt](https://github.com/Antoine-pa/bot-Descartes) vers
  votre compte.
- Clonez votre dépôt vers votre machine.
```
git clone https://github.com/{votre_compte}/bot-Descartes
```
- Créez une nouvelle branche pour votre modification.
```
git branch {branche}
```
- Allez sur cette branche.
```
git checkout {branche}
```
- Faites vos modifications, et ajoutez vos changements à Git.
```
git add {fichier0} {fichier1}
# ou si vous voulez ajouter tout le dossier courant
git add .
```
- Commit vos changements. Votre message de commit doit suivre
  [la commit style](https://commit.style).
```
git commit -m "{message}"
# ou, si vous avez plusieurs ligne dans votre message
git commit
```
- Envoyez vos changements vers votre GitHub.
```
git push -u origin {branche}
```
- Créez une [pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request)
depuis votre dépôt vers le dépôt original.
- Attendez que votre pull request soit acceptée. Il se peut qu'on vous
  demande des changements.