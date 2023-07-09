# Academic Paper QA Automation

This is a Python script that uses the OpenAI GPT-4 API to generate question-answer pairs for academic papers. The answers are based on the content of the papers and the predefined set of questions.

## Features
- Processes all PDF files in a given directory and its subdirectories.
- Converts PDF files to plain text using `pdfminer.six`.
- Uses the OpenAI GPT-4 API to generate answers to a predefined set of questions based on the content of each paper.
- Saves the questions and answers for each paper in a JSON file.
- Generates a summary HTML file displaying all the questions and answers.

## Setup and Usage

1. Install the required Python packages with pip:

    ```
    pip install openai pdfminer.six glob2
    ```

2. Replace `'sk-xxx'` in `openai.api_key = 'sk-xxx'` with your actual OpenAI API key.

3. Modify the `questions` list to include the questions you want to ask about each paper.

4. Specify the input directory and output directory:

    ```python
    input_dir = "/path/to/your/pdf/files"
    output_dir = "/path/to/store/json/and/html"
    ```

5. Run the script:

    ```
    python paper_reader.py
    ```

## Notes

- The OpenAI GPT API is a paid service. Ensure you understand the cost before running the script on a large number of papers.
- The script does not perform error checking on the input files. Ensure that the input directory contains valid PDF files.
- The script assumes that the PDF files are text-based, not image-based. It may not be able to extract text from scanned documents or documents with other forms of images.

