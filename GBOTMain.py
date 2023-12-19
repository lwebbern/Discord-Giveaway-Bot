
import discord
import time
import asyncio
import os
import humanfriendly
from humanfriendly import format_timespan
from humanfriendly import parse_timespan

bot = discord.Client()
token = ""
choosing_channel = False
choosing_time = False
choosing_winners = False
choosing_item = False
confirm = False
giveaway = False
ongoing = False
counter = False
edited = 0
start = 1
counter1 = 0

s = ""
print("test")


@bot.event
async def on_ready():
    os.system("cls")
    print("{0} is ready".format(bot.user.name))
    print("ID: {0}".format(bot.user.id))

@bot.event
async def on_message(message):


    global choosing_channel
    global choosing_time
    global choosing_winners
    global choosing_item
    global channel_selection
    global hours_to_sec
    global giveaway
    global convert
    global edited
    global confirm
    global counter
    global ongoing
    global winners
    global counter1
    global start
    global item
    global s

    if confirm:
        if message.author.id != bot.user.id:
            if message.content.lower() == "!yes" or message.content.lower() == "!confirm":

                await bot.send_message(message.channel, "**Giveaway confirmed**")
                start = time.time()
                print("test")

                embed = discord.Embed(title="{0}".format(item), description="React with 🎉 to enter", color=0x1ff200)
                embed.add_field(name="{0} Winner{1}".format(winners, s), value="{0} Left".format(convert), inline=False)
                starting = await bot.send_message(bot.get_channel(channel_selection), "@everyone\n🎉 GIVEAWAY 🎉", embed=embed)

                await bot.add_reaction(starting, "🎉")

                confirm = False
                ongoing = True

                end = int(time.time()) + hours_to_sec

                while ongoing:
                    edited = edited +1

                    print(time.time())
                    time.sleep(1)
                    remaining_sec = end - time.time()

                    convert = format_timespan(int(remaining_sec))
                    print("giveaway ongoing [edited {0}]".format(edited))

                    embed=discord.Embed(title="{0}".format(item), description="React with 🎉 to enter", color=0x1ff200)
                    embed.add_field(name="{0} Winner{1}".format(winners, s), value="{0} Left".format(convert), inline=False)
                    edit = await bot.edit_message(starting,new_content="@everyone\n🎉 GIVEAWAY 🎉", embed=embed)

                    if time.time() > start+hours_to_sec:
                        reactions = await bot.get_reaction_users(":tada:", limit=500)

                        print(reactions)
                        print("[{0}] giveaway ended".format(counter))

                        embed = discord.Embed(title="{0}".format(item), description="Winners", color=0x000000)
                        embed.add_field(name="@everyone".format(winners, s), value="Over".format(convert), inline=False)
                        edit = await bot.edit_message(starting,new_content="🎉 GIVEAWAY OVER 🎉", embed=embed)

                        ongoing = False

            elif message.content.lower() == "!no" or message.content.lower() == "!cancel":
                await bot.send_message(message.channel, "**Giveaway canceled**")
                confirm = False

    if choosing_item:
        if message.author.id != bot.user.id:
            if message.content == "!cancel":
                await bot.send_message(message.channel, "**Giveaway canceled**")
                choosing_item = False
            else:
                item = message.content
                await bot.send_message(message.channel, "**{0}** Will be given away in channel <#{1}> with {2} winner{3} and the giveaway will last **{4}** ({5} seconds)!\n `are you sure you want to start this giveaway? type !confirm or !cancel`".format(item, channel_selection, winners, s, convert, hours_to_sec))
                choosing_item = False
                confirm = True

    if choosing_winners:
        if message.author.id != bot.user.id:
            if message.content == "!cancel":
                await bot.send_message(message.channel, "**Giveaway canceled**")
                choosing_winners = False
            s = ""
            print(message.content + "2")
            if int(message.content) > 1 or int(message.content) <= 0:
                s = "s"
            elif int(message.content) <= 0:
                await bot.send_message(message.channel, "please enter a valid amount")
            elif int(message.content):
                winners = int(message.content)
                await bot.send_message(message.channel, "{0} winner{1} chosen!\n`Last but not least, what will be given away?`".format(winners, s))
                print(channel_selection)
                choosing_winners = False
                choosing_item = True

    if choosing_time:
        print(message.content)
        print(message.content[-1])
        if message.author.id != bot.user.id:

            if message.content.lower() == "!cancel": #if user cancels
                await bot.send_message(message.channel, "**Canceled giveaway**")
                choosing_time = False

            if message.content[-1] == "s":
                s = ""
                time1 = "second"
                amount = int(message.content[:-1])
                hours_to_sec = amount
                convert = format_timespan(hours_to_sec)
                if amount > 1 or amount <= 0:
                    s = "s"
                if amount > 1 or amount == 1:
                    print(channel_selection + "1")
                    await bot.send_message(message.channel, "{0} ({1} seconds) chosen\n`How many winners you would like?`".format(convert,hours_to_sec))
                    choosing_time = False
                    choosing_winners = True
                else:
                    await bot.send_message(message.channel, "Please enter a valid amount of {0}{1}!".format(time,s))

            if message.content[-1] == "m":
                s = ""
                time1 = "minute"
                amount = int(message.content[:-1])
                hours_to_sec = amount*60
                convert = format_timespan(hours_to_sec)
                if amount > 1 or amount <= 0:
                    s = "s"
                if amount > 1 or amount == 1:
                    print(channel_selection + "1")
                    await bot.send_message(message.channel, "{0} ({1} seconds) chosen\n`How many winners you would like?`".format(convert,hours_to_sec))
                    choosing_time = False
                    choosing_winners = True
                else:
                    await bot.send_message(message.channel, "Please enter a valid amount of {0}{1}!".format(time,s))

            elif message.content[-1] == "h":
                 s = ""
                 time1 = "hour"
                 amount = int(message.content[:-1])
                 hours_to_sec = (amount*60)*60
                 convert = format_timespan(hours_to_sec)
                 if amount > 1 or amount <= 0:
                     s = "s"
                 if amount >= 1:
                    await bot.send_message(message.channel, "{0} ({1} seconds) chosen\n`How many winners you would like?`".format(convert,hours_to_sec))
                    choosing_time = False
                    choosing_winners = True
                 else:
                    await bot.send_message(message.channel, "Please enter a valid amount of {0}{1}!".format(time,s))

            elif message.content[-1] == "d":
                s = ""
                time1 = "day"
                amount = int(message.content[:-1])
                hours_to_sec = ((amount*60)*60)*24
                convert = format_timespan(hours_to_sec)
                if amount > 1 or amount <= 0:
                    s = "s"
                if amount >= 1:
                   await bot.send_message(message.channel, "{0} ({1} seconds) chosen\n`How many winners you would like?`".format(convert,hours_to_sec))
                   choosing_time = False
                   choosing_winners = True
                else:
                   await bot.send_message(message.channel, "Please enter a valid amount of {0}{1}!".format(time))
            elif message.content[-1] == "w":
                s = ""
                time1 = "week"
                amount = int(message.content[:-1])
                hours_to_sec = (((amount*60)*60)*24)*7
                convert = format_timespan(hours_to_sec)
                if amount > 1 or amount <= 0:
                    s = "s"
                if amount >= 1:
                   await bot.send_message(message.channel, "{0} ({1} seconds) chosen\n`How many winners you would like?`".format(convert,hours_to_sec))
                   choosing_time = False
                   choosing_winners = True
                else:
                   await bot.send_message(message.channel, "Please enter a valid amount of {0}{1}!".format(time,s))




    if choosing_channel:
        if message.author.id != bot.user.id:
            channel_selection = message.channel_mentions
            channel_amount = len(channel_selection)

            if message.content.lower() == "!cancel": #if user cancels
                await bot.send_message(message.channel, "**Canceled giveaway**")
                choosing_channel = False

            elif channel_amount == 0: #if no channel is entered
                await bot.send_message(message.channel, "Please enter a valid channel!")

            elif channel_amount > 1: #if more than 1 channel is entered
                await bot.send_message(message.channel, "Please enter only 1 channel!")

            else:
                channel_selection = channel_selection[0]
                channel_selection = channel_selection.id
                await bot.send_message(message.channel, "Sweet, giveaway will start in <#{0}>!\n``How long do you want the giveaway to last?``".format(channel_selection))
                choosing_channel = False
                choosing_time = True


    else:
        if message.content.lower() == "!create":
            channelname = await message.channel.send(message.channel, "Alright, you started a giveaway!\n``What channel would you like it to start in?``")
            choosing_channel = True

bot.run(token)
