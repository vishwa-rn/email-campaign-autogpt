import os

from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.tools import tool, Tool
from langchain.base_language import BaseLanguageModel
from langchain.prompts import PromptTemplate
from langchain.agents import AgentExecutor, ZeroShotAgent
from prompts import ORCHESTRATOR_PROMPT
from gain_context import gain_context_chain
from gather_leads_agent import gather_leads_chain
from content_creator_chain import get_email_content_chain
from create_campaign_chain import create_campaign_chain
from send_campaign_chain import send_campaign_chain
from utils import update_pickle_file
from user_details import user_details
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(
    temperature=0, openai_api_key="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")  # type: ignore


def gain_context(objective: str):
    return gain_context_chain(llm=llm, user_objective=objective)


def _gain_context_tool(llm: BaseLanguageModel) -> Tool:
    tool = Tool(
        name="gain_context",
        description="Can be used to ask questions about the objective to gain more context to do a better job.",
        func=gain_context
    )
    return tool


def gather_leads(objective: str):
    return gather_leads_chain(llm=llm, user_objective=objective)


def _gather_leads_tool(
        llm: BaseLanguageModel
) -> Tool:
    tool = Tool(
        name="lead_generator",
        description="Can be used to generate leads and save them in the shared memory, like lead_generator.",
        func=gather_leads
    )
    return tool


def generate_mail_content(plan_str: str):
    return get_email_content_chain()


def _generate_mail_content_tool(
        llm: BaseLanguageModel
) -> Tool:
    tool = Tool(
        name="content_creator",
        description="Can be used to create the mail subject and the body for different individuals",
        func=generate_mail_content
    )
    return tool


def create_campaign(plan_str: str):
    return create_campaign_chain()


def _create_campaign_tool(llm: BaseLanguageModel) -> Tool:
    tool = Tool(
        name="create_campaign",
        description="Can be used to create an email campaign in mailchimp with the leads and the mail content",
        func=create_campaign
    )
    return tool


def start_campaign(plan_str: str):
    return send_campaign_chain()


def _start_campaign_tool(llm: BaseLanguageModel) -> Tool:
    tool = Tool(
        name="start_campaign",
        description="Can be used to start the campaign which was created earlier with the leads and the mail content.",
        func=start_campaign
    )
    return tool


def create_agent(
        llm: BaseLanguageModel
) -> AgentExecutor:
    tools = [
        _gather_leads_tool(llm=llm),
        _gain_context_tool(llm=llm),
        _generate_mail_content_tool(llm=llm),
        _start_campaign_tool(llm=llm),
        _create_campaign_tool(llm=llm)
    ]
    prompt = PromptTemplate(
        template=ORCHESTRATOR_PROMPT,
        input_variables=["input", "agent_scratchpad"],
        partial_variables={
            "tool_names": ", ".join([tool.name for tool in tools]),
            "tool_descriptions": "\n".join(
                [f"{tool.name}: {tool.description}" for tool in tools]
            ),
        },
    )
    agent = ZeroShotAgent(
        llm_chain=LLMChain(llm=llm, prompt=prompt),
        allowed_tools=[tool.name for tool in tools],
    )
    return AgentExecutor.from_agent_and_tools(
        agent=agent,
        tools=tools,
        verbose=True
    )


agentExecutor = create_agent(llm=llm)
objective = input("> What is your objective? \n")

update_pickle_file(key="user_objective", value=objective)
update_pickle_file(key="user_details", value=user_details)

agentExecutor.run(objective)
