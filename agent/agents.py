from agent.constants import * 
from langchain_core.prompts import FewShotChatMessagePromptTemplate, ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os

google_api_key = os.getenv("GOOGLE_API_KEY")
if not google_api_key:
    raise ValueError("GOOGLE_API_KEY environment variable not set")

os.environ["GOOGLE_API_KEY"] = google_api_key

prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "{input} {state}"),
        ("ai", "{answer}"),
    ]
)

modify_few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=prompt,
    examples=modify_examples,
)

modify_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", modify_instructions),
        modify_few_shot_prompt,
        ("human", "{input} {state}"),
    ]
)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

modify_agent = modify_prompt | llm

execute_few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=prompt,
    examples=execute_examples,
)

execute_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", execute_instructions),
        execute_few_shot_prompt,
        ("human", "{input} {state}"),
    ]
)

execute_agent = execute_prompt | llm