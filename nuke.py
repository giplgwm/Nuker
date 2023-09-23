from utils import *
import shelve


async def backup(guild):
    categories, text_channels, voice_channels, members, icon, banner = await serialize_server_info(guild)
    d = shelve.open(str(guild.id))
    d['name'], d['owner'], d['emojis'], d['stickers'], d['categories'], d['text_channels'], d['voice_channels'], d['members'], d['member_count'], d['icon'], d['banner'] = guild.name, guild.owner.name, guild.emojis, guild.stickers, categories, text_channels, voice_channels, members, guild.member_count, icon, banner
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
    if guild.name != d['name']:
        await guild.edit(name=d['name'])
    # Replace missing emojis/stickers
    await replace_categories(guild, d)
    await replace_text_channels(guild, d)
    await replace_voice_channels(guild, d)
    # Check for missing members - for now only prints their info
    await invite_members(guild, d)
    # Set icon and banner back if changed > Compare bytes, set back if changed
