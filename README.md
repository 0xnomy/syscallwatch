# SysCallWatch

SysCallWatch is a Python-based tool designed for monitoring and tracing system calls in Linux systems. The application allows users to generate logs of system calls executed by a target program, analyze the traces, and generate easy-to-understand reports using the Gemini API.

Made as a semester project for OS course taught by Nazia Shahzadi & Mah Rukh

## Features

- **System Call Monitoring**: Track system calls executed by a given program.
- **Log Generation**: Save detailed logs of system call executions.
- **Report Generation**: Automatically send logs to Gemini API for analysis and generate detailed reports.
- **System Call List**: View and copy a list of common system calls for reference.
- **Graphical User Interface (GUI)**: Interactive Tkinter-based GUI to make the tool user-friendly.
- **Log File**: Save logs to a file and easily access them for analysis.
- **About Section**: Information about the project and its creator.

## Requirements

- Python 3.x
- Tkinter
- Requests library (for Gemini API integration)
- C compiler (for the `system_call_tracer` program)
- Gemini API Key (for report generation)

## Installation

1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/0xnomy/SysCallWatch.git
   ```
   
2. Install the necessary Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

3. Compile the `system_call_tracer.c` program using a C compiler:
   ```bash
   gcc system_call_tracer.c -o system_call_tracer
   ```

4. Make sure you have a valid Gemini API key and replace the hardcoded one in the `generate_report()` function.

## Usage

1. Launch the application:
   ```bash
   python main.py
   ```

2. **Generate Log**: Enter the name of the target program and click "Generate Log" to start tracing system calls.

3. **Generate Report**: Once the log is generated, click "Generate Report" to analyze the log using the Gemini API and get a detailed summary.

4. **System Call List**: Click "System Call List" to view a list of commonly used system calls, and easily copy any of them to your clipboard.

5. **About**: Click the "About" button to view details about the project, including its creator and the repository link.

## Sample System Calls

The tool tracks a variety of system calls including:

- `mkdir`: Create a directory
- `rm`: Remove a file
- `cp`: Copy a file
- `cat`: Display file content
- `pwd`: Print working directory
- `touch`: Create an empty file
- `echo`: Display text

## Code Structure

### `main.py`
The main Python script that runs the Tkinter GUI. It handles:
- User input for target program names
- Generating logs by tracing system calls
- Sending logs to the Gemini API for report generation
- Displaying logs and reports in a user-friendly manner

### `system_call_tracer.c`
A C program that uses `ptrace()` to trace system calls executed by a target program. It logs the system calls to a file for analysis.

### `Gemini API Integration`
The tool uses Gemini’s API to generate human-readable reports based on the system call logs. The API request is sent with the log content, and the response is displayed to the user.

## Contributing

1. Fork this repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Gemini API for text generation.
- Tkinter for building the GUI.
- GIK Institute and Ms. Nazia Shahzadi for project inspiration and guidance.

## Contact

For any questions or contributions, feel free to reach out through the GitHub issues section or email the repository owner.
