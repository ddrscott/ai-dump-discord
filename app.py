import logging
import os
from textwrap import dedent

import langlang
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.dm_messages = True
intents.guilds = True
intents.message_content = True
intents.messages = True
intents.presences = True
intents.typing = True

MAX_MESSAGE_LENGTH = 4000
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    logging.info(f'Logged in as {bot.user}')


@bot.event
async def on_message(message):
    # Ignore messages sent by the bot
    if message.author == bot.user:
        return

    # Get the context of the message
    ctx = await bot.get_context(message)

    if f'<@{bot.user.id}>' in message.content:
        pass
    elif message.channel.type == discord.ChannelType.private:
        pass
    else:
        return

    # Fetch message history
    history = ["Given the following chat history:\n```"]
    async for m in ctx.channel.history(limit=10):
        # Corrected to use m.author.name
        history.append(f"[{m.created_at.strftime('%Y-%m-%d %H:%M:%S')}] {m.author.name}: {m.content}")

    # Join the history records with newlines
    history_str = "\n".join(history)
    history_str += "\n```\n"
    history_str = dedent(f"""\
        Respond to the following request or question:

        # Message
        {message.content}
        """)

    messages = [
        {"role": "user", "content": history_str},
    ]

    async with ctx.typing():
        full_response = ''.join(list(langlang.generate(messages)))
        messages += [
            {"role": "ai", "content": full_response},
            {"role": "user", "content": f"Summarize for a Discord bot response less than {MAX_MESSAGE_LENGTH} letters and cite only relevant links."}
        ]
        succinct = ''.join(list(langlang.generate(messages)))

        # Send the response back to the user
        await ctx.send(succinct[:MAX_MESSAGE_LENGTH])


async def startup():
    await bot.start(DISCORD_BOT_TOKEN, reconnect=True)

if __name__ == '__main__':
    bot.run(DISCORD_BOT_TOKEN, reconnect=True)
