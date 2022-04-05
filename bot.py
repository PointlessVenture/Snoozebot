"""
Snoozebot Bot by Aiden Tracy
"""

import asyncio
import discord
import random
import threading
import time
true = True
false = False

#TOKEN = "Upload Token Here!"

CLIENT = discord.Client()

user_list = []

def wait_and_remove(timer, user):
    time.sleep(timer)
    user_list.remove(user)

@CLIENT.event
async def on_ready():
    print(f'{CLIENT.user} has connected to Discord!')
    await CLIENT.change_presence(activity=discord.Game(name="Use z!help!"))

@CLIENT.event
async def on_message(message):
    # print(message)
    # print(message.author.id)
    if message.author == CLIENT.user:
        return
    try:
        if message.content[0] == "z" and message.content[1] == "!":
            valid = true
            text = message.content.split("z!")
            # print(text[1])
            args = text[1].split(" ")
            command = args[0]
            if command == "help":
                helpmsg = "Snoozebot Reporting for Duty!\n"
                helpmsg += "Use z!Snooze @(somebody) to send me out to check on someone.\n"
                helpmsg += "They have 5 minutes to respond to me. If they don't, I send them to the AFK channel.\n"
                helpmsg += "Whether they respond or not, I only check on someone once every 15 minutes.\n"
                await message.channel.send(helpmsg)
                # await message.channel.send("")
            elif command.lower() == "snooze":
                user = ""
                mod = ""
                channel = message.guild.afk_channel
                voice_state = ""
                if channel is None:
                    await message.channel.send("Hey, um, does your server have somewhere to send sleepyheads? Please add an AFK channel!")
                    valid = false

                if valid:
                    try:
                        user = message.mentions[0]
                        mod = args[1]
                    except IndexError:
                        await message.channel.send("If someone's snoozing, I gotta know who! You can use the @ symbol.")
                        valid = false

                if valid:
                    voice_state = user.voice
                    if voice_state is None:
                        valid = false
                        await message.channel.send("That person isn't in a voice chat. *yawn*  I'm going back to bed.")

                if valid:
                    if voice_state.channel == channel:
                        await message.channel.send("That person is already in bed. *yawn*  I'm going to join them.")
                        valid = false

                if valid:
                    for i in user_list:
                        if user == i:
                            valid = false
                            await message.channel.send("I just checked if they were snoozing... I won't check again for a bit.")
                if valid:
                    helpmsg = mod + ", are you snoozing? React to this with 😴 in 5 minutes or be moved to " + channel.name + "!"
                    user_list.append(user)
                    sentMessage = await message.channel.send(helpmsg)
                    await sentMessage.add_reaction("😴")

                    def check(reaction, userB):
                        return userB == user and str(reaction.emoji) == '😴'

                    try:
                        await CLIENT.wait_for('reaction_add', timeout=300.0, check = check)
                    except asyncio.TimeoutError:
                        await message.channel.send(mod + " must be snoozing!")
                        await user.move_to(channel)
                        wait_args = (600, user)
                        wait_thread = threading.Thread(target=wait_and_remove, args=wait_args)
                        wait_thread.start()
                    else:
                        await message.channel.send("Okay, " + mod + ", I won't move you.")
                        wait_args = (900, user)
                        wait_thread = threading.Thread(target=wait_and_remove, args=wait_args)
                        wait_thread.start()
                    # await message.channel.send("")
            else:
                await message.channel.send("Huh? Did somebody try to get my attention? Use z!help!")
                valid = false
    except IndexError:
        pass

"""
@CLIENT.event
async def on_message(message):
    if message.author == CLIENT.user:
        return
"""

CLIENT.run(TOKEN)
#CLIENT.change_presence(activity = "Use [help")
