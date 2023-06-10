from langchain.base_language import BaseLanguageModel
from langchain.agents import AgentExecutor, ZeroShotAgent
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.tools import Tool

leads_prompt = """
How would you want to setup leads for the mails?
1. Upload an excel?
2. Use an existing mailchimp list?
Type the choice. 1 or 2.
"""


def ask_human(objective: str) -> str:
    # Input to take the choice here.
    response = input(leads_prompt)
    return response


def _ask_human_tool(
        llm: BaseLanguageModel
) -> Tool:
    tool = Tool(
        name="ask_human",
        description="Can be used to ask a human to choose between the tools which are being built.",
        func=ask_human
    )
    return tool


def fetch_mailchimp_lists(objective: str) -> str:
    return "Retrieved the list suitable for the objective and stored it in the shared memory"


def _fetch_mailchimp_list_tool(
        llm: BaseLanguageModel
) -> Tool:
    tool = Tool(
        name="fetch_mailchimp_lists",
        description="Can be used to fetch a list of leads in Mailchimp",
        func=fetch_mailchimp_lists
    )
    return tool


def upload_excel(objective: str):
    return "Uploaded excel to mailchimp and the list id is stored in the shared memory."


def _upload_excel_tool(
        llm: BaseLanguageModel
) -> Tool:
    tool = Tool(
        name="upload_excel",
        description="Can be used to take an excel from the user and check if it works out.",
        func=upload_excel
    )
    return tool


def create_leads_agent(llm: BaseLanguageModel) -> AgentExecutor:
    tools = [
        _ask_human_tool(llm=llm),
        _fetch_mailchimp_list_tool(llm=llm),
        _upload_excel_tool(llm=llm)
    ]
    prompt = PromptTemplate(
        template="Hello leads",
        input_variables=["input", "agent_scratchpad"],
        partial_variables={
            "tool_names":  ", ".join([tool.name for tool in tools]),
            "tool_descriptions": "\n".join(
                [f"{tool.name}: {tool.description}" for tool in tools]
            ),
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


def gather_leads_chain(llm: BaseLanguageModel, user_objective: str, memory: dict) -> str:
    agent_executor = create_leads_agent(llm=llm)
    agent_executor.run()
    return "Gathered leads for this objective and saved them in the shared memory"
