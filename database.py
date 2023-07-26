import os
import uuid
import typing
import time
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)


class Database:
    """A vector database for storing the data of the user and its generated podcast"""

    def __init__(self, id: str, name: str, topic: str, voice: str, audio_len: float, transcription: str, lang: str, vector_id: str):
        self.id = id
        self.name = name
        self.topic = topic
        self.length = audio_len
        self.voice = voice
        self.transcription = transcription
        self.lang = lang
        self.vector_id= vector_id

    def insert_data(self):
        data, count = (
            supabase.table("podcasts_database")
            .insert(
                {
                    "id": self.id,
                    "username": self.name,
                    "topic": self.topic,
                    "language": self.lang,
                    "voice": self.voice,
                    "audio_length": self.length,
                    "transcription": self.transcription,
                    "vectordbid": self.vector_id
                }
            )
            .execute()
        )
        return "Success"

    @staticmethod
    def query():
        response = supabase.table("podcasts_database").select("*").execute()
        return response
