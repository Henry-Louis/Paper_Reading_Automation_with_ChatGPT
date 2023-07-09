import os
import glob
import json
import openai
from datetime import datetime
from pdfminer.high_level import extract_text


def process_papers(file_path):
    # Converting PDF to text
    text = extract_text(file_path)

    return text

def ask_gpt3(paper_content, question):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # As per your requirements, use the model you want here
        messages=[
            {"role": "system", "content": "You are an academic researcher. You should answer question by reading the given academic paper."},
            {"role": "user", "content": paper_content},
            {"role": "assistant", "content": "Please input your question:"},
            {"role": "user", "content": question}
        ]
    )
    
    return response['choices'][0]['message']['content']

def generate_qa_json(file_path, list_of_questions):
    # Process papers
    paper_content = process_papers(file_path)
    if len(paper_content)>7500:
        paper_content = paper_content[:7500]

    # Container for Q&As
    qa_dict = {}

    # Ask questions
    for question in list_of_questions:
        answer = ask_gpt3(paper_content, question)
        qa_dict[question] = answer

    # Convert to JSON
    qa_json = json.dumps(qa_dict)

    return qa_json

def process_files_in_directory(input_dir, output_dir, list_of_questions):
    for input_file_path in glob.glob(input_dir + '/**/*.pdf', recursive=True):
        filename = os.path.basename(input_file_path)
        output_file_path = os.path.join(output_dir, filename.replace(".pdf", ".json"))

        if not os.path.exists(output_file_path):
            print(f"Processing file: {input_file_path}")
            qa_json = generate_qa_json(input_file_path, list_of_questions)

            with open(output_file_path, 'w') as output_file:
                output_file.write(qa_json)
            print(f"Saved answers to: {output_file_path}")
        else:
            print(f"Output file {output_file_path} already exists. Skipping.")
        print("")

def create_html_from_json_files(output_dir):
    html_content = "<html><body>"

    # Get list of all .json files in output directory, sorted by creation date
    json_files = sorted(glob.glob(os.path.join(output_dir, "*.json")), key=os.path.getctime, reverse=True)

    for file_path in json_files:
        with open(file_path, 'r') as json_file:
            # Load JSON data
            qa_data = json.load(json_file)

            # Extract filename without extension for the title
            title = os.path.basename(file_path).replace(".json", "")

            # Get file creation time and format it
            creation_time = datetime.fromtimestamp(os.path.getctime(file_path)).strftime("%Y-%m-%d %H:%M:%S")

            # Add to HTML content
            html_content += f"<h2>{title} - Created at: {creation_time}</h2><div style='margin-left: 10px; margin-right: 10px;'>"

            for question, answer in qa_data.items():
                html_content += f"<p><strong>Q: {question}</strong><br/>A: {answer}</p>"

            html_content += "</div><hr/>"

    html_content += "</body></html>"

    # Write HTML content to file
    with open(os.path.join(output_dir, "summary.html"), 'w') as html_file:
        html_file.write(html_content)

    print("HTML file created at:", os.path.join(output_dir, "summary.html"))
	
### Please Change the Setups below ###

# Set your API key
openai.api_key = 'Put-Your-OpenAI-API-Key-Here'

input_dir = "Put-Your-Input-Path-Here"
output_dir = "Put-Your-Output-Path-Here"
os.makedirs(output_dir, exist_ok=True)

# Change the list of Questions, if you need
questions = ["What is the research question? What is the main conclusion?", "What methodology was used? Which variables was used? Any alternative variables or data source?"]


# Run the program
# If you are using GPT-3.5-turbo, it only takes seconds for each paper
process_files_in_directory(input_dir, output_dir, questions)
create_html_from_json_files(output_dir)
