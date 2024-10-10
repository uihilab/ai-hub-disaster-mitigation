import fitz  # PyMuPDF for PDF handling
import pandas as pd
from llama_cpp import Llama
import torch
import json

# Initialize device as GPU (cuda) if available, otherwise fall back to CPU
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")

# Initialize the Llama model with increased context length and send it to the appropriate device
llm = Llama.from_pretrained(
    repo_id="QuantFactory/DarkIdol-Llama-3.1-8B-Instruct-1.2-Uncensored-GGUF",
    filename="DarkIdol-Llama-3.1-8B-Instruct-1.2-Uncensored.Q8_0.gguf",
    n_ctx=35000, n_gpu_layers=33, n_threads=6,  # Increased context length
    device_map="auto"  # Automatically chooses GPU if available
)

# Define a reminder message
discussion_reminder = ("Just give me the adaptation options chosen and strategies, budget used, "
                       "and budget remaining in the response together. This make selections according to your traits "
                       "and think accordingly. Make a reasonable strategy (if you are taking recreational add-ons "
                       "specify the options you have chosen)")

def extract_text_from_one_pdf(pdf_paths):
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
pdf_text = extract_text_from_one_pdf(pdf_paths)
reso_text = extract_text_from_one_pdf(reso_path)

# Recreation options as a formatted string
rec_options = json.dumps([
    {"Zone Name": "Shelter—Small", "Cost": "$25,000", "RecreationIndex": 1},
    # Add other options as needed
], indent=4)

# Prepare the initial message with a clear structure
initial_message = f"""
**Topic of Discussion:** Decision-Making Process for Flood Mitigation

**Objective:** Optimize mitigation strategies to protect water resources, habitats, and communities. 
Use the budget to get maximum benefits and also try to save.

**Location and Issue:** Find it in the Resources
**Total Budget:** $15,000,000
**Remaining Budget:** To be calculated based on the discussion and decisions.
**Adaptation Options Considered:** To be considered from the Resources.
**Reference Material:** (just use this for reference)
{pdf_text}
**Resources:** (Take options from here)
{reso_text}
**Note:** {discussion_reminder} so the structure is:

Adaption options:(Just the options along with cost and justification)
Budget Spent:(Give me the breakdown of calculation, calculate correctly do not give me wrong answers)
Budget Remaining:(Give me the breakdown of calculation, calculate correctly do not give me wrong answers)
strictly consider the options from below:
{reso_text}
After each category of datapoint add a semicolon so that its easier to extrapolate and parse the data 
"""

# Load roles from CSV file, limiting to the specified number of rows
roles_df = pd.read_csv('path_to_roles_csv.csv', nrows=20)  # Adjust the number of rows as needed

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

    # Repeatedly generate responses until no avoid_keywords are present
    while True:
        # Use the Llama model for chat completion with increased token limit
        chat_response = llm.create_chat_completion(
            messages=[
                {"role": "system", "content": role_system_message},
                {"role": "user", "content": initial_message},
            ]
        )

        # Collect the last message from the role
        role_last_message = chat_response["choices"][0]["message"]["content"]

        # Check if the response contains any avoid_keywords
        keywords_found = ["Alternative Approach"]  # Check for actual keywords to avoid
        if not any(keyword in role_last_message for keyword in keywords_found):
            break  # If no avoid_keywords are found, break out of the loop

        # Provide an alternative prompt to refine the response if keywords are found
        chat_response = llm.create_chat_completion(
            messages=[
                {"role": "system", "content": role_system_message},
                {"role": "user", "content": "Please reassess the adaptation options and strategies."},
            ]
        )

        # Update the role_last_message with the new response
        role_last_message = chat_response["choices"][0]["message"]["content"]

    # Append the final valid response
    responses.append({
        "Role": role_name,
        "Options Chosen": json.dumps({"Options Chosen": role_last_message})
    })

# Convert the responses to a DataFrame and save as CSV
options_df = pd.DataFrame(responses)
options_df.to_csv('Outputs(NEW).csv', index=False)

print("Responses and options chosen have been saved.")
