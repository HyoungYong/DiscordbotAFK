import discord
import datetime
import pymysql.cursors

token = 'NTI2MDk2MzUzNzQzNjAxNjg2.Xe6PWw.eNJzuROAKUQ2k9RcFk0xWkGdeH4'
client = discord.Client()

#[DATABASE CONNECTION]######################################
# Database Connect
conn = pymysql.connect(
        host='127.0.0.1',
        user='afk',
        password='afk',
        db='r6sDiscordBotAFK',
        charset='utf8'
)
curs = conn.cursor()
#######################################

#[DATABASE COMMANDS]######################################
# Add Member
def addMember(MEMBER_INDEX, MEMBER_ID, MEMBER_LEVEL=1):
    sql = 'INSERT INTO members (MEMBER_INDEX, MEMBER_ID) VALUES (%s, %s)'
    curs.execute(sql, (MEMBER_INDEX, MEMBER_ID,))
    conn.commit()

# 웹 경로 추가
def addWebData(LINK_NAME, LINK_URL, REG_USER):
    now = datetime.datetime.now()
    sql = 'INSERT INTO R6S_LINKS (LINK_NAME, LINK_URL, REG_USER, REG_DT) VALUES (%s, %s, %s, %s)'
    curs.execute(sql, (LINK_NAME, LINK_URL, REG_USER, now))
    conn.commit()

# 웹 경로 불러오기
def getWebData():
    sql = 'SELECT * from R6S_LINKS'
    curs.execute(sql)
    return curs.fetchall()
#######################################

# if message.content == '$AFK-HAN':
#     embed = discord.Embed(title="AFK-HAN", description="자신도 모르는 세 정점에 도달한 한 남자의 이야기", color=0x00ff00)
#     embed.add_field(name="생일", value="안알려줌", inline=False)
#     embed.add_field(name="트위치 홈페이지", value="https://www.twitch.tv/han91", inline=False)
#     file = discord.File("./han.PNG", filename="han.png")
#     embed.set_image(url="attachment://han.png")
#     embed.add_field(name="IDs", value="JUVE_HAN._.", inline=False)
#     embed.add_field(name="공격", value="하드브리처", inline=True)
#     embed.add_field(name="수비", value="앵커", inline=True)
#     embed.timestamp = datetime.datetime.now()
#     await message.channel.send(file=file, embed=embed)


@client.event
async def on_ready():
    print('Logged on as '+f'{client.user}')
    activity = discord.Game(name="우어어어어어어어")
    await client.change_presence(status=discord.Status.idle, activity=activity)

@client.event
async def on_message(message):
    # don't respond to ourselves
    if message.author == client.user:
        return

    # 멤버 추가
    if message.content[:4] == "$add":
        print("ADD member")
        tempID = message.content[5:]
        addMember(message.author.id, tempID)
        await message.channel.send("{} add {}".format(message.author.id, tempID))

    # 멤버 제거
    if message.content[:4] == "$del":
        print("DEL member")
        tempID = message.content[5:]

    # 멤버 정보 보기
    if message.content[:4] == "$usr":
        print("SHOW member")
        tempID = message.content[6:]

    # 레식 관련 홈페이지 보기
    if message.content[:8] == "$r6swebs":
        print("SHOW r6sWebs")
        embed = discord.Embed(title="Rainbow Six Siege", description="관련 홈페이지", color=0x0000ff)

        rows = getWebData()
        for row in rows:
            embed.add_field(name=row[0], value=row[1], inline=False)

        await message.channel.send(embed=embed)

    # 레식 관련 홈페이지 추가
    if message.content[:4] == "$adw":
        print("ADD r6sWebs")
        tmp = message.content[5:].split('|')
        addWebData(tmp[0], tmp[1], message.author.id)
        await message.channel.send("{} ADDED\n{}".format(tmp[0], tmp[1]))

    if message.content[:5] == "$help":
        print("SHOW all commands")

        embed = discord.Embed(title="모든 명령어", description="명령어 설명일껄요?", color=0x0000ff)
        embed.add_field(name="$add <r6 닉네임>", value="레식 닉네임 등록", inline=False)
        embed.add_field(name="$del", value="등록한 레식 정보 삭제", inline=False)
        embed.add_field(name="$usr <등록한 r6 닉네임>", value="멤버 상세정보 보기", inline=False)

        embed.add_field(name="$adw <홈페이지명>|<홈페이지URL>", value="참고할만한 레식 사이트 등록", inline=False)
        embed.add_field(name="$dlw <홈페이지명>", value="등록된 레식 사이트 제거", inline=False)
        embed.add_field(name="$r6swebs", value="등록된 참고 홈페이지들 보기", inline=False)

        await message.channel.send(embed=embed)


client.run(token)