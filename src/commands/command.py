from abc import ABC, abstractmethod
from argparse import ArgumentParser
from langchain_ollama import OllamaLLM
from rich.console import Console
from rich.status import Status
from typing import Optional, Any
from langchain_core.prompts import ChatPromptTemplate
from utils.console_manager import future_console as console
from init.create_collections import FILES_COLLECTION
from langchain_core.runnables import RunnablePassthrough


class Command(ABC):
    """Base class for all shell commands."""

    _instance = None

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
        cls.model = OllamaLLM(
            # model="llama3.2",
            model="gemma2:2b",
            max_length=100,  # Shorter responses
            top_p=0.95,  # High top_p for more focused responses
        )
        return cls._instance

    def _configure_parser(self) -> None:
        pass

    @abstractmethod
    def execute(self, *args: Any, **kwargs: Any) -> None:
        pass

    def print(self, message: str, style: Optional[str] = None) -> None:
        console.print(message, style=style)

    def get_file(self, question: str, max_distance=2.0) -> str:
        with console.status("Searching for the file..."):
            results = FILES_COLLECTION.query(query_texts=[question], n_results=1)
        filename = results["ids"][0][0]
        self.print(f"Best match: {filename}", style="green")
        if results["distances"][0][0] > max_distance:
            self.print(
                f"I did not find a good match for the question in the files {results['distances'][0][0]:.2f}",
                style="yellow",
            )
            return
        return filename

    def run_chain(
        self, chain: RunnablePassthrough, input: dict, stream: bool = False
    ) -> Any:
        with console.status("Running the model..."):
            if stream:
                result = ""
                for chunk in chain.stream(input=input):
                    result += chunk
                    print(chunk, end="")
                return result
            else:
                result = chain.invoke(input=input)
                return result

    def __call__(self, *args: Any, **kwargs: Any) -> None:
        self.execute(self.parser.parse_args(*args))
