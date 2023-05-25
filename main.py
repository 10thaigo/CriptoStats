import discord
import requests
import json
import datetime
from discord.ext import commands

version = '1.0'

###
command_prefix = 'c!'
syntax_data = command_prefix + 'data <crypto id> <currency>'
##

coingecko_idandsymbols = []
coingecko_currency = []

def loadGeckoArrays():
	coins = requests.get('https://api.coingecko.com/api/v3/coins/list?include_platform=false', headers={"accept" : "application/json"})
	currency = requests.get('https://api.coingecko.com/api/v3/simple/supported_vs_currencies', headers={"accept" : "application/json"})
	w = coins.json()
	curr = currency.json()
	for i in w:
		lista = [i['id'], i['symbol']]
		coingecko_idandsymbols.append(lista)
	for x in curr:
		coingecko_currency.append(x)

def cryptoExists(crypto = ''):
	for i in coingecko_idandsymbols:
		if(crypto == i[1]):
			return i[0]
	return -1

def currencyExists(currency = ''):
	for i in coingecko_currency:
		if(currency == i):
			return i[0]
	return -1

###

bot = commands.Bot(command_prefix = command_prefix, activity=discord.Game(name="cs!cmds"))

@bot.command()
async def cmds(ctx):
	embed = discord.Embed(title="Commands list", description="Here is the list of available commands:", color=0xFFFFFF)
	embed.add_field(name="c!cmds", value="The commands list.", inline=False)
	embed.add_field(name="c!data <crypto> <currency>", value="You will get the current data of the cryptocurrency. Example: c!data btc usd", inline=False)
	embed.add_field(name="c!currencies", value="You will get the list with available currencies.", inline=False)
	await ctx.send(embed=embed)

@bot.command()
async def data(ctx, geckoid = '', currency = ''):
	geckoid = geckoid.lower()
	currency = currency.lower()
	existe = cryptoExists(geckoid)
	if(not geckoid):
		await ctx.send('You must enter a cryptocurrency ID. Example: btc / eth / ltc...')
	elif(not currency):
		await ctx.send('You must enter a currency. Example: USD / EUR / BTC ...')
	elif(cryptoExists(geckoid) == -1):
		await ctx.send('That cryptocurrency could not be found.')
	elif(currencyExists(currency) == -1):
		await ctx.send('Invalid currency. Use c!currencies to see the list of currencies.')
	else:
		data = requests.get('https://api.coingecko.com/api/v3/coins/'+existe, headers={"accept" : "application/json"})
		w = data.json()
		x = datetime.datetime.now()
		embed = discord.Embed(title=w['name'] + ' ('+currency.upper()+')', color=0xffa500)
		embed.set_thumbnail(url=w['image']['small'])
		embed.add_field(name='Average price: '+ str(w['market_data']['current_price'][currency]) + ' ' + currency.upper(), value='᲼', inline=False)
		embed.add_field(name='Market cap: '+ str(w['market_data']['market_cap'][currency]) + ' ' + currency.upper(), value='᲼', inline=True)
		embed.add_field(name='Rank: '+ str(w['market_cap_rank']), value='᲼', inline=True)
		embed.add_field(name='Total Volume: '+ str(w['market_data']['total_volume'][currency]) + ' ' + currency.upper(), value='᲼', inline=False)
		embed.add_field(name='High 24h: '+ str(w['market_data']['high_24h'][currency]) + ' ' + currency.upper(), value='᲼', inline=False)
		embed.add_field(name='Low 24h: '+ str(w['market_data']['low_24h'][currency]) + ' ' + currency.upper(), value='᲼', inline=False)
		embed.add_field(name='Price percentage 24h: '+ str(w['market_data']['price_change_percentage_24h_in_currency'][currency]) + '% ' + 'in ' + currency.upper(), value='**__________**', inline=False)
		await ctx.send(embed=embed)
	
@bot.command()
async def currencies(ctx):
	embed = discord.Embed(title="Available currencies", description="Here is the list of available currencies:", color=0xFFFFFF)

	formateado = ''
	for i in coingecko_currency:
		formateado += i + ' - '
	embed.add_field(name='᲼', value='**'+ formateado + '**', inline=False)
	await ctx.send(embed=embed)


###

 ## @bot.event
 ## async def on_ready():
 ## REMOVIDO
 
### 	
	
if __name__ == '__main__':
	print('CryptoStats version ' + version)
	loadGeckoArrays()
	bot.remove_command('help')
