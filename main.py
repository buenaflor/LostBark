import discord, enum
import re

class Commands(enum.Enum):
    MatsGoldPrice = "!matsprice"

    def usage(self):
        if self.value == Commands.MatsGoldPrice.value:
            # default return is gold per 10 bundle
            return "Usage: !matsprice [-peritem] { -exr 1000 -amrcv 50 -ttlprice 40 }"
            #return "Usage: !download [-u] { -subreddit LivestreamFail -limit 5 | -single https://www.twitch.tv/hasanabi/clip/PerfectPlacidCrabsPanicVis }"
        return "Usage not defined"

class Options(enum.Enum):
    # CashShopExchangeRate = "-csexr"
    PerBundle = "-bundle"
    PerItem = "-peritem" 
    ExchangeRate = "-exr"
    AmountReceived = "-amrcv"
    TotalPriceOfProduct = "-ttlprice"

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

                if Options.PerItem.value in message.content:
                    await message.channel.send("Gold price per item: " + str(gold_per_bundle / 10))
                else:
                    await message.channel.send("Gold price per bundle: " + str(gold_per_bundle))
            else:
                await message.channel.send(Commands.MatsGoldPrice.usage())

    def index_containing_substring(the_list, substring):
        for i, s in enumerate(the_list):
            if substring in s:
                return i
        return -1
    
client = MyClient()

# This is bad practice, never expose your token by hardcoding it
client.run('OTUzMDU1MDIwMTA5MTY0NzE0.Yi-_pw.A4cyjrzP0p8b6vfN_H1hQ7psexI')