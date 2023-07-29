import discord
from discord.ext import commands
import sqlite3


prefix = "!" 
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=prefix, intents=intents)


conn = sqlite3.connect('ctf.db')
cursor = conn.cursor()


def create_table():
    cursor.execute('''CREATE TABLE IF NOT EXISTS ctf_users (
                      user_id INTEGER PRIMARY KEY,
                      points INTEGER DEFAULT 0
                      )''')
    conn.commit()


def add_points_db(user_id, points):
    cursor.execute("INSERT OR IGNORE INTO ctf_users (user_id) VALUES (?)", (user_id,))
    cursor.execute("UPDATE ctf_users SET points = points + ? WHERE user_id = ?", (points, user_id))
    conn.commit()


def get_user_info(user_id):
    cursor.execute("SELECT points FROM ctf_users WHERE user_id = ?", (user_id,))
    return cursor.fetchone()

def get_leaderboard():
    cursor.execute("SELECT user_id, points FROM ctf_users ORDER BY points DESC")
    return cursor.fetchall()

@bot.event
async def on_ready():
    print(f'{bot.user.name} 🐌 Joined!')


@bot.command()
async def points(ctx):
    user_id = ctx.author.id
    points = get_user_info(user_id)[0]
    await ctx.send(f'{ctx.author.mention}, Aandek {points} points.')

@bot.command()
async def truth(ctx):
    fakroun_id=235148962103951360
    await ctx.send(f'l 7alazoun 🐌 a9wa w a7sen bot mawjoud f market! <@{fakroun_id}> haw chway 🥬')

@bot.command()
async def who(ctx,target_user: discord.Member):
    xhalyl_id=699792446128914502
    if target_user.id == xhalyl_id:
        await ctx.send(f' 🥒 و الجوااااااب صحيح ربحت معانا ')
    else:
        await ctx.send(f'Chkounou {target_user.mention} godem l maalem !!')

@bot.command()
async def add_points(ctx, target_user: discord.Member = None, points: int = None):
    if points is None or points <= 0:
        await ctx.send("Rakezli ro7ek fl points")
        return

    if discord.utils.get(ctx.author.roles, name='sudo') or discord.utils.get(ctx.author.roles, name='Helpers'):
        if target_user is None:
            user_id = ctx.author.id
            await ctx.send(f'Mabrouk! {ctx.author.mention}, rbe7t m3ana {points} points!')
        else:

            user_id = target_user.id
            await ctx.send(f'Mabrouk! {target_user.mention} rbe7t m3ana {points} points!')

        add_points_db(user_id, points)
    else:
        await ctx.send(f"Ya {ctx.author.mention} taw yji nhar w tetra9a 🤭")

@bot.command()
async def scores(ctx):
    leaderboard_data = get_leaderboard()

    if leaderboard_data:
        embed = discord.Embed(title="Scores", description="Leaderboard:")
        for rank, (user_id, points) in enumerate(leaderboard_data, start=1):
            user = bot.get_user(user_id)
            if user:
                embed.add_field(name=f"{rank}. {user.display_name}", value=f"{points} points", inline=False)
        embed.color = discord.Color.gold()
        await ctx.send(embed=embed)
    else:
        await ctx.send("Mafama hata score!")

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def commands(ctx):
    command_list = [
        ("!points", "Tchouf l points mte3ek."),
        ("!add_points [user.mention] <points>", "Tzid points l rohek wela member okher"),
        ("!scores", "Tchouf scores mta3 ness lkol"),
        ("!truth", "Ygolek lah9i9a"),
        ("!who [user.mention]",'who is the best ctf player')
    ]

    embed = discord.Embed(title="Commands", description="Commands :")

    for command, description in command_list:
        embed.add_field(name=command, value=description, inline=False)


    embed.color = discord.Color.blue()

    await ctx.send(embed=embed)


if __name__ == "__main__":
    create_table()
    bot.run("TOKEN")  
