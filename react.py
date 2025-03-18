import discord
from discord.ext import tasks
import asyncio
import requests

token = ['x']

target_users_file = 'users.txt'

emojis = ['☠', '😭']

# uncomment and replace with voice channel ID if you want the bot to join a voice channel

# voice_channel_id = 123456789890123

class SelfBot(discord.Client):
    def __init__(self, token, voice_channel_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = token
        self.voice_channel_id = voice_channel_id
        self.target_user_ids = set()
        self.reload_target_users.start()

    async def on_ready(self):
        print(f'Logged in as {self.user}')
        channel = self.get_channel(self.voice_channel_id)
        if isinstance(channel, discord.VoiceChannel):
            voice_client = await channel.connect()
            await voice_client.guild.change_voice_state(channel=channel, self_mute=True, self_deaf=False)
        else:
            print(f'Channel ID {self.voice_channel_id} is not a voice channel')

    async def on_message(self, message):
        if message.author.id in self.target_user_ids:
            for emoji in emojis:
                try:
                    await message.add_reaction(emoji)
                except Exception as e:
                    print(f'Error adding reaction: {e}')

    @tasks.loop(seconds=5)
    async def reload_target_users(self):
        try:
            with open(target_users_file, 'r') as f:
                lines = f.readlines()
            self.target_user_ids = set(int(line.strip()) for line in lines if line.strip())
            print(f'Reloaded target_user_ids: {self.target_user_ids}')
        except Exception as e:
            print(f'Error reloading target users: {e}')



    def run(self):
        super().run(self.token, bot=False)

clients = [SelfBot(token, voice_channel_id) for token in token]

for client in clients:
    client.run()
