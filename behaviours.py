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


async def handle_mono_mention(client, phab_url, match, message):
    ''' Trigger: r'!([rPTDF]\d+)'
    '''
    if match:
        response = '{}{}'.format(
            phab_url,
            match.group(1)
        )
        await client.send_message(message.channel, response)


async def handle_commit_mention(client, phab_url, match, message):
    ''' Trigger: r'!(r\w+)'
    '''
    if match:
        response = '{}{}'.format(
            phab_url,
            match.group(1)
        )
        await client.send_message(message.channel, response)
