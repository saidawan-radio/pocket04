from telethon.tl.types import DocumentAttributeAudio, Message
from config import conf
import re
import json

extension_map = {
    'audio/mpeg': 'mp3',
    'audio/mp3': 'mp3',
    'audio/mp4': 'm4a',
    'audio/m4a': 'm4a',
    'audio/ogg': 'ogg',
    'audio/flac': 'flac',
    'audio/aac': 'aac',
    'audio/wav': 'wav',
    'audio/x-wav': 'wav',
    'audio/webm': 'webm',
    'audio/x-aac': 'acc',
    'audio/x-aiff': 'aiff'
}

class AudioDetail:
    def __init__(self, msg=None, id=None):
        if msg:
            self._id = id
            self.attribute_audio = self.getDocumentAttributeAudio(msg)
            self.title = self.get_title(self.attribute_audio)
            self.performer = self.get_performer(self.attribute_audio)
            self.duration = self.get_duration(self.attribute_audio)
            self.date = self.get_date(msg)
            self.author_name = self.get_author(msg)
            self.channel = self.get_channel(msg)
            self.msg_id = self.get_msg_id(msg)
            self.message = self.get_msg_text(msg)
            self.edit_date = self.get_edit_date(msg)
            self.mime_type = self.get_mime_type(msg)
            self.extension = self.get_extension()
            self.size = self.get_size(msg)
            self.document_id = self.get_document_id(msg)
    
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, val):
        self._id = str(val)

    @property
    def filename(self):
        return self.generate_filename()

    def getDocumentAttributeAudio(self, msg):
        for atribute in msg.audio.attributes:
            if isinstance(atribute, DocumentAttributeAudio):
                return atribute

    def get_title(self, attribute_audio):
        return attribute_audio.title
    
    def get_performer(self, attribute_audio):
        return attribute_audio.performer
    
    def get_duration(self, attribute_audio):
        return attribute_audio.duration
    
    def get_date(self, msg):
        return msg.date.strftime("%Y%m%d-%H%M")
    
    def get_author(self, msg):
        return msg.post_author
    
    def get_channel(self, msg):
        return {
            "id" : msg.chat.id,
            "username" : msg.chat.username,
            "name" : msg.chat.title
        }

    def get_msg_id(self, msg):
        return str(msg.id)
    
    def get_msg_text(self, msg):
        return msg.message
    
    def get_mime_type(self, msg):
        if msg.audio:
            return msg.audio.mime_type
    
    def get_extension(self):
        mime = self.mime_type.lower()
        if mime in extension_map:
            return extension_map[mime]
        else:
            print(f"msg id: {self.msg_id}: extension not found: ", self.mime_type)
            return None
    
    def get_size(self, msg):
        # Return size in MB
        return msg.audio.size // 10 ** 6 + 1
    
    def get_document_id(self, msg):
        return msg.audio.id
    
    def is_allowed_filename(self, word):
        pat = re.compile(conf.FILENAME_PATTERN)
        if word and re.match(pat, word):
            return True
        else:
            return False

    def char_normalization(self, char, input_string):

        return re.sub(rf'{char}+', char, input_string)

        
    def clean_and_format_string(self, input_string):
        # Replace space, _, and | with -
        transformed_string = re.sub(r'^\d+', '', input_string)
        transformed_string = transformed_string.replace('@', '-').replace('_', '-')\
                                            .replace('|', '-').replace('@', '-')\
                                            .replace('~', "-").replace('.', '-')\
                                            .replace("'", "-").replace(' ', '-')\
                                            .replace("&", "-")
        
        # Remove hyphens from the beginning of the string
        transformed_string = transformed_string.lstrip('-')
        
        # Replace multiple consecutive hyphens with a single hyphen
        transformed_string = self.char_normalization('-', transformed_string)
        
        return transformed_string

    def generate_filename(self):
        channel_username = self.channel["username"]
        date = self.date
        audio_title = ""
        audio_artist = ""

        if self.is_allowed_filename(self.title):
            audio_title = self.clean_and_format_string(self.title)
        if self.is_allowed_filename(self.performer):
            audio_artist = self.clean_and_format_string(self.performer)
        
        filename = str(self.id) + f"_{channel_username}_{audio_title}_{audio_artist}_{date}.{self.extension}"
        return self.char_normalization("_", filename)

    def get_edit_date(self, msg):
        if msg.edit_date:
            return msg.edit_date.strftime(conf.DATE_FORMAT)
        return self.get_date(msg)
    
    def to_dict(self):
       return {
        "id": self.id,
        "title": self.title,
        "performer": self.performer,
        "duration": self.duration,
        "date": self.date,
        "author_name": self.author_name,
        "channel": self.channel,
        "msg_id": self.msg_id,
        "message": self.message,
        "filename": self.filename,
        "mime_type": self.mime_type,
        "edit_date": self.edit_date,
        "size" : self.size,
        "document_id" : self.document_id
    }
    
    @staticmethod
    def from_dict(detail):
        audio_detail = AudioDetail()
        audio_detail.id = detail["id"]
        audio_detail.title = detail["title"]
        audio_detail.performer = detail["performer"]
        audio_detail.duration = detail["duration"]
        audio_detail.date = detail["date"]
        audio_detail.author_name = detail["author_name"]
        audio_detail.channel = detail["channel"]
        audio_detail.msg_id = detail["msg_id"]
        audio_detail.message = detail["message"]
        audio_detail.edit_date = detail["edit_date"]
        audio_detail.mime_type = detail["mime_type"]
        audio_detail.extension = extension_map[detail["mime_type"].lower()]
        audio_detail.size = detail["size"]
        audio_detail.document_id = detail["document_id"]
    
        return audio_detail
        