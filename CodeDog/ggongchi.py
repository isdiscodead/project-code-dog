import discord
from discord.ext import commands
 
app = commands.Bot(command_prefix='/')
 
@app.event
async def on_ready():
    print(f'{app.user.name} 연결 성공')
    await app.change_presence(status=discord.Status.online, activity=None)
    
app.run('Token')