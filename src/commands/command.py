from abc import ABC, abstractmethod
from argparse import ArgumentParser
from langchain_ollama import OllamaLLM
from rich.console import Console
from rich.status import Status
from typing import Optional, Any
from langchain_core.prompts import ChatPromptTemplate


class Command(ABC):
    """Base class for all shell commands."""

    _instance = None
    console = Console()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.parser = ArgumentParser(
                prog=cls.__name__, description=cls.__doc__
            )
            cls._instance.parser.add_argument(
                "-q",
                "--query",
                type=str,
                help="Natural language query to run the command",
            )
            cls._instance._configure_parser()
        return cls._instance

    @abstractmethod
    def _configure_parser(self) -> None:
        pass

    @abstractmethod
    def execute(self, *args: Any, **kwargs: Any) -> None:
        pass

    def print(self, message: str, style: Optional[str] = None) -> None:
        self.console.print(message, style=style)

    def run_nlp(self, context: str, question: str, prompt: str) -> str:
        with Status("[blue]Processing...", console=self.console):
            model = OllamaLLM(model="llama3.2", max_length=40, temperature=0.2)
            chain = ChatPromptTemplate.from_template(prompt) | model
            return chain.invoke({"question": question, "context": context})

    def __call__(self, *args: Any, **kwargs: Any) -> None:
        self.execute(self.parser.parse_args(*args))
