import discord
from discord.ext.commands import Cog, Bot
from discord.ext import tasks
import asyncio
from discord.ui import View, Button, button
from discord import app_commands, Interaction, Colour, Attachment, ButtonStyle, Message, File
from config import PATHS, PICTURES_ETXTENSIONS, DAYS
from dotenv import load_dotenv
from os import getenv, rename
from utils import write_json, read_json, date_to_timestamp, build_embed, get_file_archive_name, date
from time import time
import datetime
timezone = datetime.timezone.utc
timeloop = [datetime.time(hour=19-2, minute=0, second=0, tzinfo=timezone)]
load_dotenv()

path_archives = f'{PATHS["storage"]}/{getenv("ARCHIVES_STORAGE")}'

class ArchiveView(View):
    def __init__(self, bot: Bot, message: Message, level: str, subject: str, name: str, archive: dict):
        super().__init__(timeout=3600)
        self.bot = bot
        self.index = 0
        self.message = message
        self.level = level
        self.subject = subject
        self.name = name
        self.archive = archive

    async def edit_message(self):
        embed = self.message.embeds[0]
        filename = get_file_archive_name(self.level, self.subject, self.name, self.archive, self.index)
        file = File(fp=f"{PATHS['pictures']}/{filename}", filename=filename)
        if filename.split(".")[-1] in PICTURES_ETXTENSIONS:
            embed.set_image(url=f"attachment://{filename}")
        else:
            embed = build_embed(title=embed.title, color=embed.color, message=embed.description)
        embed.set_footer(text=f"{self.index}/{len(self.archive['files'])-1}")
        await self.message.edit(embed = embed, attachments=[file])

    @discord.ui.button(label="before", style=ButtonStyle.green)
    async def before_button(self, interaction: Interaction, button: Button):
        if self.index == 0:
            self.index = len(self.archive["files"])-1
        else:
            self.index -= 1
        await interaction.response.defer()
        await self.edit_message()
        
    @discord.ui.button(label="after", style=ButtonStyle.green)
    async def after_button(self, interaction: Interaction, button: Button):
        if self.index == len(self.archive["files"])-1:
            self.index = 0
        else:
            self.index += 1
        await interaction.response.defer()
        await self.edit_message()
    
    @discord.ui.button(label="delete", style=ButtonStyle.danger)
    async def delete_button(self, interaction: Interaction, button: Button):
        self.stop()
        await self.message.edit(view=None)

    @discord.ui.button(label="infos", style=ButtonStyle.blurple)
    async def infos_button(self, interaction: Interaction, button: Button):
        self.stop()
        message = f"""
- Chemin de l'archive : {self.level} - {self.subject} - {self.name}
- Date de création : {date(self.archive['timestamp'])}
- Auteur : {await self.bot.fetch_user(self.archive['author'])}
- Nombre de travailleurs : {len(self.archive['workers'])}
- Nombre de fichiers : {len(self.archive['files'])}
        """
        embed = build_embed(title=f"Informations sur l'archive {self.name} :", color=Colour.green(), message=message)
        for i in range(min(len(self.archive["files"]), 25)):
            file = self.archive['files'][i]
            filename = get_file_archive_name(self.level, self.subject, self.name, self.archive, i)
            embed.add_field(name=f"Fichier {i} :", value=f"- auteur : {file['author_name']}\n- modification : {date(file['edit_date'])}\n- nom complet : {filename}")
        await self.message.edit(embed=embed, attachments = [], view=None)
        await interaction.response.defer()

    async def on_timeout(self):
        self.stop()
        await self.message.edit(view=None)

class ArchiveCog(Cog):
    def __init__(self, bot: Bot):
        super().__init__()
        self.bot = bot
        self.data_archives = read_json(path_archives)
        self.levels = ["terminale", "mp2i", "mpi"]
        self.workers = {}
        change_data = False
        for level in self.levels:
            if level not in self.data_archives:
                change_data = True
                self.data_archives[level] = {}
        if change_data:
            write_json(path_archives, self.data_archives)
    
    get_group = app_commands.Group(name="get", description="group get commands")
    delete_group = app_commands.Group(name="delete", description="group delete commands")
    purge_group = app_commands.Group(name="purge", description="group purge commands")
    rename_group = app_commands.Group(name="rename", description="group rename commands")
    add_group = app_commands.Group(name="add", description="group add commands")
    insert_group = app_commands.Group(name="insert", description="group insert commands")
    change_group = app_commands.Group(name="change", description="group change commands")
    start_group = app_commands.Group(name="start", description="group start commands")
    stop_group = app_commands.Group(name="stop", description="group stop commands")
    start_learn_group = app_commands.Group(name="learn", description="group start learn commands", parent=start_group)
    stop_learn_group = app_commands.Group(name="learn", description="group stop learn commands", parent=stop_group)


    def change_index_filename(self, level: str, subject: str, name: str, index: int, value: int) -> tuple:
        filename = get_file_archive_name(level, subject, name, self.data_archives[level][subject][name], index)
        new_name = "_".join(filename.split("_")[:-1]) + "_" + str(index+value) + "." + filename.split(".")[1]
        return (filename, new_name)

    def get_level(self, level: str) -> str:
        if level.lower() in ("terminale", "terminal", "term", "tale", "tal"):
            return "terminale"
        if level.lower() in ("mp2i"):
            return "mp2i"
        if level.lower() in ("mpi"):
            return "mpi"
    
    def dict_file(self, interaction: Interaction, filename: str) -> dict:
        return {"author_id": interaction.user.id, "author_name": str(interaction.user), "edit_date": time(), "type": filename.split(".")[-1]}

    async def name_level_error(self, interaction: Interaction, level: str) -> None:
        embed = build_embed(title="Erreur :", color=Colour.red(), message=f"{level} n'est pas une classe.\nRéférez vous à la commande /levels pour avoir la liste des classes.")
        await interaction.response.send_message(embed=embed)
    
    async def name_subject_error(self, interaction: Interaction, level: str, subject: str) -> None:
        embed = build_embed(title="Erreur :", color=Colour.red(), message=f"{subject} n'est pas une matière de la classe {level}.\nRéférez-vous à la commande /subjects pour avoir la liste des matières.")
        await interaction.response.send_message(embed=embed)
    
    async def name_archive_error(self, interaction, level: str, subject: str, archive: str) -> None:
        embed = build_embed(title="Erreur :", color=Colour.red(), message=f"{archive} n'est pas une archive de la matière {subject} de la classe {level}.\n Référez-vous à la commande /archives pour avoir la liste des archives.")
        await interaction.response.send_message(embed=embed)
    
    async def index_error(self, interaction: Interaction, level: str, subject: str, archive: str, index: int) -> None:
        embed = build_embed(title="Erreur :", color=Colour.red(), message=f"L'index {index} ne correspond pas à un index d'un fichier de l'archive {archive} de la matière {subject} de la classe {level}.\nRéférez-vous aux indices des fichiers de la commande /get archive")
        await interaction.response.send_message(embed=embed)

    async def check_args(self, interaction: Interaction, level: str, subject: str=None, archive: str=None, index: int=None):
        if level not in self.data_archives:
            await self.name_level_error(interaction, level)
            return False
        if subject is not None and subject not in self.data_archives[level]:
            await self.name_subject_error(interaction, level, subject)
            return False
        if archive is not None and archive not in self.data_archives[level][subject]:
            await self.name_archive_error(interaction, level, subject, archive)
            return False
        if index is not None and not (0 <= index <= len(self.data_archives[level][subject][archive]["files"])-1):
            await self.index_error(interaction, level, subject, archive, index)
            return False
        return True

    def embed_archive(self, level, subject, name, archive) -> tuple:
        if archive["files"] == []:
            message = "Aucun fichier dans cette archive.\nPour en ajouter utiliser /file_archive add"
            embed = build_embed(title=name, color=Colour.blue(), message=message)
            return (embed, None)
        message = f"- date de création : {date(archive['timestamp'])}\n**Fichiers :**\n"
        i = 0
        for file in archive["files"]:
            message += f"- {i} : {get_file_archive_name(level, subject, name, archive, i)}\n"
            i+=1
        filename = get_file_archive_name(level, subject, name, archive, 0)
        file = File(fp=f"{PATHS['pictures']}/{filename}", filename=filename)
        embed = build_embed(title=name, color=Colour.blue(), message=message, footer=f"0/{len(archive['files'])-1}")
        if filename.split(".")[-1] in PICTURES_ETXTENSIONS:
            embed.set_image(url=f"attachment://{filename}")
        return embed, file

    #COMMANDS :
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

    @add_group.command(name="subject", description="Ajoute une matière à la classe.")
    async def add_subject_command(self, interaction: Interaction, level: str, name: str):
        level = self.get_level(level)
        check = await self.check_args(interaction, level)
        if not check:
            return
        self.data_archives[level][name] = {}
        write_json(path_archives, self.data_archives)
        embed = build_embed(title="Nouvelle matère :", color=Colour.blue(), message=f"La matère {name} a été ajoutée en {level}.")
        await interaction.response.send_message(embed=embed)

    @rename_group.command(name="subject", description="Change le nom d'une matière à la classe.")
    async def rename_subject_command(self, interaction: Interaction, level: str, subject: str, name: str):
        level = self.get_level(level)
        check = await self.check_args(interaction, level, subject)
        if not check:
            return
        self.data_archives[level][name] = self.data_archives[level][subject]
        del self.data_archives[level][subject]
        write_json(path_archives, self.data_archives)
        embed = build_embed(title="Changement d'un nom de matière :", color=Colour.blue(), message=f"La matière {subject} a été renommée par {name}.")
        await interaction.response.send_message(embed = embed)

    @delete_group.command(name="subject", description="Supprime une matière à la classe.")
    async def delete_subject_command(self, interaction: Interaction, level: str, subject: str):
        level = self.get_level(level)
        check = await self.check_args(interaction, level, subject)
        if not check:
            return
        del self.data_archives[level][subject]
        write_json(path_archives, self.data_archives)
        embed = build_embed(title="Supression d'une matière :", color=Colour.blue(), message=f"La matière {subject} a été suprimée.")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='archives', description="Liste les archives d'une matière.")
    async def archives_command(self, interaction: Interaction, level: str, subject: str):
        level = self.get_level(level)
        check = await self.check_args(interaction, level, subject)
        if not check:
            return
        if len(self.data_archives[level][subject]) == 0:
            message = "Pas d'archive.\nPour en ajouter une utilisez la commande /archive create."
        else:
            message = ""
            for archive in self.data_archives[level][subject].items():
                message += f"- {archive[0]} ({len(archive[1]['files'])} fichiers)\n"
        embed = build_embed(title=f"Archive de {subject} de {level} :", color=Colour.blue(), message=message)
        await interaction.response.send_message(embed=embed)

    @add_group.command(name='archive', description='Crée une archive.')
    async def add_archive_command(self, interaction: Interaction, date: str, level: str, subject: str, name: str, zip_file: Attachment):
        level = self.get_level(level)
        check = await self.check_args(interaction, level, subject)
        if not check:
            return
        timestamp = date_to_timestamp(date)
        print("A faire dans add archive : ajouter les fichiers")
        if name in self.data_archives[level][subject]:
            await interaction.response.send_message(f"L'archive {name} existe déjà.")
            return
        self.data_archives[level][subject][name] = {"author": interaction.user.id, "timestamp": timestamp, "workers": [interaction.user.id], "files": []}
        write_json(path_archives, self.data_archives)
        
        embed = build_embed(title="Création d'une archive :", color=Colour.blue(), message=f"L'archive {name} de {subject} en {level} a été créé.")
        await interaction.response.send_message(embed=embed)

    @get_group.command(name='archive', description='Renvoit une archive.')
    async def get_archive_command(self, interaction: Interaction, level: str, subject: str, archive: str):
        level = self.get_level(level)
        check = await self.check_args(interaction, level, subject, archive)
        if not check:
            return
        arch = self.data_archives[level][subject][archive]
        channel = interaction.channel
        await interaction.response.defer()
        embed, file = self.embed_archive(level, subject, archive, arch)
        message = await channel.send(embed=embed, file=file)
        if len(arch["files"]) == 1:
            return
        await message.edit(view = ArchiveView(self.bot, message, level, subject, archive, arch))
        

    @start_learn_group.command(name='archive', description="Lance l'apprentissage d'une notion.")
    async def start_learn_archive_command(self, interaction: Interaction, level: str, subject: str, archive: str):
        level = self.get_level(level)
        check = await self.check_args(interaction, level, subject, archive)
        if not check:
            return
        if interaction.user.id in self.data_archives[level][subject][archive]["workers"]:
            await interaction.response.defer()
            return
        self.data_archives[level][subject][archive]["workers"].append(interaction.user.id)
        write_json(path_archives, self.data_archives)
        embed = build_embed(title=f"Archive {archive}", color=Colour.blue(), message="Vous venez d'être ajouté à la la liste des travailleurs de cette archive.")
        await interaction.response.send_message(embed = embed)

    @stop_learn_group.command(name='archive', description="Arrète l'apprentissage d'une notion.")
    async def stop_learn_archive_command(self, interaction: Interaction, level: str, subject: str, archive: str):
        level = self.get_level(level)
        check = await self.check_args(interaction, level, subject, archive)
        if not check:
            return
        if interaction.user.id not in self.data_archives[level][subject][archive]["workers"]:
            await interaction.response.defer()
            return
        self.data_archives[level][subject][archive]["workers"].remove(interaction.user.id)
        write_json(path_archives, self.data_archives)
        embed = build_embed(title=f"Archive {archive}", color=Colour.blue(), message="Vous venez d'être supprimé de la liste des travailleurs de cette archive.")
        await interaction.response.send_message(embed = embed)

    @delete_group.command(name='file', description="Supprime un fichier d'une archive")
    async def delete_file_command(self, interaction: Interaction, level: str, subject: str, archive: str, index: int):
        level = self.get_level(level)
        check = await self.check_args(interaction, level, subject, archive, index)
        if not check:
            return
        filename = get_file_archive_name(level, subject, archive, self.data_archives[level][subject][archive], index)
        new_name = "_old.".join(filename.split("."))
        rename(PATHS["pictures"]+"/"+filename, PATHS["pictures"]+"/"+new_name)
        i = index+1
        for file in self.data_archives[level][subject][archive]["files"][index+1:]:
            filename, new_name = self.change_index_filename(level, subject, archive, i, -1)
            rename(PATHS["pictures"]+"/"+filename, PATHS["pictures"]+"/"+new_name)
            i+=1
        del self.data_archives[level][subject][archive]["files"][index]
        write_json(path_archives, self.data_archives)
        embed = build_embed(title=f"Archive {archive} :", color=Colour.blue(), message="Fichier supprimé.")
        await interaction.response.send_message(embed=embed)

    @add_group.command(name='file', description="Ajoute un fichier dans une archive.")
    async def add_file_command(self, interaction: Interaction, level: str, subject: str, archive: str, file1: Attachment, file2: Attachment=None, file3: Attachment=None, file4: Attachment=None, file5: Attachment=None):
        level = self.get_level(level)
        check = await self.check_args(interaction, level, subject, archive)
        if not check:
            return
        i = 0
        for file in [file1, file2, file3, file4, file5]:
            if file is not None:
                i += 1
                arch = self.data_archives[level][subject][archive]
                arch["files"].append(self.dict_file(interaction, file.filename))
                await file.save(PATHS["pictures"]+"/"+get_file_archive_name(level, subject, archive, arch, len(arch["files"])-1))
        write_json(path_archives, self.data_archives)
        if i > 1:
            message = "Fichiers ajoutés."
        else:
            message = "Fichier ajouté."
        embed = build_embed(title=f"Archive {archive} :", color=Colour.blue(), message=message)
        await interaction.response.send_message(embed = embed)

    @change_group.command(name='file', description="Change un fichier d'une archive.")
    async def change_file_command(self, interaction: Interaction, level: str, subject: str, archive: str, index: int, file: Attachment):
        level = self.get_level(level)
        check = await self.check_args(interaction, level, subject, archive, index)
        if not check:
            return
        arch = self.data_archives[level][subject][archive]
        filename = get_file_archive_name(level, subject, archive, self.data_archives[level][subject][archive], index)
        new_name = "_old.".join(filename.split("."))
        rename(PATHS["pictures"]+"/"+filename, PATHS["pictures"]+"/"+new_name)
        await file.save(PATHS["pictures"]+"/"+filename)
        arch["files"][index]["edit_date"] = time()
        arch["files"][index]["author"] = interaction.user.id
        arch["files"][index]["type"] = filename.split(".")[-1]
        write_json(path_archives, self.data_archives)
        embed=build_embed(title=f"Archive {archive} :", color=Colour.blue(), message="Le fichier a correctement été remplacé.")
        await interaction.response.send_message(embed=embed)

    @insert_group.command(name='file', description="Insert un fichier dans une archive.")
    async def insert_file_command(self, interaction: Interaction, level: str, subject: str, archive: str, index: int, file: Attachment):
        level = self.get_level(level)
        check = await self.check_args(interaction, level, subject, archive, index)
        if not check:
            return
        arch = self.data_archives[level][subject][archive]
        change_name = []
        i = index
        for f in self.data_archives[level][subject][archive]["files"][index:]:
            change_name.append(self.change_index_filename(level, subject, archive, i, 1))
            i+=1
        for filename in change_name[::-1]:
            rename(PATHS["pictures"]+"/"+filename[0], PATHS["pictures"]+"/"+filename[1])
        arch["files"].insert(index, self.dict_file(interaction, file.filename))
        write_json(path_archives, self.data_archives)
        await file.save(PATHS["pictures"] + "/" + get_file_archive_name(level, subject, archive, arch, index))
        embed=build_embed(title=f"Archive {archive} :", color=Colour.blue(), message="Le fichier a correctement été remplacé.")
        await interaction.response.send_message(embed=embed)

    @purge_group.command(name='archive', description="Supprime tout les fichiers d'une archive.")
    async def purge_archive_command(self, interaction: Interaction, level: str, subject: str, archive: int):
        await interaction.response.send_message("coming soon...")

    @tasks.loop(time=timeloop)
    async def archive_work_loop(self):
        start = time()
        send = False
        for level in self.data_archives.items():
            for subject in level[1].items():
                for name, archive in subject[1].items():
                    if (start - archive["timestamp"] - (start - archive["timestamp"])%60) in DAYS:
                        delete_worker = []
                        for worker in archive["workers"]:
                            if worker not in self.workers:
                                try:
                                    self.workers[worker] = self.bot.get_user(worker)
                                except:
                                    try:
                                        self.workers[worker] = await self.bot.fetch_user(worker)
                                    except:
                                        delete_worker.append(worker)
                            if worker in self.workers:
                                embed, file = self.embed_archive(level[0], subject[0], name, archive)
                                try:
                                    message = await self.workers[worker].send(embed=embed, file = file)
                                    if len(archive["files"]) > 1:
                                        await message.edit(view = ArchiveView(self.bot, message, level[0], subject[0], name, archive))
                                    send = True
                                except:
                                    delete_worker.append(worker)
                        for user in delete_worker:
                            archive["workers"].remove(worker)
                            print("faire les logs de delete worker pourpotentiellement les remettres")
        if send:
            await asyncio.sleep(30)
    @Cog.listener()
    async def on_ready(self):
        self.data_archives["terminale"]["maths"]["int_gauss"]["timestamp"] = time()-24*60*60
        write_json(path_archives, self.data_archives)
        await asyncio.sleep(1)
        self.archive_work_loop.start()