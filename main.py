''' Core code for Phabricator Discord bot, phabbot
'''
import logging
import asyncio
import re
import uvloop

import discord

import behaviours

logging.basicConfig(level=logging.INFO)
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
LOOP = uvloop.new_event_loop()


CLIENT = discord.Client(loop=LOOP)


@CLIENT.event
async def on_ready():
    ''' Log Phabbot base details on connection to Discord
    '''
    print(
        'Logged in as {}, with ID: {}'.format(
            CLIENT.user.name, CLIENT.user.id
        )
    )
    print('------')


def learn_behaviours():
    ''' Returns a mapping of regex strings and callables, to be used when
        on_message triggers, to react to messages.

        TODO: After retrieving all behaviours, rebuild the behaviour mapping
              with compiled patterns before returning
    '''
    behaviour_map = {}
    for _, function in behaviours.__dict__.items():
        if callable(function):
            function_doc = function.__doc__.strip().split('\n')
            for line in function_doc:
                if line.startswith('Trigger: '):
                    pattern = line.split('Trigger: ')[1]
                    pattern = re.search(r"^r'(.+)'$", pattern).group(1)
                    behaviour_map.update(
                        {
                            pattern: function
                        }
                    )

    return behaviour_map


@CLIENT.event
async def on_message(message):
    ''' Process messages reeived on channels phabbot is listening to
    '''
    # Phabbot must never talk to itself
    if 'phabbot' in message.author.name:
        return

    if message.content.startswith('!test'):
        counter = 0
        tmp = await CLIENT.send_message(message.channel, 'Calculating messages...')
        async for log in CLIENT.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1

        await CLIENT.edit_message(tmp, 'You have {} messages.'.format(counter))
    elif message.content.startswith('!sleep'):
        await asyncio.sleep(5)
        await CLIENT.send_message(message.channel, 'Done sleeping')

    learned_behaviours = learn_behaviours()
    for pattern in learned_behaviours:
        print('pattern: {}, message: {}'.format(pattern, message.content))
        match = re.search(pattern, message.content)
        if match is not None:
            print('Found a match! Calling behaviour')
            await learned_behaviours[pattern](CLIENT, match, message)


if __name__ == '__main__':
    CLIENT.run('MzY5OTQ5MTM2MjM5MzI5Mjgz.DMgC5A.MrxR71mAAiYIRDZgjF5y7fztZRU')
