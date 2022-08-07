######################################
#                                    #
#              IMPORTS               #
#                                    #
######################################
import discord
from discord.ext import tasks, commands
from discord.ext.commands import MemberConverter, TextChannelConverter, has_permissions, errors
from discord import Spotify, Embed, Colour, Permissions
import urllib.parse, urllib.request, re
from pyowm import OWM
from random import choice, randint, shuffle
import operator
import requests
from bs4 import BeautifulSoup
import datetime
from PIL import Image, ImageDraw, ImageFont
import textwrap
from io import BytesIO
import googletrans
from googletrans import Translator


######################################
#                                    #
#               TODOS                #
#                                    #
######################################
# todo allow specific servers to change prefixes LATER (hard)
# todo add a english dictionary(input word, get definition) (urban dictionary and other websites too) (medium)
# todo unban, mute (with timer), unmute (more?) (medium)
# todo make a website for the bot (make a commands tab on the website too)  (hard, long)
# todo make some games/a points system (server specific points)  (hard, long)
# todo make better bot invite link(compare to dyno/mee6) (make sure perms are good) (hard)
# todo check how many servers bot is in and other server/bot specific stats (easy/medium, long)
# todo make a mod log
# todo .nickname (or .nick) command
# todo add a google search (title is search with hyperlist of the google list for the search)
# todo add a .remind me command (.remind me 1 hour to brush teeth)
# todo maybe, just maybe get live radio broadcasts for the bot to play (insanely hard)), use iheartradio
# todo use twitter api somehow (maybe for my bots twitter)
# todo add games with reactions or just text (a,b,c,d) like a gameshow
# todo welcome messages like in frc discord
# todo add a swear word filter
# todo make an embed generator (they say what to put in each part of the embed)
# todo timezone stuff


######################################
#                                    #
#          INITIALIZATIONS           #
#                                    #
######################################
prefix = '.'

client = commands.Bot(command_prefix=commands.when_mentioned_or(prefix), case_insensitive=True, owner_id=326191223301734401, max_messages=999999999999999999)

client.remove_command('help')

mconverter = MemberConverter()

tconverter = TextChannelConverter()

owm = OWM('KEY')  # pyown api key

mgr = owm.weather_manager()

activityL = ['info', 'owner', 'commands', 'botinfo', 'userinfo', 'serverinfo', 'mememaker', 'meme', 'avatar', 'status', 'spotify', 'ping', 'dm', 'searchyt', 'funfact', 'wake up lavish', 'lovemeter', '8ball', 'time', 'translate', 'slots 100', 'slotsinfo', 'kick', 'ban', 'unban', 'unbanall', 'purge', 'weather', 'weatherC', 'weatherF', 'convert'] #todo this lol

randomFact = ['The average person will spend six months of their life waiting for red lights to turn green.', 'A bolt of lightning contains enough energy to toast 100,000 slices of bread', 'Cherophobia is the word for the irrational fear of being happy', "You can hear a blue whale's heartbeat from two miles away", 'Nearly 30,000 rubber ducks were lost a sea in 1992 and are still being discovered today', "Subway footlongs aren't a foot long.", 'A U.S. Park Ranger once got hit by lightning seven times.', 'Bottled water expiration dates are for the bottle, not the water.', 'Pandas fake pregnancy for better care.', 'NASCAR drivers can lose up to 10 pounds in sweat due to high temperatures during races', 'Indians spend more than 10 hours a week reading, more than any other country in the world', 'The IKEA catalog is the most widely printed book in history', 'The largest snowflake on record was 15 inches wide', 'Someone tried to sell New Zealand on eBay but was stopped once the bid reached $3,000', 'A Canadian woman who lost her wedding ring while gardening found it 13 years later growing on a carrot', "McDonald's once tried to sell bubblegum-flavored broccoli to encourage kids to eat healthier", 'Doritos are flammable and can be used as kindling', "It's illegal to own only one guinea pig in Switzerland", 'In 2016, a Florida man was charged with assault after throwing a live alligator through a drive-thru window', 'The first written use of "OMG" was in a 1917 letter to Winston Churchill', 'Male students at Brigham Young University in Utah need special permission to grow a beard', 'In the 16th century, poets exchanged rap-battle like stylized insults in an act called "flyting"', 'Beauty and the Beast was written to help girls accept arranged marriages.', 'The voice actor of SpongeBob and the voice actor of Karen, Plankton’s computer wife, have been married since 1995.', 'Nowadays, millionaires with just $1 million isn’t considered wealthy anymore by most Americans. Now, the typical American sees at least $2.4 million as wealthy.', 'Standing around burns calories. On average, a 150 pound person burns 114 calories per hour while standing and doing nothing.', 'Until 2016, the “Happy Birthday” song was not for public use. Meaning, prior to 2016, the song was copyrighted and you had to pay a license to use it.', 'There are only two countries in the world that have the color purple in their flags: Nicaragua and Dominica.', 'When Shakira was in second grade, she was rejected for the school choir because her vibrato was too strong. The music teacher told her that she sounded like a goat.', 'On average, 46.1% of Americans have less than $10,000 in assets when they die.', 'Video games have been found to be more effective at battling depression than therapy.', 'Will Smith owed $2.8 Million to the IRS and almost went bankrupt, just before he signed the contract for The Fresh Prince Of Bel-Air.', 'Albert Einstein had mastered calculus by the tender age of 15.', 'A woman was elected to the U.S. House of Representatives four years before women even won the right to vote.', 'Canada eats more macaroni and cheese than any other nation in the world.', 'Surgeons who play video games at least 3 hours a week perform 27% faster and make 37% fewer errors.', 'Only 2% of the world’s population has green eyes.', 'Every second, the human eye moves about 50 times.', 'PewDiePie supported his YouTube channel by selling hot dogs. His persistence paid off when in 2012 his YouTube channel garnered over one million subscribers.', 'In Switzerland, it is illegal to flush the toilet after 10pm.', 'At any given moment, there are 1,800 thunderstorms happening on Earth. This amounts to 16 million storms each year.', 'Saturn is so big that Earth could fit into it whooping 755 times!', 'A man, Ben Sliney, grounded 4,000 commercial planes across the United States on 9/11 due to the attacks – it was his first day on the job.', 'The oldest “your mom” joke was discovered on a 3,500 year old Babylonian tablet', 'The fear of vegetables is called Lachanophobia.', 'According to scientists, the weight of the average cloud is 1.1 million pounds.', 'As per the Shark Tank contract, if you mention the name of any company you own, then Shark Tank automatically owns 5% of that company or gets 2% of the lifetime profits.', 'In the Pokémon games, Poliwag & Ditto have the same cry sounds.', 'In a survey, 33% of dog owners admitted to chatting over the telephone to their dogs.', "The entire world's population could fit inside Los Angeles.", 'More people visit France than any other country.', "There are only three countries in the world that don't use the metric system.", 'Four babies are born every second.', "The Earth's ozone layer will make a full recovery in 50 years.", 'Scotland has 420 words for “snow”', '29th May is officially “Put a Pillow on Your Fridge Day”.', '7% of American adults believe that chocolate milk comes from brown cows.', 'The inventor of the Frisbee was cremated and made into a Frisbee after he died.', 'In 2017 more people were killed from injuries caused by taking a selfie than by shark attacks.', 'A lion’s roar can be heard from 5 miles away.', 'Approximately 10-20% of U.S. power outages are caused by squirrels.', 'Facebook, Instagram and Twitter are all banned in China.', 'While trying to find a cure for AIDS, the Mayo Clinic made glow in the dark cats.', 'In 1998, Sony accidentally sold 700,000 camcorders that had the technology to see through people’s clothes.', "It's illegal to own just one guinea pig in Switzerland because they get lonely.", 'The voice of Mickey Mouse and the voice of Minnie Mouse got married in real life.', 'A can of Mountain Dew can dissolve a mouse', 'The loneliest creature on earth is a whale that has been calling for a mate for two decades.', 'Cuba and North Korea are the only two counties in the World without Coca-Cola', 'This bot contains 69 fun facts. Nice.']

commonChannels = ['general', 'public', 'global', 'welcome', 'discussion', 'chat']

commonCats = ['general', 'text', 'discussion']

importantCats = ['announcement', 'rule', 'info', 'important']

eightballL = ["I don't think so.", 'For now, yes.', 'My sources say no.', 'My sources say yes.', 'I am undecided, it is a tough one.', 'Definitely.', 'Absolutely not.', "Don't count on it.", 'Signs are pointing to yes.', 'The outlook is not so good.', 'Most likely yes.', 'Ask again later. I cannot decide.']

translator = Translator()

URL_REG = re.compile(r'https?://(?:www\.)?.+')

######################################
#                                    #
#           CLIENT EVENTS            #
#                                    #
######################################
@client.event
async def on_ready():
    print('Bot is ready')
    client.add_cog(DynamicStatus())


@client.event
async def on_guild_join(guild):
    if guild.id != 81384788765712384:
        welcomeMessage = 'Hello, I dont have a join message yet so... Here I am lol'
        if guild.system_channel is not None:
            await guild.system_channel.send(welcomeMessage)
        else:
            done = False
            for cChannel in commonChannels:
                if done: break
                for textchannel in guild.text_channels:
                    if cChannel in str(textchannel):
                        try:
                            await textchannel.send(welcomeMessage)
                            done = True
                            break
                        except:
                            pass
            if not done:
                for cCat in commonCats:
                    if done: break
                    for cat in guild.categories:
                        if done:
                            break
                        elif cCat in str(cat).lower():
                            for textchannel in cat.text_channels:
                                try:
                                    await textchannel.send(welcomeMessage)
                                    done = True
                                    break
                                except:
                                    pass
                if not done:
                    for textchannel in guild.text_channels:
                        if done: break
                        for i, cat in enumerate(importantCats):
                            if cat in str(textchannel.category).lower():
                                break
                            elif i == len(importantCats) - 1:
                                try:
                                    await textchannel.send(welcomeMessage)
                                    done = True
                                    break
                                except:
                                    pass
                    if not done:
                        for textchannel in guild.text_channels:
                            try:
                                await textchannel.send(welcomeMessage)
                                done = True
                                break
                            except:
                                pass
                        if not done:
                            try:
                                await guild.owner.send(welcomeMessage)
                            except:
                                pass


######################################
#                                    #
#             FUNCTIONS              #
#                                    #
######################################
def readFilesSlots(fileName):  #used in slots
    file = ''
    fi = open(fileName + '.txt', 'r')
    for line in fi:
        file = line.strip()
    return eval(file)


def readFiles(fileName):
    file = []
    fi = open(fileName + '.txt', 'r')
    for line in fi:
        file.append(line.strip())
    return file


def editFiles(fileName, edit):  # used in slots
    open(fileName + '.txt', 'w').close()
    open(fileName + '.txt', "a").write(str(edit))


def plus(s):  # used in weather
    s = list(s)
    for i in range(len(s)):
        if s[i] == ' ':
            s[i] = '+'
    return ''.join(s)


def removeTrailingZeros(n):  # used in conversions
    if n.is_integer():
        return int(n)
    else:
        return n


def getSongBar(current, end):  # used in spotify
    time = int(current.replace(':', '')) / int(end.replace(':', '')) # todo bar more accurate maybe???
    s = ''
    for i in range(14):
        if i/14 <= time <= (i+1)/14:
            for ii in range(i):
                s += '─'
            s += ':white_circle:'
            for ii in range(13-i):
                s += '─'
            return s


def formatTime(t: str):  # used in music
    for i in range(len(t)):
        if t[i] != '0' and t[i] != ':':
            if '.' in t:
                if len(t[i:t.index('.')]) == 2:
                    return f"0:{extraZero(t[i:t.index('.')])}"
                else:
                    return extraZero(t[i:t.index('.')])
            if len(t[i:]) == 2:
                return f"0:{extraZero(t[i:])}"
            else:
                return extraZero(t[i:])


def extraZero(t: str):
    if t.endswith(':0'):
        t += '0'
    return t


######################################
#                                    #
#              CLASSES               #
#                                    #
######################################
######################################
#          DYNAMIC STATUS            #
######################################
class DynamicStatus(commands.Cog):
    def __init__(self):
        self.index = 0
        self.activity.start()

    def cog_unload(self):
        self.activity.cancel()

    @tasks.loop(seconds=10.0)
    async def activity(self):
        try:
            activityL[self.index]
        except IndexError:
            self.index = 0
        finally:
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f'.help | .{activityL[self.index]}'))
            self.index += 1


######################################
#               EMOTES               #
######################################
class unicodeEmotes:
    thumbsup = '\U0001F44D'
    okhand = '\U0001F44C'
    slightly_frown_face = '\U0001F641'
    crown = '\U0001f451'
    earth_americas = '\U0001f30e'
    scroll = '\U0001f4dc'
    speech_bubble = '\U0001f4ac'
    speaker = '\U0001f508'
    person_standing = '\U0001f9cd'
    robot = '\U0001f916'
    baby = '\U0001f476'
    sports_medal = '\U0001f3c5'
    grinning = '\U0001f600'
    repeat = '\U0001f501'
    repeatloop = '\U0001f502'
    #empty_space = '\u200b'  # can be used in embed to make name nothing


class customEmotes:
    nitro_boost = '<:boost:693135164875735101>'

######################################
#                                    #
#                HELP                # # todo add a faq (leading to website) and a inquires
#                                    #
######################################
@client.command()
async def help(ctx):
    embed = Embed(title='Help (NOT WORKING YET)', description='[List of Commands](https://google.com)\n[Add Lavish Bot To Your Own Server](https://discordapp.com/oauth2/authorize?client_id=679888673864679496&permissions=2147446015&scope=bot)\n[Lavish Bot Official Discord Server](https://discordapp.com/invite/QzhuGTv)', colour=discord.Colour.green())
    await ctx.send(embed=embed)


@client.command(name='info', aliases=['information', 'about'])
async def info(ctx):
    botowner = client.get_user(client.owner_id)
    embed = Embed(title='Information', description=f'This bot was started on February 24th, 2020 by **{botowner}**. '
                                                   'At the time, I was a High School student with only a 2-3 of '
                                                   'coding experience looking for a new project to start, so I made '
                                                   'this Discord Bot!', colour=Colour.green())
    botname = await mconverter.convert(ctx, 'Lavish#7844')
    embed.set_image(url=botname.avatar_url)
    embed.set_footer(text=botowner.name, icon_url=botowner.avatar_url)
    #embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/326191223301734401/485fb2dbdd345b5c07875ff6823c8a94.webp?size=1024')
    await ctx.send(embed=embed)


@client.command()
async def owner(ctx): await ctx.send(f'The owner and creator of this bot is: **{client.get_user(client.owner_id)}**')


@client.command()
async def sourcecode(ctx): await ctx.send('The source code for this bot is currently unavailable to the public. Sorry!')


@client.command(name='commands', aliases=['command'])
async def commands(ctx):
    s = ''
    for i in client.all_commands:
        if str(client.all_commands[i]) + ', ' not in s:
            s += str(client.all_commands[i]) + ', '
    await ctx.send(s[:len(s)-2])


@client.command(name='botinfo', aliases=['botinformation'])
async def botinfo(ctx):
    botowner = client.get_user(client.owner_id)
    totalMembersServed = 0
    for guild in client.guilds:
        totalMembersServed += guild.member_count
    embed = Embed(title='Lavish Info', colour=Colour.green())
    embed.add_field(name='Developer', value=botowner)
    embed.add_field(name='Servers', value=f'Lavish is in {len(client.guilds)} servers.', inline=False)
    embed.add_field(name='Users', value=f'Lavish is serving {totalMembersServed} users.', inline=False)
    embed.set_thumbnail(url=client.user.avatar_url)
    await ctx.send(embed=embed)


@client.command(name='userinfo', aliases=['userinformation', 'myinfo', 'whois'])
async def userinfo(ctx, member: discord.Member=None):
    member = member or ctx.author
    # JOIN POS
    joins = tuple(sorted(member.guild.members, key=operator.attrgetter("joined_at")))
    joinPos = ''
    for i, memberJoined in enumerate(joins):
        if memberJoined.id == member.id:
            joinPos = f'{i+1}/{member.guild.member_count}'
    # ROLES
    rolesPrint = ''
    for role in reversed(member.roles[1:]):
        rolesPrint += f'{role.mention} '
    rolesPrint = rolesPrint[:-1]
    # PERMISSIONS
    userPermsList = []
    userPerms = ''
    if member.guild_permissions.administrator:
        userPerms = 'Administrator, Kick Members, Ban Members, Manage Server, Manage Channels, Manage Messages, ' \
                    'Mention Everyone, Manage Nicknames, Manage Roles, Manage Webhooks, Manage Emojis'
    else:
        if member.guild_permissions.kick_members:
            userPermsList.append('Kick Members')
        if member.guild_permissions.ban_members:
            userPermsList.append('Ban Members')
        if member.guild_permissions.manage_guild:
            userPermsList.append('Manage Server')
        if member.guild_permissions.manage_channels:
            userPermsList.append('Manage Channels')
        if member.guild_permissions.manage_messages:
            userPermsList.append('Manage Messages')
        if member.guild_permissions.mention_everyone:
            userPermsList.append('Mention Everyone')
        if member.guild_permissions.manage_nicknames:
            userPermsList.append('Manage Nicknames')
        if member.guild_permissions.manage_roles:
            userPermsList.append('Manage Roles')
        if member.guild_permissions.manage_webhooks:
            userPermsList.append('Manage Webhooks')
        if member.guild_permissions.manage_emojis:
            userPermsList.append('Manage Emojis')
        if userPermsList:
            for perm in userPermsList:
                userPerms += f'{perm}, '
            userPerms = userPerms[:-2]
    # DEVICES
    devicesList = []
    devices = ''
    if str(member.status) != 'offline':
        if str(member.desktop_status) != 'offline':
            devicesList.append('Discord Desktop App')
        if str(member.web_status) != 'offline':
            devicesList.append('Discord Website')
        if str(member.mobile_status) != 'offline':
            devicesList.append('Discord Mobile App')
        for device in devicesList:
            devices += f'{device}, '
        devices = devices[:-2]
    # EMBEDS
    if member.id == member.guild.owner.id:
        embed = Embed(description=f"{member.mention}'s Info, the Server Owner.", colour=Colour.green())
    else:
        embed = Embed(description=f"{member.mention}'s Info", colour=Colour.green())
    embed.set_author(name=member, icon_url=member.avatar_url)
    embed.set_thumbnail(url=member.avatar_url)
    embed.add_field(name='Joined Server at', value=member.joined_at.strftime("%A, %B %d, %Y %I:%M %p"))
    embed.add_field(name='Join Position', value=joinPos)
    embed.add_field(name='Account Created at', value=member.created_at.strftime("%A, %B %d, %Y %I:%M %p"))
    embed.add_field(name='Display Name', value=member.display_name)
    embed.add_field(name='Current Status', value=str(member.status).capitalize())
    try:
        if str(member.activity.type) == 'ActivityType.custom':
            if len(str(member.activity)) > 30:
                embed.add_field(name='Current Activity', value=f'{str(member.activity)[:30]}...')
            else:
                embed.add_field(name='Current Activity', value=member.activity)
        else:
            if len(str(member.activity.name)) > 30:
                embed.add_field(name='Current Activity', value=f'{str(member.activity.name)[:30]}...')
            else:
                embed.add_field(name='Current Activity', value=member.activity.name)
    except:
        embed.add_field(name='Current Activity', value='No Activity')
    if devices != '':
        if len(devicesList) == 1:
            embed.add_field(name='Device', value=devices, inline=False)
        else:
            embed.add_field(name='Devices', value=devices, inline=False)
    else:
        embed.add_field(name='Device', value=f'{member.name} is not online or is appearing offline.', inline=False)
    if rolesPrint != '':
        embed.add_field(name=f'Roles ({len(member.roles[1:])})', value=rolesPrint, inline=False)
    else:
        embed.add_field(name=f'Roles (0)', value=f'This user has no roles other than the default {unicodeEmotes.slightly_frown_face}', inline=False)
    if userPerms != '':
        embed.add_field(name=f'Users Top Permissions', value=userPerms, inline=False)
    else:
        embed.add_field(name=f'Users Top Permissions', value=f'This user has no top permissions {unicodeEmotes.slightly_frown_face}', inline=False)
    embed.set_footer(text=f'User ID: {member.id} | {datetime.datetime.now().strftime("%m/%d/%Y %I:%M %p")}')
    await ctx.send(embed=embed)


@client.command(name='serverinfo', aliases=['serverinformation', 'guildinfo', 'guildinformation'])
async def serverinfo(ctx):
    guild = ctx.author.guild
    # HUMAN/BOT USERS
    users, botusers, usersOnline, botusersOnline = 0, 0, 0, 0
    for member in guild.members:
        if member.bot:
            botusers += 1
            if str(member.status) != 'offline':
                botusersOnline += 1
        else:
            users += 1
            if str(member.status) != 'offline':
                usersOnline += 1
    totalUsersOnline = usersOnline + botusersOnline
    # USERS 24H
    joins = tuple(sorted(guild.members, key=operator.attrgetter("joined_at")))
    usersJoined24H = 0
    for member in reversed(joins):
        days = (datetime.datetime.utcnow() - member.joined_at).days
        if days == 0:
            usersJoined24H += 1
        else:
            break
    usersJoined24H = str(usersJoined24H)
    embed = Embed(colour=Colour.green())
    embed.set_author(name=guild, icon_url=guild.icon_url)
    embed.add_field(name=f'Server Owner {unicodeEmotes.crown}', value=guild.owner)
    embed.add_field(name=f'Server Region {unicodeEmotes.earth_americas}', value=guild.region)
    embed.add_field(name=f'Server Boosters {customEmotes.nitro_boost}', value=f'{guild.premium_subscription_count}/Tier {guild.premium_tier}')
    embed.add_field(name=f'Channel Categories {unicodeEmotes.scroll}', value=str(len(guild.categories)))
    embed.add_field(name=f'Text Channels {unicodeEmotes.speech_bubble}', value=str(len(guild.text_channels)))
    embed.add_field(name=f'Voice Channels {unicodeEmotes.speaker}', value=str(len(guild.voice_channels)))
    embed.add_field(name=f'Total Members {unicodeEmotes.person_standing}{unicodeEmotes.robot}', value=f'{guild.member_count} ({totalUsersOnline} Online)')
    embed.add_field(name=f'Humans {unicodeEmotes.person_standing}', value=f'{users} ({usersOnline} Online)')
    embed.add_field(name=f'Bots {unicodeEmotes.robot}', value=f'{botusers} ({botusersOnline} Online)')
    embed.add_field(name=f'New Members {unicodeEmotes.baby}', value=f'{usersJoined24H} in last 24H')
    embed.add_field(name=f'Roles {unicodeEmotes.sports_medal}', value=str(len(guild.roles)))
    embed.add_field(name=f'Emojis {unicodeEmotes.grinning}', value=str(len(guild.emojis)))
    embed.set_footer(text=f'ID: {guild.id} | Created: {guild.created_at.strftime("%m/%d/%Y %I:%M %p")}')
    await ctx.send(embed=embed)


######################################
#                                    #
#         RANDOM FUN COMMANDS        #
#                                    #
######################################
@client.command(name='mememaker', aliases=['memesmaker', 'memeformat'])  # todo add more memes and error messages, set a max length
async def mememaker(ctx, meme, *, content):
    if meme.lower() == 'drake':  # todo maybe make font larger?
        img = Image.open('drakememe.jpg')  # FOR VM: img = Image.open('C:/Users/nickjano/PycharmProjects/discordbot/drakememe.jpg')
        draw = ImageDraw.Draw(img)
        content = content.split('//')
        if len(content) == 2:
            for contentpart in content:
                contentpart.strip()
            width, height = img.size
            mlength1 = textwrap.wrap(content[0], width=25)
            mlength2 = textwrap.wrap(content[1], width=25)
            content[0] = ''
            for i, line in enumerate(mlength1):
                content[0] += line
                if i != len(mlength1) - 1:
                    content[0] += '\n'
            content[1] = ''
            for i, line in enumerate(mlength2):
                content[1] += line
                if i != len(mlength2) - 1:
                    content[1] += '\n'
            bounding_box = [width / 2 + 1, height / 2 - 21, width, 0]
            bounding_box2 = [width / 2 + 1, height / 2 - 15, width, height]
            x1_1, y1_1, x2_1, y2_1 = bounding_box
            x1_2, y1_2, x2_2, y2_2 = bounding_box2

            font = ImageFont.truetype('impact.ttf', 25)

            w1, h1 = draw.textsize(content[0], font=font)
            w2, h2 = draw.textsize(content[1], font=font)

            x_1 = (x2_1 - x1_1 - w1) / 2 + x1_1
            y_1 = (y2_1 - y1_1 - h1) / 2 + y1_1
            x_2 = (x2_2 - x1_2 - w2) / 2 + x1_2
            y_2 = (y2_2 - y1_2 - h2) / 2 + y1_2

            draw.text((x_1, y_1), content[0], (0, 0, 0), align='center', font=font)
            draw.text((x_2, y_2), content[1], (0, 0, 0), align='center', font=font)

            buffer = BytesIO()
            img.save(buffer, format='PNG')
            imgByteArr = buffer.getvalue()
            buffer.seek(0)
            buffer = BytesIO(imgByteArr)

            f = discord.File(buffer, filename=f'{ctx.author.id}-drake.png')
            embed = Embed(title='Drake Meme Format', colour=Colour.green())
            embed.set_image(url='attachment://{}-drake.png'.format(ctx.author.id))
            embed.set_footer(text=f'{ctx.author} Requested this meme', icon_url=ctx.author.avatar_url)
            await ctx.send(file=f, embed=embed)
        else:
            await ctx.send(f'{ctx.author.mention}, please input: `.mememaker drake phrase1//phrase2`', delete_after=7.0)
    else:
        await ctx.send(f'{ctx.author.mention}, please input: `.mememaker MEMEFORMAT TEXT`, for help do **.mememakerhelp**', delete_after=12.0)


@mememaker.error
async def mememaker_error(ctx, error):
    if isinstance(error, errors.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.mention}, please input: `.mememaker MEMEFORMAT TEXT`, for help do **.mememakerhelp**', delete_after=12.0)


@client.command(name='mememakerhelp', aliases=['mememakerinfo'])
async def mememakerhelp(ctx):
    embed = Embed(title='Meme Maker Information',
                  description='This page shows how to make a meme in every format.',
                  colour=Colour.green())
    embed.add_field(name='**Meme Formats:**', value='''DRAKE MEME FORMAT: **.mememaker drake text1//text2**
                                                       
                                                       MORE MEME FORMATS COMING SOON!''')
    embed.set_thumbnail(url='https://www.memesmonkey.com/images/memesmonkey/47/476205720118717aadf1144dae839af3.jpeg')
    await ctx.send(embed=embed)


@client.command()
async def avatar(ctx, member: discord.Member=None):
    member = member or ctx.author
    embed = Embed(colour=Colour.green())
    embed.set_author(name=member.name, icon_url=member.avatar_url)
    embed.set_image(url=member.avatar_url)
    await ctx.send(embed=embed)


@client.command()
async def status(ctx, member: discord.Member=None):
    member = member or ctx.author
    await ctx.send(str(member.status).capitalize())


@client.command()
async def spotify(ctx, member: discord.Member=None):
    member = member or ctx.author
    if 'Spotify' in str(member.activities):
        for activity in member.activities:
            if isinstance(activity, Spotify):
                embed = Embed(title=f"{member.name}'s Spotify", colour=Colour.green())
                embed.add_field(name='Currently listening to:', value=f'**{activity.title}** by ' + str(f'**{activity.artist}**').replace(';', ','))
                durationstart = 0
                currenttimestart = 0
                for i in range(3):
                    if str(activity.duration)[i].isdigit():
                        if int(str(activity.duration)[i]) > 0:
                            break
                        else:
                            durationstart += 1
                    else:
                        durationstart += 1
                    if str(datetime.datetime.utcnow() - activity.start)[i].isdigit():
                        if int(str(datetime.datetime.utcnow() - activity.start)[i]) > 0:
                            break
                        else:
                            currenttimestart += 1
                    else:
                        currenttimestart += 1
                if str(activity.duration).find('.') == -1:
                    durationlen = str(activity.duration)[durationstart:]
                else:
                    durationlen = str(activity.duration)[durationstart:str(activity.duration).find('.')]
                currenttime = str(datetime.datetime.utcnow() - activity.start)[currenttimestart:str(datetime.datetime.utcnow() - activity.start).find(".")]
                embed.add_field(name='Bar', value=f'{getSongBar(currenttime, durationlen)} {currenttime} / {durationlen} 🔊', inline=False)
                embed.set_footer(text='Bar might be a tiny bit off from rounding') #todo maybe make bar more accurate???
                embed.set_thumbnail(url=activity.album_cover_url)
                await ctx.send(embed=embed)
                #await ctx.send(f'{member.name} is listening to **{activity.title}** by ' + str(f'**{activity.artist}**').replace(';', ','))
    else:
        await ctx.send(f"{member.name} is not listening to Spotify, or they don't have their Spotify account linked to their Discord account.", delete_after=10.0)


@spotify.error
async def spotify_error(ctx, error):
    if isinstance(error, errors.BadArgument):
        await ctx.send(f'{ctx.author.mention}, please input a user in the server/chat for this command.', delete_after=5.0)


@client.command()
async def ping(ctx): await ctx.send(f'Pong! :ping_pong: {round(client.latency * 1000)}ms') # todo get time of message read by bot - time of message sent to see user latency


@client.command()
async def dm(ctx):
    try:
        await ctx.author.send('Sup')
    except:
        await ctx.send(f"{ctx.author.mention}, I cannot DM you. :slight_frown:", delete_after=5.0)


@client.command()
async def searchyt(ctx, *, search): #todo for this and .play, add error messages
    query_string = urllib.parse.urlencode({'search_query': search})
    htm_content = urllib.request.urlopen('https://www.youtube.com/results?' + query_string)
    search_results = re.findall('href=\"/watch\\?v=(.{11})', htm_content.read().decode())
    await ctx.send('Top result: ' + 'https://www.youtube.com/watch?v=' + search_results[0])


@searchyt.error
async def searchyt_error(ctx, error):
    if isinstance(error, errors.MissingRequiredArgument):
        await ctx.send('Please enter something to search.', delete_after=5.0)
    elif isinstance(error, errors.CommandInvokeError):
        await ctx.send('There are no results for that search.', delete_after=5.0)


@client.command(name='funfact', aliases=['randomfact'])
async def funfact(ctx): await ctx.send(f'Fun Fact: {choice(randomFact)}')


@client.command()
async def wake(ctx, *, message):
    if 'up lavish' in message.lower(): await ctx.send(f"I'm here, {ctx.author.name}.")


@client.command()
async def wakeup(ctx, *, message):
    if 'lavish' in message.lower(): await ctx.send(f"I'm here, {ctx.author.name}.")


@client.command(name='lovemeter')
async def lovemeter(ctx, member1: discord.Member=None, member2: discord.Member=None):
    if member2 is not None:
        await ctx.send(f':revolving_hearts: There is a **{randint(-1, 100)}%** chance of a successful relationship between {member1.name} and {member2.name} :revolving_hearts:')
    else:
        await ctx.send(f':revolving_hearts: There is a **{randint(-1, 100)}%** chance of a successful relationship between {ctx.author.name} and {member1.name} :revolving_hearts:')


@lovemeter.error
async def lovemeter_error(ctx, error):
    if isinstance(error, errors.CommandInvokeError):
        await ctx.send(f'{ctx.author.mention}, please input at lease one name for the love meter to work!', delete_after=5.0)


@client.command(name='8ball', aliases=['magic8ball'])
async def eightball(ctx, message=None): await ctx.send(choice(eightballL))


@client.command(name='wordscramble', aliases=['scramble'])
async def wordscramble(ctx):
    nouns = ['people', 'history', 'way', 'art', 'world', 'information', 'map', 'two', 'family', 'government', 'health', 'system', 'computer', 'meat', 'year', 'thanks', 'music', 'person', 'reading', 'method', 'data', 'food', 'understanding', 'theory', 'law', 'bird', 'literature', 'problem', 'software', 'control', 'knowledge', 'power', 'ability', 'economics', 'love', 'internet', 'television', 'science', 'library', 'nature', 'fact', 'product', 'idea', 'temperature', 'investment', 'area', 'society', 'activity', 'story', 'industry', 'media', 'thing', 'oven', 'community', 'definition', 'safety', 'quality', 'development', 'language', 'management', 'player', 'variety', 'video', 'week', 'security', 'country', 'exam', 'movie', 'organization', 'equipment', 'physics', 'analysis', 'policy', 'series', 'thought', 'basis', 'boyfriend', 'direction', 'strategy', 'technology', 'army', 'camera', 'freedom', 'paper', 'environment', 'child', 'instance', 'month', 'truth', 'marketing', 'university', 'writing', 'article', 'department', 'difference', 'goal', 'news', 'audience', 'fishing', 'growth', 'income', 'marriage', 'user', 'combination', 'failure', 'meaning', 'medicine', 'philosophy', 'teacher', 'communication', 'night', 'chemistry', 'disease', 'disk', 'energy', 'nation', 'road', 'role', 'soup', 'advertising', 'location', 'success', 'addition', 'apartment', 'education', 'math', 'moment', 'painting', 'politics', 'attention', 'decision', 'event', 'property', 'shopping', 'student', 'wood', 'competition', 'distribution', 'entertainment', 'office', 'population', 'president', 'unit', 'category', 'cigarette', 'context', 'introduction', 'opportunity', 'performance', 'driver', 'flight', 'length', 'magazine', 'newspaper', 'relationship', 'teaching', 'cell', 'dealer', 'debate', 'finding', 'lake', 'member', 'message', 'phone', 'scene', 'appearance', 'association', 'concept', 'customer', 'death', 'discussion', 'housing', 'inflation', 'insurance', 'mood', 'woman', 'advice', 'blood', 'effort', 'expression', 'importance', 'opinion', 'payment', 'reality', 'responsibility', 'situation', 'skill', 'statement', 'wealth', 'application', 'city', 'county', 'depth', 'estate', 'foundation', 'grandmother', 'heart', 'perspective', 'photo', 'recipe', 'studio', 'topic', 'collection', 'depression', 'imagination', 'passion', 'percentage', 'resource', 'setting', 'ad', 'agency', 'college', 'connection', 'criticism', 'debt', 'description', 'memory', 'patience', 'secretary', 'solution', 'administration', 'aspect', 'attitude', 'director', 'personality', 'psychology', 'recommendation', 'response', 'selection', 'storage', 'version', 'alcohol', 'argument', 'complaint', 'contract', 'emphasis', 'highway', 'loss', 'membership', 'possession', 'preparation', 'steak', 'union', 'agreement', 'cancer', 'currency', 'employment', 'engineering', 'entry', 'interaction', 'limit', 'mixture', 'preference', 'region', 'republic', 'seat', 'tradition', 'virus', 'actor', 'classroom', 'delivery', 'device', 'difficulty', 'drama', 'election', 'engine', 'football', 'guidance', 'hotel', 'match', 'owner', 'priority', 'protection', 'suggestion', 'tension', 'variation', 'anxiety', 'atmosphere', 'awareness', 'bread', 'climate', 'comparison', 'confusion', 'construction', 'elevator', 'emotion', 'employee', 'employer', 'guest', 'height', 'leadership', 'mall', 'manager', 'operation', 'recording', 'respect', 'sample', 'transportation', 'boring', 'charity', 'cousin', 'disaster', 'editor', 'efficiency', 'excitement', 'extent', 'feedback', 'guitar', 'homework', 'leader', 'mom', 'outcome', 'permission', 'presentation', 'promotion', 'reflection', 'refrigerator', 'resolution', 'revenue', 'session', 'singer', 'tennis', 'basket', 'bonus', 'cabinet', 'childhood', 'church', 'clothes', 'coffee', 'dinner', 'drawing', 'hair', 'hearing', 'initiative', 'judgment', 'lab', 'measurement', 'mode', 'mud', 'orange', 'poetry', 'police', 'possibility', 'procedure', 'queen', 'ratio', 'relation', 'restaurant', 'satisfaction', 'sector', 'signature', 'significance', 'song', 'tooth', 'town', 'vehicle', 'volume', 'wife', 'accident', 'airport', 'appointment', 'arrival', 'assumption', 'baseball', 'chapter', 'committee', 'conversation', 'database', 'enthusiasm', 'error', 'explanation', 'farmer', 'gate', 'girl', 'hall', 'historian', 'hospital', 'injury', 'instruction', 'maintenance', 'manufacturer', 'meal', 'perception', 'pie', 'poem', 'presence', 'proposal', 'reception', 'replacement', 'revolution', 'river', 'son', 'speech', 'tea', 'village', 'warning', 'winner', 'worker', 'writer', 'assistance', 'breath', 'buyer', 'chest', 'chocolate', 'conclusion', 'contribution', 'cookie', 'courage', 'dad', 'desk', 'drawer', 'establishment', 'examination', 'garbage', 'grocery', 'honey', 'impression', 'improvement', 'independence', 'insect', 'inspection', 'inspector', 'king', 'ladder', 'menu', 'penalty', 'piano', 'potato', 'profession', 'professor', 'quantity', 'reaction', 'requirement', 'salad', 'sister', 'supermarket', 'tongue', 'weakness', 'wedding', 'affair', 'ambition', 'analyst', 'apple', 'assignment', 'assistant', 'bathroom', 'bedroom', 'beer', 'birthday', 'celebration', 'championship', 'cheek', 'client', 'consequence', 'departure', 'diamond', 'dirt', 'ear', 'fortune', 'friendship', 'funeral', 'gene', 'girlfriend', 'hat', 'indication', 'intention', 'lady', 'midnight', 'negotiation', 'obligation', 'passenger', 'pizza', 'platform', 'poet', 'pollution', 'recognition', 'reputation', 'shirt', 'sir', 'speaker', 'stranger', 'surgery', 'sympathy', 'tale', 'throat', 'trainer', 'uncle', 'youth', 'time', 'work', 'film', 'water', 'money', 'example', 'while', 'business', 'study', 'game', 'life', 'form', 'air', 'day', 'place', 'number', 'part', 'field', 'fish', 'back', 'process', 'heat', 'hand', 'experience', 'job', 'book', 'end', 'point', 'type', 'home', 'economy', 'value', 'body', 'market', 'guide', 'interest', 'state', 'radio', 'course', 'company', 'price', 'size', 'card', 'list', 'mind', 'trade', 'line', 'care', 'group', 'risk', 'word', 'fat', 'force', 'key', 'light', 'training', 'name', 'school', 'top', 'amount', 'level', 'order', 'practice', 'research', 'sense', 'service', 'piece', 'web', 'boss', 'sport', 'fun', 'house', 'page', 'term', 'test', 'answer', 'sound', 'focus', 'matter', 'kind', 'soil', 'board', 'oil', 'picture', 'access', 'garden', 'range', 'rate', 'reason', 'future', 'site', 'demand', 'exercise', 'image', 'case', 'cause', 'coast', 'action', 'age', 'bad', 'boat', 'record', 'result', 'section', 'building', 'mouse', 'cash', 'class', 'nothing', 'period', 'plan', 'store', 'tax', 'side', 'subject', 'space', 'rule', 'stock', 'weather', 'chance', 'figure', 'man', 'model', 'source', 'beginning', 'earth', 'program', 'chicken', 'design', 'feature', 'head', 'material', 'purpose', 'question', 'rock', 'salt', 'act', 'birth', 'car', 'dog', 'object', 'scale', 'sun', 'note', 'profit', 'rent', 'speed', 'style', 'war', 'bank', 'craft', 'half', 'inside', 'outside', 'standard', 'bus', 'exchange', 'eye', 'fire', 'position', 'pressure', 'stress', 'advantage', 'benefit', 'box', 'frame', 'issue', 'step', 'cycle', 'face', 'item', 'metal', 'paint', 'review', 'room', 'screen', 'structure', 'view', 'account', 'ball', 'discipline', 'medium', 'share', 'balance', 'bit', 'black', 'bottom', 'choice', 'gift', 'impact', 'machine', 'shape', 'tool', 'wind', 'address', 'average', 'career', 'culture', 'morning', 'pot', 'sign', 'table', 'task', 'condition', 'contact', 'credit', 'egg', 'hope', 'ice', 'network', 'north', 'square', 'attempt', 'date', 'effect', 'link', 'post', 'star', 'voice', 'capital', 'challenge', 'friend', 'self', 'shot', 'brush', 'couple', 'exit', 'front', 'function', 'lack', 'living', 'plant', 'plastic', 'spot', 'summer', 'taste', 'theme', 'track', 'wing', 'brain', 'button', 'click', 'desire', 'foot', 'gas', 'influence', 'notice', 'rain', 'wall', 'base', 'damage', 'distance', 'feeling', 'pair', 'savings', 'staff', 'sugar', 'target', 'text', 'animal', 'author', 'budget', 'discount', 'file', 'ground', 'lesson', 'minute', 'officer', 'phase', 'reference', 'register', 'sky', 'stage', 'stick', 'title', 'trouble', 'bowl', 'bridge', 'campaign', 'character', 'club', 'edge', 'evidence', 'fan', 'letter', 'lock', 'maximum', 'novel', 'option', 'pack', 'park', 'plenty', 'quarter', 'skin', 'sort', 'weight', 'baby', 'background', 'carry', 'dish', 'factor', 'fruit', 'glass', 'joint', 'master', 'muscle', 'red', 'strength', 'traffic', 'trip', 'vegetable', 'appeal', 'chart', 'gear', 'ideal', 'kitchen', 'land', 'log', 'mother', 'net', 'party', 'principle', 'relative', 'sale', 'season', 'signal', 'spirit', 'street', 'tree', 'wave', 'belt', 'bench', 'commission', 'copy', 'drop', 'minimum', 'path', 'progress', 'project', 'sea', 'south', 'status', 'stuff', 'ticket', 'tour', 'angle', 'blue', 'breakfast', 'confidence', 'daughter', 'degree', 'doctor', 'dot', 'dream', 'duty', 'essay', 'father', 'fee', 'finance', 'hour', 'juice', 'luck', 'milk', 'mouth', 'peace', 'pipe', 'stable', 'storm', 'substance', 'team', 'trick', 'afternoon', 'bat', 'beach', 'blank', 'catch', 'chain', 'consideration', 'cream', 'crew', 'detail', 'gold', 'interview', 'kid', 'mark', 'mission', 'pain', 'pleasure', 'score', 'screw', 'sex', 'shop', 'shower', 'suit', 'tone', 'window', 'agent', 'band', 'bath', 'block', 'bone', 'calendar', 'candidate', 'cap', 'coat', 'contest', 'corner', 'court', 'cup', 'district', 'door', 'east', 'finger', 'garage', 'guarantee', 'hole', 'hook', 'implement', 'layer', 'lecture', 'lie', 'manner', 'meeting', 'nose', 'parking', 'partner', 'profile', 'rice', 'routine', 'schedule', 'swimming', 'telephone', 'tip', 'winter', 'airline', 'bag', 'battle', 'bed', 'bill', 'bother', 'cake', 'code', 'curve', 'designer', 'dimension', 'dress', 'ease', 'emergency', 'evening', 'extension', 'farm', 'fight', 'gap', 'grade', 'holiday', 'horror', 'horse', 'host', 'husband', 'loan', 'mistake', 'mountain', 'nail', 'noise', 'occasion', 'package', 'patient', 'pause', 'phrase', 'proof', 'race', 'relief', 'sand', 'sentence', 'shoulder', 'smoke', 'stomach', 'string', 'tourist', 'towel', 'vacation', 'west', 'wheel', 'wine', 'arm', 'aside', 'associate', 'bet', 'blow', 'border', 'branch', 'breast', 'brother', 'buddy', 'bunch', 'chip', 'coach', 'cross', 'document', 'draft', 'dust', 'expert', 'floor', 'god', 'golf', 'habit', 'iron', 'judge', 'knife', 'landscape', 'league', 'mail', 'mess', 'native', 'opening', 'parent', 'pattern', 'pin', 'pool', 'pound', 'request', 'salary', 'shame', 'shelter', 'shoe', 'silver', 'tackle', 'tank', 'trust', 'assist', 'bake', 'bar', 'bell', 'bike', 'blame', 'boy', 'brick', 'chair', 'closet', 'clue', 'collar', 'comment', 'conference', 'devil', 'diet', 'fear', 'fuel', 'glove', 'jacket', 'lunch', 'monitor', 'mortgage', 'nurse', 'pace', 'panic', 'peak', 'plane', 'reward', 'row', 'sandwich', 'shock', 'spite', 'spray', 'surprise', 'till', 'transition', 'weekend', 'welcome', 'yard', 'alarm', 'bend', 'bicycle', 'bite', 'blind', 'bottle', 'cable', 'candle', 'clerk', 'cloud', 'concert', 'counter', 'flower', 'grandfather', 'harm', 'knee', 'lawyer', 'leather', 'load', 'mirror', 'neck', 'pension', 'plate', 'purple', 'ruin', 'ship', 'skirt', 'slice', 'snow', 'specialist', 'stroke', 'switch', 'trash', 'tune', 'zone', 'anger', 'award', 'bid', 'bitter', 'boot', 'bug', 'camp', 'candy', 'carpet', 'cat', 'champion', 'channel', 'clock', 'comfort', 'cow', 'crack', 'engineer', 'entrance', 'fault', 'grass', 'guy', 'hell', 'highlight', 'incident', 'island', 'joke', 'jury', 'leg', 'lip', 'mate', 'motor', 'nerve', 'passage', 'pen', 'pride', 'priest', 'prize', 'promise', 'resident', 'resort', 'ring', 'roof', 'rope', 'sail', 'scheme', 'script', 'sock', 'station', 'toe', 'tower', 'truck', 'witness', 'a', 'you', 'it', 'can', 'will', 'if', 'one', 'many', 'most', 'other', 'use', 'make', 'good', 'look', 'help', 'go', 'great', 'being', 'few', 'might', 'still', 'public', 'read', 'keep', 'start', 'give', 'human', 'local', 'general', 'she', 'specific', 'long', 'play', 'feel', 'high', 'tonight', 'put', 'common', 'set', 'change', 'simple', 'past', 'big', 'possible', 'particular', 'today', 'major', 'personal', 'current', 'national', 'cut', 'natural', 'physical', 'show', 'try', 'check', 'second', 'call', 'move', 'pay', 'let', 'increase', 'single', 'individual', 'turn', 'ask', 'buy', 'guard', 'hold', 'main', 'offer', 'potential', 'professional', 'international', 'travel', 'cook', 'alternative', 'following', 'special', 'working', 'whole', 'dance', 'excuse', 'cold', 'commercial', 'low', 'purchase', 'deal', 'primary', 'worth', 'fall', 'necessary', 'positive', 'produce', 'search', 'present', 'spend', 'talk', 'creative', 'tell', 'cost', 'drive', 'green', 'support', 'glad', 'remove', 'return', 'run', 'complex', 'due', 'effective', 'middle', 'regular', 'reserve', 'independent', 'leave', 'original', 'reach', 'rest', 'serve', 'watch', 'beautiful', 'charge', 'active', 'break', 'negative', 'safe', 'stay', 'visit', 'visual', 'affect', 'cover', 'report', 'rise', 'walk', 'white', 'beyond', 'junior', 'pick', 'unique', 'anything', 'classic', 'final', 'lift', 'mix', 'private', 'stop', 'teach', 'western', 'concern', 'familiar', 'fly', 'official', 'broad', 'comfortable', 'gain', 'maybe', 'rich', 'save', 'stand', 'young', 'heavy', 'hello', 'lead', 'listen', 'valuable', 'worry', 'handle', 'leading', 'meet', 'release', 'sell', 'finish', 'normal', 'press', 'ride', 'secret', 'spread', 'spring', 'tough', 'wait', 'brown', 'deep', 'display', 'flow', 'hit', 'objective', 'shoot', 'touch', 'cancel', 'chemical', 'cry', 'dump', 'extreme', 'push', 'conflict', 'eat', 'fill', 'formal', 'jump', 'kick', 'opposite', 'pass', 'pitch', 'remote', 'total', 'treat', 'vast', 'abuse', 'beat', 'burn', 'deposit', 'print', 'raise', 'sleep', 'somewhere', 'advance', 'anywhere', 'consist', 'dark', 'double', 'draw', 'equal', 'fix', 'hire', 'internal', 'join', 'kill', 'sensitive', 'tap', 'win', 'attack', 'claim', 'constant', 'drag', 'drink', 'guess', 'minor', 'pull', 'raw', 'soft', 'solid', 'wear', 'weird', 'wonder', 'annual', 'count', 'dead', 'doubt', 'feed', 'forever', 'impress', 'nobody', 'repeat', 'round', 'sing', 'slide', 'strip', 'whereas', 'wish', 'combine', 'command', 'dig', 'divide', 'equivalent', 'hang', 'hunt', 'initial', 'march', 'mention', 'spiritual', 'survey', 'tie', 'adult', 'brief', 'crazy', 'escape', 'gather', 'hate', 'prior', 'repair', 'rough', 'sad', 'scratch', 'sick', 'strike', 'employ', 'external', 'hurt', 'illegal', 'laugh', 'lay', 'mobile', 'nasty', 'ordinary', 'respond', 'royal', 'senior', 'split', 'strain', 'struggle', 'swim', 'train', 'upper', 'wash', 'yellow', 'convert', 'crash', 'dependent', 'fold', 'funny', 'grab', 'hide', 'miss', 'permit', 'quote', 'recover', 'resolve', 'roll', 'sink', 'slip', 'spare', 'suspect', 'sweet', 'swing', 'twist', 'upstairs', 'usual', 'abroad', 'brave', 'calm', 'concentrate', 'estimate', 'grand', 'male', 'mine', 'prompt', 'quiet', 'refuse', 'regret', 'reveal', 'rush', 'shake', 'shift', 'shine', 'steal', 'suck', 'surround', 'anybody', 'bear', 'brilliant', 'dare', 'dear', 'delay', 'drunk', 'female', 'hurry', 'inevitable', 'invite', 'kiss', 'neat', 'pop', 'punch', 'quit', 'reply', 'representative', 'resist', 'rip', 'rub', 'silly', 'smile', 'spell', 'stretch', 'stupid', 'tear', 'temporary', 'tomorrow', 'wake', 'wrap', 'yesterday']
    word = choice(nouns).capitalize()
    while True:
        lettersList = list(word)
        shuffle(lettersList)
        scrambled = ''.join(lettersList)
        if scrambled == word:
            word = choice(nouns).capitalize()
        else:
            break
    embed = Embed(title='Word Scramble', colour=Colour.green())
    embed.add_field(name='Scrambled Word:', value=scrambled)
    embed.set_thumbnail(url='https://lh3.googleusercontent.com/proxy/SycvTldL4UfW1ijxo1JlVCaoEM6GMBHtrGsgtl_62-3CTTHvD2hlcKK2SqpxPM47m4orEPbakcSyG9D-wI7_Fa7BhbGVmv2t2ZbjLNbRNCOAx3LPg56HnlV-Cfn5JV20lzZsHxtjilY')
    await ctx.send(embed=embed)
    msg = await client.wait_for('message', check=lambda message: message.content.lower().capitalize() == word)
    embed = Embed(title='Word Scramble Winner', colour=Colour.green())
    embed.add_field(name='Winner:', value=msg.author.mention)
    embed.add_field(name='Word:', value=word)
    embed.set_thumbnail(url='https://lh3.googleusercontent.com/proxy/SycvTldL4UfW1ijxo1JlVCaoEM6GMBHtrGsgtl_62-3CTTHvD2hlcKK2SqpxPM47m4orEPbakcSyG9D-wI7_Fa7BhbGVmv2t2ZbjLNbRNCOAx3LPg56HnlV-Cfn5JV20lzZsHxtjilY')
    await ctx.send(embed=embed)


@client.command(name='time', aliases=['timein'])  # todo make it look better(embed) maybe add town picture here?
async def time(ctx, *, city):  # todo if you spell it wrong, the [38:40] (probably) is incorrect, add a fix like if it says they spelt it wrong, to get the proper info anyways
    query_string = plus(city)
    URL = f'https://www.google.com/search?q=current+time+in+{query_string}'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all("div")[38:40]
    results.extend(results[1].text.splitlines())
    del results[1]
    if ' p.m.' in results[0].text or ' a.m.' in results[0].text and 9 <= len(results[0].text) <= 10:  # FOR VM: if ' PM' in results[0].text or ' AM' in results[0].text and 7 <= len(results[0].text) <= 8:
        await ctx.send(f'The current time in {results[2][8:]} is: {results[0].text[:-1]} on {results[1]}.')  # FOR VM: results[0].text[:-1] is results[0].text[:]
    else:
        await ctx.send(f'{ctx.author.mention}, the place to check time for is not valid.', delete_after=5.0)


@time.error
async def time_error(ctx, error):
    if isinstance(error, errors.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.mention}, please enter a place to check time for.', delete_after=5.0)


@client.command(name='translate', aliases=['translator', 'googletranslate'])  # todo embed (maybe make it input the langue your word is from, die detects as german)
async def translate(ctx, *, wordtolang):
    objects = wordtolang.lower().split('from lang:')
    objects[0] = objects[0].strip().capitalize()
    objects.extend(objects[1].split('to lang:'))
    del objects[1]
    objects[1], objects[2] = objects[1].strip(), objects[2].strip()
    src, dest = '', ''
    if len(objects) == 3:
        if objects[1] != 'chinese':
            for key in googletrans.LANGUAGES.keys():
                if googletrans.LANGUAGES.get(key) == objects[1]:
                    src = key
        else:
            src = 'zh-cn'
        if objects[2] != 'chinese':
            for key in googletrans.LANGUAGES.keys():
                if googletrans.LANGUAGES.get(key) == objects[2]:
                    dest = key
        else:
            dest = 'zh-cn'
        if dest != '':
            embed = Embed(title='Lavish Translator', colour=Colour.blue())
            if src != '':
                translated = translator.translate(objects[0], src=src, dest=dest)
                embed.add_field(name=objects[1].capitalize(), value=objects[0])
            else:
                translated = translator.translate(objects[0], dest=dest)
                embed.add_field(name=googletrans.LANGUAGES[translator.detect(objects[0]).lang].capitalize(), value=objects[0])
            embed.add_field(name=objects[2].capitalize(), value=translated.text.capitalize())
            embed.set_thumbnail(url='https://seeklogo.com/images/G/google-translate-logo-66F8665D22-seeklogo.com.png')
            embed.set_footer(text='Translations are provided by Google Translate')
            await ctx.send(embed=embed)
        else:
            if dest == '' and src == '':
                await ctx.send(f'{ctx.author.mention}, {objects[1]} and {objects[2]} are not valid countries.', delete_after=5.0)
            elif dest == '':
                await ctx.send(f'{ctx.author.mention}, {objects[2]} is not a valid country.', delete_after=5.0)
    else:
        await ctx.send(f'{ctx.author.mention}, please enter: `.translate WORD/PHRASE from lang: LANGUAGE to lang: LANGUAGE`, it needs to be exact.', delete_after=10.0)


@translate.error
async def translate_error(ctx, error):
    if isinstance(error, errors.CommandInvokeError):
        await ctx.send(f'{ctx.author.mention}, please enter: `.translate WORD/PHRASE from lang: LANGUAGE to lang: LANGUAGE`, it needs to be exact.', delete_after=10.0)
    elif isinstance(error, errors.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.mention}, please enter: `.translate WORD/PHRASE from lang: LANGUAGE to lang: LANGUAGE`, it needs to be exact.', delete_after=10.0)


######################################
#                                    #
#             MOD TOOLS              #
#                                    #
######################################
@client.command(name='kick')
@has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member=None, *, reason=None): #todo maybe change the error message for when someone does these in a dm
    if ctx.guild.roles.index(ctx.author.top_role) > ctx.guild.roles.index(member.top_role) and member != ctx.guild.owner or ctx.author == ctx.guild.owner:
        await member.kick(reason=reason), await ctx.send(f'Kick successful on {member} :wave:', delete_after=5.0)
    elif member == ctx.guild.owner:
        await ctx.send('You cannot kick the owner of the server.', delete_after=5.0)
    else:
        await ctx.send(f"{ctx.author.mention}, you don't have enough permission to do that! :slight_frown:", delete_after=5.0)


@kick.error
async def kick_error(ctx, error):
    if isinstance(error, errors.MissingPermissions):
        await ctx.send(f"{ctx.author.mention}, you don't have enough permission to do that! :slight_frown:", delete_after=5.0)
    elif isinstance(error, errors.CommandInvokeError):
        if str(error) == 'Command raised an exception: Forbidden: 403 FORBIDDEN (error code: 50013): Missing Permissions':
            await ctx.send("My role is too low or I don't have enough permissions to kick that user.", delete_after=20.0) # todo add a explination for all errors individually on the website
        else:
            await ctx.send('Please enter someone to kick.', delete_after=5.0)
    elif isinstance(error, errors.BadArgument):
        await ctx.send('The user entered was invalid or is not in this server.', delete_after=5.0)


@client.command(name='ban')
@has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member=None, *, reason=None):
    if ctx.guild.roles.index(ctx.author.top_role) > ctx.guild.roles.index(member.top_role) and member != ctx.guild.owner or ctx.author == ctx.guild.owner:
        await member.ban(reason=reason), await ctx.send(f'Ban successful on {member} :wave:', delete_after=5.0)
    elif member == ctx.guild.owner:
        await ctx.send('You cannot ban the owner of the server.', delete_after=5.0)
    else:
        await ctx.send(f"{ctx.author.mention}, you don't have enough permission to do that! :slight_frown:", delete_after=5.0)


@ban.error
async def ban_error(ctx, error):
    if isinstance(error, errors.MissingPermissions):
        await ctx.send(f"{ctx.author.mention}, you don't have enough permission to do that! :slight_frown:", delete_after=5.0)
    elif isinstance(error, errors.CommandInvokeError):
        if str(error) == 'Command raised an exception: Forbidden: 403 FORBIDDEN (error code: 50013): Missing Permissions':
            await ctx.send("My role is too low or I don't have enough permissions to ban that user.", delete_after=20.0) #todo change delete after later for these
        else:
            await ctx.send('Please enter someone to ban.', delete_after=5.0)
    elif isinstance(error, errors.BadArgument):
        await ctx.send('The user entered was invalid or is not in this server.', delete_after=5.0)


@client.command(name='unban')
@has_permissions(ban_members=True)
async def unban(ctx, *, member):
    for BanEntry in await ctx.guild.bans():
        if member == str(BanEntry.user):
            await ctx.guild.unban(BanEntry.user), await ctx.send(f'Unban successful on {member}.', delete_after=5.0)


@unban.error
async def unban_error(ctx, error):
    if isinstance(error, errors.MissingPermissions):
        await ctx.send(f"{ctx.author.mention}, you don't have enough permission to do that! :slight_frown:", delete_after=5.0)
    elif isinstance(error, errors.CommandInvokeError):
        await ctx.send("I don't have enough permissions to unban users in this server.", delete_after=20.0)
    elif isinstance(error, errors.MissingRequiredArgument):
        await ctx.send('Please enter someone to unban.', delete_after=5.0)


@client.command(name='unbanall')
@has_permissions(ban_members=True)
async def unbanall(ctx):
    if len(await ctx.guild.bans()) > 0:
        bannedusers = len(await ctx.guild.bans())
        await ctx.send(f'Are you sure you would like to unban {bannedusers} user(s) from the server? `yes` or `no`')
        msg = await client.wait_for('message', check=lambda message: message.author == ctx.author and (message.content.lower() == 'yes' or message.content.lower() == 'no' or message.content.lower() == 'y' or message.content.lower() == 'n'))
        if msg.content.lower().startswith('y'):
            for BanEntry in await ctx.guild.bans():
                await ctx.guild.unban(BanEntry.user)
            await ctx.send(f'You have successfully unbanned {bannedusers} user(s) from the server.')
        else:
            await ctx.send('Unbanall cancelled.', delete_after=5.0)
    else:
        await ctx.send('Your server has 0 banned members.', delete_after=5.0)


@unbanall.error
async def unbanall_error(ctx, error):
    if isinstance(error, errors.MissingPermissions):
        await ctx.send(f"{ctx.author.mention}, you don't have enough permission to do that! :slight_frown:", delete_after=5.0)
    elif isinstance(error, errors.CommandInvokeError):
        await ctx.send("I don't have enough permissions to unban users in this server.", delete_after=20.0) # todo say how to fix later on website(or make message longer to explain) (all errors)


@client.command(name='purge')
@has_permissions(manage_messages=True)
async def purge(ctx, amount: int):  # todo add confirmation for 100+ messages
    if amount > 0:
        await ctx.channel.purge(limit=amount+1), await ctx.send(f'Successfully deleted {amount} message(s). :thumbsup:', delete_after=5.0)
    elif amount == 0:
        confirm = await ctx.send(f'Are you sure you would like to delete EVERY message in {ctx.message.channel}? `yes` or `no`') # todo make this delete after yes or no is said
        msg = await client.wait_for('message', check=lambda message: message.author == ctx.author and (message.content.lower() == 'yes' or message.content.lower() == 'no' or message.content.lower() == 'y' or message.content.lower() == 'n'))
        if msg.content.lower().startswith('y'):
            await ctx.channel.purge(limit=None), await ctx.send(f'Successfully deleted all messages in {ctx.message.channel}. :thumbsup:', delete_after=5.0)
        else:
            await ctx.send('Purge cancelled.', delete_after=5.0)
            await confirm.edit(delete_after=5.0)
    elif amount < 0:
        await ctx.send('You cannot delete negative messages, nice try! :smile:', delete_after=5.0)


@purge.error
async def purge_error(ctx, error):
    if isinstance(error, errors.MissingPermissions):
        await ctx.send(f"{ctx.author.mention}, you don't have enough permission to do that! :slight_frown:", delete_after=5.0)
    elif isinstance(error, errors.BadArgument) or isinstance(error, errors.MissingRequiredArgument): # bad argument is if they didn't input a int, missing required argument is if they input nothing
        await ctx.send(f'{ctx.author.mention}, please input a number of messages to purge.', delete_after=5.0)
    elif isinstance(error, errors.CommandInvokeError):
        await ctx.send(f"{ctx.author.mention}, I don't have enough permissions to delete messages in this server.", delete_after=20.0)


######################################
#                                    #
#            WEATHER API             #
#                                    #
######################################
@client.command(name='weather', aliases=['weatherhelp'])  # todo maybe allow weather c city?
async def weather(ctx):
    await ctx.send(f'{ctx.author.mention}, do `.weatherc` to get the temperature in Celsius or `.weatherf` to get the temperature in Fahrenheit. To get more specific towns, seperate the town and the country names by a comma: (Ex: New York,US)', delete_after=25.0)


@client.command(name='weatherC')
async def weatherC(ctx, *, city): #todo make the more info work for buffalo, than fucking
    town = city.title()
    cityw = mgr.weather_at_place(city)
    w = cityw.weather
    # reg = owm.city_id_registry()
    # cityid = 0
    # minfo = True
    # if len(reg.ids_for(city)) != 0:
    #     for i in reg.ids_for(city):
    #         testcity = owm.weather_at_id(i[0])
    #         w2 = testcity.get_weather()
    #         if w.get_temperature("celsius")["temp"] == w2.get_temperature("celsius")["temp"]:
    #             cityid = i[0]
    #             break
    # else:
    #     try:
    #         cityid = reg.ids_for(city.split(',')[0], country=city.split(',')[1].upper())[0][0]
    #     except:
    #         minfo = False
    if float(w.temperature("celsius")["temp"]) > 0:
        embed = Embed(title=town, colour=Colour.red())
    else:
        embed = Embed(title=town, colour=Colour.blue())
    # query_string = plus(town)
    # URL = 'https://www.google.com/search?q=' + query_string + '&source=lnms&tbm=isch'
    # webpage = requests.get(URL)
    # soup = BeautifulSoup(webpage.content, 'html.parser')
    # for link in soup.find_all('img')[4:len(soup.find_all('img'))-15]:
    #     try:
    #         embed.set_image(url=link.get('src'))  # todo images aren't full size, try to get full sized images
    #         break
    #     except:
    #         pass
    embed.add_field(name='Temperature', value=f'{w.temperature("celsius")["temp"]}°C')
    embed.add_field(name='Forecast', value=f'{w.detailed_status.capitalize()}')
    # if minfo and cityid != 0:
    #     embed.add_field(name='More Info', value=f'https://openweathermap.org/city/{cityid}', inline=False)
    embed.set_thumbnail(url=w.weather_icon_url())
    await ctx.send(embed=embed)
    #await ctx.send(f'The current weather in {town} is {w.get_temperature("celsius")["temp"]}°C with a forcast of {w.get_detailed_status()}.')


@weatherC.error
async def weatherC_error(ctx, error):
    if isinstance(error, errors.CommandInvokeError):
        await ctx.send(f'{ctx.author.mention}, the city you entered is not a valid city.', delete_after=5.0)
    elif isinstance(error, errors.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.mention}, please enter a city to check the weather for.', delete_after=5.0)


@client.command(name='weatherF')
async def weatherF(ctx, *, city):
    town = city.title()
    cityw = mgr.weather_at_place(city)
    w = cityw.weather
    if float(w.temperature("fahrenheit")["temp"]) > 32:
        embed = Embed(title=town, colour=Colour.red())
    else:
        embed = Embed(title=town, colour=Colour.blue())
    embed.add_field(name='Temperature', value=f'{w.temperature("fahrenheit")["temp"]}°F')
    embed.add_field(name='Forecast', value=f'{w.detailed_status().capitalize()}')
    embed.set_thumbnail(url=w.weather_icon_url())
    await ctx.send(embed=embed)


@weatherF.error
async def weatherF_error(ctx, error):
    if isinstance(error, errors.CommandInvokeError):
        await ctx.send(f'{ctx.author.mention}, the city you entered is not a valid city.', delete_after=5.0)
    elif isinstance(error, errors.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.mention}, please enter a city to check the weather for.', delete_after=5.0)


######################################
#                                    #
#            CONVERSIONS             #
#                                    #
######################################
@client.command(name='convert', aliases=['conversion', 'conversions']) #todo add a errors section, ADD ELSE TO END
async def convert(ctx, unit1, unit2, num: float=None):
    unit1 = unit1.lower()
    unit2 = unit2.lower()

    # TEMPERATURES #

    if unit1 == 'c' or unit1 == 'celsius':
        if unit2 == 'f' or unit2 == 'fahrenheit':
            if num is None:
                await ctx.send(f'{0}°C = {32}°F (values rounded)')
            else:
                await ctx.send(f'{removeTrailingZeros(num)}°C = {removeTrailingZeros(round((num * 9 / 5) + 32, 2))}°F (values rounded)')
        elif unit2 == 'k' or unit2 == 'kelvin':
            if num is None:
                await ctx.send(f'{0}°C = {273.15}K (values rounded)')
            else:
                await ctx.send(f'{removeTrailingZeros(num)}°C = {removeTrailingZeros(round(num + 273.15, 2))}K (values rounded)')
    elif unit1 == 'f' or unit1 == 'fahrenheit':
        if unit2 == 'c' or unit2 == 'celsius':
            if num is None:
                await ctx.send(f'{0}°F = {-17.78}°C (values rounded)')
            else:
                await ctx.send(f'{removeTrailingZeros(num)}°F = {removeTrailingZeros(round((num - 32) * (5 / 9), 2))}°C (values rounded)')
        elif unit2 == 'k' or unit2 == 'kelvin':
            if num is None:
                await ctx.send(f'{0}°F = {255.37}K (values rounded)')
            else:
                await ctx.send(f'{removeTrailingZeros(num)}°F = {removeTrailingZeros(round((num - 32) * (5 / 9) + 273.15, 2))}K (values rounded)')
    elif unit1 == 'k' or unit1 == 'kelvin':
        if unit2 == 'c' or unit2 == 'celsius':
            if num is None:
                await ctx.send(f'{0}K = {-273.15}°C (values rounded)')
            else:
                await ctx.send(f'{removeTrailingZeros(num)}K = {removeTrailingZeros(round(num - 273.15, 2))}°C (values rounded)')
        elif unit2 == 'f' or unit2 == 'fahrenheit':
            if num is None:
                await ctx.send(f'{0}K = {-459.67}°F (values rounded)')
            else:
                await ctx.send(f'{removeTrailingZeros(num)}K = {removeTrailingZeros(round((num - 273.15) * 9 / 5 + 32, 2))}°F (values rounded)')

    # MEASUREMENTS #

    # TIME #

    elif 'sec' in unit1:
        if 'min' in unit2:
            if num is None:
                await ctx.send(f'{1} second = {0.0167} minutes (values rounded)')
            else:
                await ctx.send(f'{removeTrailingZeros(num)} second(s) = {removeTrailingZeros(round(num / 60, 4))} minute(s) (values rounded)')
        elif 'hour' in unit2:
            if num is None:
                await ctx.send(f'{1} second = {0.000278} hours (values rounded)')
            else:
                await ctx.send(f'{removeTrailingZeros(num)} second(s) = {removeTrailingZeros(round(num / 3600, 6))} hour(s) (values rounded)')
        elif 'day' in unit2:
            if num is None:
                await ctx.send(f'{1} second = {0.00001157} days (values rounded)')
            else:
                await ctx.send(f'{removeTrailingZeros(num)} second(s) = {removeTrailingZeros(round(num / 86400, 8))} day(s) (values rounded)')
    elif 'min' in unit1:
        if 'sec' in unit2:
            if num is None:
                await ctx.send(f'{1} minute = {60} seconds (values rounded)')
            else:
                await ctx.send(f'{removeTrailingZeros(num)} minute(s) = {removeTrailingZeros(round(num * 60, 2))} second(s) (values rounded)')
        elif 'hour' in unit2:
            if num is None:
                await ctx.send(f'{1} minute = {0.0167} hours (values rounded)')
            else:
                await ctx.send(f'{removeTrailingZeros(num)} minute(s) = {removeTrailingZeros(round(num / 60, 4))} hour(s) (values rounded)')
        elif 'day' in unit2:
            if num is None:
                await ctx.send(f'{1} minute = {0.00069} days (values rounded)')
            else:
                await ctx.send(f'{removeTrailingZeros(num)} minute(s) = {removeTrailingZeros(round(num / 1440, 5))} day(s) (values rounded)')
    elif 'hour' in unit1:
        if 'sec' in unit2:
            if num is None:
                await ctx.send(f'{1} hour = {3600} seconds (values rounded)')
            else:
                await ctx.send(f'{removeTrailingZeros(num)} hour(s) = {removeTrailingZeros(round(num * 3600, 2))} second(s) (values rounded)')
        elif 'min' in unit2:
            if num is None:
                await ctx.send(f'{1} hour = {60} minutes (values rounded)')
            else:
                await ctx.send(f'{removeTrailingZeros(num)} hour(s) = {removeTrailingZeros(round(num * 60, 2))} minute(s) (values rounded)')
        elif 'day' in unit2:
            if num is None:
                await ctx.send(f'{1} hour = {0.0417} days (values rounded)')
            else:
                await ctx.send(f'{removeTrailingZeros(num)} hour(s) = {removeTrailingZeros(round(num / 24, 4))} day(s) (values rounded)')
    elif 'day' in unit1:
        if 'sec' in unit2:
            if num is None:
                await ctx.send(f'{1} day = {86400} seconds (values rounded)')
            else:
                await ctx.send(f'{removeTrailingZeros(num)} day(s) = {removeTrailingZeros(round(num * 86400, 2))} seconds(s) (values rounded)')
        elif 'min' in unit2:
            if num is None:
                await ctx.send(f'{1} day = {1440} minutes (values rounded)')
            else:
                await ctx.send(f'{removeTrailingZeros(num)} day(s) = {removeTrailingZeros(round(num * 1440, 2))} minute(s) (values rounded)')
        elif 'hour' in unit2:
            if num is None:
                await ctx.send(f'{1} day = {24} hours (values rounded)')
            else:
                await ctx.send(f'{removeTrailingZeros(num)} day(s) = {removeTrailingZeros(round(num * 24, 2))} hour(s) (values rounded)')


# @client.event
# async def on_raw_reaction_add(payload):
#     if payload.message_id == 692511298839117836:
#         guild = client.get_guild(payload.guild_id)
#         member = guild.get_member(payload.user_id)
#         role = guild.get_role(692468151623090257)
#         #role = discord.utils.get(guild.roles, name='Lavish Crew')
#         await member.add_roles(role)


# @client.event
# async def on_raw_reaction_remove(payload):
#     if payload.message_id == 692511298839117836:
#         guild = client.get_guild(payload.guild_id)
#         member = guild.get_member(payload.user_id)
#         role = guild.get_role(692468151623090257)
#         #role = discord.utils.get(guild.roles, name='Lavish Crew')
#         await member.remove_roles(role)


# @client.command()
# async def ci(ctx):
#     await ctx.channel.purge(limit=1)
#     for i in range(5):
#         await ctx.channel.create_invite()


@client.event
async def on_member_join(member):
    if member.guild.id == 691878463237259315:  # my guild
        channel = client.get_channel(692779960552652860)  # my join/leave log
        embed = Embed(description=f'{member.mention}\n{member} ({member.id})', colour=Colour.green())
        embed.set_author(name='Member Joined', icon_url=member.avatar_url)
        embed.set_footer(text=f'{member.guild} | {len(member.guild.members)} members')
        await channel.send(embed=embed)
        channel = client.get_channel(692814360569184257)  # my mod log
        embed.set_footer(text=datetime.datetime.now().strftime("%m/%d/%Y %I:%M %p"))
        await channel.send(embed=embed)


@client.event
async def on_member_remove(member):
    if member.guild.id == 691878463237259315:
        channel = client.get_channel(692779960552652860)
        embed = Embed(description=f'{member.mention}\n{member} ({member.id})', colour=Colour.red())
        embed.set_author(name='Member Left', icon_url=member.avatar_url)
        embed.set_footer(text=f'{member.guild} | {len(member.guild.members)} members')
        await channel.send(embed=embed)
        channel = client.get_channel(692814360569184257)  # my mod log
        embed.set_footer(text=datetime.datetime.now().strftime("%m/%d/%Y %I:%M %p"))
        await channel.send(embed=embed)


@client.event
async def on_member_ban(guild, user):
    if guild.id == 691878463237259315:
        channel = client.get_channel(692814360569184257)
        embed = Embed(description=f'{user.mention}\n{user} ({user.id})', colour=Colour.red())
        embed.set_author(name='Member Banned', icon_url=user.avatar_url)
        embed.set_footer(text=datetime.datetime.now().strftime("%m/%d/%Y %I:%M %p"))
        await channel.send(embed=embed)


@client.event
async def on_member_unban(guild, user):
    if guild.id == 691878463237259315:
        channel = client.get_channel(692814360569184257)
        embed = Embed(description=f'{user.mention}\n{user} ({user.id})', colour=Colour.green())
        embed.set_author(name='Member Unbanned', icon_url=user.avatar_url)
        embed.set_footer(text=datetime.datetime.now().strftime("%m/%d/%Y %I:%M %p"))
        await channel.send(embed=embed)


@client.event
async def on_member_update(before, after):
    if after.guild.id == 691878463237259315:
        channel = client.get_channel(692814360569184257)
        if before.nick != after.nick:
            if before.nick is None or after.nick is None:
                if before.nick is None:
                    embed = Embed(description=f'{after.mention}\n{before.name} → {after.nick}', colour=Colour.blue())
                else:
                    embed = Embed(description=f'{after.mention}\n{before.nick} → {after.name}', colour=Colour.blue())
            else:
                embed = Embed(description=f'{after.mention}\n{before.nick} → {after.nick}', colour=Colour.blue())
            embed.set_author(name='Member Changed Nickname', icon_url=after.avatar_url)
            embed.set_footer(text=datetime.datetime.now().strftime("%m/%d/%Y %I:%M %p"))
            await channel.send(embed=embed)
        elif before.roles != after.roles:
            if len(before.roles) > len(after.roles):
                role = [i for i in before.roles if i not in after.roles][0]
                embed = Embed(description=f'{after.mention}\nRole removed: {role.name}', colour=Colour.red())
                embed.set_author(name='Member Role Removed', icon_url=after.avatar_url)
            else:
                role = [i for i in after.roles if i not in before.roles][0]
                embed = Embed(description=f'{after.mention}\nRole added: {role.name}', colour=Colour.green())
                embed.set_author(name='Member Role Added', icon_url=after.avatar_url)
            embed.set_footer(text=f'Role ID: {role.id} | {datetime.datetime.now().strftime("%m/%d/%Y %I:%M %p")}')
            await channel.send(embed=embed)


@client.event
async def on_raw_message_edit(payload):
    if 'guild_id' in payload.data:
        if int(payload.data['guild_id']) == 691878463237259315:
            if 'content' in payload.data:
                guild = client.get_guild(int(payload.data['guild_id']))
                editedMessageChannel = client.get_channel(payload.channel_id)
                channel = client.get_channel(692814360569184257)
                if editedMessageChannel.category is not None:
                    embed = Embed(description=f'Message edited in {editedMessageChannel.mention}\nCategory: {editedMessageChannel.category}', colour=Colour.blue())
                else:
                    embed = Embed(description=f'Message edited in {editedMessageChannel.mention}', colour=Colour.blue())
                if payload.cached_message is not None:
                    embed.add_field(name='Before:', value=payload.cached_message.content)
                else:
                    embed.add_field(name='Before:', value=f'Before Message Not Found {unicodeEmotes.slightly_frown_face}')
                embed.add_field(name='After:', value=payload.data['content'], inline=False)
                embed.add_field(name='Message ID:', value=payload.message_id, inline=False)

                embed.set_author(name=f"{payload.data['author']['username']}#{payload.data['author']['discriminator']}",
                                 icon_url=guild.get_member(int(payload.data['author']['id'])).avatar_url)
                embed.set_footer(text=f"User ID: {payload.data['author']['id']} | {datetime.datetime.now().strftime('%m/%d/%Y %I:%M %p')}")
                await channel.send(embed=embed)


@client.event
async def on_raw_message_delete(payload):
    if payload.guild_id == 691878463237259315:
        guild = client.get_guild(payload.guild_id)
        deletedMessageChannel = client.get_channel(payload.channel_id)
        channel = client.get_channel(692814360569184257)
        if deletedMessageChannel.category is not None:
            embed = Embed(description=f'Message deleted in {deletedMessageChannel.mention}\nCategory: {deletedMessageChannel.category}', colour=Colour.red())
        else:
            embed = Embed(description=f'Message deleted in {deletedMessageChannel.mention}', colour=Colour.red())
        if payload.cached_message is not None:
            embed.add_field(name='Deleted Message:', value=payload.cached_message.content)
            embed.add_field(name='Message ID:', value=payload.message_id, inline=False)
            embed.set_author(name=f'{payload.cached_message.author.name}#{payload.cached_message.author.discriminator}',
                             icon_url=guild.get_member(payload.cached_message.author.id).avatar_url)
            embed.set_footer(text=f"User ID: {payload.cached_message.author.id} | {datetime.datetime.now().strftime('%m/%d/%Y %I:%M %p')}")
        else:
            embed.add_field(name='Deleted Message:', value=f'Deleted Message Not Found {unicodeEmotes.slightly_frown_face}')
            embed.add_field(name='Message ID:', value=payload.message_id, inline=False)
            embed.set_author(name=guild, icon_url=guild.icon_url)
            embed.set_footer(text=f'{datetime.datetime.now().strftime("%m/%d/%Y %I:%M %p")}')  # todo maybe try to make date changing like in dyno, and make them able to change timezone
        await channel.send(embed=embed)


@client.event
async def on_raw_bulk_message_delete(payload):
    if payload.guild_id == 691878463237259315:
        guild = client.get_guild(payload.guild_id)
        deletedMessagesChannel = client.get_channel(payload.channel_id)
        channel = client.get_channel(692814360569184257)
        if deletedMessagesChannel.category is not None:
            embed = Embed(description=f'{len(payload.message_ids)} messages deleted in {deletedMessagesChannel.mention}\nCategory: {deletedMessagesChannel.category}', colour=Colour.red())
        else:
            embed = Embed(description=f'{len(payload.message_ids)} messages deleted in {deletedMessagesChannel.mention}', colour=Colour.red())
        embed.set_author(name=guild, icon_url=guild.icon_url)
        embed.set_footer(text=datetime.datetime.now().strftime("%m/%d/%Y %I:%M %p"))
        await channel.send(embed=embed)


@client.event
async def on_guild_update(before, after):
    if after.id == 691878463237259315:
        if before.name != after.name:
            channel = client.get_channel(692814360569184257)
            embed = Embed(description=f'Server name changed', colour=Colour.blue())
            embed.add_field(name='Before:', value=before.name)
            embed.add_field(name='After:', value=after.name, inline=False)
            embed.set_author(name=after, icon_url=after.icon_url)
            embed.set_footer(text=f'Server ID: {after.id} | {datetime.datetime.now().strftime("%m/%d/%Y %I:%M %p")}')
            await channel.send(embed=embed)


@client.event
async def on_guild_channel_create(channel):
    if channel.guild.id == 691878463237259315:
        channelModLog = client.get_channel(692814360569184257)
        if channel.category is not None:
            embed = Embed(description=f'New channel created named {channel.name}\nCategory: {channel.category}', colour=Colour.green())
        else:
            embed = Embed(description=f'New channel created named {channel.name}', colour=Colour.green())
        embed.set_author(name=channel.guild, icon_url=channel.guild.icon_url)
        embed.set_footer(text=f'New Channel ID: {channel.id} | {datetime.datetime.now().strftime("%m/%d/%Y %I:%M %p")}')
        await channelModLog.send(embed=embed)


@client.event
async def on_guild_channel_delete(channel):
    if channel.guild.id == 691878463237259315:
        channelModLog = client.get_channel(692814360569184257)
        if channel.category is not None:
            embed = Embed(description=f'Channel {channel.name} deleted\nCategory: {channel.category}', colour=Colour.red())
        else:
            embed = Embed(description=f'Channel {channel.name} deleted', colour=Colour.red())
        embed.set_author(name=channel.guild, icon_url=channel.guild.icon_url)
        embed.set_footer(text=f'Deleted Channel ID: {channel.id} | {datetime.datetime.now().strftime("%m/%d/%Y %I:%M %p")}')  # todo maybe make the date of the servers home?
        await channelModLog.send(embed=embed)


@client.event
async def on_guild_channel_update(before, after):
    if after.guild.id == 691878463237259315:
        if before.name != after.name:
            channel = client.get_channel(692814360569184257)
            if after.category is not None:
                embed = Embed(description=f'Channel {before.name} renamed\nCategory: {before.category}', colour=Colour.blue())
            else:
                embed = Embed(description=f'Channel {before.name} renamed', colour=Colour.blue())
            embed.add_field(name='Before:', value=before.name)
            embed.add_field(name='After:', value=after.name, inline=False)
            embed.set_author(name=after.guild, icon_url=after.guild.icon_url)
            embed.set_footer(text=f'Renamed Channel ID: {after.id} | {datetime.datetime.now().strftime("%m/%d/%Y %I:%M %p")}')
            await channel.send(embed=embed)


@client.event
async def on_guild_role_create(role):
    if role.guild.id == 691878463237259315:
        channel = client.get_channel(692814360569184257)
        embed = Embed(description=f'Role **{role.name}** was created', colour=Colour.green())
        embed.set_author(name=role.guild, icon_url=role.guild.icon_url)
        embed.set_footer(text=f'Role ID: {role.id} | {datetime.datetime.now().strftime("%m/%d/%Y %I:%M %p")}')
        await channel.send(embed=embed)


@client.event
async def on_guild_role_delete(role):
    if role.guild.id == 691878463237259315:
        channel = client.get_channel(692814360569184257)
        embed = Embed(description=f'Role **{role.name}** was deleted', colour=Colour.red())
        embed.set_author(name=role.guild, icon_url=role.guild.icon_url)
        embed.set_footer(text=f'Role ID: {role.id} | {datetime.datetime.now().strftime("%m/%d/%Y %I:%M %p")}')
        await channel.send(embed=embed)


@client.event
async def on_guild_role_update(before, after):
    if after.guild.id == 691878463237259315:
        if before.name != after.name:
            channel = client.get_channel(692814360569184257)
            embed = Embed(description=f'Role **{before.name}** was renamed', colour=Colour.blue())
            embed.add_field(name='Before:', value=before.name)
            embed.add_field(name='After:', value=after.name, inline=False)
            embed.set_author(name=after.guild, icon_url=after.guild.icon_url)
            embed.set_footer(text=f'Role ID: {after.id} | {datetime.datetime.now().strftime("%m/%d/%Y %I:%M %p")}')
            await channel.send(embed=embed)


@client.event
async def on_guild_emojis_update(guild, before, after):
    if guild.id == 691878463237259315:
        channel = client.get_channel(692814360569184257)
        if len(before) == len(after):
            beforeList, afterList = [], []
            for emoji in before:
                beforeList.append(emoji.name)
            for emoji in after:
                afterList.append(emoji.name)
                afterList.append(emoji.id)
            s = set(beforeList)
            afterName = [x for x in afterList[::2] if x not in s][0]
            emoji = client.get_emoji(afterList[afterList.index(afterName) + 1])
            beforeName = beforeList[afterList.index(afterName) // 2]
            embed = Embed(description=f'Emoji **{beforeName}** was renamed <:{afterName}:{emoji.id}>', colour=Colour.blue())
            embed.add_field(name='Before:', value=beforeName)
            embed.add_field(name='After:', value=afterName, inline=False)
        elif len(before) > len(after):
            emoji = [i for i in before if i not in after][0]
            embed = Embed(description=f'Emoji **{emoji.name}** was removed', colour=Colour.red())
        else:
            emoji = [i for i in after if i not in before][0]
            embed = Embed(description=f'Emoji **{emoji.name}** was added <:{emoji.name}:{emoji.id}>', colour=Colour.green())
        embed.set_author(name=guild, icon_url=guild.icon_url)
        embed.set_footer(text=f'Emoji ID: {emoji.id} | {datetime.datetime.now().strftime("%m/%d/%Y %I:%M %p")}')
        await channel.send(embed=embed)


@client.event
async def on_voice_state_update(member, before, after):
    if member.guild.id == 691878463237259315:
        if before.channel != after.channel:
            channel = client.get_channel(692814360569184257)
            if before.channel is None:
                embed = Embed(description=f'{member.mention} joined VC: **{after.channel.name}**', colour=Colour.green())
                embed.add_field(name='Channel ID:', value=after.channel.id)
            elif after.channel is None:
                embed = Embed(description=f'{member.mention} left VC: **{before.channel.name}**', colour=Colour.red())
                embed.add_field(name='Channel ID:', value=before.channel.id)
            else:
                embed = Embed(description=f'{member.mention} moved from VC: **{before.channel.name}** to VC: **{after.channel.name}**', colour=Colour.blue())
                embed.add_field(name='Before Channel ID:', value=before.channel.id)
                embed.add_field(name='After Channel ID:', value=after.channel.id)
            embed.set_author(name=member, icon_url=member.avatar_url)
            embed.set_footer(text=f'User ID: {member.id} | {datetime.datetime.now().strftime("%m/%d/%Y %I:%M %p")}')
            await channel.send(embed=embed)


######################################
# MY COMMAND TO STOP RUNNING THE BOT #
######################################
@client.command()
async def endbot(ctx):
    botowner = client.get_user(client.owner_id)
    if str(ctx.author) == botowner:
        editFiles('usedchannelsslots', '[]')
        await client.logout()


######################################
#               TOKEN                #
######################################
client.run('KEY')
