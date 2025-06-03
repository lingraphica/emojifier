import os
from keys import openAIapikey
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import (SystemMessage, HumanMessage)

def main():
    os.environ["OPENAI_API_KEY"] = openAIapikey
    st.set_page_config(
        page_title="Emoji Summary",
        page_icon="🤖")

    container = st.container()
    with container:
        with st.form(key="my form", clear_on_submit=False):

            #Allow the user to enter some text
            userText  = st.text_area(label="Enter some text: ", key="userText", height = 200)
            
            #Add a button to summarize the text
            submit_button = st.form_submit_button(label="Summarize Into Emojis")

        if submit_button:

            #Check that text was provided
            if not userText:
                st.error("Text is missing")

            if userText:
                with st.spinner("Thinking..."):
                    llm = ChatOpenAI(model_name="gpt-4.1-nano", temperature=0.3) #run the LLM slightly chilled to prevent hallucinations
                    messages = [
                        SystemMessage(content="""
You are helping people with aphasia understand text by converting it to emojis. Your task is to summarize the given text using only emojis that clearly represent the main ideas and emotions.

Guidelines:
- Use 3-8 emojis maximum
- Focus on the main message, not every detail
- Include emotions when present (😊😢😠etc.)
- Use sequence that tells the story from left to right
- No text, only emojis in your response"""),
                        HumanMessage(content=f"{userText}"),]
                    result = llm.invoke(messages)
            
                #Display the ressponse to the user
                st.markdown(f"{result.content}")
    
if __name__ == "__main__":
    main()