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


GAIN_CONTEXT_QUESTIONS_PROMPT = """Given the user objective and the instruction, here are all the necessary questions to gather more information for an email campaign, presented in a single array:

Example:
User objective: Drive 200 signups to my hackathon event.
Questions: ["What is the name of your hackathon event?", "What are the date and time of the event?", "Is it an online event or a physical event? If physical, where is the location?", "What's the theme or focus of the hackathon (e.g., AI, Blockchain, IoT, general coding, etc.)?", "How long is the hackathon (e.g., 24 hours, 48 hours, a week, etc.)?", "What benefits can participants expect from the event (e.g., prizes, networking opportunities, learning new skills, etc.)?", "Who are your target participants (e.g., students, professionals, coding enthusiasts, etc.)?", "What are the likely interests or motivations of these participants?", "Is there any specific skill level required to participate in the hackathon?", "How can participants sign up for the event? Is there a website or platform they should visit?", "What information do you require from the participants during the signup process?", "Is there a registration fee? If so, how much is it?", "Have you run similar email campaigns in the past? If so, what worked and what didn't?", "Are there any specific messages or offers that have resonated well with your target audience in the past?", "Do you have a preferred email marketing platform?", "Do you have any email templates or branding guidelines we should stick to?", "Do you have a specific timeline in mind for this email campaign?"]


User objective: {user_objective}",
Questions: 
"""

GAIN_CONTEXT_PROMPT = """
User Objective:
"{user_objective}"

Instruction:
"Given the following questions and corresponding answers, generate a context about the user objective for an email campaign."

Questions & Answers:
{questions_and_answers}
"""


LEADS_AGENT_PROMPT = """You are an lead gathering agent which gathers leads for an email campaign. We are running the email campaign to achieve a user objective.

Here are the tools to gather the leads: {tool_descriptions}

All the tools have the shared memory and they know how to extract the information which they need from that shared memory.

User is given a choice for gathering leads.
1. Upload Excel
2. Use an existing mailchimp list.

One of the above tools which represents the choice can get the results.

Starting below, you should follow this format:

User Objective: The objective user is trying to achieve.
User Choice: Choice between uploading an excel or an existing mailchimp list.
Thought: you should always think about what to do.
Action: the action to take, should be one of the tools [{tool_names}]
Action Input: the input to the action generally N/A or the objective
Observation: the result of the action
Final Answer: the final output from executing the plan


Example 1:
User Objective: Gather 200 signups for my hackathon event.
User choice: Upload Excel
Thought: User asked to go with uploading excel.
Action: upload_excel
Action Input: N/A
Observation: Uploaded excel to mailchimp and the list id is stored in the shared memory.
Thought: I am finished gathering the leads for the email campaign.
Final Answer: Gathered leads for this objective and saved them in the shared memory


Example 2:
User Objective: Gather 200 signups for my hackathon event.
User choice: Use an existing mailchimp list.
Thought: User asked to go with fetching an existing mailchimp list.
Action: fetch_from_mailchimp_lists
Action Input: Gather 200 signups for my hackathon event.
Observation: Retrieved the list suitable for the objective and stored it in the shared memory
Thought: I am finished gathering the leads for the email campaign.
Final Answer: Gathered leads for the objective and saved them in the shared memory.
...

Begin!

User objective: {user_objective}
User choice: {input}
{agent_scratchpad}"""

CHOOSE_FROM_LISTS_PROMPT = """
You are given a json of lists (id and name as the fields for each list). Your task to ask the user to choose from the options.

For example:

Instruction:
"Given the following Mailchimp lists in JSON format, generate a list of options for the user to choose from for their email campaign."

JSON:
[
{{"id": "11c96381fc", "name": "BLACK PROPELLER"}},
{{"id": "3605614fe5", "name": "Pixis"}},
{{"id": "6677798d7f", "name": "WEBINAR FINAL REGISTRANT"}}
]

Choose from the following lists for your email campaign:
1. "BLACK PROPELLER" (List ID: 11c96381fc)
2. "Pixis" (List ID: 3605614fe5)
3. "WEBINAR FINAL REGISTRANT" (List ID: 6677798d7f)

Please enter the number corresponding to the list you would like to use for your email campaign:

Begin!
Instruction:
"Given the following Mailchimp lists in JSON format, generate a list of options for the user to choose from for their email campaign."

JSON: {json}

Choose from the following lists for your email campaign:
"""

CHOOSE_FROM_LISTS_SELECTION_PROMPT = """Your task is to return the formatted result.

Example:

Choose from the following lists for your email campaign:
1. "YELLO STONE" (List ID: 11123b21fc)
2. "Automake it" (List ID: 2134b23a12)
3. "Hackathon list" (List ID: 6677798d7f)

User choice: 3

Answer: {{"list_id": "6677798d7f", "list_name": "Hackathon list" }}

{questions}

User choice: {user_choice}

Answer:
"""


SUBJECT_LINE_PROMPT = """
You are an email content creator. You would be given user objective and context. Your task is to generate email subject line suitable for running an email campaign to achieve the user objective.

Starting below, you should follow this format:

User objective: The objective which user is trying to achieve.
User Context: The context which user gave to build the email to achieve the objective.
Output: Subject line of the mail
...

Begin!
User objective: {user_objective}
User Context: {user_context}
Output:
"""

EMAIL_BODY_PROMPT = """
You are an email content creator. You would be given user objective and context. Your task is to generate email body suitable for running an email campaign to achieve the user objective.

Starting below, you should follow this format:

User objective: The objective which user is trying to achieve.
User Context: The context which user gave to build the email to achieve the objective.
User Details: The details of the person who is sending the mail which can be included in the body.
Output: Body of the mail which start with Dear *|FNAME|*
...

Begin!
User objective: {user_objective}
User Context: {user_context}
User Details: {user_details}
Output: Dear *|FNAME|*,

"""

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
