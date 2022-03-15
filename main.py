import discord, enum
import re

# todo: use more functions and isolated classes: formatting, conversion, etc...

class Commands(enum.Enum):
    # Mats to Gold
    MatsGoldPrice = "!mtg"

    def usage(self):
        if self.value == Commands.MatsGoldPrice.value:
            # default return is gold per 10 bundle
            return "Usage: !mtg [-peritem] { -exr 1000 -amount 50 -price 40 }"
        return "Usage not defined"

class Options(enum.Enum):
    PerBundle = "-bundle"
    PerItem = "-peritem" 
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

                gold_per_bundle = (float(exr) * 0.95) * (float(ttl_price) / 100) / (float(amrcv) / 10)
                res = "_Crystal Exchange Rate: " + exr + " Gold for 95 Crystals\nCost of Mats: " + ttl_price + " Crystals\nAmount of Mats: " + amrcv + "_\n\n"
                if Options.PerItem.value in message.content:
                    # Result per item
                    res = res + "Gold price per item: " + "**" + str(gold_per_bundle / 10) + "**"
                    await message.channel.send(res)
                else:
                    # Result per bundle
                    res = res + "Gold price per bundle: " + "**" + str(gold_per_bundle) + "**"
                    await message.channel.send(res)
            else:
                await message.channel.send(Commands.MatsGoldPrice.usage())
    
client = MyClient()

# This is bad practice, never expose your token by hardcoding it
client.run('OTUzMDU1MDIwMTA5MTY0NzE0.Yi-_pw.A4cyjrzP0p8b6vfN_H1hQ7psexI')