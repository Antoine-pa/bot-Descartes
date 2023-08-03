import discord
from discord.ext import commands
from discord import app_commands
import os
import io
import contextlib
import textwrap
import traceback
import time
import math

def isOwner(ctx):
    return ctx.author.id in [627191994699087873]

class OldVar:
	def __init__(self):
		self.dico_var = {}
	
	def set(self, name, value):
		self.dico_var[name] = value

Vars = OldVar()

class AdministrationCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot
    
    @app_commands.command(name="clear", description="Commande pour clear les messages.")
    @commands.has_permissions(manage_messages=True)
    async def clear_command(self, interaction: discord.Interaction, number: int, member:discord.Member = None):
        number = min(number+1, 50)
        channel = interaction.channel
        await interaction.response.send_message("Purge en cours")
        if member is None:
            await channel.purge(limit=number)
        else:
            def check(m):
                return m.author == member
            await channel.purge(limit=number,check=check)
        resp = await channel.send("Salon purgé.")
        await resp.delete(delay=5)

    def clean_code(self, code):
        one_line = False
        if code.startswith("```"):
            code = code[3:]
        if code.endswith("```"):
            code = code[:-3]
        code = code.split("\\n")
        if code[-1].startswith("```"):
            code = code[:-1]
        if len(code) == 1:
            if "=" not in code[0]:
                one_line = True
        code = "\n".join(code)
        if "await " in code:
            one_line=False
        return code, one_line

    def clean_output(self, output):
        lvl_indent = 0
        var = ""
        space = False
        for a in output:
            if a in ("[", "{", "("):
                lvl_indent += 1
                var += a + "\n" + "    " * lvl_indent
            elif a in ("]", "}", ")"):
                lvl_indent -= 1
                var += "\n" + "    " * lvl_indent + a
            elif a == ",":
                var += ",\n" + "    " * lvl_indent
                """
            elif a in ("'", '"'):
                if space: space = False
                else: space = True
                var += a
            elif a == " ":
                if space: var += a
                """
            else:
                var += a
        return var
    
    @app_commands.command(name="exec", description="Commande éxécuter du code.")
    @commands.check(isOwner)
    async def exec_command(self, interaction: discord.Interaction, code: str, shell: bool = None):
        start = time.time()
        message: discord.Message = await interaction.channel.send("Evalution en cours")
        local_variables = {
            "commands" : commands,
            "client" : self.bot,
            "discord" : discord,
            "message" : message,
            "interaction": interaction,
            "code" : code,
            "os" : os,
            "time": time,
            "math": math,
            "m": math,
            "imp" : __import__
        }
        for value in Vars.dico_var.items():
            local_variables[value[0]] = value[1]
        code, one_line = self.clean_code(code)
        buffer = io.StringIO()
        result = f"Input :\n```py\n{code}\n```"
        ret = ""
        try:
            with contextlib.redirect_stdout(buffer):
                if one_line:
                    output = eval(code, local_variables)
                    if output is None:
                        output = ""
                    output = self.clean_output(str(output) + "\n" + buffer.getvalue())
                else:
                    exec(f"async def _func():\n{textwrap.indent(code, '	')}", local_variables)
                    #pylint: disable=not-callable
                    ret = await local_variables["_func"]()
                    #pylint: enable=not-callable
                    if ret is not None:
                        ret = f"\nreturn :\n```\n{ret}```"
                    else:
                        ret = ""
                    if buffer.getvalue() == "":
                        output = "/"
                    else:
                        output = self.clean_output(buffer.getvalue())
                result += f"\nOutput :\n```\n{output}\n```" + ret
            if shell:
                print(output)
            _vars = local_variables.get("code", "").split("\n")
            for var in _vars:
                var = var.split("=")
                if len(var) > 1:
                    if var[1][0] in ("'", '"') and var[1][-1] in ("'", '"'):
                        var[1] = var[1][1:-1]
                    try:
                        if var[0].endswith(" "):
                            var[0] = var[0][:-1]
                        Vars.set(var[0], eval(var[1], local_variables))
                    except:
                        result += f"""\nan error occured"""
        except:
            result += f"""\nerror :\n```\n{traceback.format_exc()}```\n"""
        finally:
            await interaction.response.send_message("Votre évaluation est prête dans une seconde...", delete_after=5)
            end = time.time()
            embed = self.bot.tools.embed(title = "EVAL", color = 0xCC0000, message = result, footer = f"in {end-start}s")
            await message.edit(content="", embed=embed)