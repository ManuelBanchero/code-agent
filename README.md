# Code Agent

An AI-powered coding agent built in Python that uses Google Gemini to autonomously read, write, and execute code within a sandboxed working directory.

Built as part of the [boot.dev](https://boot.dev) curriculum, and refactored to apply Object-Oriented Programming principles including abstraction, inheritance, and separation of concerns.

---

## Features

- List files and directories within a working directory
- Read file contents with a character limit for safety
- Write or overwrite files
- Execute Python scripts with optional arguments
- Autonomous multi-step reasoning — the agent calls tools iteratively until it reaches a final answer

---

## Project Structure

```
src/
├── main.py                  # Entry point
├── build_agent.py           # Factory function that wires up the Agent
├── config/
│   └── config.py            # Environment variables and global constants
├── utils/
│   └── prompts.py           # System prompt for the AI model
└── model/
    ├── Agent.py             # Orchestrates the conversation loop
    ├── AIModel.py           # Wraps the Gemini API, handles all AI-specific formatting
    └── Tool/
        ├── Tool.py          # Abstract base class for all tools
        ├── Schema.py        # Provider-agnostic schema definition
        ├── GetFilesInfo.py
        ├── GetFileContent.py
        ├── WriteFile.py
        └── RunPythonFile.py
```

---

## Design

The project is structured around three main responsibilities:

**`Agent`** — Manages the conversation loop and tool dispatch. It has no knowledge of the Gemini API internals. It receives plain results and delegates formatting to `AIModel`.

**`AIModel`** — The only class that imports from `google.genai`. Responsible for translating the agent's generic data structures into Gemini-specific types (`types.Content`, `types.FunctionDeclaration`, etc.) and back.

**`Tool` (abstract base class)** — Defines the contract for all tools: a `get_schema()` method that returns a provider-agnostic dict, and an `execute()` method with the tool's logic. Each subclass implements only its own behavior.

This separation means swapping Gemini for another provider (e.g. OpenAI) would only require changes to `AIModel` — nothing else.

---

## Requirements

- Python 3.10+
- A [Google Gemini API key](https://aistudio.google.com/app/apikey)

---

## Setup

1. Clone the repository:

```bash
git clone <repo-url>
cd code-agent
```

2. Create a virtual environment and install dependencies:

```bash
uv sync
```

Or with pip:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory:

```
GEMINI_API_KEY=your_api_key_here
```

4. Set your working directory in `src/config/config.py`:

```python
WORKING_DIRECTORY = '/absolute/path/to/your/project'
```

---

## Usage

Run the agent from the `src/` directory:

```bash
cd src
python main.py "your prompt here"
```

### Examples

```bash
python main.py "List all the files in the project"
python main.py "Read the main.py file and explain what it does"
python main.py "Fix the bug in calculate.py and run the tests"
```

---

## Configuration

| Constant | Description | Default |
|---|---|---|
| `MAX_CHARS` | Max characters read per file | `10,000` |
| `MAX_MODEL_CALLS` | Max iterations before the agent stops | `20` |
| `AI_MODEL` | Gemini model to use | `gemini-2.5-flash` |
| `WORKING_DIRECTORY` | Sandboxed directory the agent can access | *(set manually)* |

---

## Security

The agent is sandboxed to a single working directory. All file operations validate that the target path stays within the permitted directory — attempts to escape via `..` or absolute paths are rejected.
