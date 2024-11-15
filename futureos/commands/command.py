from abc import ABC, abstractmethod
from argparse import ArgumentParser
from chromadb import Collection
from langchain_ollama import OllamaLLM
from rich.console import Console
from rich.status import Status
from typing import Literal, Optional, Any
from langchain_core.prompts import ChatPromptTemplate
from futureos.utils.console_manager import future_console as console
from futureos.init.create_collections import (
    FILES_COLLECTION,
    initialize_directories_collection,
    initialize_files_collection,
)
from futureos.init.create_collections import DIRECTORIES_COLLECTION
from futureos import constants
from langchain_core.runnables import RunnablePassthrough

from futureos.utils.path_utils import get_relative_path


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
            num_predict=192,
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
        if results["distances"][0][0] > max_distance:
            self.print(
                f"I did not find a good match for the question in the files. Distance: {results['distances'][0][0]:.3f} > max Distance: {max_distance}",
                style="yellow",
            )
            return
        self.print(f"{self.__class__.__name__} {filename}", style="green")
        return filename

    def get_directory(self, question: str, max_distance=2.0) -> str:
        with console.status("Searching for the directory..."):
            enhanced_query = f"Current directory: {get_relative_path(constants.CURRENT_DIRECTORY)}\n{question}"
            results = DIRECTORIES_COLLECTION.query(
                query_texts=[enhanced_query], n_results=1
            )
        directory = results["ids"][0][0]

        if results["distances"][0][0] > max_distance:
            self.print(
                f"I did not find a good match for the question in the directories {results['distances'][0][0]:.2f}",
                style="yellow",
            )
            return
        self.print(f"{self.__class__.__name__} {directory}", style="green")
        return directory

    def run_chain(
        self, chain: RunnablePassthrough, input: dict, stream: bool = False
    ) -> Any:
        with console.status(f"{self.__class__.__name__} is Running llm..."):
            if stream:
                result = ""
                for chunk in chain.stream(input=input):
                    result += chunk
                    print(chunk, end="")
                return result
            else:
                result = chain.invoke(input=input)
                return result

    def confirm_action(self, message: str) -> bool:
        """Prompt the user for confirmation."""
        self.print(f"{message} (y/n): ", style="yellow")
        response = input().strip().lower()
        return response == "y"

    def update_indexes(
        self, collection: Literal["files", "directories"], ids: list[str]
    ):
        self.print(f"Updating {collection} collection...", style="yellow")
        function = {
            "files": initialize_files_collection,
            "directories": initialize_directories_collection,
        }
        function[collection](ids)

    def __call__(self, *args: Any, **kwargs: Any) -> None:
        self.execute(self.parser.parse_args(*args))
