import discord
import asyncio


client = discord.Client()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    if message.content.startswith('!test'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1

        await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    elif message.content.startswith('!sleep'):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')

    elif '!T123' in message.content:
        await client.send_message(message.channel, 'You mentioned a task!  T123 to be precise!')

client.run('MzY5OTQ5MTM2MjM5MzI5Mjgz.DMgC5A.MrxR71mAAiYIRDZgjF5y7fztZRU')
