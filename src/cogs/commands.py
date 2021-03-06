import asyncio
import random

import discord
import requests
from discord.ext import commands

from src.cogs import BaseCog


class Commands(BaseCog):
    @commands.command(aliases=["hi", "sup", "안녕"])
    async def hello(self):
        """Returns a random hello phrase"""
        choices = ["hi",
                   "ohai",
                   "hello",
                   "안녕",
                   "안녕하세요",
                   "sup",
                   ]
        return await self.bot.say(random.choice(choices))

    @commands.command(aliases=["prune"], pass_context=True)
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=10):
        """Clears chat"""
        messages = self.bot.logs_from(ctx.message.channel, amount)
        count = 0
        async for msg in messages:
            try:
                await self.bot.delete_message(msg)
            except discord.Forbidden as e:
                print(e.args[0])
            if count >= 10:
                count = 0
                # Take a break to help avoid rate limit
                await asyncio.sleep(1)

    @commands.command(no_pm=True)
    async def say(self, *, message=None):
        """Says what you tell it to say"""
        if message is not None:
            return await self.bot.say(message)

    @commands.command()
    async def joined(self, member: discord.Member):
        """Says when a member joined."""
        return await self.bot.say("{0.name} joined on {0.joined_at}".format(member))

    @commands.command(aliases=["emojis"], pass_context=True)
    async def emoji(self, ctx):
        """Gets the emoji for this server"""
        server = ctx.message.server
        msg = ""
        for e in server.emojis:
            msg = msg + str(e) + " "
        return await self.bot.say(msg)

    @commands.command(pass_context=True)
    async def listserveroles(self, ctx):
        """Gets the roles for this server"""
        server = ctx.message.server
        msg = ""
        for e in server.roles:
            msg = msg + str(e) + "\n"
        return await self.bot.send_message(ctx.message.author, msg)

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_emojis=True)
    async def addemoji(self, ctx, name, url):
        """Add an emoji to this server based on the url"""
        server = ctx.message.server
        response = requests.get(url)
        image = response.content
        emoji = await self.bot.create_custom_emoji(server, name=name, image=image)
        return await self.bot.say("Done: {}".format(emoji))

    @commands.command()
    async def invite(self):
        """Get Invite link for bot"""
        return await self.bot.say("https://tny.click/invite")

    @commands.group(pass_context=True)
    async def cool(self, ctx):
        """Says if a something is cool."""
        if ctx.invoked_subcommand is None:
            return await self.bot.say("No, {0.subcommand_passed} is not cool.".format(ctx))

    @cool.command(name="bot")
    async def _bot(self):
        """Is the bot cool?"""
        return await self.bot.say("Yes, the bot is cool.")


def setup(bot, kwargs):
    bot.add_cog(Commands(bot))
