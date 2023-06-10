import os
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from prompt_variables import USER_OBJECTIVE, USER_CONTEXT, USER_DETAILS
from prompts import SUBJECT_LINE_PROMPT, EMAIL_BODY_PROMPT

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


def get_subject_line_for_email_campaign(user_objective=USER_OBJECTIVE, user_context=USER_CONTEXT):
    subject_line = subject_line_chain.run({"user_objective": user_objective,
                                           "user_context": user_context})
    return subject_line


def get_body_for_email_campaign(user_objective, user_context=USER_CONTEXT, user_details=USER_DETAILS):
    body = body_line_chain.run({"user_objective": user_objective,
                                "user_context": user_context, "user_details": user_details})
    return body


def get_email_content(user_objective=USER_OBJECTIVE, user_context=USER_CONTEXT, user_details=USER_DETAILS):
    subject_line = get_subject_line_for_email_campaign(
        user_objective=user_objective, user_context=user_context)

    body = get_body_for_email_campaign(
        user_objective=user_objective, user_context=user_context, user_details=user_details)
    body = "Dear " + body
    return [
        subject_line, body
    ]
