import re
import google.generativeai as genai
from dotenv import load_dotenv
import os
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
def generate_quiz_with_gemini(key_points_text, num_mcq=5, num_tf=3):
    print("\n[3/4] Generating quiz using Google Gemini API...")
    load_dotenv()
 
    api_key = os.getenv("GEMINI_API_KEY")
   
    if not api_key:
        print("Error: GEMINI_API_KEY not found. Make sure it is set in your .env file.")
        return None
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=api_key)
    except Exception as e:
        print(f"Error configuring Gemini API: {e}")
        return None
 
    prompt = f"""
    You are an expert quiz creator. Your task is to generate a quiz based on the key points provided below. You must follow all formatting rules precisely.
 
    **Formatting Rules:**
    1.  Create a section for Multiple Choice Questions.
    2.  Generate exactly {num_mcq} multiple-choice questions with four options each (A. ,B. , C. , D. ).
    3.  The final line for each multiple-choice question must be in the format "ANSWER: [LETTER]". For example: "ANSWER: C".
    4.  After the multiple-choice questions, you MUST include a separator line exactly like this: "--- TRUE/FALSE ---".
    5.  After the separator, generate exactly {num_tf} True/False questions.
    6.  The final line for each True/False question must be in the format "ANSWER: True" or "ANSWER: False".
    7.  For the both MCQ and True/False questions do not inlcude any numbering before the questions
    8.  Do not add any other text, introductions, or conclusions.
   
    **KEY POINTS TO USE FOR THE QUIZ:**
    ---
    {key_points_text}
    ---
    """
    try:
        model = genai.GenerativeModel('gemini-2.0-flash-lite')
        response = model.generate_content(prompt)
        quiz_text = response.text.strip()
        print("-> Successfully received quiz from Gemini.")
        print(f'HERE! {quiz_text}')
        return quiz_text
 
    except Exception as e:
        print(f"An error occurred while calling the Gemini API: {e}")
        return None
 
def parse_quiz_text(quiz_text):
    mcq_data = []
    tf_data = []
 
    if not isinstance(quiz_text, str) or not quiz_text.strip():
        print("Warning: Received empty or invalid text from the API.")
        return mcq_data, tf_data
 
    quiz_text = quiz_text.replace('\r\n', '\n').strip()
    quiz_text = re.sub(r'^.*Multiple Choice Questions:?\s*', '', quiz_text, flags=re.IGNORECASE)
    splits = re.split(r'---\s*TRUE/FALSE\s*---', quiz_text, flags=re.IGNORECASE)
    mcq_text = splits[0].strip()
    tf_text = splits[1].strip() if len(splits) > 1 else ""
    mcq_blocks = []
    current_block = []
    if mcq_text:
        for line in mcq_text.split('\n'):
            stripped_line = line.strip()
            if not stripped_line:
                continue
            if not re.match(r'^[A-D]\.', stripped_line) and not stripped_line.upper().startswith('ANSWER:'):
                if current_block:
                    mcq_blocks.append('\n'.join(current_block))
                current_block = [stripped_line]
            else:
                current_block.append(stripped_line)
 
        if current_block:
            mcq_blocks.append('\n'.join(current_block))
 
    for block in mcq_blocks:
        lines = [l.strip() for l in block.split('\n') if l.strip()]
 
        if len(lines) < 4:
            continue
 
        question = lines[0]
        answer_line = lines[-1]
       
        options = [re.sub(r'^[A-D]\.\s*', '', opt) for opt in lines[1:-1] if re.match(r'^[A-D]\.', opt)]
 
        if not options or not answer_line.upper().startswith("ANSWER:"):
            continue
 
        try:
            answer_match = re.search(r'ANSWER:\s*([A-D])', answer_line, flags=re.IGNORECASE)
            if not answer_match:
                continue
           
            answer_letter = answer_match.group(1).upper()
            answer_index = ord(answer_letter) - ord('A')
 
            if 0 <= answer_index < len(options):
                answer_text = options[answer_index]
                mcq_data.append({
                    "type": "Multiple Choice",
                    "question": question,
                    "options": options,
                    "answer": answer_text
                })
        except (IndexError, TypeError):
            continue
 
    if tf_text:
        tf_lines = [l.strip() for l in tf_text.split('\n') if l.strip()]
        i = 0
        while i < len(tf_lines) - 1:
            question_line = tf_lines[i]
            answer_line = tf_lines[i+1]
            if answer_line.upper().startswith("ANSWER:"):
                answer = None
                if "TRUE" in answer_line.upper():
                    answer = "True"
                elif "FALSE" in answer_line.upper():
                    answer = "False"              
                if answer:
                    tf_data.append({
                        "type": "True/False",
                        "question": question_line,
                        "answer": answer
                    })
                i += 2
            else:
                i += 1
    print(f"-> Parsed {len(mcq_data)} MCQs and {len(tf_data)} True/False questions.")
    return mcq_data, tf_data