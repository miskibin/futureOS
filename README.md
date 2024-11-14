# FutureOS

My take of how Operating systems will be build in the future.

Currently there are a lot of tools for both windows and mac, like: 
- [claude computer use](https://www.anthropic.com/news/3-5-models-and-computer-use)
- [github copilot](https://copilot.github.com)
or new siri on the mac.

But those are just tools that implement thiers own method of indexing and searching files, and they are not integrated with the OS.
qWell. Guess what. Now it is. (It is POC).

What if every utility in the OS had access to `vector search` for collection for all `files`, `directoires`, `pictures` and so on. All those would be indexed by the OS every time a file is created or modified.
What if every utility had access to `AI chain` like lanchain chain, that would be deeply integrated into the OS, and every command would be able to use it.

Let's get further
Why force the user to remember what command should he use with what parameters and arguments. 
If we create descriptive docstring for the command, we could create vector store with all commands, and then just choose best command for user input. He does not even needs to know the exact command name.
Yep but it seems like without proper testing user wouldn't like it. I know. That is why there are [multiple tests](/tests/test_create_collections.py) for every command with output easy to parse by llm.

![image](https://github.com/user-attachments/assets/4bdf7e12-0f9b-4f68-a588-4aed67ec6d45)

## Key Features

### 💡 Natural Language Understanding

- Interact with your system using everyday language
- No need to remember exact command syntax
- System understands context and intent of your requests

```bash
"what should I do today?"
"show me my financial data"
"I don't need this file anymore"
```

### 🧠 Core AI Capabilities

Each command can utilize:

- **Vector Search**: Find relevant files and directories based on semantic meaning
- **LangChain Integration**: Process and understand content intelligently
- **Content Analysis**: Understand file contents and respond to queries about them
- **Context Awareness**: Maintain awareness of current directory and previous interactions

## Architecture

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

### AI Integration

- **Vector Embeddings**: Files and directories are embedded for semantic search
- **Language Models**: Integrated LLM support for understanding and processing
- **Prompt Templates**: Structured communication with AI models
- **Streaming Responses**: Real-time AI-generated responses

## Examples

### Natural Interaction

```bash
# Finding and reading relevant files
> "what's in my budget file?"
System: *finds and reads financial data using content understanding*

# Directory navigation
> "go to my pictures folder"
System: *understands intent and changes directory*

# File management
> "I don't need this file anymore"
System: *identifies file from context and confirms deletion*
```

### Content Understanding

```bash
# Task Management
> "what should I do today?"
System: *finds and analyzes task files, provides summary*

# Data Analysis
> "show me my spending from last month"
System: *locates and interprets financial data*
```

## Installation

```bash
pip install futureos
python -m futureos
```

## Contributing

Contributions are welcome! Key areas:

- New AI capabilities
- Enhanced natural language understanding
- Improved content analysis
- Additional command features

## License

MIT License - See LICENSE file for details.
