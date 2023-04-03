import discord
from discord.ext import commands
from discord.ui import Select, Button, View
from discord import SelectOption
 

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


# 익명 질문을 위한 data
qTitle = ""
qContent = ""

# tag 선택을 위한 view
class TagView(View):
    def __init__(self, tags, ctx):
        super().__init__()

        options = []
        for i in tags :
            options.append(SelectOption(label=(i.emoji + i.name), value=i.name))

        self.select = Select(
            placeholder="질문 카테고리를 선택해주세요.",
            options=options
        )
        self.add_item(self.select)

        def check(msg): 
            return msg.author == ctx.author and msg.channel == ctx.channel

        async def callback(interaction):
            ctx.bot.selected_tag = interaction.data['values'][0]
            await interaction.response.send_message(content=f"😎 현재 선택된 질문 카테고리 `{ ctx.bot.selected_tag }`로 익명 질문을 진행하시려면 3분 내로 `/제목 질문제목` 명령어를 사용해서 질문의 제목을 입력해주세요. 질문 작성을 원하지 않으실 경우 `/취소`를 입력해주세요.")
            
            # 질문 제목 입력받기 
            try: 
                title = app.wait_for("message", check=check, timeout=180.0)

                if title == "/취소" :
                    ctx.send("프로세스가 종료됩니다. 익명 질문을 남기시려면 다시 `/익명질문` 명령어를 사용해주세요.")
                    return
                
                if title[:4] != "/제목" :
                    return

                title = title[4:]
                if title == "" :
                    ctx.send("제목은 비워둘 수 없습니다. 프로세스가 종료됩니다. 익명 질문을 남기시려면 다시 `/익명질문` 명령어를 사용해주세요.")
                    return
                ctx.bot.qTitle = title
                
            except asyncio.TimeoutError:
                await ctx.send("3분이 경과되어 익명 질문 프로세스를 종료합니다.")
                return
            
            # 질문 내용 입력받기 
            await ctx.send(f"익명 질문을 계속해서 작성하시려면 5분 내로 `/내용 질문내용` 명령어를 사용해서 질문의 내용을 입력해주세요. 질문 작성을 원하지 않으실 경우 `/취소`를 입력해주세요.")
            try: 
                content = app.wait_for("message", check=check, timeout=300.0)

                if content == "/취소" :
                    ctx.send("프로세스가 종료됩니다. 익명 질문을 남기시려면 다시 `/익명질문` 명령어를 사용해주세요.")
                    return
                
                if content[:4] != "/내용" :
                    return

                content = content[4:]
                if content == "" :
                    ctx.send("내용은 비워둘 수 없습니다. 프로세스가 종료됩니다. 익명 질문을 남기시려면 다시 `/익명질문` 명령어를 사용해주세요.")
                    return
                ctx.bot.qContent = content
                
            except asyncio.TimeoutError:
                await ctx.send("3분이 경과되어 익명 질문 프로세스를 종료합니다.")
                return
            

            # 내용 확인용 임베드 
            embed = discord.Embed(title = f"{ctx.bot.qTitle}",
            description = f"{ctx.bot.qContent}", color = 0x62c1cc)
            embed.add_field(name = "카테고리", value = f"{ctx.bot.selected_tag}")
            embed.set_footer(text = "익명 질문")

            # 확인 / 취소 버튼 
            class ButtonView(View):
                def __init__(self):
                    super().__init__()
                    self.add_item(Button(style=discord.ButtonStyle.green, label="확인", custom_id="submit"))
                    self.add_item(Button(style=discord.ButtonStyle.red, label="취소", custom_id="cancel"))

                @discord.ui.button(label='확인')
                async def on_button_click(self, button: discord.ui.Button, interaction: discord.Interaction):
                    qChannel = discord.utils.get(client.guilds[0].channels, name="포럼-테스트용")
                    await interaction.response.send_message('익명 질문이 업로드 됩니다.')
                    await qChannel.create_thread(name=ctx.bot.qTitle, content=ctx.bot.qContent, applied_tags=[ctx.bot.selected_tag])

                @discord.ui.button(label='취소')
                async def on_button_click(self, button: discord.ui.Button, interaction: discord.Interaction):
                    await interaction.response.send_message('프로세스가 종료됩니다. 익명 질문을 남기시려면 다시 `/익명질문` 명령어를 사용해주세요.')
                    return

            ctx.send("아래 내용으로 질문을 올리시려면 확인 버튼을 눌러주시고, 원하지 않으실 경우 취소 버튼을 눌러주세요.", embed=embed, )

        self.select.callback = callback


# 익명 질문 기능 
@app.command(aliases=['익명질문', '질문'])
async def anony_question(ctx, message):
    # commands.Bot에서 처리되는 명령어 메시지는 무시
    if message.author.bot:
        return

    # DM을 받은 경우가 아니면 return 
    if not isinstance(message.channel, discord.DMChannel):
        return
    
    # 질문 채널 정보 가져오기 
    qChannel = discord.utils.get(client.guilds[0].channels, name="포럼-테스트용")
    tags = qChannel.available_tags

    # 작성자 정보 가져오기 
    author_id = message.author.id
    user = await client.fetch_user(author_id) 

    # 익명 질문을 위한 태그 input 메세지 내보내기
    await user.send(view=TagView(tags, ctx))


client.run(token)