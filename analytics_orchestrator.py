from langchain.base_language import BaseLanguageModel
from langchain.agents import AgentExecutor, ZeroShotAgent
from langchain.tools import Tool
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from retrieve_campaign_reports_chain import retrieve_campaign_reports_chain
from improve_opens_chain import improve_opens_chain
from prompts import ANALYTICS_ORCHESTRATOR_PROMPT
import dotenv


dotenv.load_dotenv()

llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")


def improve_opens(objective: str) -> str:
    return improve_opens_chain()


def _improve_opens_tool(llm: BaseLanguageModel) -> Tool:
    return Tool(
        name="improve_opens",
        description="Can be used to improve the open rate of campaign",
        func=improve_opens
    )


def improve_clicks(objective: str) -> str:
    return "Started a new campaign with changes to improve clicks."


def _improve_clicks_tool(llm: BaseLanguageModel) -> Tool:
    return Tool(
        name="improve_clicks",
        description="Can be used to improve the click rate of the campaign",
        func=improve_clicks
    )


def create_analytics_agent(
        llm: BaseLanguageModel,
        analytics: str
) -> AgentExecutor:
    tools = [
        _improve_opens_tool(llm=llm),
        _improve_clicks_tool(llm=llm)
    ]
    prompt = PromptTemplate(
        template=ANALYTICS_ORCHESTRATOR_PROMPT,
        input_variables=["input", "agent_scratchpad"],
        partial_variables={
            "tool_names": ", ".join([tool.name for tool in tools]),
            "tool_descriptions": "\n".join(
                [f"{tool.name}: {tool.description}" for tool in tools]
            ),
            "analytics": analytics
        },
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


report_summary = retrieve_campaign_reports_chain("Dummy objective")

print(report_summary)

agent_executor = create_analytics_agent(
    llm=llm,
    analytics=report_summary
)

agent_executor.run("Drive 100 signups for my webinar event.")
