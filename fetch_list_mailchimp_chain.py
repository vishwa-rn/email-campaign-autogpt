# Get the mailchimp lists from the server and ask user which one to choose. Once the user selects the list. The chain saves the list id in the memory.

# 1. This is a chain.
# 2. Fetch the lists from the user.
# 3. Ask the user to choose from them.
# 4. Ask LLM to return the choosen list id.


from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.base_language import BaseLanguageModel
import prompts
from connectors.mailchimp.main import MailchimpConnector
import json
import dotenv
from utils import update_pickle_file

# The chain takes in the lists information and returns a question to choose from for the user. Which we will chain with input and then the answer is sent back.


def fetch_list_chain():
    dotenv.load_dotenv()
    llm = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo')
    connector = MailchimpConnector()

    # Call get_lists on the connector object
    lists = connector.get_lists()
    print("got the lists")

    question_generation_prompt = PromptTemplate(
        template=prompts.CHOOSE_FROM_LISTS_PROMPT,
        input_variables=["json"]
    )
    chain = LLMChain(llm=llm, prompt=question_generation_prompt)
    questions = chain.run({
        "json": lists
    })

    choice = input(questions)

    question_generation_with_answer_prompt = PromptTemplate(
        template=prompts.CHOOSE_FROM_LISTS_SELECTION_PROMPT,
        input_variables=["questions", "user_choice"]
    )

    convert_list_to_json_chain = LLMChain(
        llm=llm, prompt=question_generation_with_answer_prompt)

    list = convert_list_to_json_chain.run({
        "questions": questions,
        "user_choice": choice
    })

    list = json.loads(list)
    update_pickle_file(key="list_id", value=list["list_id"])
    update_pickle_file(key="list_name", value=list["list_name"])
    return "Retrieved the list suitable for the objective and stored it in the shared memory"
