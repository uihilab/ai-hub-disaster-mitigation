# AI-Hub-disaster-mitigation
Decision-Making Process for Water Resources Planning and Hazard Mitigation Using AI-Driven Agents

This repository contains the implementation of the Multi-Hazard Tournament (MHT) framework using AI-driven tools for decision-making in water resource planning and hazard mitigation. The project integrates AutoGen and DarkIdol-Llama models to simulate interactions among community stakeholders based on various demographic factors.

# Table of Contents

- Project Overview
- Features
- Installation
- Usage
- Code Structure
- Inputs and Outputs
- Acknowledgments

# Project Overview

The project explores how individual factors such as age, occupation, and personal values can influence budget allocation and the selection of mitigation strategies. By leveraging AI agents that represent diverse community members, the framework promotes a collaborative and adaptive approach to resource management, enhancing both the technical and social dimensions of decision-making.


The key objective is to optimize disaster mitigation strategies, ensuring maximum protection within a given budget while considering recreational enhancements for community benefit.

# Features

- PDF Text Extraction: Extracts and processes text from PDF documents to provide context for decision-making.
- AI-Driven Agents: Simulates discussions using AI agents powered by OpenAI's GPT models, configured through the autogen library and Dark-Idol LLM.
- Customizable Roles: Users can define roles with specific characteristics to simulate diverse perspectives.

# Installation

## Prerequisites
- Python 3.x

### Required Python Libraries:
- autogen
- fitz (PyMuPDF)
- openai
- pandas
- torch
- llama-cpp

### Steps

1. Clone this repository:

```
git clone https://github.com/uihilab/ai-hub-disaster-mitigation.git
cd flood-mitigation-tool
```

2. Install the required Python packages:
```   
pip install -r requirements.txt
```

# Usage

## Running the Tool
1. Prepare the necessary input files:
- PDF Files: Relevant documents containing flood mitigation strategies.
- CSV Files: Define the roles and their characteristics.
2. Configure the script with your OpenAI API key and any other necessary configurations.(Ignore this step for Dark Idol simulation)
3. Ensure the paths to your PDF files and CSV file are correctly specified in the script. The script will extract text from the PDFs, simulate a decision-making process using the roles defined in the CSV, and save the results to a CSV file.
4. Run the script:
```
python Disaster_mitigation(AutoGen).py    ## For AutoGen simulation
python Disaster_mitigation(DarkIdol).py    ## For Dark-Idol simulation

```
5. The outputs will be saved as a CSV file containing the options chosen by each role.

# Code Structure

- Disaster_mitigation(AutoGen).py and Disaster_mitigation(DarkIdol).py : Main script to run the decision-making process.
- requirements.txt: List of required Python libraries.
- README.md: Project documentation.
  
# Inputs and Outputs

## Inputs:
- PDF Documents: Containing flood mitigation strategies and adaptation options.
- CSV Files: Defining roles and their characteristics.
### Outputs:
CSV File: Detailing the options chosen, budget spent, and remaining budget for each role.

#### Visual Outputs:
1. Impact of Each Feature on Budget Spent and Options Chosen:
   ![image](https://github.com/user-attachments/assets/061de146-fae4-40f1-9af8-0876c7f36a3c)
- The charts illustrate how various features (e.g., Age, Occupation, Interests, etc.) influence the budget spent and the options chosen during the decision-making process.

2. Histogram of Selected Recreational Options Chosen:
   ![image](https://github.com/user-attachments/assets/552c5a0e-eff6-4fa7-9a48-9fd6d296f581)

- This histogram shows the frequency of Recreational Options Chosen in DarkIdol-Llama-3.1-8B model.

   ![image](https://github.com/user-attachments/assets/3a8bf403-6c10-48a6-b3ca-6c8f91e81fdb)


- This histogram shows the frequency of Recreational Options Chosen in AutoGen model.



# Acknowledgments

- Thank you to all the contributors who have helped shape this project.
- Special thanks to QuantFactory for providing access to the DarkIdol-Llama model.
- Thanks to OpenAI for the GPT models








