import discord
from discord.ext import commands
import asyncio
import os

TOKEN = os.getenv('DISCORD_BOT_TOKEN')

intents = discord.Intents.all()
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

phases = ["肯定側立論", "否定側反対尋問", "否定側立論", "肯定側反対尋問", "否定側反駁", "肯定側反駁", "否定側最終弁論", "肯定側最終弁論"]
phase_times = [120, 120, 120, 120, 120, 120, 120, 120]  # 各フェーズの時間をデフォルトで120秒に設定
current_phase_index = 0
debate_active = False

affirmative_name = ""
negative_name = ""

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def set_names(ctx, affirmative: str, negative: str):
    global affirmative_name, negative_name
    affirmative_name = affirmative
    negative_name = negative
    await ctx.send(f"肯定側: {affirmative_name}, 否定側: {negative_name}")

@bot.command()
async def set_phase_times(ctx, *times: int):
    global phase_times
    if len(times) != len(phases):
        await ctx.send(f"各フェーズの時間を設定してください。例: !set_phase_times {' '.join(map(str, [120]*len(phases)))}")
    else:
        phase_times = list(times)
        await ctx.send(f"フェーズの時間を設定しました: {phase_times}")

@bot.command()
async def start_debate(ctx):
    global current_phase_index, debate_active
    current_phase_index = 0
    debate_active = True
    await display_phase(ctx)

@bot.command()
async def next_phase(ctx):
    global current_phase_index
    if current_phase_index < len(phases) - 1:
        current_phase_index += 1
        await display_phase(ctx)
    else:
        await ctx.send("これが最後のフェーズです。")

@bot.command()
async def previous_phase(ctx):
    global current_phase_index
    if current_phase_index > 0:
        current_phase_index -= 1
        await display_phase(ctx)
    else:
        await ctx.send("これが最初のフェーズです。")

async def display_phase(ctx):
    global current_phase_index, debate_active
    if debate_active:
        phase_message = await ctx.send(f"フェーズ: {phases[current_phase_index]} - 残り時間: {phase_times[current_phase_index]}秒")
        await countdown(ctx, phase_message, phase_times[current_phase_index])
    else:
        await ctx.send("ディベートがアクティブではありません。")

async def countdown(ctx, message, seconds: int):
    global current_phase_index, debate_active
    while seconds and debate_active:
        await asyncio.sleep(1)
        seconds -= 1
        await message.edit(content=f"フェーズ: {phases[current_phase_index]} - 残り時間: {seconds}秒")
        if seconds == 60:
            await ctx.send("残り1分です。")
        elif seconds == 30:
            await ctx.send("残り30秒です。")
    if debate_active:
        await ctx.send("フェーズが終了しました。")
        if current_phase_index < len(phases) - 1:
            current_phase_index += 1
            await display_phase(ctx)
        else:
            await ctx.send("ディベートが終了しました。")
            debate_active = False

@bot.command()
async def help_debate(ctx):
    help_message = """
    **利用可能なコマンド**
    `!next_phase` - 次のフェーズに進みます。
    `!previous_phase` - 前のフェーズに戻ります。
    `!help` - このヘルプメッセージを表示します。
    """
    await ctx.send(help_message)

bot.run(TOKEN)