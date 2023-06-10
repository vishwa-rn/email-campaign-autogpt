import os
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from prompt_variables import USER_OBJECTIVE, USER_CONTEXT, USER_DETAILS
from prompts import SUBJECT_LINE_PROMPT, EMAIL_BODY_PROMPT
from utils import update_pickle_file, get_value_from_pickle

from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")


subject_line_prompt = PromptTemplate(
    input_variables=["user_objective", "user_context"],
    template=SUBJECT_LINE_PROMPT,
)
body_line_prompt = PromptTemplate(
    input_variables=["user_objective", "user_context", "user_details"],
    template=EMAIL_BODY_PROMPT
)

subject_line_chain = LLMChain(llm=llm, prompt=subject_line_prompt)
body_line_chain = LLMChain(llm=llm, prompt=body_line_prompt)


def get_subject_line_for_email_campaign():
    user_context = get_value_from_pickle(key="user_context")
    user_objective = get_value_from_pickle(key="user_objective")
    subject_line = subject_line_chain.run(
        {"user_objective": user_objective, "user_context": user_context})
    update_pickle_file(key="email_subject_line", value=subject_line)
    return subject_line


def get_body_for_email_campaign():
    user_context = get_value_from_pickle(key="user_context")
    user_objective = get_value_from_pickle(key="user_objective")
    user_details = get_value_from_pickle(key="user_details")
    body = body_line_chain.run({"user_objective": user_objective,
                                "user_context": user_context, "user_details": user_details})
    update_pickle_file(key="email_body", value=body)
    return body


def get_email_content():
    subject_line = get_subject_line_for_email_campaign()

    body = get_body_for_email_campaign()
    body = "Dear " + body
    return [subject_line, body]
