# Personal LLM Agent Framework

Autonomous AI agent built with Python and Google Gemini that executes complex tasks independently through function calling and an agentic loop.

## Motivation

Built as a learning project on [Boot.dev](https://boot.dev) to explore core patterns behind autonomous LLM agents.

The agent can navigate the filesystem, read/write files, execute Python scripts, and make decisions based on the results of its actions — completing complex tasks across multiple iterations without human intervention.

Key techniques demonstrated:

- **Function Calling (Tool Use)** — structured schema-based invocation of Python functions by the LLM
- **Agentic Loop** — autonomous loop with full conversation history, iteration limit, and self-termination
- **Security Sandboxing** — directory traversal prevention; agent confined to its working directory
- **Dynamic Function Dispatch** — dictionary-based mapping from LLM calls to Python functions
- **Process Execution** — safe subprocess execution with timeout and stdout/stderr capture
- **Message History Management** — multi-turn context kept across all iterations of a task

## Quick Start

**Prerequisites:** Python 3.13+, [Google Gemini API key](https://aistudio.google.com/)

```bash
git clone <repo-url>
cd personal-llm
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file:

```
GEMINI_API_KEY=your_api_key_here
```

**Tech stack:** Python 3.13 · Google Gemini 2.5-Flash · google-genai · python-dotenv

**Project structure:**

```
personal-llm/
├── main.py                 # Entry point and agent loop
├── call_function.py        # Function dispatcher and tool definitions
├── prompt.py               # System prompt for the LLM
├── config.py               # Configuration constants
├── functions/              # Tool implementations
│   ├── get_files_info.py
│   ├── get_file_content.py
│   ├── write_file.py
│   └── run_python_file.py
└── calculator/             # Example project for testing
```

## Usage

```bash
python main.py "Your task here"
python main.py --verbose "Your task here"   # debug output
```

**Available agent tools:**

| Tool | Description |
|------|-------------|
| `get_files_info` | List files in a directory with metadata |
| `get_file_content` | Read file contents |
| `write_file` | Create or overwrite files |
| `run_python_file` | Execute a Python script and capture output |

**Execution flow:**

```
User provides task
       │
       ▼
  LLM analyzes and responds
       │
       ▼
  Has function calls? ──YES──▶ Execute functions
       │                              │
       NO                             │
       │                              │
       ▼                              │
  Final response ◀───────────────────┘
```

## Contributing

Bug reports and feature requests: open an issue.

Pull requests are welcome. Please follow the existing code style and keep tool implementations self-contained under `functions/`.
