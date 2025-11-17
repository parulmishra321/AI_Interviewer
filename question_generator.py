# question_generator.py
# Generates simple interview questions based on job description text.

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import re
from collections import Counter

# Load FLAN-T5-small
tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-small")
model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-small")

# Clean a generated question
def clean_question(q: str) -> str:
    q = q.strip()
    q = q.replace("\n", " ").strip()

    # Remove unwanted tokens or bullet markers
    q = re.sub(r"^[\-\*\d\.\)]+", "", q).strip()

    # Ensure it ends with ?
    if not q.endswith("?"):
        q += "?"

    return q

# Keyword extraction (regex-based)
def extract_keywords(text, top_k=7):
    cleaned = re.sub(r"[^a-zA-Z0-9 ]", " ", text.lower())
    words = cleaned.split()

    stopwords = {
        "the", "is", "and", "a", "an", "to", "in", "for", "of", "on", "with",
        "as", "by", "this", "that", "from", "your", "you", "are", "we", "our",
        "will", "be", "have", "has", "using", "use", "used", "build", "develop",
        "design", "including"
    }

    filtered = [w for w in words if w not in stopwords and not w.isdigit()]

    if not filtered:
        return []

    return [kw for kw, _ in Counter(filtered).most_common(top_k)]

# Summarize long job descriptions
def summarize_text(text):
    prompt = "Summarize this job description in 5 short bullet points:\n" + text

    inputs = tokenizer(prompt, return_tensors="pt")

    output = model.generate(
        **inputs,
        max_length=180,
        temperature=0.7,
        top_p=0.9,
        do_sample=True
    )

    summary = tokenizer.decode(output[0], skip_special_tokens=True)
    return summary


# Generate interview questions
def generate_questions(job_desc: str, num_q=5):

    # 1. Summarize JD for small model’s understanding
    job_summary = summarize_text(job_desc)

    # 2. Extract keywords for relevance filtering & fallback
    extracted = extract_keywords(job_desc, top_k=7)

    # 3. Build the question-generation prompt
    prompt = f"""
    Generate {num_q} technical interview questions based on the job summary
    and the important keywords.

    Job Summary:
    {job_summary}

    Keywords:
    {", ".join(extracted)}

    The questions must be:
    - technical
    - specific to the job role
    - clear and complete
    - not generic
    - not asking about interests or willingness

    Write only questions. No explanation.
    """

    # 4. Generate raw model output
    inputs = tokenizer(prompt, return_tensors="pt")

    output = model.generate(
        **inputs,
        max_length=250,
        temperature=0.8,
        top_p=0.9,
        do_sample=True,
    )

    text = tokenizer.decode(output[0], skip_special_tokens=True)

    # 5. Extract individual lines
    raw_lines = text.split("\n")

    final_questions = []

    # 6. Filter + clean questions
    for line in raw_lines:
        q = line.strip()

        if len(q) < 10:
            continue

        # Remove instruction-echo questions
        lower_q = q.lower()

        if "ask" in lower_q and "question" in lower_q:
            continue
        if "professional" in lower_q and "job" in lower_q:
            continue
        if "write" in lower_q and "questions" in lower_q:
            continue
        if "instructions" in lower_q:
            continue
        if "requirements" in lower_q:
            continue
        if "generate" in lower_q and "question" in lower_q:
            continue
        if "based on" in lower_q:
            continue

        # Clean & validate
        q = clean_question(q)

        if len(q.split()) >= 4:
            final_questions.append(q)

        if len(final_questions) == num_q:
            break

    # Smart, keyword-based fallback (if model fails)
    if len(final_questions) < num_q:

        if extracted:
            fallback = [
                f"What experience do you have related to '{extracted[0]}'?",
                f"Can you describe a project involving {extracted[1] if len(extracted)>1 else extracted[0]}?",
                f"How would you solve a problem related to {extracted[2] if len(extracted)>2 else extracted[0]}?",
                f"What tools or methods have you used for {extracted[3] if len(extracted)>3 else extracted[0]}?",
                f"Why is {extracted[0]} important in your work?",
            ]
        else:
            fallback = [
                "What experience do you have related to this role?",
                "Can you explain a challenging project you worked on?",
                "How do you stay updated in your field?",
                "What tools or technologies are you most comfortable with?",
                "Describe how you approach solving complex problems.",
            ]

        needed = num_q - len(final_questions)
        final_questions += fallback[:needed]

    return final_questions[:num_q]
