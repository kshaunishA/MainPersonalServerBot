#Discord Bot Initialization
import re
import discord
from discord.ext import commands


#Discord Bot Source Initializations
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)


#Number of people in server not including bot
number_of_members = 1


#Number of strikes per individual in server (aside from admin)
strikes = {}


#Reference Lists
helloPrompts = ["hey server", "yo server", "hello server"]


f = open("/Users/kshaunishaddala/Downloads/facebook-bad-words-list_comma-separated-text-file_2021_01_18.txt", "r")
bannedWords = f.read().split(", ")


#When bot is running (console message)
@client.event
async def on_ready():
    print("Woah, I'm Alive!")


#When a member joins the server
@client.event
async def on_member_join(member):
    #increment number_of_members
    global number_of_members
    number_of_members = number_of_members + 1

    #console output
    print(f"{member} has joined a server")

    #create a strike profile in the strikes dict
    strikes[str(member.id)] = 0
    print(strikes[str(member.id)])


#When a member leaves the server
@client.event
async def on_member_remove(member):
    global number_of_members
    number_of_members = number_of_members - 1
    print(f"{member} has left a server.")


#Main commands handler
@client.event
async def on_message(message):
    serverAdminID = "495654597730500621"
    messageString = message.content.lower()

    #says hello to bot
    if messageString.lower() in helloPrompts:
        await message.channel.send(f"Hey {message.author}!")

    #displays all current commands
    elif messageString.lower() == ".help":
        await message.channel.send(f"Hey {message.author}! These are the following commands you can use! \n .ping \n .checklatency \n .howmanypeople")

    #outputs number of memebers in server (not including bot)
    elif messageString == ".howmanypeople":
        await message.channel.send(f"There are currently {number_of_members} member(s) in this server.")

    #censoring system (lone banned word)
    elif messageString.lower() in bannedWords:
        numberStrikesKey = str(message.author.id)

        await message.channel.purge(limit=1)
        strikes[numberStrikesKey] += 1

        if(strikes[numberStrikesKey] == 3):
            await message.author.send(f"Hey {message.author}, due to your usage of innapropriate words, you have been kicked from the server.")
            await message.author.kick(reason = None)
        else:
            await message.channel.send(f"Hey {message.author}, that word is banned on this server. You have {strikes[numberStrikesKey]} strikes.")

    #returns latency of user
    elif messageString.lower() == ".checklatency":
        await ctx.send(f"Hey {message.author}! Your latency is {round(client.latency * 1000)}ms")

    #clears the last 15 messages (only if admin)
    elif messageString.lower() == ".clear" and str(message.author.id) == serverAdminID:
        await message.channel.purge(limit = 15)

    #Sends user file of every banned word on the server
    elif messageString.lower() == ".bannedwords":
        file = discord.File("/Users/kshaunishaddala/Downloads/facebook-bad-words-list_comma-separated-text-file_2021_01_18.txt")
        await message.author.send(file=file, content=f"Here are all the words that are banned on the server: {message.guild.name}.")

    #censoring system (banned word in sentence)
    else:
        for letter in re.split('[,. !?]', messageString):
            if letter in bannedWords:
                numberStrikesKey = str(message.author.id)
                await message.channel.purge(limit=1)
                strikes[numberStrikesKey] += 1

                if(strikes[numberStrikesKey] == 3):
                    await message.author.send(f"Hey {message.author}, due to your usage of innapropriate words, you have been kicked from the server.")
                    await message.author.kick(reason = None)
                else:
                    await message.channel.send(f"Hey {message.author}, that word is banned on this server. You have {strikes[numberStrikesKey]} strikes.")


#bot run statement
client.run("ODY0OTMwNjA5MTg4ODMxMjMy.YO8nZg.8OSxPVrz1uSx_G0GleyobloqZ8Q")
