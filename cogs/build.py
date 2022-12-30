from discord.ext.commands import Cog, Bot
from discord.app_commands import command, guilds
from discord import Interaction

from ..utils import Default


class Build(Cog):
	def __init__(self, bot: Bot) -> None:
		self.bot = bot
		
		super().__init__()

	
	@command(description="Build something in your town.")
	@guilds(Default.test_server)
	async def build(self, inter: Interaction) -> None:
		pass


async def setup(bot: Bot) -> None:
	await bot.add_cog(Build(bot), guilds=[Default.test_server])