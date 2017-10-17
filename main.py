import discord
import asyncio
import re

client = discord.Client()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


def check_phab_object (message):
    ''' Checks if the user mentioned a !task
    '''
    task_regex = re.compile(r'!(T\d+)')
    diff_regex = re.compile(r'!(D\d+)')
    # repo_regex = re.compile(r'!(r\d+)')
    # commit_regex = re.compile(r'!(r\d+)')
    task_result = task_regex.search(str(message))
    diff_result = diff_regex.search(str(message))
    response = ''
    if task_result:
        response = 'You mentioned a task!\n{} to be precise!'.format(task_result.group(1))
    if diff_result:
        response += 'You mentioned a task!\n{} to be precise!'.format(diff_result.group(1))

    if response == '':
        return None
    return response

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

    print('Checking for a task in: {}'.format(message.content))
    task = check_phab_object(message.content)
    if task is not None:
        await client.send_message(message.channel, task)

client.run('MzY5OTQ5MTM2MjM5MzI5Mjgz.DMgC5A.MrxR71mAAiYIRDZgjF5y7fztZRU')
