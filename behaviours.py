''' Phabbot's repertoire of learnt behavious.
'''
import asyncio
import re


async def help_prompt(client, phab_url, match, message):
    ''' Trigger: r'@phabbot help'
    '''
    if match:
        response = '''
        My name is Phabbot, I'm here to provide a bridge between Discord and
        Phabricator. Currently, if you mention either a Task or a Diff (i.e.
        T123 or D123), I will annoy you and tell you you did it.
        '''
        response_lines = response.strip().split('\n')
        response = ''
        for line in response_lines:
            response += line.strip()
        await client.send_message(message.channel, response)


async def handle_task_mention(client, phab_url, match, message):
    ''' Trigger: r'(T\d+)'
    '''
    if match:
        response = '{}{}'.format(
            phab_url,
            match.group(1)
        )
        await client.send_message(message.channel, response)


async def handle_diff_mention(client, phab_url, match, message):
    ''' Trigger: r'(D\d+)'
    '''
    if match:
        response = '{}{}'.format(
            phab_url,
            match.group(1)
        )
        await client.send_message(message.channel, response)


async def handle_test(client, _, message):
    ''' Trigger: r'!test'
    '''
    counter = 0
    tmp = await client.send_message(message.channel, 'Calculating messages...')
    async for log in client.logs_from(message.channel, limit=100):
        if log.author == message.author:
            counter += 1

    await client.edit_message(tmp, 'You have {} messages.'.format(counter))


async def handle_sleep(client, _, message):
    ''' Trigger: r'!sleep'
    '''
    await asyncio.sleep(5)
    await client.send_message(message.channel, 'Done sleeping')
