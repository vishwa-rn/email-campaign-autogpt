from langchain.base_language import BaseLanguageModel
from langchain.prompts import PromptTemplate
from prompts import GAIN_CONTEXT_PROMPT, GAIN_CONTEXT_QUESTIONS_PROMPT
from langchain.chains import LLMChain
import os
from utils import update_pickle_file
import json

user_objective_test = """Drive 200 signups for my upcoming webinar"""

questions_and_answers_test = """
1. ["What is the topic of your webinar?", "Deep Reinforcement learning"]
2. ["Who is the target audience for your webinar?", "Students, Working professionals, Enterprenuers"]
3. ["What are the date and time of the webinar?", "25 June 2023"]
4. ["Is it a live webinar or a pre-recorded one?", "Live webinar"]
5. ["What benefits can participants expect from attending the webinar (e.g., learning new skills, networking opportunities, access to exclusive content, etc.)?", "Learning new skills"]
6. ["How can participants register for the webinar? Is there a website or platform they should visit?", "codeasy.ai"]
7. "What information do you require from the participants during the registration process?", "Name, What do they want to learn from this experience, What is their working experience?"
8. ["Is there a registration fee? If so, how much is it?", "100$"]
9. ["Are there any specific messages or offers that have resonated well with your target audience in the past?", "No"]
10. ["Do you have a preferred email marketing platform?", "Mailchimp"]
11. ["Do you have any email templates or branding guidelines we should stick to?", "No"]
12. ["Do you have a specific timeline in mind for this email campaign?" "Introduction mail today and reminder mails for the people who haven't applied."]
13. ["Have you run similar email campaigns in the past? If so, what worked and what didn't?","No"]
"""


def gain_context_questions(llm: BaseLanguageModel, user_objective: str):
    prompt = PromptTemplate(
        input_variables=["user_objective"],
        template=GAIN_CONTEXT_QUESTIONS_PROMPT
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run(user_objective)


def gain_context_chain(llm: BaseLanguageModel, user_objective: str):
    questions = gain_context_questions(llm=llm, user_objective=user_objective)
    try:
        questions = json.loads(questions)
    except json.JSONDecodeError:
        print("json.JSONDecodeError for the questions from the LLM.")

    total_questions = len(questions)

    questions_and_answers = ""

    # Adding start=1 to start the enumeration from 1 instead of 0
    for i, question in enumerate(questions, start=1):
        response = input(f"\nQuestion {i} of {total_questions}: {question}\n")
        questions_and_answers += str([question, response]) + "\n"

    prompt = PromptTemplate(
        input_variables=["user_objective", "questions_and_answers"],
        template=GAIN_CONTEXT_PROMPT
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    context = chain.run(user_objective=user_objective,
                        questions_and_answers=questions_and_answers)
    update_pickle_file(key="user_context", value=context)
    return "Gained context about the objective."
