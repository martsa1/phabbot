''' Core code for Phabricator Discord bot, phabbot
'''
import logging
import asyncio
import os
import re

import discord
import yaml

import behaviours

logging.basicConfig(level=logging.INFO)


CLIENT = discord.Client()
PHAB_URL = ''
LEARNED_BEHAVIOURS = {}


@CLIENT.event
async def on_ready():
    ''' Log Phabbot base details on connection to Discord
    '''
    logging.info(
        'Logged in as {}, with ID: {}'.format(
            CLIENT.user.name, CLIENT.user.id
        )
    )
    logging.info('------')


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

    for pattern in LEARNED_BEHAVIOURS:
        print('pattern: {}, message: {}'.format(pattern, message.content))
        matches = re.findall(pattern, message.content)
        if matches is not None:
            print('Found a match! Calling behaviour')
            await LEARNED_BEHAVIOURS[pattern](
                CLIENT,
                PHAB_URL,
                matches,
                message
            )


if __name__ == '__main__':
    LEARNED_BEHAVIOURS = learn_behaviours()

    config_file_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
    if os.path.isfile(config_file_path):
        with open(config_file_path, 'r') as config_file:
            config = yaml.load(config_file)

    discord_token = config.get('discord_token', None)
    if discord_token is None:
        raise ValueError('Discord token is required for operation!  I need to '
                         'know who I am...')

    PHAB_URL = config.get('phabricator_url', None)
    if PHAB_URL is None:
        raise ValueError('Phabricator URL is required for operation!  I need '
                         'to know where to point you!')

    if PHAB_URL[-1] != '/':
        PHAB_URL += '/'

    CLIENT.run(discord_token)
