"""
https://replit.com/@subinps/TakeOutRequest
"""

import asyncio
from pyrogram import Client
from pyrogram.raw.functions.channels import GetLeftChannels
from pyrogram.errors import TakeoutInitDelay, FloodWait

async def take_out(api_id=None, api_hash=None, session=None):
    msg = "<b><u>Chats</u></b>\n\n"
    try:
        if not api_id:
            api_id   = int(input("Enter API ID: "))
        if not api_hash:
            api_hash = input("Enter API HASH: ")
        if not session:
            async with Client(name="name", api_id=api_id, api_hash=api_hash) as client:
                session = await client.export_session_string()
    except Exception as e:
        print(e)
        print("Error, Exiting")
        return
    try:
        async with Client(name="name", api_id=api_id, api_hash=api_hash, session_string=session, takeout=True) as client:
            ch = await client.send(GetLeftChannels(offset=0))
            for channel in ch.chats:
                if channel.creator:
                   try:
                       link = await client.export_chat_invite_link(int("-100" + str(channel.id)))
                   except FloodWait as e:
                       await asyncio.sleep(e.x)
                       link = await client.export_chat_invite_link(int("-100" + str(channel.id)))
                   msg += f"{channel.title}: {link}"
            await client.send_message("me", msg)
            print("Check your saved messages!")
    except TakeoutInitDelay as e:
        k = input('Please Confirm the takeout request from your other device and enter yes: ')
        if k.lower() == 'yes':
            await take_out(api_id, api_hash, session)
        else:
            print("Cancelled")
            return
    except Exception as e:
        print(e)
        return

if ___name___ == "__main__":
   asyncio.get_event_loop().run_until_complete(take_out())
