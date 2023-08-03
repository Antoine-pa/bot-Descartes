# bot-Descartes
conventions de nommage:
    classes:
        PascalCase
    variables / fonction / attributs / méthodes / instances:
        snake_case

    créer une commande:
        choisir le nom de la commande en snake_case et lors de la définission de la fonction asynchrone associée, nommer cette fonction nom_command_command

développement :
    ajout d'un cog:
        (le pluriel est optionnel et dépend de l'humeur xD)
        choisir le nom de la catégorie du cog en snake_case (exemple)
        créer le dossier core/src/bot_descartes/engine/cogs/exemples
        créer le fichier core/src/bot_descartes/engine/cogs/nom_cog/exemple_commands.py
        créer la classe ExempleCog dans exemple_commands.py
        créer le fichier core/src/bot_descartes/engine/cogs/nom_cog/__init__.py et y ajouter from .exemple_commands import ExempleCog
        dans le fichier core/src/bot_descartes/engine/__init__.py, ajouter from .exemple import ExempleCog
        pour finir, dans core/src/bot_descartes/engine/bot.py, dans la méthode setup_hook, instancier le cog et l'ajouter au bot.
    
    Contenu d'un cog:
        un cog doit avoir comme attribut l'instance du bot.
        il doit contenir une commande ou un event

    - pour la création d'un event, le faire dans core/src/bot_descartes/engine/cogs/events/event.py et se reporter sur la doc pour plus de détails
    - pour la création d'une commande, voir les autres cogs qui utilisent les slash commands.
    - pour l'utilisation des components (boutons, menu déroulants, input text), voir dans core/src/bot_descartes/engine/cogs/tournaments/tournaments_commands.py
    - pour la sauvegarde de données, pour le moments, nous utiliserons les json
        - pour utiliser un json, créer un fichier json dans le dossier du cog.
        - ajouter un attribut à core/src/bot_descartes/utils/Tools avec le chemain vers le dossier du cog et du fichier sur le modèle des autres
        - ajouter un attribut data_... au cog dans lequel vous chargerez le fichier avec self.bot.tools.load_json et l'attribut path de Tools
        - pour update des données, changer l'attribut data_... et save le json avec tools.save_json(path, data)
    - pour l'utilisations d'image dans un cog:
        - ajouter un dossier pictures et y mettre les images
        - ajouter le path vers le dossier du cog si ce n'est pas fait et un autre path vers les images dans Tools sur le modèle des autres.
    - pour faire une loop:
        - créer le dossier python de la loop dans core/src/bot_descartes/engine/loops/
        - se reporter aux modèles de core/src/bot_descartes/engine/loops/ratios.py
    - en cas de création d'une commande à risque pour les serveurs, se reporter aux sécurités et aux checks utilisés dans core/src/bot_descartes/engine/admin/administration_commands

pour clonner le dépot:
    - installer un tools git
    - éxécuter dans le dossier où vous voulez télécharger le repo : git clone https://github.com/Antoine-pa/bot-Descartes
    - aller dans repo : cd bot-Descartes
    - créer une nouvelle branche pour ne pas écraser le travail des autres : git branch votre_nom
pour commit (envoyer une sauvegarde de vos modifs):
    - retourner dans le repo
    - changer l'utilisation de la branche : git checkout votre_nom
    - ajouter les fichiers créer au repo : git add *
    - sauvegarder le repo : git commit -am "il faut détailler tout ce que vous avec ajouté/modifié/supprimer ici et il ne faut pas hésiter à bcp écrire"
    - envoyer les modification à github : git push
        /!\ : au moment de push, comme le dépot est privé, il faudra mettre votre identifiant et mot de passe github
              mais github à changer des paramètres de sécurité et pour le mot de passe, il faudra générer des clés de push :
              aller sur github, dans vos settings puis dev settings. aller dans personnal access token puis dans tokens classic.
              faire generate new token puis generate new token classic
              entrez votre mdp github
              séléctionner no expiration et séléctionner toutes les cases (c'est long) en haut dans notes, mettez clé bot Descartes
              faites générer en bas et copiez votre clé en verte (elle commence par ghp)
              mettez là dans un fichier sur votre pc et il faudra l'utiliser à chaque push

        au moment de rentrer votre mot de passe, ouvrez ce fichier avec votre clé, copiez la, retournez sur votre client git et collez là (pour collez, essayez CTRL-V ou CTRL-SHIFT-V)
