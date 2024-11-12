from abc import ABC, abstractmethod
from argparse import ArgumentParser
from langchain_ollama import OllamaLLM
from rich.console import Console
from rich.status import Status
from typing import Optional, Any
from langchain_core.prompts import ChatPromptTemplate

from init.create_collections import FILES_COLLECTION


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

    def get_file(self, question: str) -> str:
        with self.console.status("Searching for the file..."):
            results = FILES_COLLECTION.query(query_texts=[question], n_results=1)
        filename = results["ids"][0][0]
        self.print(f"Best match: {filename}", style="green")
        return filename

    def run_nlp(self, context: str, question: str, prompt: str) -> str:
        model = OllamaLLM(model="llama3.2:1b", max_length=40, temperature=0.2)
        chain = ChatPromptTemplate.from_template(prompt) | model
        # show full prompt
        # self.print(f"\n\n{prompt.format(context=context, question=question)}\n")
        with self.console.status("Processing natural language query..."):
            result = chain.invoke({"question": question, "context": context})
        return result

    def __call__(self, *args: Any, **kwargs: Any) -> None:
        self.execute(self.parser.parse_args(*args))

