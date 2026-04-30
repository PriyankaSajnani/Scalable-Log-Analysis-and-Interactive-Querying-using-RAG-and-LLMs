import csv #read cleaned logs
import json #format logs for AI prompts
import random # sample logs
import subprocess #call Ollama LLM
from tkinter import Tk, filedialog #Opens file selection dialog
from sklearn.feature_extraction.text import TfidfVectorizer #Converts text → numbers,Based on word importance,Classical NLP (pre-deep learning)
from sklearn.metrics.pairwise import cosine_similarity  # Measures how similar two texts are, Used for retrieval, This is where RAG-style retrieval starts
import numpy as np

# ---------------- reference corpus ----------------

corpus_logs = [ # this is A static log knowledge base,Acts like a mini log encyclopedia,Used for retrieval,Helps AI ground its answers,this replaces a vector database (FAISS, Pinecone, etc.)
    "The Windows Update service entered the stopped state.",
    "Audit Failure: An account failed to log on. Subject: Security ID: NULL SID, Logon Type: 3.",
    "The system has rebooted without cleanly shutting down first.",
    "The Application Host Helper Service service terminated unexpectedly.",
    "The driver \\Driver\\WudfRd failed to load for the device.",
    "Windows Defender Antivirus Service terminated unexpectedly.",
    "Process winlogon.exe attempted to access a token without permission.",
    "Event 4625: An account failed to log on.",
    "The server did not register with DCOM within the required timeout.",
    "The system detected a possible attempt to compromise security.",
    "Unexpected shutdown due to power failure.",
    "Windows failed to start due to a recent change.",
    "Group Policy Client service failed the logon.",
    "svchost.exe generated an application error.",
    "Volume Shadow Copy Service error.",
    "Software Protection service has stopped.",
    "Kerberos client received a KRB_AP_ERR_MODIFIED error.",
    "Time difference between client and server prevented logon.",
    "The computer rebooted from a bugcheck.",
    "DNS Client detected network configuration changes."
]

vectorizer = TfidfVectorizer()
corpus_vectors = vectorizer.fit_transform(corpus_logs)
# Each log sentence is tokenized , Important words get higher weight , Text → numeric vectors

def get_top_chunks(query, top_n=3): #Purpose: Given a user query, retrieve the most relevant logs
    
    try:
        query_vec = vectorizer.transform([query]) #Converts user question → TF-IDF vector
        sim_scores = cosine_similarity(query_vec, corpus_vectors).flatten() # Measures similarity between: Query , stored logs
        top_indices = np.argsort(sim_scores)[-top_n:][::-1] #Finds top matching log entries , THIS IS RETRIEVAL , THIS IS RAG (without fancy name)
        return [corpus_logs[i] for i in top_indices]
    except Exception as e:
        print(f"[!] Chunking Error: {e}")
        return []

# ---------------- select CSV ----------------

Tk().withdraw()
file_path = filedialog.askopenfilename(
    title="Select Log CSV File",
    filetypes=[("CSV Files", "*.csv")]
)

if not file_path:
    print("No file selected. Exiting.")
    exit()

# ---------------- load & sample logs ----------------

logs_by_severity = {"Warning": [], "Error": [], "Critical": []}

with open(file_path, newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        level = row.get("Level")
        message = row.get("Message")
        if level in logs_by_severity and message:
            logs_by_severity[level].append(
                {"Level": level, "Message": message}
            )

sampled_logs = {
    level: random.sample(logs, min(2, len(logs)))
    for level, logs in logs_by_severity.items()
}

print("\n===== SELECTED LOG ENTRIES =====\n")
for level, logs in sampled_logs.items():
    print(f"\n--- {level.upper()} LOGS ---")
    for i, log in enumerate(logs, 1):
        print(f"{i}. {log['Message']}")

# ---------------- Ollama summarization  (THIS IS AI) ----------------

def summarize_logs(level, logs):
    prompt = f"""
You are a system log analyst.

Analyze the following '{level}' logs and provide:
1. Detailed Analysis
2. Future Steps
3. Recommendations
4. Preventive Measures

Logs:
{json.dumps(logs, indent=2)}

Even if logs are minor, still respond.
"""
    try:
        result = subprocess.run(
            ["ollama", "run", "llama3.2"], # This is where: Natural language understanding happens, Calls local LLM.
            input=prompt,
            text=True,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=60
        )
        return (
            result.stdout.strip()
            or result.stderr.strip()
            or "(No summary generated)"
        )
    except subprocess.TimeoutExpired:
        return "(Model timed out during summary generation)"

# ---------------- print summaries ----------------

print("\n===== SUMMARY REPORTS =====\n")

for level, logs in sampled_logs.items():
    print(f"\n{level.upper()} SUMMARY:\n")
    if logs:
        print(summarize_logs(level, logs))
    else:
        print("(No logs available)")

# ---------------- interactive chat ----------------

def chat_about_logs(combined_logs):
    system_context = f"""
You are an AI assistant analyzing Windows system logs.

Recent logs:
{json.dumps(combined_logs, indent=2)}

Use them as context when answering.
"""

    print("\n===== INTERACTIVE LOG CHAT =====")
    print("Type /bye to exit\n")

    while True:
        user_q = input("You: ")
        if user_q.strip().lower() in {"/bye", "exit", "quit"}:
            print("Assistant: Bye! Ending chat.")
            break

        prompt = system_context + "\nUser question:\n" + user_q

        try:
            result = subprocess.run(
                ["ollama", "run", "llama3.2"],
                input=prompt,
                text=True,
                capture_output=True,
                encoding="utf-8",
                errors="replace",
                timeout=60
            )
            answer = result.stdout.strip() or result.stderr.strip()
        except subprocess.TimeoutExpired:
            answer = "(Model timed out while responding)"

        if answer:
            print("\nAssistant:\n" + answer + "\n")
        else:
            print("\nAssistant: (No response generated)\n")

# ---------------- start chat ----------------

combined_logs = [log for logs in sampled_logs.values() for log in logs]

if combined_logs:
    input("\nPress Enter to start interactive log chat...\n")
    chat_about_logs(combined_logs)
else:
    print("\nNo logs available for interactive chat.")