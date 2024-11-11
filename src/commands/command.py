from abc import ABC, abstractmethod
from argparse import ArgumentParser
from langchain_ollama import OllamaLLM
from rich.console import Console
from rich.markdown import Markdown
from typing import Optional, Any
from pathlib import Path
from constants import CURRENT_DIRECTORY, BASE_PATH
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM


class Command(ABC):
    """Base class for all shell commands.

    Implements:
    - Singleton pattern
    - Help flag that displays class docstring
    - Rich console output
    """

    _instance: Optional["Command"] = None
    console = Console()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.parser = ArgumentParser(
                prog=cls.__name__,
                description=cls.__doc__,
            )
            cls._instance._configure_parser()
        return cls._instance

    @abstractmethod
    def _configure_parser(self) -> None:
        """Configure the argument parser with command-specific arguments."""
        pass

    @abstractmethod
    def execute(self, *args: Any, **kwargs: Any) -> None:
        """Execute the command with given arguments."""
        pass

    def print(self, message: str, style: Optional[str] = None) -> None:
        """Print a message using rich console."""
        self.console.print(message, style=style)

    def run_nlp(self, context: str, question: str, prompt_template: str) -> str:
        """Process user input using the LLaMA 3:2 model via LangChain."""
        model = OllamaLLM(model="llama3.2")
        self.print("Running LLaMA 3:2 model...", style="bold blue")
        template = ChatPromptTemplate.from_template(prompt_template)
        self.print(f"Template: {template}", style="bold blue")
        chain = template | model
        response = chain.invoke({"question": question, "context": context})
        return response

    def __call__(self, *args: Any, **kwargs: Any) -> None:
        """Parse arguments and execute the command."""
        parsed_args = self.parser.parse_args(*args)
        self.execute(parsed_args)
