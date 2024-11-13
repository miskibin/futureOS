# FutureOS

FutureOS is a next-generation AI-powered command-line (POC) operating system that understands natural language and can interact with files and system resources intelligently.

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

### 🔍 Intelligent Search

- Vector-based search for files and directories
- Content-aware file finding
- Understands semantic meaning, not just keywords
- Automatically indexes file contents for smart searching

### 🤖 AI-Powered Commands

Every command in FutureOS is AI-enabled with:

- Natural language processing
- Content understanding
- Context awareness
- Intelligent decision making

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
