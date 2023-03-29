import discord
from discord.ext import commands
from discord.ui import Select, View
from discord import SelectOption
 

app = commands.Bot(command_prefix='/', intents=discord.Intents.all())
client = discord.Client(intents=discord.Intents.all())
tags = []
selected_tag = ""

token = ""


@client.event
async def on_ready():
    print('[Client] Bot is ready!')
    channel = discord.utils.get(client.guilds[0].channels, name="포럼-테스트용")
    for i in channel.available_tags :
        tags.append(SelectOption(label=i, value=i))
    await client.login(token)


@app.event
async def on_ready(): # 이 함수가 끝나기 전에 다른 함수를 호출할 수 있도록 비동기 실행 
    print(f'{app.user.name} 연결 성공')
    await app.change_presence(status=discord.Status.online, activity=None)


# tag 선택을 위한 view
class TagView(View):
    def __init__(self, options):
        super().__init__()
        self.select = Select(
            placeholder="Please select an option...",
            options=options
        )
        self.add_item(self.select)

    async def select_callback(self, select, option):
        await select.response.defer()
        await select.message.edit(content=f"You selected {option.label}.")


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
        
        author_id = message.author.id
        
        # 채팅을 올릴 서버 채널 객체 가져오기
        qChannel = discord.utils.get(client.guilds[0].channels, name="포럼-테스트용")

        # 익명 질문을 위한 태그 input 메세지 내보내기
        await message.channel.send("Please select an option.", view=TagView(tags))

        # 선택한 태그로 태그 작성
        print(selected_tag)

        # 질문 제목 받기

        # 질문 내용 입력 받기 


        await qChannel.create_thread(name="익명", content=message.content)

client.run(token)