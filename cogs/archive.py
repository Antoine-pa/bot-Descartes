from discord.ext.commands import Cog, Bot
from discord import app_commands, Interaction, Colour
from config import PATHS
from dotenv import load_dotenv
from os import getenv
from utils import write_json, read_json, date_to_timestamp, build_embed
from time import time

load_dotenv()

path_archives = f'{PATHS["storage"]}/{getenv("ARCHIVES_STORAGE")}'

class ArchiveCog(Cog):
    def __init__(self, bot: Bot):
        super().__init__()
        self.bot = bot
        self.data_archives = read_json(path_archives)
        self.levels = ["terminale", "mp2i", "mpi"]
        change_data = False
        for level in self.levels:
            if level not in self.data_archives:
                change_data = True
                self.data_archives[level] = {}
        if change_data:
            write_json(path_archives, self.data_archives)
    
    archive_group = app_commands.Group(name="archive", description="group archive commands")
    archive_get_group = app_commands.Group(name="get", description="group archive get commands", parent=archive_group)
    
    file_archive_group = app_commands.Group(name="file_archive", description="group file archive commands")
    file_archive_change_group = app_commands.Group(name="change", description="group file archive change commands", parent=file_archive_group)
    file_archive_delete_group = app_commands.Group(name="delete", description="group file archive delete commands", parent=file_archive_group)
    file_archive_insert_group = app_commands.Group(name="insert", description="group file archive insert commands", parent=file_archive_group)
    file_archive_add_group = app_commands.Group(name="add", description="group file archive add commands", parent=file_archive_group)
    
    learn_group = app_commands.Group(name="learn", description="group learn commands")
    learn_archive_group = app_commands.Group(name="archive", description="group learn archive commands", parent=learn_group)
    
    subject_group = app_commands.Group(name="subject", description="group subject commands")

    @archive_get_group.command(name='by_id', description='Renvoit une archive.')
    async def archive_get_by_id_command(self, interaction: Interaction, id_archive: int):
        await interaction.response.send_message("coming soon...")
    @archive_get_group.command(name='by_name', description='Renvoit une archive.')
    async def archive_get_by_name_command(self, interaction: Interaction, level: str, subject: str, chapter: int):
        await interaction.response.send_message("coming soon...")

    @archive_get_group.command(name="id", description="Renvoit l'id d'une archive.")
    async def archive_get_id(self, interaction: Interaction, level: str, subject: str, chapter: int):
        await interaction.response.send_message("coming soon...")



    @file_archive_change_group.command(name='by_id_file', description="Change un fichier d'une archive.")
    async def change_file_command(self, interaction: Interaction, id_file: int):
        await interaction.response.send_message("coming soon...")
    @file_archive_change_group.command(name='by_id_archive', description="Change un fichier d'une archive.")
    async def change_file_command(self, interaction: Interaction, id_archive: int, position: int):
        await interaction.response.send_message("coming soon...")
    @file_archive_change_group.command(name='by_name', description="Change un fichier d'une archive.")
    async def change_file_command(self, interaction: Interaction, level: str, subject: str, chapter: int, position: int):
        await interaction.response.send_message("coming soon...")

    @file_archive_delete_group.command(name='by_id_file', description="Supprime un fichier d'une archive.")
    async def delete_file_command(self, interaction: Interaction, id_file: int):
        await interaction.response.send_message("coming soon...")
    @file_archive_delete_group.command(name='by_id_archive', description="Supprime un fichier d'une archive.")
    async def delete_file_command(self, interaction: Interaction, id_archive: int, position: int):
        await interaction.response.send_message("coming soon...")
    @file_archive_delete_group.command(name='by_name', description="Supprime un fichier d'une archive")
    async def delete_file_command(self, interaction: Interaction, level: str, subject: str, chapter: int, position: int):
        await interaction.response.send_message("coming soon...")

    @file_archive_insert_group.command(name='by_id_file', description="Insert un fichier dans une archive.")
    async def insert_file_command(self, interaction: Interaction, id_file: int):
        await interaction.response.send_message("coming soon...")
    @file_archive_insert_group.command(name='by_id_archive', description="Insert un fichier dans une archive.")
    async def insert_file_command(self, interaction: Interaction, id_archive: int, position: int):
        await interaction.response.send_message("coming soon...")
    @file_archive_insert_group.command(name='by_name', description="Insert un fichier dans une archive.")
    async def insert_file_command(self, interaction: Interaction, level: str, subject: str, chapter: int, position: int):
        await interaction.response.send_message("coming soon...")

    @file_archive_add_group.command(name='by_id_archive', description="Ajoute un fichier dans une archive.")
    async def add_file_command(self, interaction: Interaction, id_archive: int):
        await interaction.response.send_message("coming soon...")
    @file_archive_add_group.command(name='by_name', description="Ajoute un fichier dans une archive.")
    async def add_file_command(self, interaction: Interaction, level: str, subject: str, chapter: int):
        await interaction.response.send_message("coming soon...")



    @learn_archive_group.command(name='start', description="Lance l'apprentissage d'une notion.")
    async def learn_archive_start_command(self, interaction: Interaction, id_archive: int):
        await interaction.response.send_message("coming soon...")
    @learn_archive_group.command(name='stop', description="Arrète l'apprentissage d'une notion.")
    async def learn_archive_stop_command(self, interaction: Interaction, id_archive: int):
        await interaction.response.send_message("coming soon...")

    @app_commands.command(name='archives', description="Liste les archives d'une matière.")
    async def chapters_command(self, interaction: Interaction, level: str, subject: str):
        await interaction.response.send_message("coming soon...")



    def get_level(self, level: str) -> str:
        if level.lower() in ("terminale", "terminal", "term", "tale", "tal"):
            return "terminale"
        if level.lower() in ("mp2i"):
            return "mp2i"
        if level.lower() in ("mpi"):
            return "mpi"

    async def name_level_error(self, interaction: Interaction, level) -> None:
        await interaction.response.send_message(f"{level} n'est pas une classe.\nRéférez vous à la commande /levels pour avoir la liste.")
    
    async def name_subject_error(self, interaction: Interaction, level, subject) -> None:
        await interaction.response.send_message(f"{subject} n'est pas une matière de la classe {levem}.\nRéférez-vous à la commande /subjects pour avoir la liste.")

    async def check_args(self, interaction: Interaction, level: str, subject: str=None, chapter: int=None):
        if level not in self.data_archives:
            await self.name_level_error(interaction, level)
            return False
        if subject is not None and subject not in self.data_archives[level]:
            await self.name_subject_error(interaction, level, subject)
            return False
        return True


    #FINISH :
    @app_commands.command(name='levels', description='Liste les classes.')
    async def levels_command(self, interaction: Interaction):
        embed = build_embed(title="Classes :", color=Colour.blue(), message="- "+"\n- ".join(self.levels))
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='subjects', description="Liste les matières d'une classe.")
    async def subjects_command(self, interaction: Interaction, level: str):
        level = self.get_level(level)
        check = await self.check_args(interaction, level)
        if not check:
            return
        if self.data_archives[level] == {}:
            message = "Pas de matière.\nPour en ajouter une utilisez la commande /subject add."
        else:
            message = "- "+"\n- ".join(self.data_archives[level].keys())
        embed = build_embed(title=f"Matière de la classe de {level} :", color=Colour.blue(), message=message)
        await interaction.response.send_message(embed=embed)

    @subject_group.command(name="add", description="Ajoute une matière à la classe.")
    async def subject_add_command(self, interaction: Interaction, level: str, name: str):
        level = self.get_level(level)
        check = await self.check_args(interaction, level)
        if not check:
            return
        self.data_archives[level][name] = []
        write_json(path_archives, self.data_archives)
        embed = build_embed(title="Nouvelle matère :", color=Colour.blue(), message=f"La matère {name} a été ajoutée en {level}.")
        await interaction.response.send_message(embed=embed)

    @subject_group.command(name="rename", description="Change le nom d'une matière à la classe.")
    async def subject_rename_command(self, interaction: Interaction, level: str, subject: str, name: str):
        level = self.get_level(level)
        check = await self.check_args(interaction, level, subject)
        if not check:
            return
        self.data_archives[level][name] = self.data_archives[level][subject]
        del self.data_archives[level][subject]
        write_json(path_archives, self.data_archives)
        embed = build_embed(title="Changement d'un nom de matière :", color=Colour.blue(), message=f"La matière {subject} a été renommée par {name}.")
        await interaction.response.send_message(embed = embed)

    @subject_group.command(name="delete", description="Supprime une matière à la classe.")
    async def subject_delete_command(self, interaction: Interaction, level: str, subject: str):
        level = self.get_level(level)
        check = await self.check_args(interaction, level, subject)
        if not check:
            return
        del self.data_archives[level][subject]
        write_json(path_archives, self.data_archives)
        embed = build_embed(title="Supression d'une matière :", color=Colour.blue(), message=f"La matière {subject} a été suprimée.")
        await interaction.response.send_message(embed=embed)


    @archive_group.command(name='create', description='Crée une archive.')
    async def archive_create_command(self, interaction: Interaction, date: str, level: str, subject: str, name: str):
        level = self.get_level(level)
        check = await self.check_args(interaction, level, subject)
        if not check:
            return
        timestamp = date_to_timestamp(date)
        id_archive = len(self.data_archives[level][subject])
        print("A faire dans archive create : ajouter les fichiers")
        self.data_archives[level][subject].append({"id": id_archive, "name": name, "timestamp": timestamp, "workers": [interaction.user.id], "files": []})
        write_json(path_archives, self.data_archives)
        
        embed = build_embed(title="Création d'une archive :", color=Colour.blue(), message=f"L'archive {name} de {subject} en {level} a été créé.")
        await interaction.response.send_message(embed=embed)