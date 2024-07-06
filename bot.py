import discord
from dotenv import load_dotenv
from discord.ext import commands,  tasks
from datetime import datetime, timedelta
import asyncio
import os

TOKEN=os.getenv('DISCORD_BOT_TOKEN')
# client = discord.Client(intents=discord.Intents.all())
# @client.event
# async def on_ready():
#     print(f'We have logged in as {client.user}')
# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
#     if message.content == 'hello':
#         await message.channel.send('hay')
# client.run(TOKEN)

intents = discord.Intents.all()
intents.messages = True
intents.guild_messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command(name='timer')
async def timer(ctx, *, time: str):
    # 時間の解析
    try:
        t = datetime.strptime(time, '%H:%M:%S')
        delta = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
    except ValueError:
        await ctx.send('時間の形式が正しくありません。正しい形式: h:m:s')
        return

    message = await ctx.send(f"タイマー設定: {str(delta)}")
    await start_timer(ctx, delta, message)

async def start_timer(ctx, delta: timedelta, message):
    end_time = datetime.now() + delta
    while datetime.now() < end_time:
        if (end_time - datetime.now()).seconds <= 10:
            # 残り10秒で音を鳴らす（Discordでは直接音を鳴らすことはできませんが、通知を送ることは可能です）
            await ctx.send('⏰ 残り10秒です！')
        # 残り時間の更新
        await message.edit(content=f"残り時間: {(end_time - datetime.now()).seconds}秒")
        await asyncio.sleep(1)
    await message.edit(content="タイマー終了！")

bot.run(TOKEN)