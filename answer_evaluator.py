# answer_evaluator.py
# Checks how similar candidate's answer is to the expected meaning using sentence embeddings.

from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def evaluate_answer(user_answer, question):
    if user_answer.strip() == "":
        return 1.0  # minimum score for empty answer

    emb_user = model.encode(user_answer, convert_to_tensor=True)
    emb_question = model.encode(question, convert_to_tensor=True)

    similarity = util.pytorch_cos_sim(emb_user, emb_question)
    score = float(similarity[0][0]) * 10

    # penalty for very short answers
    if len(user_answer.split()) < 4:
        score = 1.0

    return round(score, 2)
