# AI Interviewer 

## Overview
This project was built as part of my assignment.
It is a simple AI-based interviewer that:

- generates interview questions from a job description
- lets the user type answers
- evaluates the answers using NLP similarity
- saves everything in a results file

I kept the code modular and easy to understand.

## Features I Added
- Question generator using FLAN-T5 (google/flan-t5-small).
- Answer evaluation using SentenceTransformer (MiniLM).
- Automatic penalty for very short answers.
- Clean formatting for multi-line user answers.
- Saves all questions, answers and scores into 'interview_results.txt'.
- Download button in Streamlit for exporting results.
- Loading spinner while generating questions.
- Basic filtering + cleaning to avoid irrelevant or low-quality questions.

## Tech Used
- Python
- Streamlit
- HuggingFace Transformers
- SentenceTransformers
- PyTorch
- Cosine similarity
- Text preprocessing techniques

## How the System Works
1. The user pastes a job description. 
2. FLAN-T5 generates relevant interview questions. 
3. The user submits answers in the Streamlit UI. 
4. SentenceTransformer compares the meaning of the answer and question.
5. A score between 0–10 is shown.
6. All results are saved into a text file.
7. The user can download the final interview report.

## Project Structure
```
app.py                 -> Streamlit interface + evaluation logic
question_generator.py  -> FLAN-T5 based question generation
answer_evaluator.py    -> Evaluates answers using embeddings
requirements.txt       -> Required dependencies
interview_results.txt  -> Auto-generated output file
README.md              -> Documentation
```

## Architecture Diagram


                       ┌───────────────────────────┐
                       │        User Input         │
                       │(Job Description + Answers)│
                       └─────────────┬─────────────┘
                                     │
                                     ▼
                       ┌──────────────────────────┐
                       │          app.py          │
                       │    (Streamlit Frontend)  │
                       └─────────────┬────────────┘
                                     │
      ┌──────────────────────────────┼───────────────────────────────┐
      │                              │                               │
      ▼                              ▼                               ▼
┌───────────────────┐       ┌─────────────────────┐        ┌────────────────────┐
│ question_generator│       │   answer_evaluator  │        │  interview_results │
│ (FLAN-T5 Model)   │       │  (MiniLM Embedding) │        │  (Saved Q/A Score) │
└─────────┬─────────┘       └───────────┬─────────┘        └────────────────────┘
          │                             │
          ▼                             ▼
 ┌───────────────────┐        ┌─────────────────────┐
 │     Generated     │        │ Score + Evaluation  │
 │     Questions     │        │    (0–10 Scale)     │
 └─────────┬─────────┘        └───────────┬─────────┘
           │                              │
           └───────────────┬──────────────┘
                           │                           
                           ▼
               ┌──────────────────────────┐
               │    Streamlit Interface   │
               │    (Display + Download)  │
               └──────────────────────────┘


## How to Run the Project

### Step 1: Create a virtual environment
```
python -m venv .venv
```

### Activate it:
Windows:
```
.venv\Scripts\activate
```

Mac/Linux:
```
source .venv/bin/activate
```

### Step 2: Install dependencies
```
pip install -r requirements.txt
```

### Step 3: Run the app
```
streamlit run app.py
```

## Sample Output (interview_results.txt)

```
Question 1: How would you apply your skills mentioned in this job description?
Answer: I have used these skills in various projects and I can explain them in detail.
Score: 7.8/10
--------------------------------------------------

Question 2: What experience do you have that relates to this role?
Answer: I have worked on similar tasks and have hands-on experience in the mentioned technologies.
Score: 8.1/10
--------------------------------------------------
```

## What I Learned
- How to use a small instruction-tuned model (FLAN-T5) for question generation
- How embeddings work for semantic similarity
- How to process and clean model outputs
- How to build a simple UI using Streamlit
- How to save and export formatted results

## Future Improvements
- Deploy the application online.
- Add resume-based question generation.  
- Add multiple interview rounds (easy → medium → hard).
- Add technical, communication, and problem-solving score categories.
- Use a larger instruction-tuned model for higher quality questions.

## Conclusion
This project demonstrates how AI models can be combined with a simple interface to create a functional interview simulation tool.
The main goal was to build a working system in a short time, and the essential objectives were successfully achieved.

## Contributing
Pull requests and suggestions are welcome.
For any major changes, please open an issue first to discuss what you want to modify.


## Contact
**Name:** Parul Mishra
**Email:** parulmishra321@gmail.com
