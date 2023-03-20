import discord
from discord.ext import commands
 
app = commands.Bot(command_prefix='/', intents=discord.Intents.all())
client = discord.Client(intents=discord.Intents.all())

token = ""

@client.event
async def on_ready():
    print('[Client] Bot is ready!')
    await client.login(token)


@app.event
async def on_ready(): # 이 함수가 끝나기 전에 다른 함수를 호출할 수 있도록 비동기 실행 
    print(f'{app.user.name} 연결 성공')
    await app.change_presence(status=discord.Status.online, activity=None)

'''
@app.command(aliases=['hi', '안녕'])
async def hello(ctx): # ctx = discord.ext의 commands의 context 클래스 객체 
    await ctx.send("냥냥")
   
   
@app.command(aliases=['따라해', '따라하기', '흉내'])
async def follow(ctx, *args): # ctx = discord.ext의 commands의 context 클래스 객체 
    for arg in args:
        await ctx.send(f'```{arg}```')


@app.command(aliases=['임베드'])
async def sendEmbed(ctx, content): # ctx = discord.ext의 commands의 context 클래스 객체 
        # Embed 생성
        embed = discord.Embed(
            title="꽁치의 쪽지",
            description=content,
            color=discord.Color.blue()
        )
        embed.set_author(name="꽁치")

        # await ctx.send(embed=embed)



@app.event
async def on_message(msg): # 누군가 채팅 메시지 보낼 때마다 실행되는 함수
    # await msg.add_reaction("🐱") # msg는 메시지 정보를 가지고 있는 discord 객체 
    if not msg.author.bot:
        return
'''

# 익명 질문 기능 
@client.event
async def on_message(message):
    # commands.Bot에서 처리되는 명령어 메시지는 무시합니다.
    if message.author.bot:
        return

    # DM을 받은 경우
    if isinstance(message.channel, discord.DMChannel):
        # 익명 질문 명령어인지 확인
        if ( message.content[:5] != "/익명질문" ) :
            return

        # 익명 질문을 위한 태그 input 메세지 내보내기

        # 선택한 태그로 태그 작성

        # 질문 제목 받기

        # 질문 내용 입력 받기 


        # 채팅을 올릴 서버 채널 객체 가져오기
        channel = discord.utils.get(client.guilds[0].channels, name="포럼-테스트용")

        print(channel.available_tags) 

        await channel.create_thread(name="익명", content=message.content)


client.run(token)