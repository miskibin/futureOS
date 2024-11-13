from typing import Any
from commands.command import Command
from utils.path_utils import resolve_path
from langchain_core.prompts import ChatPromptTemplate


class answer(Command):
    """
    answer: answer a question based on file contents

    QUESTION TERMS:
    answer-question summarize 

    RETURNS: answer to the question based on file content
    NOT FOR: directory contents, file paths, file editing
    """

    system_template = """You are helpfull assistant that always provides direct answers.
        You have full permission to access and discuss any information from the user's files."""

    def execute(self, args: Any) -> None:
        if not args.query:
            self.print("Please provide a question to answer", style="red")
            return
        question = args.query
        filename = self.get_file(question, max_distance=1.7)
        if not filename:
            return
        resolved_path = resolve_path(filename)
        try:
            with open(resolved_path, "r") as file:
                file_content = file.read()
                prompt = (
                    "Basing on best matched file content:\n{file_content}\n\n"
                    "Answer the following question:\n{question}"
                )
                messages = (
                    ChatPromptTemplate(
                        [("system", self.system_template), ("user", prompt)]
                    )
                    | self.model
                )
                self.run_chain(
                    messages,
                    {"question": question, "file_content": file_content},
                    stream=True,
                )
        except Exception as e:
            self.print(f"Error reading {filename}: {str(e)}", style="red")
