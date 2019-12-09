import discord
import datetime

token = 'NTI2MDk2MzUzNzQzNjAxNjg2.Xe5ilQ.-aMK0r38yBIR_VATZd5f1ha-e8w'
client = discord.Client()


@client.event
async def on_ready():
    print('Logged on as '+f'{client.user}')

@client.event
async def on_message(message):
    nick = ["$AFK-HAN", "$MOYAMOHAE"]
    nickID = ["NUMBER_ONE_N00B"]

    # don't respond to ourselves
    if message.author == client.user:
        return

    # try:
    #     getNameIndex = nick.index(message.content)
    #     await message.channel.send("r6tab {} as".format(nickID[getNameIndex]))
    #
    # except ValueError:
    #     await message.channel.send("{}: Not registered".format(message.content))

    # if message.content == '한형':
    #     embed = discord.Embed(title="자신도 모르는 세 정점에 도달한 한 남자의 이야기", description="이거슨 설명이라고 합니다!", color=0x00ff00)
    #     embed.add_field(name="제목", value="부제목", inline=False)
    #     embed.add_field(name="제목2", value="부제목", inline=True)
    #     embed.add_field(name="제목2", value="부제목", inline=False)
    #     embed.add_field(name="제목2", value="부제목", inline=True)
    #     embed.add_field(name="제목2", value="부제목", inline=True)
    #     embed.add_field(name="제목2", value="부제목", inline=True)
    #     embed.timestamp = datetime.datetime.now()
    #     embed.set_footer(text="뭐넣을까")
    #     await message.channel.send(embed=embed)

    if message.content == '$AFK-HAN':
        embed = discord.Embed(title="AFK-HAN", description="자신도 모르는 세 정점에 도달한 한 남자의 이야기", color=0x00ff00)
        embed.add_field(name="나이", value="안알려줌", inline=False)
        embed.add_field(name="트위치 홈페이지", value="https://www.twitch.tv/han91", inline=False)
        file = discord.File("./han.PNG", filename="han.png")
        embed.set_image(url="attachment://han.png")
        embed.add_field(name="ID_1", value="부제목", inline=True)
        embed.add_field(name="ID_2", value="부제목", inline=True)
        embed.add_field(name="ID_3", value="JUVE_HAN._.", inline=True)
        embed.timestamp = datetime.datetime.now()
        await message.channel.send(file=file, embed=embed)

    if message.content == '$MOYAMOHAE':
        embed = discord.Embed(title="MOYAMOHAE", description="힘을 숨긴 찐따인척하는 인싸", color=0x00ff00)
        embed.add_field(name="나이", value="안알려줌", inline=False)
        embed.add_field(name="트위치 홈페이지", value="https://www.twitch.tv/moyamohae02", inline=False)
        file = discord.File("./mon.png", filename="mon.png")
        embed.set_image(url="attachment://mon.png")
        embed.add_field(name="ID_1", value="TWITCH_MOYA", inline=True)
        embed.add_field(name="ID_2", value="부제목", inline=True)
        embed.add_field(name="기타", value="플레쌉가능", inline=True)
        embed.timestamp = datetime.datetime.now()
        await message.channel.send(file=file, embed=embed)

    if message.content == "^r6hList":
        embed = discord.Embed(title="Rainbow Six Siege", description="관련 홈페이지", color=0x0000ff)
        embed.add_field(name="Tom Clancy's Rainbow Six Siege", value="https://rainbow6.ubisoft.com/siege/ko-kr/home/", inline=False)
        embed.add_field(name="r6s 디시갤러리 ", value="https://gall.dcinside.com/board/lists/?id=r6s", inline=False)
        embed.add_field(name="FPSGAME MANIA FORUM (에펨포)", value="https://cafe.naver.com/fpsgame.cafe", inline=False)
        await message.channel.send(embed=embed)

client.run(token)