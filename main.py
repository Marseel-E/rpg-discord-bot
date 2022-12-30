from os import environ, getcwd, listdir
from traceback import print_tb

from discord import Activity, ActivityType, Status, Intents
from discord.ext.commands import Bot, ExtensionNotFound, ExtensionAlreadyLoaded, NoEntryPointError, ExtensionFailed
from discord.ext.tasks import loop

from dotenv import load_dotenv

load_dotenv(f"{getcwd()}/utils/.env")

from utils import Default, log


class Watching(Activity):
	def __init__(self, text: str) -> None:
		super().__init__(name=text, type=ActivityType.watching)


class RPGBot(Bot):
	def __init__(self) -> None:
		super().__init__(
			command_prefix=".",
			case_sensitive=False,
			status=Status.online,
			intents=Intents.default(),
			application_id=environ.get("APP_ID"),
			description="rpg"
		)

	
	@loop(seconds=30.0)
	async def continous_handler(self) -> None:
		self.activity = Watching(f"{len(self.users)} players")

	@continous_handler.before_loop
	async def before_continous_handler(self) -> None:
		log("status", "waiting to start 'continous_handler'")
		
		await self.wait_until_ready()

		log("status", "ready to start 'continous_handler'")


	async def on_ready(self) -> None:
		log("status", "running")


	async def setup_hook(self) -> None:
		for cog in listdir(f"{getcwd()}/cogs"):
			if not cog.endswith(".py"):
				continue

			try:
				await self.load_extension(f"cogs.{cog[:-3]}")
			except Exception as e:
				log("error", f"failed to load '{cog}'")
				print_tb(e)
			else:
				log("status", f"loaded '{cog}'")

		try:
			await self.tree.sync()
			await self.tree.sync(guild=Default.test_server)
		except Exception as e:
			log("error", "failed to sync commands")
			print_tb(e)
		else:
			log("status", "synced commands")

		self.continous_handler.start()

		log("status", "started 'continous_handler'")

bot = RPGBot()


if __name__ == '__main__':
	bot.run(environ.get("TOKEN"))
