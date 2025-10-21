# AI Coding Agent

A terminal-based AI agent powered by Google's Gemini 2.0 Flash that can autonomously interact with your filesystem, read/write code, execute Python files, and perform multi-step tasks like debugging and code modifications.

## Overview

This project demonstrates an AI agent with multi-step reasoning and tool-calling capabilities. It can understand natural language requests, create execution plans, and interact with your codebase through a set of predefined tools. The included `calculator` directory serves as a demo project for the agent to analyze, modify, and debug.

## Features

- **Multi-Step Reasoning**: The agent can break down complex tasks into multiple function calls
- **File System Operations**: List directories, read file contents, and write/modify files
- **Code Execution**: Run Python files with optional command-line arguments
- **Security**: Path validation ensures the agent only operates within the designated working directory
- **Verbose Mode**: Optional detailed logging of agent actions and token usage
- **Autonomous Debugging**: The agent can read code, identify issues, make fixes, and verify solutions

## Available Tools

1. **`get_files_info`**: List files and directories to understand project structure
2. **`get_file_content`**: Read file contents (truncates to 10,000 characters for large files)
3. **`write_file`**: Create or overwrite files with new content
4. **`run_python_file`**: Execute Python scripts with optional arguments

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Aryannnthakurrr/AIagent.git
cd AIagent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
# or with uv
uv pip install -r requirements.txt
```

3. Set up your Gemini API key:
```bash
# Create a .env file in the project root
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey).

## Usage

Basic usage:
```bash
python3 main.py "your request here"
```

With verbose output (shows function calls and token usage):
```bash
python3 main.py "your request here" --verbose
```

### Example Commands

```bash
# Ask the agent to analyze the calculator project
python3 main.py "what files are in the calculator directory?"

# Request a bug fix
python3 main.py "fix any bugs in calculator/tests.py"

# Run tests
python3 main.py "run the calculator tests and tell me if they pass"

# Create new code
python3 main.py "create a new function in calculator that adds two numbers"
```

## Project Structure

```
AIagent/
├── main.py                 # Main agent entry point
├── config.py              # Configuration settings
├── .env                   # API keys (not tracked)
├── calculator/            # Demo project for agent to interact with
│   ├── main.py
│   ├── tests.py
│   ├── pkg/
│   │   ├── calculator.py
│   │   └── render.py
│   └── lorem.txt
├── functions/             # Agent tool implementations
│   ├── call_function.py   # Function call dispatcher
│   ├── get_file_content.py
│   ├── get_files_info.py
│   ├── run_python_file.py
│   └── write_file.py
└── tests.py              # Unit tests for agent functions
```

## How It Works

1. **User Input**: You provide a natural language request via command line
2. **Planning**: The agent analyzes the request and determines which tools to use
3. **Execution**: The agent makes function calls to interact with the filesystem
4. **Iteration**: The agent can make up to 20 sequential tool calls to complete complex tasks
5. **Response**: The agent provides a final summary of actions taken

The agent follows a system prompt that encourages:
- Reading files before executing them
- Getting directory structure before reading specific files
- Verifying fixes by running tests after modifications
- Adding clear comments when modifying code

## Security

- All file operations are restricted to the `./calculator` working directory
- Path validation prevents directory traversal attacks (`../`, absolute paths)
- Symlinks are resolved to prevent escaping the working directory
- The agent cannot access files outside the designated workspace

## Configuration

Edit `config.py` to modify:
- `MAX_CHARS`: Maximum characters to read from a file (default: 10,000)

## Development

### Running Tests

```bash
# Run all tests
python3 -m unittest tests -v

# Run specific test class
python3 -m unittest tests.TestGetFileContent -v
```

### Adding New Tools

1. Create a new function declaration schema in `functions/`
2. Implement the function logic
3. Add the schema to `available_functions` in `main.py`
4. Update `call_function.py` to handle the new function

## Future Enhancements

- Multi-turn conversations with context memory
- Support for multiple working directories
- Integration with version control systems
- Support for additional programming languages
- Web interface for easier interaction

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License

Copyright (c) 2025 Aryan Thakur

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Acknowledgments

- Powered by [Google Gemini 2.0 Flash](https://deepmind.google/technologies/gemini/)
- Built with the [Google GenAI Python SDK](https://github.com/google/generative-ai-python)

---

**Note**: This is a demonstration project. Be cautious when giving an AI agent write access to your filesystem. Always review generated code before execution in production environments.