import os
import wikipediaapi  # ✅ Wikipedia alternative
import sympy  # ✅ Math solver
from crewai import Crew, Agent, Task
from dotenv import load_dotenv
import streamlit as st
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from bidi.algorithm import get_display  
import arabic_reshaper  

# Load environment variables
load_dotenv()

# ✅ Verify Font File
urdu_font_path = r"F:\crewai\edu_proj\paper_generator\fonts\NotoNastaliqUrdu-Regular.ttf"


# ✅ Check if the font file exists before using it
# if not os.path.exists(urdu_font_path):
#     raise FileNotFoundError(f"❌ Font file missing: {urdu_font_path}")

# ✅ Register the Urdu Font
pdfmetrics.registerFont(TTFont("UrduFont", urdu_font_path))

# ✅ Wikipedia Fetch Function
def get_wikipedia_summary(topic):
    wiki_wiki = wikipediaapi.Wikipedia("en")
    page = wiki_wiki.page(topic)
    return page.summary if page.exists() else "No Wikipedia data available."

# ✅ Math Problem Solver
def solve_math_expression(expression):
    try:
        return sympy.sympify(expression).evalf()
    except Exception as e:
        return f"Error solving math: {e}"

# Streamlit UI Setup
st.title("📄 AI Academic Paper Generator")

subject = st.selectbox("Select Subject", ["English_A", "English_B", "Urdu_A", "Urdu_B", "Islamiat", "Mathematics", "Science", "Social Studies","Biology","Chemistry","Physics"])
grade = st.selectbox("Select Class", ["5", "6", "7", "8", "9", "10", "11", "12"])
board = st.selectbox("Select Board", ["Federal", "Punjab", "Sindh", "KPK", "Balochistan"])

BOARD_PATTERNS = {
    "Federal": {"MCQs": 20, "Short Qs": 30, "Long Qs": 50, "Syllabus": "Federal Board Syllabus"},
    "Punjab": {"MCQs": 25, "Short Qs": 25, "Long Qs": 50, "Syllabus": "Punjab Board Syllabus"},
}

paper_pattern = BOARD_PATTERNS.get(board, {"MCQs": 20, "Short Qs": 30, "Long Qs": 50, "Syllabus": "Default Syllabus"})

question_type = "curriculum-based questions" if subject in ["English_A", "Urdu_A"] else "general academic questions"

# Define Agents
paper_designer = Agent(
    name="Paper Designer",
    role=f"Structuring {subject} academic papers for Grade {grade} - {board} Board",
    goal=f"Ensure the {subject} paper follows the {board} board guidelines for Class {grade}, adhering to the {paper_pattern['Syllabus']}.",
    backstory="An AI assistant skilled in designing structured academic papers.",
    model="gemini/gemini-2.0-flash",
)

question_generator = Agent(
    name="Question Generator",
    role=f"Creating diverse questions for {subject} academic paper",
    goal=f"Generate various types of {subject} questions for Class {grade}, ensuring alignment with the {paper_pattern['Syllabus']}.",
    backstory="An AI expert in crafting academic questions.",
    model="gemini/gemini-2.0-flash",
)

quality_checker = Agent(
    name="Quality Checker",
    role=f"Ensuring high-quality and relevant {subject} questions",
    goal="Review and refine questions for clarity, accuracy, and adherence to the current syllabus.",
    backstory="An AI specialized in verifying academic content quality.",
    model="gemini/gemini-2.0-flash",
)

# Define Tasks
structure_task = Task(
    name="Design Paper Structure",
    agent=paper_designer,
    description=f"Create an academic paper structure for {subject}, Class {grade}, {board} Board, following the {paper_pattern['Syllabus']}.",
    expected_output=f"A structured {subject} exam paper template."
)

question_task = Task(
    name="Generate Questions",
    agent=question_generator,
    description=f"Generate long-questions, short-questions, MCQs, fill-in-the-blanks, and true/false questions for {subject}, adhering to the {paper_pattern['Syllabus']}.",
    expected_output=f"A set of well-formatted {subject} academic questions."
)

review_task = Task(
    name="Review and Refine Questions",
    agent=quality_checker,
    description="Review the generated questions and improve clarity, correctness, and ensure they align with the current syllabus.",
    expected_output="A set of well-formatted and syllabus-aligned academic questions."
)

paper_generator_crew = Crew(name="Academic Paper Generator", agents=[paper_designer, question_generator, quality_checker], tasks=[structure_task, question_task, review_task])

def generate_paper():
    st.write(f"Generating {subject} paper for Class {grade} ({board} Board)... Please wait.")
    
    if subject == "Islamiat":
        question_task.description = f"Generate Islamiat questions **in Urdu** for Class {grade}, following the syllabus."
    
    result = paper_generator_crew.kickoff()
    output_text = getattr(result, "raw_output", str(result))
    
    st.success("Paper generated successfully!")
    return output_text

def generate_pdf(subject, grade, board, text):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)

    # ✅ Fix Urdu text rendering
    if subject in ["Urdu_A", "Urdu_B", "Islamiat"]:
        pdf.setFont("UrduFont", 14)
        text = get_display(arabic_reshaper.reshape(text))  # 🔥 Fix Urdu text
    else:
        pdf.setFont("Helvetica", 12)

    # ✅ Draw Text in PDF
    y = 750  # Start position
    for line in text.split("\n"):
        if subject in ["Urdu_A", "Urdu_B", "Islamiat"]:
            pdf.drawRightString(550, y, line)  # 🔥 Align Right for Urdu
        else:
            pdf.drawString(50, y, line)  # Align left for English

        y -= 25  # Move down for next line
        if y < 50:  # New page if near bottom
            pdf.showPage()
            pdf.setFont("UrduFont" if subject in ["Urdu_A", "Urdu_B", "Islamiat"] else "Helvetica", 12)
            y = 750

    pdf.save()
    buffer.seek(0)
    return buffer


# Streamlit Button for PDF Download
if st.button("Generate Paper"):
    output = generate_paper()
    st.subheader(f"Generated {subject} Paper:")
    st.text_area("Paper Content", output, height=300)

    # ✅ Generate and provide a downloadable PDF
    pdf_buffer = generate_pdf(subject, grade, board, output)
    st.download_button(
        label="📥 Download Paper as PDF",
        data=pdf_buffer,
        file_name=f"{subject}_Paper_Class_{grade}_{board}.pdf",
        mime="application/pdf"
    )
