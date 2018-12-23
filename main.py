from discord.ext import commands
import asyncio
import discord
from random import randint

prefix = "$"
bot = commands.Bot(command_prefix=prefix, self_bot=False)
bot.remove_command('help')

@bot.event
async def on_ready():
  print("Bot on")
  await bot.change_presence(game=discord.Game(name="$ticket new", url="https://twitch.tv/~", type=1))

@bot.command(pass_context=False)
async def help():
    helpmsg = discord.Embed(title='Help', description='$help - show this message\n$ticket ``[new/close]``- create a ticket or close it.', colour=0xcc6666)
    await bot.say(embed=helpmsg)

@bot.group(pass_context=True)
async def ticket(ctx):
    if ctx.invoked_subcommand is None:
        await bot.say("Did you mean ``$ticket new``?")

@ticket.command(pass_context=True)
async def new(ctx):
        ticketno = randint(0, 999)
        ticketname = "ticket-{}".format(ticketno)
        helpmsg = discord.Embed(title='Success', description='A new channel has been created for you. (#{})'.format(ticketname), colour=0x2AC940)
        await bot.say(embed=helpmsg)
        server = ctx.message.server
        newchannel = await bot.create_channel(server, ticketname, type=discord.ChannelType.text)
        author = ctx.message.author
        newrole = await bot.create_role(author.server, name=ticketname)
        role = discord.utils.get(author.server.roles, name=ticketname)
        allusers = discord.utils.get(author.server.roles, name="🔰 Member")
        await bot.add_roles(author, newrole)
        overwrite = discord.PermissionOverwrite()
        overwrite.read_messages = False
        await bot.edit_channel_permissions(newchannel, allusers, overwrite)
        allusers = discord.utils.get(author.server.roles, name="🔰 Member")
        overwrite = discord.PermissionOverwrite()
        overwrite.read_messages = True
        await bot.edit_channel_permissions(newchannel, newrole, overwrite)
        await bot.send_message(author, "Hey there! I've noticed you need help. Remember to check channel #ticket-{}!".format(ticketno))

@ticket.command(pass_context=True)
async def close(ctx):
        author = ctx.message.author
        server = ctx.message.server
        channel = ctx.message.channel
        role_names = [role.name for role in author.roles]
        print(role_names)
        for x in role_names:
           if x == channel.name:
               print("Yes")
               role = discord.utils.get(author.server.roles, name=x)
               await bot.remove_roles(author, role)
               await bot.delete_role(server, role)
               channel = discord.utils.get(author.server.channels, name=x)
               await bot.delete_channel(channel)
               await bot.send_message(author, "Your ``{}`` ticket has been closed.".format(x))
           else:
               print("No")

bot.run('', bot=True)
