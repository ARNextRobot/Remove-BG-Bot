# Made with python3
# (C) @FayasNoushad
# Copyright permission under MIT License
# All rights reserved by FayasNoushad
# License -> https://github.com/FayasNoushad/Remove-BG-Bot/blob/main/LICENSE

import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from removebg import RemoveBG

API = os.environ["REMOVEBG_API"]
REMOVE_BG = RemoveBg(API, "removebg_error.log")
IMG_PATH = "./DOWNLOADS" + "dl_image.jpg"

FayasNoushad = Client(
    "Remove Background Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"],
)

START_TEXT = """
Hello {}, I am a photo background remover bot. Send me a photo I will send the photo without background.

**Developed with ❤️ by @SarahMaiaOff**
"""
HELP_TEXT = """
- Just send me a photo
- I will download it
- I will send the photo without background

**Developed with ❤️ by @SarahMaiaOff**
"""
ABOUT_TEXT = """
- **Bot :** `Backround Remover Bot`
- **Creator:** [Sarah Maia](https://telegram.me/SarahMaiaOff)
- **Channel:** [Fayas Noushad](https://telegram.me/ARNextRobot)
- **Support Group:** [ARNext Robot Group](https://t.me/ARNextRobotGroup)
- **Water Mark Bot:** [Python3](https://t.me/WaterMarkNextBot)
"""
START_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Channel', url='https://telegram.me/ARNextRobot'),
        InlineKeyboardButton('Feedback', url='https://telegram.me/ARNextRobotContact')
        ],[
        InlineKeyboardButton('Help', callback_data='help'),
        InlineKeyboardButton('About', callback_data='about'),
        InlineKeyboardButton('Close', callback_data='close')
        ]]
    )
HELP_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Home', callback_data='home'),
        InlineKeyboardButton('About', callback_data='about'),
        InlineKeyboardButton('Close', callback_data='close')
        ]]
    )
ABOUT_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Home', callback_data='home'),
        InlineKeyboardButton('Help', callback_data='help'),
        InlineKeyboardButton('Close', callback_data='close')
        ]]
    )
ERROR_BUTTON = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Help', callback_data='help'),
        InlineKeyboardButton('Close', callback_data='close')
        ]]
    )

@FayasNoushad.on_callback_query()
async def cb_data(bot, update):
    if update.data == "home":
        await update.message.edit_text(
            text=START_TEXT.format(update.from_user.mention),
            reply_markup=START_BUTTONS,
            disable_web_page_preview=True
        )
    elif update.data == "help":
        await update.message.edit_text(
            text=HELP_TEXT,
            reply_markup=HELP_BUTTONS,
            disable_web_page_preview=True
        )
    elif update.data == "about":
        await update.message.edit_text(
            text=ABOUT_TEXT,
            reply_markup=ABOUT_BUTTONS,
            disable_web_page_preview=True
        )
    else:
        await update.message.delete()

@FayasNoushad.on_message(filters.private & filters.command(["start"]))
async def start(bot, update):
    await update.reply_text(
        text=START_TEXT.format(update.from_user.mention),
        disable_web_page_preview=True,
        reply_markup=START_BUTTONS
    )

@FayasNoushad.on_message(filters.private & filters.media)
async def remove_background(bot, update):
    if not API:
        await update.reply_text(
            text="Error :- Api is error",
            disable_web_page_preview=True
        )
        return
    message = await update.reply_text(
        text="Analysing",
        disable_web_page_preview=True
    )
    if (update and update.media and (update.photo or (update.document and "image" in update.document.mime_type))):
        await update.download_media()
        await message.edit_text(
            text="Photo downloaded successfully. Now removing background.",
            disable_web_page_preview=True
        )
        try:
            REMOVE_BG.remove_background_from_img_file(IMG_PATH)
            await update.reply_document(
                document=IMG_PATH + "_no_bg.png"
            )
            await message.delete()
        except Exception:
            await message.edit_text(
                text="Something went wrong! May be API limits.",
                disable_web_page_preview=True
            )
