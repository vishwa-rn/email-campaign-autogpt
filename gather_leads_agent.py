import os
from langchain.base_language import BaseLanguageModel
from langchain.agents import AgentExecutor, ZeroShotAgent
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.tools import Tool
from prompts import LEADS_AGENT_PROMPT
from upload_leads_excel_chain import upload_leads_excel_chain
from fetch_list_mailchimp_chain import fetch_list_chain
# from langchain.chat_models import ChatOpenAI
# from dotenv import load_dotenv


leads_prompt = """
How would you want to setup leads for the mails?
1. Upload an excel?
2. Use an existing mailchimp list?
Type the choice. 1 or 2.
"""


def fetch_from_mailchimp_lists(objective: str) -> str:
    return fetch_list_chain()


def _fetch_mailchimp_list_tool(
        llm: BaseLanguageModel
) -> Tool:
    tool = Tool(
        name="fetch_from_mailchimp_lists",
        description="Can be used to fetch a list of leads in Mailchimp for the email campaign to achieve the user objective.",
        func=fetch_from_mailchimp_lists
    )
    return tool


def upload_excel(objective: str):
    return upload_leads_excel_chain()


def _upload_excel_tool(
        llm: BaseLanguageModel
) -> Tool:
    tool = Tool(
        name="upload_excel",
        description="Can be used to take an excel from the user and use it as leads for the email campaign",
        func=upload_excel,
    )
    return tool


def create_leads_agent(llm: BaseLanguageModel, user_objective: str) -> AgentExecutor:
    tools = [
        _fetch_mailchimp_list_tool(llm=llm),
        _upload_excel_tool(llm=llm)
    ]
    prompt = PromptTemplate(
        template=LEADS_AGENT_PROMPT,
        input_variables=["input", "agent_scratchpad"],
        partial_variables={
            "tool_names":  ", ".join([tool.name for tool in tools]),
            "tool_descriptions": "\n".join(
                [f"{tool.name}: {tool.description}" for tool in tools]
            ),
            "user_objective": user_objective
        }
    )
    agent = ZeroShotAgent(
        llm_chain=LLMChain(llm=llm, prompt=prompt),
        allowed_tools=[tool.name for tool in tools]
    )
    return AgentExecutor.from_agent_and_tools(
        agent=agent,
        tools=tools,
        verbose=True
    )

# What should be the goal?
# 1. Start an agent with three options. - human input to choose from the other two options


def gather_leads_chain(llm: BaseLanguageModel, user_objective: str) -> str:
    agent_executor = create_leads_agent(llm=llm, user_objective=user_objective)
    agent_executor.run("Use an existing mailchimp list.")
    return "Gathered leads for this objective and saved them in the shared memory"


# Remove the following code

# load_dotenv()
# llm = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo')  # type: ignore
# memory = dict()
# gather_leads_chain(llm=llm, user_objective="Drive 200 signups.", memory=memory)
