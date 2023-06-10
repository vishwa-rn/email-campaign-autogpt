from langchain.base_language import BaseLanguageModel
from langchain.agents import AgentExecutor, ZeroShotAgent
from langchain.tools import Tool
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from retrieve_campaign_reports_chain import retrieve_campaign_reports_chain
import dotenv

ANALYTICS_ORCHESTRATOR_PROMPT = """
You are an agent which takes action based on the analytics. 

Here are the tools to take action based on the analytics: 
{tool_descriptions}

All the tools have the shared memory and they know how to extract the information which they need from that shared memory.

Starting below, you should follow this format.
User Objective: An objective which the user wants to achieve through running an email campaign.
Analytics: Report summary about what happened on running an email campaign to achieve the user objective.
Thought: Based on the analytics, you take your decision on what action to take.
Action: the action to take, should be one of the tools [{tool_names}]
Action Input: The input to the action which is generally the objective which the user wants to achieve by re-running an email campaign with modified parameters.
Observation: Started a new campaign with changes to improve clicks or opens based on the action taken.
Thought: I am finished taking steps to improve the open rate or click rate.
Final Answer: Final answer after the action is executed.


Example 1:

User Objective: Drive 200 signups for my hackathon event.
Analytics: Deviation of opens from the industry is -48.95% and the deviation of clicks from the industry is 1.37%
Thought: Based on the analytics, deviation in opens is negative which implies the email campaign done better than industry stats where as the deviation in clicks is positive and greater than 1. So I should improve the clicks.
Action: improve_clicks
Action Input: Drive 200 signups for my hackathon event.
Observation: Started a new campaign with changes to improve clicks.
Thought: I am finished taking steps to improve the click rate.
Final Answer: Action is taken to improve clicks.

Example 2:
User Objective: Drive 200 signups for my hackathon event.
Analytics: Deviation of opens from the industry is 4.95% and the deviation of clicks from the industry is 1.37%
Thought: Based on the analytics, deviation in opens and clicks is positive, I should optimise for improving the opens before going for clicks. So I will improve the opens.
Action: improve_opens
Action Input: Drive 200 signups for my hackathon event.
Observation: Started a new campaign with changes to improve opens.
Thought: I am finished taking steps to improve the click rate.
Final Answer: Action is taken to improve opens.

...


Begin!

User objective: {input}
Report summary: {analytics}
{agent_scratchpad}"""

dotenv.load_dotenv()

llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
memory = dict()


def improve_opens(objective: str) -> str:
    return "Improve opens"


def _improve_opens_tool(llm: BaseLanguageModel) -> Tool:
    return Tool(
        name="improve_opens",
        description="Can be used to improve the open rate of campaign",
        func=improve_opens
    )


def improve_clicks(objective: str) -> str:
    return "Improve clicks"


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
