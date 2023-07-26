import os
import random
import streamlit as st
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
import pandas as pd
from langchain.chat_models import ChatOpenAI
from elevenlabs import generate, play, set_api_key
from dotenv import load_dotenv
from elevenlabs.api.error import UnauthenticatedRateLimitError, RateLimitError
from database import Database
from embeddings import embed_text, get_vector_by_id

load_dotenv()

API_KEY = os.getenv("ELEVENLABS_API_KEY")

set_api_key(API_KEY)

tab1, tab2 = st.tabs(["Generate your podcast", "Chat/Listen to your previous podcast"])

with tab1:
    st.title("Generate your Podcast Clip!")

    topic_name = st.text_input("Enter the topic name:")
    time = st.number_input(
        "Enter the length of the podcast in minutes:",
        min_value=5.0,
        max_value=10.0,
        value=5.0,
        step=1.0,
        format="%.1f",
    )
    voice = st.radio(
        label="Choose a voice", options=["Rachel", "Adam"], index=0, horizontal=True
    )

    if st.button("Make my clip!"):
        # Change the prompt!

        # system_template = "Generate content for a podcast monologue on {topic_name} for an approx length of {time} seconds."
        system_template = "Generate a sentence with 10 words only on {topic_name}."
        system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)

        human_template = "{text}"
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

        chat_prompt = ChatPromptTemplate.from_messages(
            [system_message_prompt, human_message_prompt]
        )

        formatted_prompt = chat_prompt.format_prompt(
            topic_name=topic_name, time=time, text=""
        ).to_messages()

        chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.3)
        response = chat(formatted_prompt)

        # st.text_area("Generated Content:", value=response.content, height=200)

        transcript = response.content

        try:
            audio = generate(
                text=transcript,
                voice=voice,
                model="eleven_monolingual_v1",
            )
            st.write("Here's your podcast clip! ")
            st.audio(data=audio)

            db_id = random.randint(1,100)
            vec_id, _ = embed_text(transcript)
            print(id)

            user_input = Database(id=db_id, name="User04",topic=topic_name, voice=voice, transcription=transcript, audio_len=2, lang="Eng", vector_id=vec_id)
            status = user_input.insert_data()
            st.write(status)


        except UnauthenticatedRateLimitError:
            e = UnauthenticatedRateLimitError("Unauthenticated Rate Limit Error")
            st.exception(e)

        except RateLimitError:
            e = RateLimitError("Rate Limit")
            st.exception(e)

        with st.expander("Transcript"):
            st.write(transcript)

with tab2:
    st.title("Listen or Chat with your previous podcasts")
    records = Database.query()
    # print(type(records.data[0]))
    df = pd.DataFrame(records.data)
    # print(df)
    options = [item["topic"] for item in records.data]
    choice = st.selectbox("Select your choice", options)
    vector_id = df[df['topic'] == choice]['vectordbid']
    vector_id = list(vector_id.values)
    print(vector_id)
    value = get_vector_by_id(vector_id)
    print(value['vectors'][vector_id[0]]['values'])
    # print(vector_id)


