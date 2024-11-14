![PyPI - Python Version](https://img.shields.io/pypi/pyversions/futureos)
![PyPI - Version](https://img.shields.io/pypi/v/futureos)
![example workflow]([https://github.com/github/docs](https://github.com/miskibin/futureOS/actions/workflows/python-app.yml/badge.svg)

# FutureOS 🚀

My take on how Operating Systems will be built in the future.

<img src="https://github.com/user-attachments/assets/4bdf7e12-0f9b-4f68-a588-4aed67ec6d45" alt="FutureOS Interface" />

## 🚀 Getting Started

```bash
# Install
pip install futureos

# Launch
python -m futureos
```

> [!IMPORTANT]  
> To use FutureOS, ensure you have Ollama installed with the `gemma2:2b` model. For optimal performance, CUDA should be enabled on your system.

## 🌟 The Challenge

Currently, there are several powerful AI tools for both Windows and macOS:

- 🤖 [Claude computer use](https://www.anthropic.com/news/3-5-models-and-computer-use)
- 👨‍💻 [GitHub Copilot](https://copilot.github.com)
- 🗣️ New Siri on Mac

However, these tools implement their own methods of indexing and searching files, and they're not integrated with the OS.

## 💡 The Vision

What if:

- Every utility in the OS had access to `vector search` for collections of all `files`, `directories`, `pictures`, and more?
- All content was automatically indexed by the OS whenever a file is created or modified?
- Every utility had access to an `AI chain` (like LangChain) deeply integrated into the OS?
- Every command could leverage these AI capabilities?

Let's go further... 🚀

Why force users to remember specific commands with their parameters and arguments? By creating descriptive docstrings for commands, we can build a vector store of all commands and automatically choose the best one for user input. Users don't even need to know exact command names!

## ✅ Quality Assurance

"But without proper testing, users wouldn't like it."

I know! That's why there are [multiple tests](/tests/test_create_collections.py) for every command with output that's easy to parse by LLM.

## 🏗️ Architecture

### Command System

Every command inherits from a base `Command` class that provides:

```python
def get_file(self, question: str, max_distance: float) -> str:
    """Find relevant files using vector similarity search"""

def get_directory(self, question: str, max_distance: float) -> str:
    """Find relevant directories using vector similarity search"""

def run_chain(self, chain: RunnablePassthrough, input: dict) -> Any:
    """Execute LangChain operations for content processing"""
```

### 🔍 How Commands Work

Let's break down how a typical command (cd) is constructed:

```python
class cd(Command):
    """
    NAME
        cd - change the current working directory

    SYNOPSIS
        cd [directory]

    DESCRIPTION
        Change the current working directory to the specified directory.

    NATURAL LANGUAGE COMMANDS
        - Change directory to X
        - Go to folder X
        - Navigate to directory X
    """
```

The docstring serves multiple purposes:

1. **Vector Embedding Source**: Used to create embeddings for command matching
2. **Natural Language Patterns**: Defines common ways users might express the command
3. **Documentation**: Serves as built-in help text

### Command Implementation

```python
def execute(self, args: Any) -> None:
    try:
        # Handle both traditional and natural language input
        directory = self.get_directory(args.query) if args.query else args.directory

        # Resolve and validate path
        target_path = resolve_path(directory)

        # Execute directory change
        if target_path.is_dir():
            constants.CURRENT_DIRECTORY = target_path
            self.print(f"Changed to {target_path}", style="green")
    except Exception as e:
        self.print(f"Error: {str(e)}", style="red")
```

## 🤝 Contributing

All contributors are welcome!

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details.
