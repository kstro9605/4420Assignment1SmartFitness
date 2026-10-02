from pathlib import Path

def write_analysis_to_file(output_dir, analysis):
    file_path = Path(f"{output_dir}/analysis_summary.csv")
    file_path.parent.mkdir(parents=True, exist_ok=True)

    if not file_path.is_file():
        with open(file_path, "w", encoding="utf-8") as file:
            file.write("session_id,participant_id,duration,average_heart_rate,max_heart_rate,min_heart_rate,average_skin_response,average_temperature,session_classification\n")
            file.write(generate_analysis_line(analysis))
    else:
        with open(file_path, "a", encoding="utf-8") as file:
            file.write(generate_analysis_line(analysis))

def generate_analysis_line(analysis):
    analysis_line = analysis["session_number"]
    analysis_line += f",{analysis["participant_id"]}"
    analysis_line += f",{analysis["duration"]}"
    analysis_line += f",{analysis["average_heart_rate"]}"
    analysis_line += f",{analysis["max_heart_rate"]}"
    analysis_line += f",{analysis["min_heart_rate"]}"
    analysis_line += f",{analysis["average_skin_response"]}"
    analysis_line += f",{analysis["average_temperature"]}"
    analysis_line += f",{analysis["session_type"]}\n"
    return analysis_line

def print_analysis_results(output_dir, participant, analysis_results):
    file_path = Path(f"{output_dir}/analysis_report.txt")
    file_path.parent.mkdir(parents=True, exist_ok=True)

    lines = ["XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        "SMART FITNESS — ANALYSIS REPORT",
        "-----------------------------------------------",
        f"Participant: {participant.participant_id}\n",
        "Baseline measurements",
        "-----------------------------------------------",
        f"Heart rate:     {participant.baseline_heart_rate} bpm",
        f"Skin response:  {participant.baseline_skin_response}",
        f"Temperature:    {participant.baseline_temperature} °C\n",
        "Session results",
        "-----------------------------------------------",
    ]

    for session in analysis_results:
        lines.extend([
            "",
            f"Session {session['session_number']} — {session['session_type']}",
            "-----------------------------------------------",
            f"Valid sensor readings: {session['valid_observations']} "
            f"out of {session['duration']} expected",
            f"Average heart rate:   {session['average_heart_rate']:.2f} bpm",
            f"Average skin response:{session['average_skin_response']:.2f}",
            f"Average temperature:  {session['average_temperature']:.2f} °C",
            f"Maximum heart rate:   {session['max_heart_rate']} bpm",
            f"Minimum heart rate:   {session['min_heart_rate']} bpm\n",
            "Summary:",
            f"  {session['session_summary']}",
            "-----------------------------------------------",
            "-----------------------------------------------",
            "-----------------------------------------------",
        ])
    summary_string = "\n".join(lines) + "\n\n"

    with open(file_path, "a", encoding="utf-8") as file:
        file.write(summary_string)

def invalid_sessions_file_explanation(output_dir, sessions_file, invalidSessions):
    file_path = Path(f"{output_dir}/rejected_records.txt")
    file_path.parent.mkdir(parents=True, exist_ok=True)

    lines = ["-----------------------------------------------",
        "-----------------------------------------------",
        "-----------------------------------------------",
        "SMART FITNESS — INVALID SESSIONS EXPLANATION FOR FILE: " + sessions_file,
        "-----------------------------------------------",
    ]

    for row_number, explanation in invalidSessions.items():
        lines.extend([
            "",
            f"Row {row_number}: {explanation}",
            "-----------------------------------------------",
        ])
    explanation_string = "\n".join(lines) + "\n\n"

    with open(file_path, "a", encoding="utf-8") as file:
        file.write(explanation_string)

def invalid_users_file_explanation(output_dir, profiles_file, invalidUsers):
    file_path = Path(f"{output_dir}/rejected_users.txt")
    file_path.parent.mkdir(parents=True, exist_ok=True)

    lines = ["-----------------------------------------------",
        "-----------------------------------------------",
        "-----------------------------------------------",
        "SMART FITNESS — INVALID USERS EXPLANATION FOR FILE: " + profiles_file,
        "-----------------------------------------------",
    ]

    for row_number, explanation in invalidUsers.items():
        lines.extend([
            "",
            f"Row {row_number}: {explanation}",
            "-----------------------------------------------",
        ])
    explanation_string = "\n".join(lines) + "\n\n"

    with open(file_path, "a", encoding="utf-8") as file:
        file.write(explanation_string)