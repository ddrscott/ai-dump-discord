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

MAX_MESSAGE_LENGTH = 2000
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
    elif f'@{bot.user.name}' in message.content:
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
    history_str += dedent(f"""\
        Respond to the following request or question:

        # Message
        {message.content}
        """)

    messages = [
        {"role": "user", "content": history_str},
    ]

    logging.info(f"Received message: {message.content}")
    async with ctx.typing():
        logging.info(f"Generating full response...")
        full_response = ''
        async for line in langlang.generate(messages):
            print(line, end='')
            full_response += line
        print('')
        if '```execute' in full_response:
            # we need to summarize the execution blocks
            messages += [
                {"role": "ai", "content": full_response},
                {"role": "user", "content": f"Summarize the response to less than {MAX_MESSAGE_LENGTH} characters and cite the most relevant reference."}
            ]
            logging.info(f"Generating summary response...")
            succinct = ''
            async for line in langlang.generate(messages):
                print(line, end='')
                succinct += line
            print('')
        else:
            succinct = full_response
    # break succinct into multiple messages if it exceeds the limit
    if len(succinct) > MAX_MESSAGE_LENGTH:
        logging.info(f"Response exceeds character limit. Splitting response...")
        while len(succinct) > MAX_MESSAGE_LENGTH:
            await ctx.send(succinct[:MAX_MESSAGE_LENGTH])
            succinct = succinct[MAX_MESSAGE_LENGTH:]
    else:
        logging.info(f"Sending response...")
        await ctx.send(succinct[:MAX_MESSAGE_LENGTH])


async def startup():
    await bot.start(DISCORD_BOT_TOKEN, reconnect=True)

if __name__ == '__main__':
    bot.run(DISCORD_BOT_TOKEN, reconnect=True)
