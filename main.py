import discord, enum
import re

# todo: use more functions and isolated classes: formatting, conversion, etc...

class Commands(enum.Enum):
    # Mats to Gold
    MatsGoldPrice = "!mtg"

    def usage(self):
        if self.value == Commands.MatsGoldPrice.value:
            # default return is gold per 10 bundle
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
                
                ttl_price_temp = (next(s for s in combined_message_split if Options.TotalPriceOfProduct.value.replace("-", "") in s))
                ttl_price = re.sub("[^0-9]", "", ttl_price_temp)

                exr_temp = next(s for s in combined_message_split if Options.ExchangeRate.value.replace("-", "") in s)
                exr = re.sub("[^0-9]", "", exr_temp)

                amrcv_temp = next(s for s in combined_message_split if Options.AmountReceived.value.replace("-", "") in s)
                amrcv = re.sub("[^0-9]", "", amrcv_temp)

                if not ttl_price or not exr or not amrcv:
                    await message.channel.send(Commands.MatsGoldPrice.usage())
                else:
                    gold_per_unit = (float(exr) / 95) * float(ttl_price) / float(amrcv)
                    res = "_Crystal Exchange Rate: " + exr + " Gold for 95 Crystals\nCost of Product: " + ttl_price + " Crystals\nAmount Received: " + amrcv + "_\n\n"
                    if Options.PerBundle.value in message.content:
                        # Result per bundle
                        res = res + "Gold price per 10 bundle: " + "**" + str(round(gold_per_unit * 10, 2)) + "**"
                        await message.channel.send(res)
                    else:
                        # Result per unit
                        res = res + "Gold price per unit: " + "**" + str(round(gold_per_unit, 2)) + "**"
                        await message.channel.send(res)
            else:
                await message.channel.send(Commands.MatsGoldPrice.usage())
    
client = MyClient()

# This is bad practice, never expose your token by hardcoding it
client.run('OTUzMDU1MDIwMTA5MTY0NzE0.Yi-_pw.A4cyjrzP0p8b6vfN_H1hQ7psexI')