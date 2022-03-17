import asyncio
import os
import enum

import discord
from discord.ext import commands
from discord_slash import SlashCommand, manage_commands

from formatter import bold, italic

# todo: use more functions and isolated classes: formatting, conversion, etc...

bot = commands.Bot(command_prefix='/')
slash = SlashCommand(bot, sync_commands=True)

class Options(enum.Enum):
    PerBundle = "-bundle"
    ExchangeRate = "-exr"
    AmountReceived = "-amount"
    TotalPriceOfProduct = "-price"

@slash.slash(name="mtg", description="Converts maris shop products worth to gold. Per default it calculates gold per product unit",
             options=[manage_commands.create_option(name="exchange_rate", description="Exchange rate from gold to crystals", option_type=3, required=True),
                      manage_commands.create_option(name="price", description="Price of the product in crystals", option_type=3, required=True),
                      manage_commands.create_option(name="amount_received", description="Amount received of the product", option_type=3, required=True),
                      manage_commands.create_option(name="bundle", description="Calculates the gold price of the product bundle", option_type=5, required=False)])
async def mtg(ctx, exchange_rate, price, amount_received, bundle = None):
    gold_per_unit = (float(exchange_rate) / 95) * float(price) / float(amount_received)
    res = "Crystal Exchange Rate: " + exchange_rate + " Gold for 95 Crystals\n"
    res += "Cost of Product: " + price + " Crystals\n"
    res += "Amount Received: " + amount_received
    res = italic(res) + "\n\n"

    if bundle:
        # Result per bundle
        res = res + "Gold price per 10 bundle: " + bold(str(round(gold_per_unit * 10, 2)))
        await ctx.send(res)
    else:
        # Result per unit
        res = res + "Gold price per unit: " + bold(str(round(gold_per_unit, 2)))
        await ctx.send(res)

@slash.slash(name="dailies", description="Lists tasks that can be done daily")
async def dailies(ctx):
    res = "2x Chaos Dungeons\n"
    res += "2x Guardian Raids\n"
    res += "3x Una's Tasks\n"
    res += "Anguished Isle\n"
    res += "Chaos Gate / Field Boss / Adventure Island\n"
    res += "Guild Task / Guild Donation / Guild Research Support\n"
    await ctx.send(italic(res))

@slash.slash(name="weeklies", description="Lists tasks that can be done weekly")
async def dailies(ctx):
    res = "Abyss Dungeon\n"
    res += "3x Weekly Una's Tasks\n"
    res += "Buy Guild Shop Products\n"
    res += "Buy Mats on Pirate Ship\n"
    res += "Buy Mats on Dungeon Exchange Shop\n"
    res += "Buy Mats on Grand Prix\n"
    await ctx.send(italic(res))


#client.run(os.environ.get('token'))

bot.run("OTUzMDU1MDIwMTA5MTY0NzE0.Yi-_pw.pdmUXzfpuxiMgN0j4kS2T76Y9QM")