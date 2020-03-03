from discord.ext import commands
from pymysql import IntegrityError
from datetime import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup

import discord
import pymysql.cursors
import threading

import pandas as pd

def get_token():
    f = open('token.txt', 'r')

    token = f.readline()
    return token
def get_database_configuration():
    f = open('dbconnect.txt', 'r')
    data = f.readline()
    host, usr, pw, db, charset = data.split(' ')
    db_connection = pymysql.connect(
        host=host,
        user=usr,
        password=pw,
        db=db,
        charset=charset
    )

    return db_connection
def add_user_command(user_command, real_command, author_id):
    sql = 'INSERT INTO user_commands (user_command, real_command, author_id) VALUES (%s, %s, %s)'
    curs.execute(sql, (user_command, real_command, str(author_id)))
    conn.commit()
def del_user_command(user_command, author_id):
    sql = 'DELETE FROM user_commands WHERE user_command=%s AND author_id=%s'
    curs.execute(sql, (user_command, str(author_id)))
    conn.commit()
def del_all_user_commands(author_id):
    sql = 'DELETE FROM user_commands WHERE author_id=%s'
    curs.execute(sql, (str(author_id), ))
    conn.commit()
def get_user_commands(author_id):
    sql = 'SELECT user_command, real_command, author_id FROM user_commands WHERE author_id=%s'
    curs.execute(sql, (str(author_id), ))
    conn.commit()

    return curs
def search_user_command(user_command, author_id):
    sql = 'SELECT user_command, real_command FROM user_commands WHERE user_command=%s and author_id=%s'
    curs.execute(sql, (user_command, str(author_id), ))
    conn.commit()

    return curs

COVID = None
update = None
def get_COVID19_status():
    global COVID
    global update
    columns = ['확진환자(증감)', '확진환자(총합)', '확진환자(격리)', '확진환자(해제)', '확진환자(사망)', '검사현황(총합)', '검사현황(진행중)', '검사현황(음성)', '총계']
    html = urlopen("http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=13&ncvContSeq=&contSeq=&board_id=&gubun=")

    bs = BeautifulSoup(html, "html.parser")
    update = bs.find('p', attrs={'class': 'info'}).find('span').text
    table = bs.find('table', attrs={'class': 'num'})
    trs = table.find_all('tr')
    columndata = []
    regions = []
    for idx, tr in enumerate(trs):
        if idx > 1:
            data = []
            regions.append(tr.find('th').text)
            tds = tr.find_all('td')
            for td in tds:
                data.append(td.text.strip())
            columndata.append(data)

    COVID = pd.DataFrame(columndata, columns=columns, index=regions)

    threading.Timer(7200, get_COVID19_status).start()

token = get_token()
bot = commands.Bot(command_prefix='.')
bot.remove_command('help')
conn = get_database_configuration()
curs = conn.cursor()

# bot EVENT
@bot.event
async def on_ready():
    get_COVID19_status()
    activity = discord.Game(name='(.도움말 ← 사용방법)')
    await bot.change_presence(status=discord.Status.online, activity=activity)

    print('ready')
@bot.event
async def on_message(ctx):
    if ctx.author == bot.user:
        return

    if ctx.content.startswith('$'):
        content = ctx.content
        commands = search_user_command(content[1:], ctx.author.id)
        for user_command, real_command in commands:
            await ctx.channel.send(real_command)

    await bot.process_commands(ctx)

# bot crawling
@bot.command()
async def 코로나(ctx):
    content = ctx.message.content

    # all_regions = data.loc[['합계'], ['확진환자(격리)', '확진환자(사망)', '검사현황(진행중)']]
    # for idx, data in enumerate(content):
    #     print(f'{idx} {data}')

    region_data = None
    if len(content) > 4:
        region = content[5:]
        if region in COVID.index.tolist():
            region_data = COVID.loc[[region], ['확진환자(격리)', '확진환자(사망)', '확진환자(사망)']].values
        else:
            regions = COVID.index.values
            await ctx.channel.send(f'검색가능지역 {regions}')
    else:
        region = '합계'
        region_data = COVID.loc[[region], ['확진환자(격리)', '확진환자(해제)', '확진환자(사망)']].values

    embed = discord.Embed(colour=discord.Colour.red(), title=f'<{region}> 지역 COVID-19 정보')
    embed.set_author(name=bot.user, icon_url=bot.user.avatar_url)
    embed.set_thumbnail(url='http://www.cdc.go.kr/cdc/img/main/h1_logo.png')
    embed.add_field(name='확진(격리)', value=f'{region_data[0][0]}', inline=True)
    embed.add_field(name='확진(해제)', value=f'{region_data[0][1]}', inline=True)
    embed.add_field(name='확진(사망)', value=f'{region_data[0][2]}', inline=True)
    embed.set_footer(text=f'질병관리본부 {update}')
    await ctx.channel.send(embed=embed)


# bot user_command
@bot.command()
async def 추가(ctx):
    author = ctx.author
    content = ctx.message.content

    commands = content.split(' ')
    user_command = commands[1]
    real_command = ' '.join(commands[2:])
    try:
        add_user_command(user_command, real_command, ctx.author.id)
        await ctx.channel.send(f'[{ctx.author}] {user_command}: {real_command} 명령어 추가완료')
    except IntegrityError:
        await ctx.channel.send(f'`{user_command}` <- 이미 저장된 명령어입니다.')
@bot.command()
async def 삭제(ctx):
    user_command = ctx.message.content[4:]
    del_user_command(user_command, ctx.author.id)
    await ctx.channel.send(f'{user_command} 명령어가 성공적으로 삭제되었습니다.')
@bot.command()
async def 전부삭제(ctx):
    del_all_user_commands(ctx.author.id)
    await ctx.channel.send(f'{ctx.author}의 모든 사용자 명령어가 삭제되었습니다.')
@bot.command()
async def 명령어(ctx):
    commands = get_user_commands(ctx.author.id)

    embed = discord.Embed(
        colour=discord.Colour.blue()
    )
    embed.set_author(name=f'{ctx.author} 명령어', icon_url=ctx.author.avatar_url)
    for user_command, real_command, _ in commands:
        embed.add_field(name=f'${user_command}', value=real_command, inline=False)
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    embed.set_footer(text=time)

    await ctx.channel.send(embed=embed)


# bot other
@bot.command()
async def 도움말(ctx):
    embed = discord.Embed(colour=discord.Colour.orange())
    embed.set_author(name='명령어 사용방법')
    embed.add_field(name='.코로나', value='코로나 현황판 보기', inline=False)
    embed.add_field(name='.코로나 지역명', value='코로나 지역 현황판 보기', inline=False)
    embed.add_field(name='.추가 명령어 출력문구(띄어쓰기가능)', value='사용자 명령어 등록', inline=False)
    embed.add_field(name='.삭제 명령어', value='사용자 명령어 삭제', inline=False)
    embed.add_field(name='.전부삭제', value='사용자 명령어 전부 삭제', inline=False)
    embed.add_field(name='.명령어', value='저장된 사용자 명령어 보기', inline=False)
    embed.add_field(name='$사용자명령어', value='사용자가 지정한 대로 출력', inline=False)
    await ctx.channel.send(embed=embed)

@bot.command()
async def test(ctx):
    pass

bot.run(token)