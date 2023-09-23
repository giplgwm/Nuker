from utils import *
import shelve


async def backup(guild):
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
    d = shelve.open(str(guild.id))
    d['name'], d['owner'], d['emojis'], d['stickers'], d['categories'], d['text_channels'], d['voice_channels'], d[
        'members'], d['member_count'], d['icon'], d[
        'banner'] = guild.name, guild.owner.name, guild.emojis, guild.stickers, categories, text_channels, voice_channels, members, guild.member_count, icon, banner
    d.close()


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
    # Reset name if it's been changed
    if guild.name != d['name']:
        await guild.edit(name=d['name'])
    # Replace missing emojis/stickers
    # Create missing categories
    categories = [cat.name for cat in guild.categories]
    cat_objects = []
    if categories != d['categories']:
        for category in guild.categories:
            await category.delete()
        for category in d['categories']:
            cat_objects.append(await guild.create_category(category))
    # Create missing text channels
    text_channels = [(channel, category) for (channel, category) in d['text_channels']]
    existing_text_channels = [(channel.name, channel.category.name if channel.category else 'No category') for channel
                              in guild.text_channels]

    if text_channels != existing_text_channels:
        for channel in guild.text_channels:
            await channel.delete()
        for (channel, category) in text_channels:
            for x in cat_objects:
                if x.name == category:
                    category = x
            if type(category) == str:
                category = None
            await guild.create_text_channel(channel, category=category)
    # Create missing voice channels
    voice_channels = [(channel, category) for (channel, category) in d['voice_channels']]
    existing_voice_channels = [(channel.name, channel.category.name if channel.category else 'No category') for channel
                               in guild.voice_channels]

    if voice_channels != existing_voice_channels:
        for channel in guild.voice_channels:
            await channel.delete()
        for (channel, category) in voice_channels:
            for x in cat_objects:
                if x.name == category:
                    category = x
            if type(category) == str:
                category = None
            await guild.create_voice_channel(channel, category=category)

    # Check for missing members - for now only prints their info
    members = [(member.name, member.id) for member in guild.members]
    if members != d['members']:
        set1 = set(members)
        set2 = set(d['members'])
        missing = set2 - set1
        await guild.text_channels[0].send(f'Missing: \n{missing}')
    # Set icon and banner back if changed > Compare bytes, set back if changed
