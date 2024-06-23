import pprint

import Globals
import requests
import response_error
import logging
import sys

_logger = logging.getLogger(__name__)


MJ_APPLICATION_COMMAND_ID = None
MJ_APPLICATION_ID = '936929561302675456'
MJ_APPLICATION_COMMAND_VERSION = None

DISCORD_API_URI = "https://discord.com/api/v10"
DISCORD_INTERACTIONS_URI = DISCORD_API_URI + "/interactions"


# TODO: initialize variables on bot startup
def get_mjw_variables() -> (str, str, str):
    global MJ_APPLICATION_ID, MJ_APPLICATION_COMMAND_ID, MJ_APPLICATION_COMMAND_VERSION

    response = get_application_commands(MJ_APPLICATION_ID)
    if response.status_code != 200:
        response_error.log_response_error(_logger, response)
        sys.exit(-1)

    mj_app_commands = response.json()
    for cmd in mj_app_commands:
        if cmd["name"] == "imagine":
            MJ_APPLICATION_COMMAND_ID = cmd["id"]
            MJ_APPLICATION_COMMAND_VERSION = cmd["version"]
    mj_application_id = MJ_APPLICATION_ID
    mj_application_command_id = MJ_APPLICATION_COMMAND_ID
    mj_application_command_version = MJ_APPLICATION_COMMAND_VERSION
    return (mj_application_id, mj_application_command_id, mj_application_command_version)

def get_application_commands(application_id: str) -> requests.Response:
    """
    Requesting command data
    :param application_id: str
    :return:
    """
    headers = {"authorization": Globals.SALAI_TOKEN}
    return requests.get(DISCORD_API_URI + f"/applications/{application_id}/commands", headers=headers)


def passPromptToSelfBot(channelID: str, prompt: str) -> requests.Response:
    """
    Sends a given prompt to the self bot for processing.

    Args:
        channelID (str):
        prompt (str): The prompt to be sent to the self bot.

    Returns:
        requests.Response: The response from the self bot.
    """
    # if MJ_APPLICATION_ID is None or MJ_APPLICATION_COMMAND_VERSION is None or MJ_APPLICATION_COMMAND_ID is None:
    #     init_mjw_variables(channelID)

    payload = {
        "type": 2,
        "application_id": MJ_APPLICATION_ID,
        "guild_id": Globals.SERVER_ID,
        "channel_id": channelID,
        "session_id": "2fb980f65e5c9a77c96ca01f2c242cf6",
        "data": {
            "version": MJ_APPLICATION_COMMAND_VERSION,
            "id": MJ_APPLICATION_COMMAND_ID,
            "name": "imagine",
            "type": 1,
            "options": [{"type": 3, "name": "prompt", "value": prompt}],
            "application_command": {
                "id": MJ_APPLICATION_COMMAND_ID,
                "application_id": MJ_APPLICATION_ID,
                "version": MJ_APPLICATION_COMMAND_VERSION,
                "default_permission": True,
                "default_member_permissions": None,
                "type": 1,
                "nsfw": False,
                "name": "imagine",
                "description": "Create images with Midjourney",
                "dm_permission": True,
                "options": [
                    {"type": 3, "name": "prompt", "description": "The prompt to imagine", "required": True}
                ]
            },
            "attachments": []
        }
    }

    headers = {"authorization": Globals.SALAI_TOKEN}
    return requests.post(DISCORD_INTERACTIONS_URI, json=payload, headers=headers)


def upscale(index: int, channel_id: str,  message_id: str, message_hash: str) -> requests.Response:
    """
    Sends a request to the self bot to upscale an image.

    Args:
        index (int): The index of the image to be upscaled.
        message_id (str): The ID of the message containing the image.
        message_hash (str): The hash of the message containing the image.

    Returns:
        requests.Response: The response from the self bot.
    """

    payload = {
        "type": 3,
        "guild_id": Globals.SERVER_ID,
        "channel_id": channel_id,
        "message_flags": 0,
        "message_id": message_id,
        "application_id": MJ_APPLICATION_ID,
        "session_id": "45bc04dd4da37141a5f73dfbfaf5bdcf",
        "data": {
            "component_type": 2,
            "custom_id": f"MJ::JOB::upsample::{index}::{message_hash}",
        },
    }
    headers = {"authorization": Globals.SALAI_TOKEN}
    return requests.post(DISCORD_INTERACTIONS_URI, json=payload, headers=headers)


def reroll(channel_id: str, message_id: str, message_hash: str) -> requests.Response:
    """
    Sends a request to the self bot to generate a new image.

    Args:
        message_id (str): The ID of the message containing the image.
        message_hash (str): The hash of the message containing the image.

    Returns:
        requests.Response: The response from the self bot.
    """

    payload = {
        "type": 3,
        "guild_id": Globals.SERVER_ID,
        "channel_id": channel_id,
        "message_flags": 0,
        "message_id": message_id,
        "application_id": MJ_APPLICATION_ID,
        "session_id": "1f3dbdf09efdf93d81a3a6420882c92c",
        "data": {
            "component_type": 2,
            "custom_id": f"MJ::JOB::reroll::0::{message_hash}::SOLO",
        },
    }

    headers = {"authorization": Globals.SALAI_TOKEN}
    return requests.post(DISCORD_INTERACTIONS_URI, json=payload, headers=headers)


def variation(index: int, channel_id: str, message_id: str, message_hash: str, isSolo: bool) -> requests.Response:
    """
    Sends a request to the self bot to generate a new image with variations.

    Args:
        index (int): The index of the image to be generated.
        message_id (str): The ID of the message containing the image.
        message_hash (str): The hash of the message containing the image.
        isSolo (bool): Whether the image is a solo variation or not.

    Returns:
        requests.Response: The response from the self bot.
    """

    if isSolo:
        custom_id = f"MJ::JOB::variation::{index}::{message_hash}::SOLO"
    else:
        custom_id = f"MJ::JOB::variation::{index}::{message_hash}"

    payload = {
        "type": 3,
        "guild_id": Globals.SERVER_ID,
        "channel_id": channel_id,
        "message_flags": 0,
        "message_id": message_id,
        "application_id":MJ_APPLICATION_ID,
        "session_id": "1f3dbdf09efdf93d81a3a6420882c92c",
        "data": {
            "component_type": 2,
            "custom_id": f"{custom_id}",
        },
    }

    headers = {"authorization": Globals.SALAI_TOKEN}
    return requests.post(DISCORD_INTERACTIONS_URI, json=payload, headers=headers)


def soloInteraction(channel_id: str, message_id: str, message_hash: str, job: str) -> requests.Response:
    """
    Sends a request to the self bot for a solo interaction.

    Args:
        message_id (str): The ID of the message containing the image.
        message_hash (str): The hash of the message containing the image.
        job (str): The job to be performed by the self bot.

    Returns:
        requests.Response: The response from the self bot.
    """

    payload = {
        "type": 3,
        "guild_id": Globals.SERVER_ID,
        "channel_id": channel_id,
        "message_flags": 0,
        "message_id": message_id,
        "application_id": MJ_APPLICATION_ID,
        "session_id": "1f3dbdf09efdf93d81a3a6420882c92c",
        "data": {
            "component_type": 2,
            "custom_id": f"MJ::JOB::{job}::1::{message_hash}::SOLO",
        },
    }

    headers = {"authorization": Globals.SALAI_TOKEN}
    return requests.post(DISCORD_INTERACTIONS_URI, json=payload, headers=headers)