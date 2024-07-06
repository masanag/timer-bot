import discord
from discord.ext import commands
import asyncio
import os

TOKEN = os.getenv('DISCORD_BOT_TOKEN')

intents = discord.Intents.all()
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

phases = ["肯定側立論", "否定側反対尋問", "否定側立論", "肯定側反対尋問", "否定側反駁", "肯定側反駁", "否定側最終弁論", "肯定側最終弁論"]
current_phase_index = 0
debate_active = False
countdown_task = None

affirmative_name = ""
negative_name = ""

default_time = 120
phase_times = [default_time] * len(phases)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command(name='names')
async def set_names(ctx, affirmative: str, negative: str):
    global affirmative_name, negative_name
    affirmative_name = affirmative
    negative_name = negative
    await ctx.send(f"肯定側: {affirmative_name}, 否定側: {negative_name}")

@bot.command(name='times')
async def set_phase_times(ctx, *times: int):
    global phase_times
    if len(times) == 1:
        phase_times = [times[0]] * len(phases)
        await ctx.send(f"すべてのフェーズの時間を {times[0]} 秒に設定しました。")
    elif len(times) == 4:
        phase_times = [
            times[0], times[1], times[0], times[1],
            times[2], times[2], times[3], times[3]
        ]
        await ctx.send(f"フェーズの時間を設定しました: {phase_times}")
    else:
        await ctx.send(f"各フェーズの時間を設定してください。例: !times {default_time} または !times 120 120 120 120")

@bot.command(name='start')
async def start(ctx):
    global current_phase_index, debate_active, countdown_task
    if not debate_active:
        debate_active = True
        countdown_task = asyncio.create_task(display_phase(ctx))
    else:
        await ctx.send("ディベートが既に開始されています。")

@bot.command(name='stop')
async def stop(ctx):
    global debate_active, countdown_task
    if debate_active:
        debate_active = False
        if countdown_task:
            countdown_task.cancel()
        await ctx.send("フェーズが中断されました。次のフェーズを開始するには !start コマンドを使用してください。")
        current_phase_index += 1
        if current_phase_index < len(phases):
            await ctx.send(f"次のフェーズ: {phases[current_phase_index]} - {get_current_speaker()}")

@bot.command(name='next')
async def next_phase(ctx):
    global current_phase_index
    if current_phase_index < len(phases) - 1:
        current_phase_index += 1
        await ctx.send(f"次のフェーズ: {phases[current_phase_index]} - {get_current_speaker()}")
    else:
        await ctx.send("これが最後のフェーズです。")

@bot.command(name='prev')
async def previous_phase(ctx):
    global current_phase_index
    if current_phase_index > 0:
        current_phase_index -= 1
        await ctx.send(f"前のフェーズ: {phases[current_phase_index]} - {get_current_speaker()}")
    else:
        await ctx.send("これが最初のフェーズです。")

@bot.command(name='end')
async def end_debate(ctx):
    global current_phase_index, debate_active, countdown_task
    debate_active = False
    if countdown_task:
        countdown_task.cancel()
    current_phase_index = 0
    await ctx.send("ディベートが終了しました。")

@bot.command(name='settings')
async def show_settings(ctx):
    settings_message = f"""
    **現在の設定**
    肯定側: {affirmative_name}
    否定側: {negative_name}
    フェーズの時間: {phase_times}
    """
    await ctx.send(settings_message)

@bot.command(name='flow')
async def show_flow(ctx):
    flow_message = f"**ディベートの流れ**\n"
    for i, phase in enumerate(phases):
        speaker = affirmative_name if "肯定側" in phase else negative_name
        status = ""
        if i < current_phase_index:
            status = "<-- done"
        elif i == current_phase_index:
            status = "<--- Now"
        flow_message += f"{i + 1}. {phase}: {speaker} - {phase_times[i]}秒 {status}\n"
    await ctx.send(flow_message)

@bot.command(name='current')
async def current_phase(ctx):
    if current_phase_index < len(phases):
        phase_message = f"**現在のフェーズ**\nフェーズ: {phases[current_phase_index]} - {get_current_speaker()} - 残り時間: {phase_times[current_phase_index]}秒"
    else:
        phase_message = "現在進行中のフェーズはありません。"
    await ctx.send(phase_message)

def get_current_speaker():
    if "肯定側" in phases[current_phase_index]:
        return affirmative_name
    else:
        return negative_name

async def display_phase(ctx):
    global current_phase_index, debate_active
    if debate_active:
        await ctx.send(f"フェーズ: {phases[current_phase_index]} - {get_current_speaker()} - 残り時間: {phase_times[current_phase_index]}秒")
        await countdown(ctx, phase_times[current_phase_index])
    else:
        await ctx.send("ディベートがアクティブではありません。")

async def countdown(ctx, seconds: int):
    global current_phase_index, debate_active
    while seconds and debate_active:
        await asyncio.sleep(1)
        seconds -= 1
        await ctx.send(f"フェーズ: {phases[current_phase_index]} - {get_current_speaker()} - 残り時間: {seconds}秒", delete_after=1)
        if seconds == 60:
            await ctx.send("残り1分です。")
        elif seconds == 30:
            await ctx.send("残り30秒です。")
    if debate_active:
        await ctx.send("フェーズが終了しました。次のフェーズを開始するには !start コマンドを使用してください。")
        debate_active = False
        current_phase_index += 1
        if current_phase_index < len(phases):
            await ctx.send(f"次のフェーズ: {phases[current_phase_index]} - {get_current_speaker()}")

@bot.command(name='help_debate')
async def help_debate(ctx):
    help_message = """
    **利用可能なコマンド**
    `!names <肯定側名> <否定側名>` - 肯定側と否定側の名前を設定します。
    `!times <時間1> <時間2> ... <時間4>` - 各フェーズの時間を設定します。1つの引数で全フェーズに同じ時間を設定します。
    `!start` - ディベートを開始します。
    `!stop` - 現在のフェーズを中断します。
    `!next` - 次のフェーズに進みます。
    `!prev` - 前のフェーズに戻ります。
    `!end` - ディベートを終了します。
    `!settings` - 現在の設定を表示します。
    `!flow` - ディベートの全体の流れを表示します。
    `!current` - 現在のフェーズを表示します。
    `!help_debate` - このヘルプメッセージを表示します。
    """
    await ctx.send(help_message)

bot.run(TOKEN)