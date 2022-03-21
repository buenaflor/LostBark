import discord
import enum
import os
from datetime import datetime, timedelta
from discord.ext import commands
from discord_slash import SlashCommand, manage_commands

from formatter import bold, italic

bot = commands.Bot(command_prefix='/')
slash = SlashCommand(bot, sync_commands=True)

def list_to_string(s):
    str1 = " "
    return (str1.join(s))

class Continents(enum.Enum):
    EastLuterra = "East Luterra"
    WestLuterra = "West Luterra"
    NorthVern = "North Vern"
    Rethramis = "Rethramis"
    Shushire = "Shushire"
    Anikka = "Anikka"
    Tortoyk = "Tortoyk"
    Arthetine = "Arthetine"
    Rohendel = "Rohendel"
    Yudia = "Yudia"
    Yorn = "Yorn"
    Feiton = "Feiton"
    Punika = "Punika"

class TravelingMerchants(enum.Enum):
    Burt = "Burt"
    Morris = "Morris"
    Ben = "Ben"
    Lucas = "Lucas"
    Peter = "Peter"
    Laitir = "Laitir"
    Mac = "Mac"
    Jeffrey = "Jeffrey"
    Oliver = "Oliver"
    Nox = "Nox"
    Rayni = "Rayni"
    Aricer = "Aricer"
    Malone = "Malone"
    Dorella = "Dorella"

    def continent(self):
        match self.value:
            case self.Burt.value | self.Morris.value:
                return Continents.EastLuterra.value
            case self.Ben.value:
                return Continents.Rethramis.value
            case self.Peter.value:
                return Continents.NorthVern.value
            case self.Laitir.value:
                return Continents.Yorn.value
            case self.Lucas.value:
                return Continents.Yudia.value
            case self.Mac.value:
                return Continents.Anikka.value
            case self.Jeffrey.value:
                return Continents.Shushire.value
            case self.Oliver.value:
                return Continents.Tortoyk.value
            case self.Nox.value:
                return Continents.Arthetine.value
            case self.Rayni.value:
                return Continents.Punika.value
            case self.Aricer.value:
                return Continents.Rohendel.value
            case self.Malone.value:
                return Continents.WestLuterra.value
            case self.Dorella.value:
                return Continents.Feiton.value

    def schedule(self):
        match self.value:
            case self.Burt.value | self.Malone.value | self.Oliver.value | self.Nox.value | self.Aricer.value | self.Rayni.value:
                return ["12:30", "2:30", "5:30", "6:30", "8:30", "9:30"]
            case self.Ben.value | self.Peter.value | self.Laitir.value:
                return ["12:30", "3:30", "4:30", "6:30", "7:30", "10:30"]
            case self.Lucas.value | self.Morris.value | self.Mac.value | self.Jeffrey.value | self.Dorella.value:
                return ["1:30", "4:30", "5:30", "7:30", "8:30", "11:30"]


    def name_and_continent(self):
        return self.value + " (" + self.continent() + ")"


@bot.event
async def on_ready():
    print("Bot Is Ready And Online!")


@slash.slash(name="mtg",
             description="Converts maris shop products worth to gold. Per default it calculates gold per product unit",
             options=[
                 manage_commands.create_option(name="exchange_rate", description="Exchange rate from gold to crystals", option_type=3, required=True),
                 manage_commands.create_option(name="price", description="Price of the product in crystals", option_type=3, required=True),
                 manage_commands.create_option(name="amount_received", description="Amount received of the product", option_type=3, required=True),
                 manage_commands.create_option(name="bundle", description="Calculates the gold price of the product bundle", option_type=5, required=False)
             ])
async def mtg(ctx, exchange_rate, price, amount_received, bundle=None):
    gold_per_unit = (float(exchange_rate) / 95) * float(price) / float(amount_received)

    embed = discord.Embed(color=0xFF5733, title="Mari's Shop to Gold")
    embed.set_author(name="BarkBot", icon_url="https://scontent-vie1-1.xx.fbcdn.net/v/t39.30808-6/273797272_437110278150626_6407164352942042066_n.jpg?stp=cp0_dst-jpg_e15_q65_s110x80&_nc_cat=1&ccb=1-5&_nc_sid=85a577&efg=eyJpIjoidCJ9&_nc_ohc=vvulOrY4KyoAX8HbPBY&_nc_ht=scontent-vie1-1.xx&oh=00_AT-zPMPFR8p1MvtszS52sp7SFIFPWHjDjooMZEQftmUx7g&oe=623CD5B1")
    embed.add_field(name="Exchange rate", value=exchange_rate + " Gold for 95 Crystals", inline=True)
    embed.add_field(name="Cost of product", value=price + " Crystals", inline=True)
    embed.add_field(name="Units received", value=amount_received, inline=True)

    if bundle:
        # Result per bundle
        embed.add_field(name="Gold price per 10 bundle (honing materials)", value=str(round(gold_per_unit * 10, 2)))
    else:
        # Result per unit
        embed.add_field(name="Gold price per unit", value=str(round(gold_per_unit, 2)))
    await ctx.send(embed=embed)



@slash.slash(name="traveling_merchants",
             description="Shows information on a specific traveling merchant",
             options=[
                 manage_commands.create_option(name="merchant_name", description="Name of the traveling merchant",
                                               option_type=3, choices=[
                         manage_commands.create_choice(name=TravelingMerchants.Burt.name_and_continent(), value=TravelingMerchants.Burt.value),
                         manage_commands.create_choice(name=TravelingMerchants.Ben.name_and_continent(), value=TravelingMerchants.Ben.value),
                         manage_commands.create_choice(name=TravelingMerchants.Peter.name_and_continent(), value=TravelingMerchants.Peter.value),
                         manage_commands.create_choice(name=TravelingMerchants.Laitir.name_and_continent(), value=TravelingMerchants.Laitir.value),
                         manage_commands.create_choice(name=TravelingMerchants.Lucas.name_and_continent(), value=TravelingMerchants.Lucas.value),
                         manage_commands.create_choice(name=TravelingMerchants.Morris.name_and_continent(), value=TravelingMerchants.Morris.value),
                         manage_commands.create_choice(name=TravelingMerchants.Mac.name_and_continent(), value=TravelingMerchants.Mac.value),
                         manage_commands.create_choice(name=TravelingMerchants.Jeffrey.name_and_continent(), value=TravelingMerchants.Jeffrey.value),
                         manage_commands.create_choice(name=TravelingMerchants.Dorella.name_and_continent(), value=TravelingMerchants.Dorella.value),
                         manage_commands.create_choice(name=TravelingMerchants.Malone.name_and_continent(), value=TravelingMerchants.Malone.value),
                         manage_commands.create_choice(name=TravelingMerchants.Oliver.name_and_continent(), value=TravelingMerchants.Oliver.value),
                         manage_commands.create_choice(name=TravelingMerchants.Nox.name_and_continent(), value=TravelingMerchants.Nox.value),
                         manage_commands.create_choice(name=TravelingMerchants.Aricer.name_and_continent(), value=TravelingMerchants.Aricer.value),
                         manage_commands.create_choice(name=TravelingMerchants.Rayni.name_and_continent(), value=TravelingMerchants.Rayni.value),
                 ], required=True)
             ])
async def traveling_merchants(ctx, merchant_name):
    embed = discord.Embed(color=0xFF5733)
    embed.add_field(name="Merchant", value=merchant_name, inline=True)
    embed.add_field(name="Continent", value=TravelingMerchants(merchant_name).continent(), inline=True)
    embed.add_field(name="Schedule", value=list_to_string(TravelingMerchants(merchant_name).schedule()), inline=True)
    # todo: embed.add_field(name="Maps", value="Blackrose Chapel", inline=False)
    embed.set_author(name="BarkBot", icon_url="https://scontent-vie1-1.xx.fbcdn.net/v/t39.30808-6/273797272_437110278150626_6407164352942042066_n.jpg?stp=cp0_dst-jpg_e15_q65_s110x80&_nc_cat=1&ccb=1-5&_nc_sid=85a577&efg=eyJpIjoidCJ9&_nc_ohc=vvulOrY4KyoAX8HbPBY&_nc_ht=scontent-vie1-1.xx&oh=00_AT-zPMPFR8p1MvtszS52sp7SFIFPWHjDjooMZEQftmUx7g&oe=623CD5B1")

    beatrice_time = datetime.utcnow() + timedelta(hours=1)
    beatrice_time_hours_minutes = "{:d}:{:02d}".format(beatrice_time.hour, beatrice_time.minute)

    # find the closest time based on schedule
    format = '%H:%M'
    d = datetime.strptime(beatrice_time_hours_minutes, format)
    schedule_times = TravelingMerchants(merchant_name).schedule()
    split = schedule_times[0].split(":")
    t_formatted = "{:s}:{:02s}".format(split[0], split[1])
    t_d = datetime.strptime(t_formatted, format)
    current_min = t_d - d
    for x in schedule_times:
        split = x.split(":")
        t_formatted = "{:s}:{:02s}".format(split[0], split[1])
        t_d = datetime.strptime(t_formatted, format)
        if t_d - d < current_min and (t_d - d).days >= 0:
            current_min = t_d - d

    hours, minutes = current_min.seconds // 3600, current_min.seconds // 60 % 60
    # embed.add_field(name="Next Appearance", value="In " + f"{hours:02d}" + ":" + f"{minutes:02d}" + " hours", inline=False)
    embed.set_footer(text="Schedule times apply to AM and PM and only on EU Central Beatrice")
    await ctx.send(embed=embed)

@slash.slash(name="dailies", description="Lists tasks that can be done daily")
async def dailies(ctx):
    res = "2x Chaos Dungeons\n"
    res += "2x Guardian Raids\n"
    res += "3x Una's Tasks\n"
    res += "Anguished Isle\n"
    res += "Chaos Gate / Field Boss / Adventure Island\n"
    res += "Guild Task / Guild Donation / Guild Research Support\n"

    embed = discord.Embed(color=0xFF5733, title="Daily Tasks", description=res)
    embed.set_author(name="BarkBot", icon_url="https://scontent-vie1-1.xx.fbcdn.net/v/t39.30808-6/273797272_437110278150626_6407164352942042066_n.jpg?stp=cp0_dst-jpg_e15_q65_s110x80&_nc_cat=1&ccb=1-5&_nc_sid=85a577&efg=eyJpIjoidCJ9&_nc_ohc=vvulOrY4KyoAX8HbPBY&_nc_ht=scontent-vie1-1.xx&oh=00_AT-zPMPFR8p1MvtszS52sp7SFIFPWHjDjooMZEQftmUx7g&oe=623CD5B1")
    await ctx.send(embed=embed)


@slash.slash(name="weeklies", description="Lists tasks that can be done weekly")
async def weeklies(ctx):
    res = "Abyss Dungeon\n"
    res += "3x Weekly Una's Tasks\n"
    res += "Buy Guild Shop Products\n"
    res += "Buy Mats on Pirate Ship\n"
    res += "Buy Mats on Dungeon Exchange Shop\n"
    res += "Buy Mats on Grand Prix\n"

    embed = discord.Embed(color=0xFF5733, title="Weekly Tasks", description=res)
    embed.set_author(name="BarkBot", icon_url="https://scontent-vie1-1.xx.fbcdn.net/v/t39.30808-6/273797272_437110278150626_6407164352942042066_n.jpg?stp=cp0_dst-jpg_e15_q65_s110x80&_nc_cat=1&ccb=1-5&_nc_sid=85a577&efg=eyJpIjoidCJ9&_nc_ohc=vvulOrY4KyoAX8HbPBY&_nc_ht=scontent-vie1-1.xx&oh=00_AT-zPMPFR8p1MvtszS52sp7SFIFPWHjDjooMZEQftmUx7g&oe=623CD5B1")
    await ctx.send(embed=embed)

bot.run("OTUzMDU1MDIwMTA5MTY0NzE0.Yi-_pw.rGg6ile-BUbpq0OVHlwEIOc-XRA")
#bot.run(os.environ.get('token'))
