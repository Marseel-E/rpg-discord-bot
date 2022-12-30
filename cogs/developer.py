from discord.ext.commands import Cog, Bot, Context


class Developer(Cog):
	def __init__(self, bot: Bot) -> None:
		self.bot = bot

		super().__init__()


	async def cog_check(self, ctx: Context) -> bool:
		super().cog_check(ctx)

		return self.bot.is_owner()


async def setup(bot: Bot) -> None:
	await bot.add_cog(Developer(bot))