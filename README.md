# AI Academic Paper Generator

## Overview

The AI Academic Paper Generator is a Streamlit application that leverages the CrewAI framework to automatically generate academic papers for various subjects and grade levels. It allows users to select a subject, grade, and board (e.g., Federal, Punjab) and generates a paper based on the specified criteria. The generated paper can then be downloaded as a PDF.

## Features

*   **Subject Selection:** Supports multiple subjects including English, Urdu, Islamiat, Mathematics, Science, and Social Studies.
*   **Grade and Board Selection:** Allows users to specify the grade level and educational board for the paper.
*   **AI-Powered Generation:** Uses the CrewAI framework with specialized agents for paper design, question generation, and quality checking.
*   **Customizable Paper Structure:** Adheres to board-specific guidelines for paper structure, including MCQs, short questions, and long questions.
*   **PDF Download:** Generates a downloadable PDF of the generated paper.
*   **Urdu Support:** Supports generating papers in Urdu, including proper text alignment and font rendering.

## Technologies Used

*   **Streamlit:** For creating the user interface.
*   **CrewAI:** For orchestrating the AI agents and tasks.
*   **Gemini AI Models:** Uses `gemini/gemini-2.0-flash` for AI agents.
*   **Wikipedia API:** For fetching background information on topics.
*   **SymPy:** For solving mathematical expressions.
*   **ReportLab:** For generating PDF files.
*   **Python-Bidi and Arabic-Reshaper:** For handling Urdu text.
*   **dotenv:** For managing environment variables.

## Setup and Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd paper_generator
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python -m venv .venv
    .\.venv\Scripts\activate  # On Windows
    source .venv/bin/activate   # On macOS and Linux
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**

    *   Create a `.env` file in the project root.
    *   Add any necessary API keys or configuration settings to the `.env` file.  For example:

        ```
        OPENAI_API_KEY=your_openai_api_key
        ```

5.  **Run the Streamlit application:**

    ```bash
    streamlit run src/paper_generator/main.py
    ```

    Or, navigate to the `src/paper_generator` directory first:

    ```bash
    cd src/paper_generator
    streamlit run main.py
    ```

## Project Structure
