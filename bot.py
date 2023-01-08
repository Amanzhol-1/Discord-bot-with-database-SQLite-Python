import discord
from discord.ext import commands
from discord.ext import tasks
from discord.ext.commands import Bot
from discord import utils
import db
from db import insert
from db import fetch
import sqlite3


MESSAGE_ID = 123 #Reaction message ID
BOT_ID = 123     #Bot ID
ROLE_ID = 123   #Role ID
BOT_TOKEN = 'your bot token'

intents = discord.Intents().all()
bot = commands.Bot(command_prefix='$', intents=intents)


@bot.event
async def on_ready():
	print("Bot Has been runned")
	#db.random_logins()


@bot.event
async def on_raw_reaction_add(payload):
	if payload.message_id == MESSAGE_ID and payload.user_id != BOT_ID:

		channel = bot.get_channel(payload.channel_id)
		message = await channel.fetch_message(payload.message_id)
		member = utils.get(message.guild.members, id=payload.user_id)

		failed = True

		login = ''
		password = ''
		

		while failed:
			auth_data = fetch(f"SELECT Login, Password FROM Auth_data")

			est_logins = []

			user = fetch(f'SELECT Login, ID FROM Users')
			for elm in user:
				est_logins.append(elm[0])

			if not auth_data[0][0] in est_logins:
				failed = False
				login = auth_data[0][0]
				password = auth_data[0][1]
			else:
				insert(f'DELETE FROM Auth_data where Login = "{auth_data[0][0]}"')
				print(f'Login: {auth_data[0][0]} was used, and now removed from active logins')
			if auth_data == None:
				await message.remove_reaction(payload.emoji, member)
				print(f'No account remains')
				Failed = False

		role = utils.get(message.guild.roles, id=ROLE_ID)

		try:
			insert(f'INSERT INTO Users VALUES ({member.id}, "{member.name}", "{login}", "{password}")')
			insert(f'DELETE FROM Auth_data where Login = "{login}"')
			await member.send(f'Login: {login}\nPassword: {password}')
			await member.add_roles(role)
			print(f'{member} got an account')
		except sqlite3.IntegrityError:
			await message.remove_reaction(payload.emoji, member)
			print(f'{member} already have account')

'''@bot.command()
async def del_user_by_nick(ctx, user_name):
	insert(f'DELETE FROM Users where Nickname = "{user_name}"')'''



bot.run(BOT_TOKEN)