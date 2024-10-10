import autogen
import fitz  # PyMuPDF for PDF handling
import openai as OpenAI
import time
import pandas as pd

# Configuration
use_docker = False

llm_config = {
    "config_list": [
        {"model": "gpt-4o-mini", "api_key": "-----------------"}  # Replace with your actual API key
    ],
    "seed": 32,
    "temperature": 1,
    "max_tokens": 2048,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
    "response_format": {"type": "json_object"}
}

discussion_reminder = ("Just give me the adaptation options chosen and strategies, "
                       "budget used, and budget remaining as the columns in the response together")

def extract_text_from_pdfs(pdf_paths):
    """Extract text from a list of PDF files."""
    all_text = ""
    for pdf_path in pdf_paths:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        all_text += text
    return all_text

# Define the paths to the PDFs
pdf_paths = ['path_to_pdf_1.pdf']  # Replace with your actual PDF path
reso_path = ['path_to_resource_pdf.pdf']  # Replace with your actual PDF path

# Extract text from PDFs
pdf_text = extract_text_from_pdfs(pdf_paths)
reso_text = extract_text_from_pdfs(reso_path)

# Prepare the initial message with a clear structure
initial_message = f"""
**Topic of Discussion:** Decision-Making Process for Flood Mitigation

Optimize mitigation strategies to protect water resources, habitats, and communities. 
Prioritize achieving maximum benefits within the budget, while identifying opportunities 
for cost savings where feasible.

**Location and Issue:** Find it in the Resources
**Total Budget:** $15,000,000
**Remaining Budget:** To be calculated based on the discussion and decisions.
**Adaptation Options Considered:** To be considered from the Resources.
**Reference Material:** (just use this for reference)
{pdf_text}
**Resources:** (Take options from here)
{reso_text}
**Note:** {discussion_reminder}
"""

# Load roles from CSV
roles_df = pd.read_csv('path_to_roles_csv.csv')  # Replace with your actual CSV path

# Collect responses for each role
responses = []

for index, row in roles_df.iterrows():
    role_name = row['Role']
    role_system_message = f"""
    You should behave taking the below traits:
    Age: {row['Age']}
    Gender: {row['Gender']}
    Occupation: {row['Occupation']}
    Personality Traits: {row['Personality Traits']}
    Communication Style: {row['Communication Style']}
    Interests and Hobbies: {row['Interests and Hobbies']}
    Educational Background: {row['Educational Background']}
    Cultural Background: {row['Cultural Background']}
    Language Proficiency: {row['Language Proficiency']}
    Technology Savviness: {row['Technology Savviness']}
    Preferred Communication Medium: {row['Preferred Communication Medium']}
    Lifestyle: {row['Lifestyle']}
    Values and Beliefs: {row['Values and Beliefs']}
    Relationship Status: {row['Relationship Status']}
    Economic Status: {row['Economic Status']}
    Health and Wellness: {row['Health and Wellness']}
    Time Availability: {row['Time Availability']}
    Problem-solving Approach: {row['Problem-solving Approach']}
    """

    # Define the role agent
    role_agent = autogen.AssistantAgent(
        name=role_name,
        system_message=role_system_message,
        llm_config=llm_config,
    )

    # Initialize GroupChat for the role
    groupchat = autogen.GroupChat(agents=[user_proxy, role_agent], messages=[], max_round=2)

    # Initialize GroupChatManager for the role
    manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

    # Initiate chat and run
    chat_result = user_proxy.initiate_chat(manager, message=initial_message)
    
    # Collect the last message from the role
    role_last_message = role_agent.last_message()

    # Collect the entire conversation
    role_responses = role_agent.chat_messages

    if role_last_message:
        responses.append({
            "Role": role_name,
            "Options Chosen": role_last_message["content"]
        })

# Save responses to CSV
options_df = pd.DataFrame(responses)
options_df.to_csv('output_responses.csv', index=False)

print("Responses and options chosen have been saved to 'output_responses.csv'")
