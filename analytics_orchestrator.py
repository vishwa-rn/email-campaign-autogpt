from langchain.base_language import BaseLanguageModel
from langchain.agents import AgentExecutor, ZeroShotAgent
from langchain.tools import Tool
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

ANALYTICS_ORCHESTRATOR_PROMPT = """
blah blah
"""


def retrieve_campaign_reports(objective: str) -> str:
    return "Retrieved the campaign report."


def _retrieve_campaign_reports_tool(llm: BaseLanguageModel) -> Tool:
    return Tool(
        name="retrieve_campaign_reports",
        description="Can be used to retrieve campaign report from the Mailchimp account to analyse and plan action accordingly",
        func=retrieve_campaign_reports
    )


def create_agent(
        llm: BaseLanguageModel
) -> AgentExecutor:
    tools = [
        _retrieve_campaign_reports_tool(llm=llm),
    ]
    prompt = PromptTemplate(
        template=ANALYTICS_ORCHESTRATOR_PROMPT
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
