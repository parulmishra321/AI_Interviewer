# app.py
# Main Streamlit app for the AI Interviewer project.
# Generates interview questions and scores the user's answers.

import streamlit as st
from question_generator import generate_questions
from answer_evaluator import evaluate_answer

st.set_page_config(page_title="AI Interviewer", layout="wide")

st.title("AI Interviewer")
st.write("Paste a job description, answer the questions, and get evaluated using NLP.")

# INPUT — JOB DESCRIPTION
st.subheader("Paste Job Description")
job_desc = st.text_area(" ", height=150)

num_q = st.number_input("Number of questions to generate:", min_value=1, max_value=20, value=5, step=1)

# STORAGE
questions = []
user_answers = []
all_results = ""

# GENERATE QUESTIONS
if st.button("Generate Questions"):
    if job_desc.strip() == "":
        st.warning("Please enter a job description.")
    else:
        with st.spinner("Generating high-quality questions..."):
            questions = generate_questions(job_desc, num_q)
        st.success("Questions generated successfully!")

# DISPLAY QUESTIONS
if questions:
    st.subheader("Answer the following questions:")

    for i, q in enumerate(questions):
        st.write(f"### Q{i+1}: {q}")
        ans = st.text_area(f"Your answer to Q{i+1}", key=f"ans_{i}", height=120)
        user_answers.append(ans)


# EVALUATE + SAVE RESULTS
if questions and st.button("Evaluate My Answers"):
    all_results = ""
    scores = []  # store all question scores

    st.subheader("Your Scores:")

    for i, q in enumerate(questions):
        user_ans = user_answers[i]
        score = evaluate_answer(user_ans, q)
        scores.append(score)  # collect scores

        st.write(f"### Q{i+1} Score: {score}/10")

        # clean multiline answers
        safe_answer = user_ans.replace("\n", " / ")

        # build results
        all_results += f"Question {i+1}: {q}\n"
        all_results += f"Answer: {safe_answer}\n"
        all_results += f"Score: {score}/10\n"
        all_results += "-" * 50 + "\n\n"

    # OVERALL SCORE
    if scores:
        overall = sum(scores) / len(scores)
        st.subheader(f"🌟 Overall Interview Score: {overall:.2f} / 10")

    # save to file
    with open("interview_results.txt", "w", encoding="utf-8") as f:
        f.write(all_results)
        f.write(f"OVERALL SCORE: {overall:.2f}/10\n")

    st.success("Evaluation complete! Download your results below:")

    st.download_button(
        label="Download Interview Results",
        data=all_results,
        file_name="interview_results.txt",
        mime="text/plain"
    )

