from bot import Bot
from dotenv import load_dotenv
from os import getenv
from sys import argv

load_dotenv()
run = True
if len(argv) <= 2:
    if "prod" in argv:
        TOKEN = getenv("TOKEN_PROD")
    elif len(argv) == 1 or (len(argv) == 2 and "test" in argv):
        TOKEN = getenv('TOKEN_TEST')
    else:
        run = False
else:
    run = False
if not run:
    print("Une erreur est survenu dans l'apelle de la commande de lancement.\n- Pour lancer une instance d'un bot de test : 'python3 main.py [test]'.\n- Pour lancer l'instance officielle : 'python3 main.py prod'.")
    exit()

if __name__ == '__main__':
    Bot().run(TOKEN)
