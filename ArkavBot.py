from lxml import etree
import discord
import re
import urllib.request
import numpy as np
from datetime import datetime

def countdown():
    dday, dhour = 22, 20
    now = datetime.now().strftime("%d:%H")
    day, hour = now.split(':')
    day = dday - int(day)
    hour = dhour - int(hour)
    
    return str(day) if day>1 else str(hour) + " Jam"
    

def openweb():
    web = urllib.request.urlopen("https://itch.io/jam/arkav-game-jam-2021/unrated")
    s = web.read()
    html = etree.HTML(s)
    tr_nodes = html.xpath('//table[@class="nice_table"]/tr')

    return tr_nodes

def check(tr_nodes):
    judul = [[[a.text for a in td.xpath('a')] for td in tr.xpath('td')[:1]] for tr in tr_nodes[0:]]
    comment = [[td.text for td in tr.xpath('td')[-1:]] for tr in tr_nodes[0:]]
    vote = [[td.text for td in tr.xpath('td')[-2:-1]] for tr in tr_nodes[0:]]

    return judul, comment, vote

def median(vote):
    return np.median([int(str(i)[2:-2]) for i in vote])

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))
        if message.author == client.user:
            return
        
        if message.content == '!checkall':
            await message.channel.send("Pengumuman H-" + countdown())
            await message.channel.send("Title/Vote/Comment")
            tr_nodes = openweb()
            judul, comment, vote = check(tr_nodes)
            for n in reversed(range(25)):
                await message.channel.send(str(judul[n])[3:-3] + " " + str(vote[n])[2:-2] + " " + str(comment[n])[2:-2])
            await message.channel.send("Median = " + str(median(vote)) + " ~Done")

        if '!top' in message.content:
            await message.channel.send("Pengumuman H-" + countdown())
            await message.channel.send("Title/Vote/Comment")
            tr_nodes = openweb()
            judul, comment, vote = check(tr_nodes)
            for n in range(24, 24-int(re.sub("[^0-9]", "", message.content)), -1):
                await message.channel.send(str(judul[n])[3:-3] + " " + str(vote[n])[2:-2] + " " + str(comment[n])[2:-2])
            await message.channel.send("Median = " + str(median(vote)) + " ~Done")

client = MyClient()
client.run('XXXX')
# print(discord.__version__)