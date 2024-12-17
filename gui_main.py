import tkinter as tk
from tkinter import messagebox, scrolledtext, Toplevel
import os
import subprocess
import requests
import json

LOG_FILE_PATH = "sys_call_log.txt"

# List of common system calls
SYSTEM_CALLS = ["mkdir", "rm", "cp", "cat", "pwd", "touch", "echo"]

# Hardcoded Gemini API Key
GEMINI_API_KEY = #ENTER YOUR API HERE.

# Function to simulate generating the log
def generate_log():
    target_program = target_program_entry.get().strip()

    if not target_program:
        messagebox.showerror("Error", "Please enter a target program name.")
        return

    try:
        result = subprocess.run(
            ["./system_call_tracer", target_program], 
            capture_output=True, text=True
        )

        if result.returncode == 0:
            with open(LOG_FILE_PATH, "w") as log_file:
                log_file.write(result.stdout)  

            terminal_output.insert(
                tk.END, f"[INFO] System call tracing completed for '{target_program}'. Log saved to {LOG_FILE_PATH}\n"
            )
            terminal_output.see(tk.END)
        else:
            messagebox.showerror("Error", f"Error running the program: {result.stderr}")

    except Exception as e:
        terminal_output.insert(tk.END, f"[ERROR] Failed to generate log: {e}\n")
        terminal_output.see(tk.END)

# Function to simulate sending the log to Gemini and getting a response
def generate_report():
    try:
        # Check if the log file exists
        if not os.path.exists(LOG_FILE_PATH):
            raise FileNotFoundError(f"Log file not found: {LOG_FILE_PATH}")

        # Read the log file
        with open(LOG_FILE_PATH, "r") as log_file:
            log_data = log_file.read()

        # Prepare request data for Gemini API
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": f"""Please analyze the following system call trace from the text file and provide a detailed report. The report should be clear, simple, and well-structured. 
                        Instead of using any bold text or headlines, give a short, plain English summary of what happened during the system call trace. 
                        Explain the behavior in an easy-to-understand way, focusing on key activities and their potential impact. 
                        Make sure the summary flows logically and is easy for someone unfamiliar with system calls to follow.:\n\n{log_data}"""}
                    ]
                }
            ]
        }

        api_key = "#ENTER YOUR API HERE"

        if not api_key:
            messagebox.showerror("Error", "Gemini API key is missing.")
            return

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"
        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(url, headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            response_data = response.json()
            print(f"Raw API response: {response_data}")

            candidates = response_data.get('candidates', [])
            if candidates:
                generated_report = candidates[0]['content']['parts'][0]['text']
                # Insert the report into the terminal_output ScrolledText widget
                terminal_output.insert(tk.END, f"[INFO] Sending log to Gemini...\n")
                terminal_output.insert(tk.END, f"[LLM RESPONSE] {generated_report}\n")
                terminal_output.see(tk.END)

                # Save the generated report to 'llm_report.txt'
                with open("llm_report.txt", "w") as report_file:
                    report_file.write(generated_report)

                terminal_output.insert(tk.END, "[INFO] Report saved to llm_report.txt\n")
                terminal_output.see(tk.END)

            else:
                terminal_output.insert(tk.END, "[ERROR] No response content received from Gemini.\n")
                terminal_output.see(tk.END)
        else:
            messagebox.showerror("Error", f"Failed to generate report: {response.text}")

    except FileNotFoundError as e:
        terminal_output.insert(tk.END, f"[ERROR] {e}\n")
        terminal_output.see(tk.END)
    except Exception as e:
        terminal_output.insert(tk.END, f"[ERROR] Failed to generate report: {e}\n")
        terminal_output.see(tk.END)

def show_syscall_list():
    def copy_to_clipboard(syscall):
        root.clipboard_clear()
        root.clipboard_append(syscall)
        root.update()  # Keeps the clipboard data after the program ends
        messagebox.showinfo("Copied", f"'{syscall}' copied to clipboard!")

    popup = Toplevel(root)
    popup.title("System Call List")
    popup.geometry("400x250")
    popup.config(bg="black")

    label = tk.Label(
        popup,
        text="Common System Calls",
        font=("Courier New", 12, "bold"),
        bg="black",
        fg="white",
    )
    label.pack(pady=5)

    # Frame for system call list
    list_frame = tk.Frame(popup, bg="black")
    list_frame.pack(fill="both", expand=True, padx=10, pady=10)

    for syscall in SYSTEM_CALLS:
        frame = tk.Frame(list_frame, bg="black")
        frame.pack(fill="x", pady=2)

        syscall_label = tk.Label(
            frame,
            text=syscall,
            font=("Courier New", 11),
            bg="black",
            fg="white",
            anchor="w",
        )
        syscall_label.pack(side="left", fill="x", expand=True)

        copy_button = tk.Button(
            frame,
            text="Copy",
            font=("Courier New", 10),
            bg="gray",
            fg="white",
            activebackground="white",
            activeforeground="black",
            command=lambda s=syscall: copy_to_clipboard(s),
        )
        copy_button.pack(side="right", padx=5)

# Function to show the About (Info) window with wrapped text
def show_info():
    popup = Toplevel(root)
    popup.title("About SysCallWatch")
    popup.geometry("400x300")
    popup.config(bg="black")

    label = tk.Label(
        popup,
        text="SysCallWatch: A Tool for System Call Monitoring",
        font=("Courier New", 12, "bold"),
        bg="black",
        fg="white",
        justify="center",
    )
    label.pack(pady=10)

    description = tk.Label(
        popup,
        text="SysCallWatch is created as semester project for the CS331 - Operating System course at GIK Instutute, taught by Ms. Nazia Shahzadi. Project Stack is Python, Gemini LLM (API) and C Language. \n\nThis tool allows users to monitor and track system calls. It provides functionality to log system calls, generate reports, and copy commonly used system calls.\n\nFor more details and to contribute, visit the GitHub repository below.",
        font=("Courier New", 10),
        bg="black",
        fg="white",
        justify="left",
        wraplength=350, 
    )
    description.pack(pady=10, padx=10)

    github_link = tk.Label(
        popup,
        text="GitHub: https://github.com/0xnomy",
        font=("Courier New", 10, "underline"),
        bg="black",
        fg="blue",
        cursor="hand2",
        justify="center",
    )
    github_link.pack(pady=10)

    github_link.bind("<Button-1>", lambda e: os.system("start https://github.com/nauman-alimurad/SysCallWatch"))

root = tk.Tk()
root.title("SysCallWatch Terminal")
root.geometry("900x600")
root.resizable(True, True)  # Allow resizing both horizontally and vertically
root.config(bg="black")

terminal_font = ("Courier New", 12)

# Header
header = tk.Label(
    root,
    text="SysCallWatch: System Call Monitoring Tool",
    font=("Courier New", 14, "bold"),
    bg="black",
    fg="white",
)
header.pack(pady=10, fill="x")

target_program_label = tk.Label(
    root, text="Enter Target Program:", font=terminal_font, bg="black", fg="white"
)
target_program_label.pack(pady=5)

target_program_entry = tk.Entry(root, font=terminal_font, bg="black", fg="white", width=50, insertbackground="white")
target_program_entry.pack(pady=5)

# Button for generating log
generate_log_button = tk.Button(
    root,
    text="Generate Log",
    font=terminal_font,
    bg="gray",
    fg="white",
    activebackground="white",
    activeforeground="black",
    command=generate_log,
)
generate_log_button.pack(pady=10)

# Button for generating report
generate_report_button = tk.Button(
    root,
    text="Generate Report",
    font=terminal_font,
    bg="gray",
    fg="white",
    activebackground="white",
    activeforeground="black",
    command=generate_report,
)
generate_report_button.pack(pady=10)

# Button for system call list
syscall_list_button = tk.Button(
    root,
    text="System Call List",
    font=terminal_font,
    bg="gray",
    fg="white",
    activebackground="white",
    activeforeground="black",
    command=show_syscall_list,
)
syscall_list_button.pack(pady=5)

info_button = tk.Button(
    root,
    text="About",
    font=terminal_font,
    bg="gray",
    fg="white",
    activebackground="white",
    activeforeground="black",
    command=show_info,
)
info_button.pack(pady=5)

terminal_output = scrolledtext.ScrolledText(
    root,
    font=terminal_font,
    bg="black",
    fg="green",  
    wrap=tk.WORD,
    height=15,
    width=100,
)
terminal_output.pack(pady=10)

root.mainloop()
