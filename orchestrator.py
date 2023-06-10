import os

from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.tools import tool, Tool
from langchain.base_language import BaseLanguageModel
from langchain.prompts import PromptTemplate
from langchain.agents import AgentExecutor, ZeroShotAgent

ORCHESTRATOR_PROMPT = """You are an agent that assists with running email campaigns based on user objectives. Generally, the email campaigns follow the following process.
1. Gathering leads
2. Generating email content for the users - subject line and the body.
3. Create a campaign with the leads and the email content.
4. Start the campaign.

Here are the tools to plan and execute the email campaign: {tool_descriptions}

All the tools have the shared memory and they know how to extract the information which they need from that shared memory.


Starting below, you should follow this format:

User objective: the objective a User wants to achieve through running an email campaign.
Thought: you should always think about what to do
Action: the action to take, should be one of the tools [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I am finished executing a plan and have the information the user asked for or the data the user asked to create
Final Answer: the final output from executing the plan


Example:
User query: Get 100 signups to my hackathon event.
Thought: I should get the leads first
Action: leads_generator
Action Input: Get 100 signups to my hackathon event.
Observation: Gathered leads for this objective and saved them in the shared memory.
Thought: I should get the mail content for the objective.
Action: content_creator
Action Input: Get 100 signups to my hackathon event.
Observation: Generated the mail content for all the leads and saved them in the shared memory
Thought: I should create an email campaign in Mailchimp to send the mails.
Action: create_campaign
Action Input: Get 100 signups to my hackathon event.
Observation: Created an email campaign with the leads and the mail content.
Thought: I should start sending the mails by starting the mail campaign.
Action: start_campaign
Action Input: Get 100 signups to my hackathon event.
Observation: Started the email campaing for this objective.
...

Begin!

User objective: {input}
Thought: I should understand about the objective first.
{agent_scratchpad}"""

os.environ["OPENAI_API_KEY"] = "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"
os.environ["SERPAPI_API_KEY"] = "5e80ac42927317d4a30a71581ec1234f7104563fa118017d89fd8b1a55cc3646"

llm = OpenAI(temperature=0)  # type: ignore
memory = dict()


def gain_context(objective: str):
    memory["objective"] = objective
    return "Gained context."


def _gain_context_tool(llm: BaseLanguageModel) -> Tool:
    tool = Tool(
        name="gain_context",
        description="Can be used to ask questions about the objective to gain more context to do a better job.",
        func=gain_context
    )
    return tool


def gather_leads(objective: str):
    return "Gathered leads for this objective and saved them in the shared memory"


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
    return "Generated the mail content for all the leads and saved them in the shared memory"


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
    return "Created an email campaign with the leads and the mail content."


def _create_campaign_tool(llm: BaseLanguageModel) -> Tool:
    tool = Tool(
        name="create_campaign",
        description="Can be used to create an email campaign in mailchimp with the leads and the mail content",
        func=create_campaign
    )
    return tool


def start_campaign(plan_str: str):
    return "Started the email campaign for this objective"


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
memory = {}
objective = input("> What is your objective? \n")
memory['objective'] = objective
agentExecutor.run(objective)
