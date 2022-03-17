import os
import enum

import discord

from formatter import bold, italic
from utils import remove_nonnumeric_chars, get_first_occurrence


# todo: use more functions and isolated classes: formatting, conversion, etc...

class Commands(enum.Enum):
    MatsGoldPrice = "!mtg"
    Daily = "!daily"
    Weekly = "!weekly"
    AllCommands = "!commands"

    # Returns a text of usage in case of false input
    def usage(self):
        if self.value == Commands.MatsGoldPrice.value:
            # default return is gold per unit
            return "Usage: !mtg [-bundle] { -exr 1000 -amount 50 -price 40 }"
        return "Usage not defined"


class Options(enum.Enum):
    PerBundle = "-bundle"
    ExchangeRate = "-exr"
    AmountReceived = "-amount"
    TotalPriceOfProduct = "-price"


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if message.content.startswith(Commands.MatsGoldPrice.value):
            if Options.TotalPriceOfProduct.value in message.content and Options.AmountReceived.value in message.content and Options.ExchangeRate.value in message.content:
                whitespace_trimmed = message.content.replace(" ", "")
                combined_message = whitespace_trimmed.replace("-", " ")
                combined_message_split = combined_message.split()

                ttl_price_temp = get_first_occurrence(combined_message_split, Options.TotalPriceOfProduct.value.replace("-", ""))
                ttl_price = remove_nonnumeric_chars(ttl_price_temp)

                exr_temp = get_first_occurrence(combined_message_split, Options.ExchangeRate.value.replace("-", ""))
                exr = remove_nonnumeric_chars(exr_temp)

                amrcv_temp = get_first_occurrence(combined_message_split, Options.AmountReceived.value.replace("-", ""))
                amrcv = remove_nonnumeric_chars(amrcv_temp)

                if not ttl_price or not exr or not amrcv:
                    await message.channel.send(Commands.MatsGoldPrice.usage())
                else:
                    gold_per_unit = (float(exr) / 95) * float(ttl_price) / float(amrcv)
                    res = "Crystal Exchange Rate: " + exr + " Gold for 95 Crystals\n"
                    res += "Cost of Product: " + ttl_price + " Crystals\n"
                    res += "Amount Received: " + amrcv
                    res = italic(res) + "\n\n"

                    if Options.PerBundle.value in message.content:
                        # Result per bundle
                        res = res + "Gold price per 10 bundle: " + bold(str(round(gold_per_unit * 10, 2)))
                        await message.channel.send(res)
                    else:
                        # Result per unit
                        res = res + "Gold price per unit: " + bold(str(round(gold_per_unit, 2)))
                        await message.channel.send(res)
            else:
                await message.channel.send(Commands.MatsGoldPrice.usage())

        if message.content.startswith(Commands.Daily.value):
            res = "2x Chaos Dungeons\n"
            res += "2x Guardian Raids\n"
            res += "3x Una's Tasks\n"
            res += "Anguished Isle\n"
            res += "Chaos Gate / Field Boss / Adventure Island\n"
            res += "Guild Task / Guild Donation / Guild Research Support\n"
            await message.channel.send(italic(res))

        if message.content.startswith(Commands.Weekly.value):
            res = "Abyss Dungeon\n"
            res += "3x Weekly Una's Tasks\n"
            res += "Buy Guild Shop Products\n"
            res += "Buy Mats on Pirate Ship\n"
            res += "Buy Mats on Dungeon Exchange Shop\n"
            res += "Buy Mats on Grand Prix\n"
            await message.channel.send(italic(res))

        if message.content.startswith(Commands.AllCommands.value):
            res = bold("!mtg") + " -> Mari's Shop products to gold\n"
            res += bold("!daily") + " -> List of daily tasks\n"
            res += bold("!weekly") + " -> List of weekly tasks\n"
            await message.channel.send(italic(res))

client = MyClient()

client.run(os.environ.get('token'))
