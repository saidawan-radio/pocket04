import asyncio
from telethon import TelegramClient
from telethon.tl.types import Message
from telethon.sessions import StringSession
from AudioDetail import AudioDetail
import logging
from datetime import datetime
import json
from config import conf


API_ID = int(conf.API_ID)
API_HASH = conf.API_HASH
SESSION_OBJ=StringSession(conf.SESSION_STR)

CHANNEL_USERNAME = conf.CHANNEL_USERNAME
DOWNLOAD_PATH= conf.DOWNLOAD_PATH
DATA_FILE_PATH = conf.DATA_FILE_PATH
DATE_FORMAT = conf.DATE_FORMAT
LOAD_START_DATE = conf.LOAD_START_DATE
DURATION_LIMIT = int(conf.DURATION_LIMIT)
MIN_MSG_ID = int(conf.MIN_MSG_ID)
DATA_FETCH_LIMIT = int(conf.DATA_FETCH_LIMIT)
DATA_FETCH_SIZE_LIMIT = conf.DATA_FETCH_SIZE_LIMIT
FILENAME_PATTERN = conf.FILENAME_PATTERN

proxy=("http", "127.0.0.1", 10808)

#-----------------------------------------------------
#---------------- Define Functions -------------------

def load_json(file):
    with open(file, 'r', encoding="utf-8") as f:
        data = json.load(f)
        return data

def dump_json(file, data):
    with open(file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def load_datetime(strdate, strformat):
    return datetime.strptime(strdate, strformat)

def audio_detail_update(audio:AudioDetail, data:dict):
    stored_detail_id = data["map_msg_id"][audio.msg_id]
    stored_detail = data["audio_info"][stored_detail_id]
    if load_datetime(audio.edit_date, DATE_FORMAT) > load_datetime(stored_detail["edit_date"], DATE_FORMAT):
        data["audio_info"][stored_detail_id] = audio.to_dict()

def audio_detail_append(audio:AudioDetail, data:dict):
    if audio.msg_id in data["map_msg_id"]:
        audio.id = data["map_msg_id"][audio.msg_id]
        audio_detail_update(audio, data)
    else:
        data["general_info"]["last_internal_id"] += 1
        audio.id = data["general_info"]["last_internal_id"]
        data["audio_info"][audio.id] = audio.to_dict()
        data["map_msg_id"][audio.msg_id] = audio.id
        
async def audio_detail_fetcher(client, channel, min_id, data_limit, duration_limit, data):
    async for msg in client.iter_messages(channel, min_id=min_id, reverse=True, limit=data_limit):
        if not msg.audio:
            continue
        audio = AudioDetail(msg)
        if audio.duration <= duration_limit:
            audio_detail_append(audio, data)
    return data

#----------------------------------------------------------

data = {
    "audio_info" : {},
    "map_msg_id" : {},
    "general_info": {
        "last_internal_id": 0
    }
}

data = load_json(DATA_FILE_PATH)
        
async def get_msg_by_audio_detail(client:TelegramClient,chat, audio:AudioDetail):

    msg = await client.get_messages(chat, ids=int(audio.msg_id))
    return msg

async def downoad_audio_by_msg(msg:Message, file_path:str, file_name:str):
    if hasattr(msg, "audio") and msg.audio:
        file = f"{file_path}/{file_name}"
        await msg.download_media(file=file)

async def download_audio_by_audio_detail(client:TelegramClient, chat, audio:AudioDetail):
    msg = await get_msg_by_audio_detail(client, chat, audio)
    await downoad_audio_by_msg(msg, DOWNLOAD_PATH, audio.filename)

async def main():
    client = TelegramClient(SESSION_OBJ, API_ID, API_HASH, proxy=proxy)
    await client.start()
    channel = await client.get_entity(CHANNEL_USERNAME)
    await audio_detail_fetcher(client, channel, MIN_MSG_ID, DATA_FETCH_LIMIT, DURATION_LIMIT, data)
    dump_json(DATA_FILE_PATH, data)

asyncio.run(main())





