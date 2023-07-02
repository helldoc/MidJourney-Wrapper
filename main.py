import discord
import logging
logging.basicConfig(level=logging.INFO)

import Globals
from Salai import passPromptToSelfBot, upscale, variation, reroll, soloInteraction

bot = discord.Bot(intents=discord.Intents.all())
logger = logging.getLogger("bot")

# Original bot by https://github.com/Wildric-Auric
# Buttons view feature by https://github.com/RomainC-lab
# Assembling, docker, view feature improvements by https://github.com/helldoc

class MainView(discord.ui.View):
    """
    A class representing a main view that displays a set of buttons.

    Args:
        target_hash (str): A target hash to be used in some of the button functions.
        target_id (str): A target ID to be used in some of the button functions.
    """
    def __init__(self, channel_id: str, target_hash: str = "", target_id: str = ""):
        super().__init__(timeout=None)
        self.value = None
        self.channelID = channel_id
        self.targetHash = target_hash
        self.targetID = target_id

    @discord.ui.button(label="U1", style=discord.ButtonStyle.green, row=0, custom_id="MainView:upscale1")
    async def button1(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = 1
        await interaction.response.send_message(await mj_upscale(self.value, self.channelID, self.targetHash, self.targetID))

    @discord.ui.button(label="U2", style=discord.ButtonStyle.green, row=0, custom_id="MainView:upscale2")
    async def button2(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = 2
        await interaction.response.send_message(await mj_upscale(self.value, self.channelID, self.targetHash, self.targetID))

    @discord.ui.button(label="U3", style=discord.ButtonStyle.green, row=0, custom_id="MainView:upscale3")
    async def button3(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = 3
        await interaction.response.send_message(await mj_upscale(self.value, self.channelID, self.targetHash, self.targetID))

    @discord.ui.button(label="U4", style=discord.ButtonStyle.green, row=0, custom_id="MainView:upscale4")
    async def button4(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = 4
        await interaction.response.send_message(await mj_upscale(self.value, self.channelID, self.targetHash, self.targetID))

    @discord.ui.button(emoji="🔄", style=discord.ButtonStyle.green, row=0, custom_id="MainView:reroll")
    async def button5(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message(await mj_reroll(self.channelID, self.targetHash, self.targetID))

    @discord.ui.button(label="V1", style=discord.ButtonStyle.green, row=1, custom_id="MainView:variation1")
    async def button6(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = 1
        await interaction.response.send_message(await mj_variation(self.value, self.channelID, self.targetHash, self.targetID, False))

    @discord.ui.button(label="V2", style=discord.ButtonStyle.green, row=1, custom_id="MainView:variation2")
    async def button7(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = 2
        await interaction.response.send_message(await mj_variation(self.value, self.channelID, self.targetHash, self.targetID, False))

    @discord.ui.button(label="V3", style=discord.ButtonStyle.green, row=1, custom_id="MainView:variation3")
    async def button8(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = 3
        await interaction.response.send_message(await mj_variation(self.value, self.channelID, self.targetHash, self.targetID, False))

    @discord.ui.button(label="V4", style=discord.ButtonStyle.green, row=1, custom_id="MainView:variation4")
    async def button9(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = 4
        await interaction.response.send_message(await mj_variation(self.value, self.channelID, self.targetHash, self.targetID, False))


class UpscaledView(discord.ui.View):
    """
    A class representing a view that displays a set of buttons for interacting with an upscaled image.

    Args:
        channel_id (str): A channel id to answer
        target_hash (str): A target hash to be used in some of the button functions.
        target_id (str): A target ID to be used in some of the button functions.
    """
    def __init__(self, channel_id: str = "", target_hash: str = "", target_id: str = ""):
        super().__init__(timeout=None)
        self.channelID = channel_id
        self.targetHash = target_hash
        self.targetID = target_id

    @discord.ui.button(label="Make Variations", emoji="\U0001FA84", style=discord.ButtonStyle.green, row=0, custom_id="UpscaledView:variation")
    async def button1(self, button: discord.ui.Button, interaction: discord.Interaction):
        # receive response from mj_solo and send it to the user
        await interaction.response.send_message(await mj_solo(self.channelID, self.targetHash, self.targetID, "variation"))

    @discord.ui.button(label="Light Upscale Redo", emoji="🔍", style=discord.ButtonStyle.green, row=0, custom_id="UpscaledView:upsample_light")
    async def button2(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message(await mj_solo(self.channelID, self.targetHash, self.targetID, "upsample_light"))

    @discord.ui.button(label="Detailed Upscale Redo", emoji="🔍", style=discord.ButtonStyle.green, row=0, custom_id="UpscaledView:upsample")
    async def button3(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message(await mj_solo(self.channelID, self.targetHash, self.targetID, "upsample"))

    @discord.ui.button(label="Remaster", emoji="🆕", style=discord.ButtonStyle.green, row=0, custom_id="UpscaledView:remaster")
    async def button4(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message(await mj_solo(self.channelID, self.targetHash, self.targetID, "remaster"))


class RemasterView(discord.ui.View):
    """
    A class representing a view that displays a set of buttons for interacting with a remastered image.

    Args:
        target_hash (str): A target hash to be used in some of the button functions.
        target_id (str): A target ID to be used in some of the button functions.
    """
    def __init__(self, channel_id: str, target_hash: str = "", target_id: str = ""):
        super().__init__(timeout=None)
        self.value = None
        self.channelID = channel_id
        self.targetHash = target_hash
        self.targetID = target_id

    @discord.ui.button(label="U1", style=discord.ButtonStyle.green, row=0, custom_id="RemasterView:upscale1")
    async def button1(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = 1
        await interaction.response.send_message(await mj_upscale(self.value, self.channelID, self.targetHash, self.targetID))

    @discord.ui.button(label="U2", style=discord.ButtonStyle.green, row=0, custom_id="RemasterView:upscale2")
    async def button2(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = 2
        await interaction.response.send_message(await mj_upscale(self.value, self.channelID, self.targetHash, self.targetID))

    @discord.ui.button(emoji="🔄", style=discord.ButtonStyle.green, row=0, custom_id="RemasterView:reroll")
    async def button5(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message(await mj_reroll(self.channelID, self.targetHash, self.targetID))

    @discord.ui.button(label="V1", style=discord.ButtonStyle.green, row=1, custom_id="RemasterView:variation1")
    async def button6(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = 1
        await interaction.response.send_message(await mj_variation(self.value, self.channelID, self.targetHash, self.targetID, False))

    @discord.ui.button(label="V2", style=discord.ButtonStyle.green, row=1, custom_id="RemasterView:variation2")
    async def button7(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = 2
        await interaction.response.send_message(await mj_variation(self.value, self.channelID, self.targetHash, self.targetID, False))


@bot.event
async def on_ready():
    """
    This function is called when the bot is ready to start.
    """
    print(f"Logged in as {bot.user}")


@bot.command(description="Make DaVinci say something")
async def hello(ctx, sentence: discord.Option(str)):
    """
    Make the bot say a sentence.

    Args:
        ctx (discord.Context): The context of the command.
        sentence (discord.Option(str)): The sentence to be said by the bot.
    """

    await ctx.respond(sentence)


@bot.command(description="This command is a wrapper of MidJourneyAI")
async def mj_imagine(ctx, prompt: discord.Option(str)):
    """
    Send a prompt to the self bot for processing.

    Args:
        ctx (discord.Context): The context of the command.
        prompt (discord.Option(str)): The prompt to be sent to the self bot.
    """
    if Globals.USE_MESSAGED_CHANNEL:
        channel_id = ctx.channel.id
    else:
        channel_id = Globals.CHANNEL_ID

    response = passPromptToSelfBot(channel_id, prompt)

    if response.status_code >= 400:
        print(response.text)
        print(response.status_code)
        await ctx.respond("Request has failed; please try later")
    else:
        await ctx.respond(
            "Your image is being prepared, please wait a moment...")


async def mj_upscale(index: discord.Option(int), channelID: discord.Option(str), targetHash: discord.Option(str), targetID: discord.Option(str)):
    """
    Send a request to the self bot to upscale an image.

    Args:
        index (discord.Option(int)): The index of the image to be upscaled.
        channelID
        targetHash (discord.Option(str)): The hash of the message containing the image.
        targetID (discord.Option(str)): The ID of the message containing the image.

    Returns:
        str: The response from the self bot.
    """

    if (index <= 0 or index > 4):
        return "Invalid argument, pick from 1 to 4"

    response = upscale(index, channelID, targetID, targetHash)

    if response.status_code >= 400:
        return "Request has failed; please try later"

    return "Your image is being upscaled, please wait a moment..."


async def mj_reroll(channelID: discord.Option(str), targetHash: discord.Option(str), targetID: discord.Option(str)):
    """
    Send a request to the self bot to generate a new image.

    Args:
        channelID
        targetHash (discord.Option(str)): The hash of the message containing the image.
        targetID (discord.Option(str)): The ID of the message containing the image.

    Returns:
        str: The response from the self bot.
    """

    response = reroll(channelID, targetID, targetHash)
    if response.status_code >= 400:
        return "Request has failed; please try later"

    return "Your image is being rerolled, please wait a moment..."


async def mj_variation(index: discord.Option(int), channelID: discord.Option(str), targetHash: discord.Option(str), targetID: discord.Option(str), isSolo: discord.Option(bool)):
    """
    Send a request to the self bot to generate a new image with variations.

    Args:
        index (discord.Option(int)): The index of the image to be generated.
        targetHash (discord.Option(str)): The hash of the message containing the image.
        targetID (discord.Option(str)): The ID of the message containing the image.
        isSolo (discord.Option(bool)): Whether the image is a solo variation or not.

    Returns:
        str: The response from the self bot.
    """

    if (index <= 0 or index > 4):
        return "Invalid argument, pick from 1 to 4"

    response = variation(index, channelID, targetID, targetHash, isSolo)

    if response.status_code >= 400:
        return "Request has failed; please try later"

    return "Your image is being varied, please wait a moment..."


async def mj_solo(channelID: discord.Option(str), targetHash: discord.Option(str), targetID: discord.Option(str), jobType: discord.Option(str)):
    """
    Send a request to the self bot to generate a new image with variations.

    Args:
        targetHash (discord.Option(str)): The hash of the message containing the image.
        targetID (discord.Option(str)): The ID of the message containing the image.
        jobType (discord.Option(str)): The type of the job to be performed.

    Returns:
        str: The response from the self bot.
    """

    response = soloInteraction(channelID, targetID, targetHash, jobType)
    if response.status_code >= 400:
        return "Request has failed; please try later"

    return "Your image is being updated, please wait a moment..."

def _create_view_from_message(message: discord.Message):
    channelId = message.channel.id
    targetHash = str((message.attachments[0].url.split("_")[-1]).split(".")[0])
    targetID = str(message.id)
    if "Image #" in message.content:
        view = UpscaledView(channelId, targetHash, targetID)
    elif "Remaster by" in message.content:
        view = MainView(channelId, targetHash, targetID)
    else:
        view = MainView(channelId, targetHash, targetID)

    return view

@bot.event
async def on_message(message: discord.Message):
    """
    If the message is in the right channel, and the message has an image, and the message is from the
    midjourney bot, then send a message with a button that links to the image.

    Args:
      message: The message object
    """
    channelId = message.channel.id
    if not Globals.USE_MESSAGED_CHANNEL and channelId != int(Globals.CHANNEL_ID):
        return

    if not message.components or message.author.id != int(Globals.MID_JOURNEY_ID):
        return

    if message.attachments:
        infoMessage = "⚠ Use this button instead of the original one"
        view = _create_view_from_message(message)
        await message.reply(infoMessage, view=view)
    else:
        await message.channel.send("No image found")

@bot.event
async def on_interaction(interaction: discord.Interaction):
    """
    https://docs.pycord.dev/en/stable/api/events.html#discord.on_interaction
    Slot called on new interaction. Here used to restore Views listeners, if bot are reloaded

    :param interaction:
    :return:
    """

    if interaction.is_component():
        state = interaction.message.channel._state
        view_store = state._view_store
        if not view_store.is_message_tracked(interaction.message.id):
            logger.debug("Restoring view for message %s", interaction.message.id)
            logger.debug("Using message reference to restore view %s", interaction.message.reference)
            if interaction.message.reference:
                replied_message = await interaction.message.channel.fetch_message(interaction.message.reference.message_id)
                logger.debug("Fetched message %s", replied_message)
                view = _create_view_from_message(replied_message)
                view_store.add_view(view, interaction.message.id)
                component_type = interaction.data["component_type"]
                custom_id = interaction.data["custom_id"]
                view_store.dispatch(component_type, custom_id, interaction)

    # default behavior
    await bot.process_application_commands(interaction)

bot.run(Globals.DAVINCI_TOKEN)
