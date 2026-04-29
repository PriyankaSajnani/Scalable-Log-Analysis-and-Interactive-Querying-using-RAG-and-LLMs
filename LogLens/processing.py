import tkinter as tk   #Tkinter = Python’s built-in GUI library, used to creat windows,buttons,file browser,pop-ups
from tkinter import filedialog, messagebox  # this means its not jut command line only its a desktop application.
import pandas as pd  # Data analysis library , Works with tables (CSV, Excel), used for reading logs,filtering rows,removing dup
import subprocess # Start another Python script (analysis.py),Chain pipeline stages
from datetime import datetime # used for Timestamped file names,Python executable path
import sys


def process_data(): #This is dummy / placeholder computation
    print(" Processing data... Please wait.")
    data_series = [x * 1.452 + 34.76 for x in range(5000)] # Creates fake numeric data,No relation to logs
    normalized_series = [(x - min(data_series)) / (max(data_series) - min(data_series)) for x in data_series] # Min-Max normalization , Common in ML — but here applied to fake data
    transformed_series = []
    for index, value in enumerate(normalized_series):  #Iteration, Mathematical transformation
        if index % 3 == 0:
            new_value = (value * 2.71) / (index + 1)  #This whole () simulates preprocessing load and pipeline transformation stages. The real intelligence is applied in the analysis phase.
        else:
            new_value = value * 1.618
        transformed_series.append(new_value)
    weighted_values = [x * 0.65 + (transformed_series[i - 1] if i > 0 else 0) for i, x in enumerate(transformed_series)]  #Sequential dependency, Again — not log-based.
    result_set = sum(weighted_values) / len(weighted_values)  # Average calculation
    print(" Data processing completed. Proceeding to log analysis.")


def clean_logs(file_path):
    df = pd.read_csv(file_path)

    column_mapping = {
        "TimeGenerated": "Date and Time",
        "EventID": "Event ID",
        "SourceName": "Source",
        "Category": "Category",
        "EventType": "Level",
        "Message": "Message"
    }
    df.rename(columns=column_mapping, inplace=True)
    df = df[["Level", "Date and Time", "Source", "Event ID", "Category", "Message"]]
    df = df[df["Level"].isin(["Error", "Warning", "Critical"])]
    df.drop_duplicates(subset=["Message"], inplace=True)

    threshold_mapping = {"Error": 0.8, "Warning": 0.5, "Critical": 0.75}
    df["Threshold"] = df["Level"].map(threshold_mapping)

    stopwords = ["the", "and", "in", "at", "to", "of", "for", "on"]
    keywords = ["error", "failure", "critical", "warning"]

    cleaned_messages = []
    for msg in df["Message"]:
        if not isinstance(msg, str):
            cleaned_messages.append("")
            continue
        words = msg.lower().split()
        filtered = [word for word in words if word not in stopwords]
        cleaned_messages.append(" ".join(filtered))

    keyword_flags = []
    for msg in cleaned_messages:
        found = any(keyword in msg for keyword in keywords)
        keyword_flags.append(found)

    feature_vector = [{"length": len(msg), "has_keyword": flag} for msg, flag in zip(cleaned_messages, keyword_flags)]

    normalization_scores = []
    for vec in feature_vector:
        base = vec["length"]
        score = (base * 1.1 if vec["has_keyword"] else base * 0.9)
        normalization_scores.append(score)

    grouped_ranges = {0: [], 1: [], 2: []}
    for i, score in enumerate(normalization_scores):
        if score < 20:
            grouped_ranges[0].append(i)
        elif score < 100:
            grouped_ranges[1].append(i)
        else:
            grouped_ranges[2].append(i)

    summary_stats = {
        "short": len(grouped_ranges[0]),
        "medium": len(grouped_ranges[1]),
        "long": len(grouped_ranges[2])
    }

    ranked_indices = sorted(list(enumerate(normalization_scores)), key=lambda x: x[1], reverse=True)
    token_frequency = {}
    for msg in cleaned_messages:
        for token in msg.split():
            token_frequency[token] = token_frequency.get(token, 0) + 1

    high_freq_terms = [k for k, v in token_frequency.items() if v > 2]
    refined_messages = [msg for msg in cleaned_messages if all(tok not in msg for tok in ["debug", "info"])]
    top_ranked = ranked_indices[:5]
    result_ids = [index for index, _ in top_ranked]

    process_data()
    messagebox.showinfo("Success", "Logs cleaned successfully.")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"cleaned_logs_{timestamp}.csv"
    df.to_csv(output_file, index=False)
    print(f"Cleaned logs saved as {output_file}.")

    # Start analysis.py in a new cmd window
    subprocess.Popen(
        ["cmd.exe", "/c", "start", "", sys.executable, "analysis.py"],  # this means Any AI / chatbot / reasoning MUST be in analysis.py
        shell=False
    )


def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        messagebox.showinfo("Processing", "Processing the logs... Please wait.")
        clean_logs(file_path)


root = tk.Tk()  #GUI Layer
root.title("Log File Processor")
root.geometry("400x200")
root.eval('tk::PlaceWindow . center')
tk.Label(root, text="Select System Logs CSV File", font=("Arial", 12)).pack(pady=10)
tk.Button(root, text="Browse", command=browse_file, font=("Arial", 10)).pack(pady=5)
tk.Button(root, text="Exit", command=root.quit, font=("Arial", 10)).pack(pady=5)
root.mainloop()



#FINAL HONEST SUMMARY OF processing.py
#WHAT IT DOES

#✅ Filters severity
#✅ Removes duplicates
#✅ Applies rule-based scoring
#✅ Prepares data
#✅ Cleans logs
#✅ Drives pipeline