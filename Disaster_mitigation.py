import autogen
import fitz  # PyMuPDF for PDF handling
import openai as OpenAI
import time
import pandas as pd

# Configuration
use_docker = False

llm_config = {
    "config_list": [
        {
            "model": "gpt-4o-mini",
            "api_key": "YOUR_API_KEY_HERE",  # Replace with your actual API key
        }
    ],
    "seed": 32
}

discussion_reminder = "Just give me the adaptation options chosen and strategies, budget used, and budget remaining as the columns in the response together in JSON format"

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

# Paths to the PDFs
pdf_paths = ['path/to/your/pdf1.pdf']  # Replace with your actual PDF paths
reso_path = ['path/to/your/pdf2.pdf']  # Replace with your actual PDF paths

rec_options = """
[
    {"Zone Name": "Shelter—Small", "Cost": "$25,000", "RecreationIndex": 1},
    {"Zone Name": "Basketball—Small", "Cost": "$15,000", "RecreationIndex": 1},
    {"Zone Name": "Football", "Cost": "$100,000", "RecreationIndex": 2},
    {"Zone Name": "Open Area—Small", "Cost": "$7,500", "RecreationIndex": 2},
    {"Zone Name": "Shelter—Medium", "Cost": "$45,000", "RecreationIndex": 2},
    {"Zone Name": "Soccer—Small", "Cost": "$40,000", "RecreationIndex": 2},
    {"Zone Name": "Volleyball—Small", "Cost": "$50,000", "RecreationIndex": 2},
    {"Zone Name": "Exercise Area—Small", "Cost": "$20,000", "RecreationIndex": 3},
    {"Zone Name": "Picnic Area", "Cost": "$4,000", "RecreationIndex": 3},
    {"Zone Name": "Playground—Large", "Cost": "$500,000", "RecreationIndex": 3},
    {"Zone Name": "Shelter—Large", "Cost": "$100,000", "RecreationIndex": 3},
    {"Zone Name": "Soccer—Large", "Cost": "$115,000", "RecreationIndex": 3},
    {"Zone Name": "Track", "Cost": "$400,000", "RecreationIndex": 3},
    {"Zone Name": "Trail—Small", "Cost": "$10,000", "RecreationIndex": 3},
    {"Zone Name": "Amphitheater", "Cost": "$50,000", "RecreationIndex": 4},
    {"Zone Name": "Open Area—Large", "Cost": "$90,000", "RecreationIndex": 4},
    {"Zone Name": "Playground—Small", "Cost": "$100,000", "RecreationIndex": 4},
    {"Zone Name": "Soccer—Medium", "Cost": "$75,000", "RecreationIndex": 4},
    {"Zone Name": "Softball/Baseball—Small", "Cost": "$200,000", "RecreationIndex": 4},
    {"Zone Name": "Trail—Medium", "Cost": "$30,000", "RecreationIndex": 4},
    {"Zone Name": "Trail—Large", "Cost": "$150,000", "RecreationIndex": 5}
]
"""

# Extract text from PDFs
pdf_text = extract_text_from_pdfs(pdf_paths)
reso_text = extract_text_from_pdfs(reso_path)

# Prepare the initial message with a clear structure
initial_message = f"""
**Topic of Discussion:** Decision-Making Process for Flood Mitigation

**Objective:** Optimize mitigation strategies to protect water resources, habitats, and communities at Damage Center (DC - San Antonio 02). Use the budget to get maximum benefits and also try to save.

**Location and Issue:** Find it in the Resources

**Total Budget:** $15,000,000

**Remaining Budget:** To be calculated based on the discussion and decisions.

**Adaptation Options Considered:** To be considered from the Resources.

**Reference Material:** (just use this for reference)
{pdf_text}

**Resources:** (Take options from here)
{reso_text}

**Note:** {discussion_reminder} so the structure is:

Adaptation options: (Just the options along with cost and justification)

Budget Spent: (Give me the breakdown of calculation, calculate correctly do not give me wrong answers)

Budget Remaining: (Give me the breakdown of calculation, calculate correctly do not give me wrong answers)

Consider the options from this:

{reso_text} 

And also consider recreational add-ons from this:

{rec_options}
"""

# Define the user_proxy agent
user_proxy = autogen.AssistantAgent(
    name="user_proxy",
    system_message="Represents the user in the conversation.",
    llm_config=llm_config,
)

# Load roles from CSV file
roles_df = pd.read_csv('path/to/your/roles.csv')  # Replace with your actual CSV path

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
    groupchat = autogen.GroupChat(
        agents=[user_proxy, role_agent],
        messages=[],
        max_round=2
    )

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
options_df.to_csv('path/to/your/output.csv', index=False)  # Replace with your actual output path

print("Responses and options chosen have been saved to 'output.csv'")
