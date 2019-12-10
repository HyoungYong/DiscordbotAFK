import discord
import asyncio
from discord.ext import commands
import pymysql.cursors
from pymysql import IntegrityError

TOKEN = ''
client = commands.Bot(command_prefix='.')
client.remove_command('help')

conn = pymysql.connect(
        host='127.0.0.1',
        user='',
        password='',
        db='r6sDiscordBotAFK',
        charset='utf8'
)
curs = conn.cursor()

# addCustomCommand(cmd, actualCmd, author.id)
def addCustomCommand(CMD, ACTUAL_CMD, AUTHOR_ID):
    sql = 'INSERT INTO CUSTOM_COMMAND (SHORT_COMMAND, ACTUAL_COMMAND, AUTHOR_ID) VALUES (%s, %s, %s)'
    curs.execute(sql, (CMD, ACTUAL_CMD, str(AUTHOR_ID)))
    conn.commit()

# delCustomCommand(cmd)
def delCustomCommand(CMD):
    sql = 'DELETE FROM CUSTOM_COMMAND WHERE SHORT_COMMAND=%S AND %s'
    curs.execute(sql, (CMD, ))
    conn.commit()

# delCustomCommandAll()
def delCustomCommandAll():
    sql = 'DELETE FROM CUSTOM_COMMAND'
    curs.execute(sql, )
    conn.commit()

# getCustomCommandList()
def getCustomCommandList():
    sql = 'SELECT SHORT_COMMAND, ACTUAL_COMMAND, AUTHOR_ID FROM CUSTOM_COMMAND'
    curs.execute(sql, )
    conn.commit()

    return curs

def searchCustomCommand(CMD):
    sql = 'SELECT SHORT_COMMAND, ACTUAL_COMMAND FROM CUSTOM_COMMAND WHERE SHORT_COMMAND=%s'
    curs.execute(sql, (CMD, ))
    conn.commit()

    return curs

@client.event
async def on_ready():
    print('Bot is ready')
    
    activity = discord.Game(name='.help < 사용방법')
    await client.change_presence(status=discord.Status.online, activity=activity)


@client.event
async def on_message(ctx):
    # 자기 자신에 반응 X
    if ctx.author == client.user:
        return

    # 사용자 임의 명령어
    if ctx.content.startswith('$'):
        cmds = searchCustomCommand(ctx.content[1:])
        for SHORT_COMMAND, ACTUAL_COMMAND in cmds:
            print('{}: {}'.format(SHORT_COMMAND, ACTUAL_COMMAND))
            await ctx.channel.send(ACTUAL_COMMAND)

    await client.process_commands(ctx)

# 봇 사용자 추가
@client.command(pass_context=True)
@commands.has_role('가입 심사자')
async def adduser(ctx):
    author = ctx.author
    content = ctx.message.content

    tmp = content.split(' ')
    usr = client.get_user(int(tmp[1][2:-1]))

    # DB 사용자 추가 (디스코드 고유ID(숫자), 결정권자)
    # addMember(usr.id, str(author.id))
    print("{} added {}".format(author, usr))

# 봇 사용자 제거
@client.command(pass_context=True)
@commands.has_role('가입 심사자')
async def deluser(ctx):
    author = ctx.author
    content = ctx.message.content

    tmp = content.split(' ')
    usr = client.get_user(int(tmp[1][2:-1]))

    # DB 사용자 추가 (디스코드 고유ID(숫자), 결정권자)
    # delMember(usr.id)
    print("{} deleted {}".format(author, usr))

# getCC
@client.command(pass_context=True)
@commands.has_role('AFK 잠수중')
async def ccl(ctx):
    channel = ctx.channel

    commandList = getCustomCommandList()

    embed = discord.Embed(
        colour=discord.Colour.blue()
    )
    embed.set_author(name='사용자 임의 명령어 리스트')
    for cmd, acmd, aus in commandList:
        ausName = client.get_user(int(aus))
        cmdTemplate = '${} <{}>'.format(cmd, ausName)
        embed.add_field(name=cmdTemplate, value=acmd, inline=False)
    await channel.send(embed=embed)

# addCustomCommand <명령어>|<출력될 문구>
@client.command(pass_context=True)
@commands.has_role('AFK 잠수중')
async def addcc(ctx):
    author = ctx.author
    channel = ctx.channel
    content = ctx.message.content

    cmd, actualCmd = content[7:].split('|')
    try:
        addCustomCommand(cmd, actualCmd, author.id)
        await channel.send("{} <- {} 명령어가 성공적으로 추가되었습니다.".format(cmd, actualCmd))
    except IntegrityError:
        await channel.send("이미 사용되고 있는 명령어입니다".format(cmd, actualCmd))


# delCustomCommand <명령어>
@client.command(pass_context=True)
@commands.has_role('AFK 잠수중')
async def delcc(ctx):
    channel = ctx.channel
    content = ctx.message.content

    cmd = content[7:]
    delCustomCommand(cmd)
    await channel.send("{} 명령어가 성공적으로 삭제되었습니다.".format(cmd))

# delCustomCommandAll
@client.command(pass_context=True)
@commands.has_role('AFK 잠수중')
async def delccall(ctx):
    channel = ctx.channel

    delCustomCommandAll()
    await channel.send("모든 사용자 명령어가 성공적으로 삭제되었습니다.")

# help
@client.command(pass_context=True)
@commands.has_role('AFK 잠수중')
async def help(ctx):
    channel = ctx.channel

    embed = discord.Embed(
        colour=discord.Colour.orange()
    )
    embed.set_author(name='명령어 리스트 및 사용방법')
    embed.add_field(name='[제작중].adduser <유저명>', value='봇 사용자 추가', inline=False)
    embed.add_field(name='[제작중].deluser <유저명>', value='봇 사용자 제거', inline=False)
    embed.add_field(name='[제작중].addcc <명령어>|<출력될 문구>', value='addCustomCommand 사용자 임의 명령어 추가( <명령어> 구간에 띄어쓰기 하시면 안되요 )', inline=False)
    embed.add_field(name='.delcc <명령어>', value='delCustomCommand 사용자 임의 명령어 제거', inline=False)
    embed.add_field(name='.delccall', value='delCustomCommandAll 모든 사용자 임의 명령어 제거', inline=False)
    embed.add_field(name='.ccl', value='CustomCommandList 사용자 명령어 리스트 출력', inline=False)
    embed.add_field(name='$<사용자임의명령어>', value='사용자가 지정한 대로 출력', inline=False)
    await channel.send(embed=embed)

client.run(TOKEN)