import pytest
from rich import print
from rich.table import Table
from rich.console import Console
from rich.panel import Panel
from futureos.commands import COMMAND_LIST
from futureos.init.create_collections import initialize_commands, COMMANDS_COLLECTION


class TestCategories:
    """Test categories for better organization"""

    BASIC = "basic"
    COMPLEX = "complex"
    EDGE = "edge"


# Test data organized by command type and complexity
LS_COMMANDS = {
    TestCategories.BASIC: [
        "Can you check what's in here?",
        "what is inside work directory?"
        "I need to see the contents of the documents folder",
        "Give me a rundown of what's in this directory",
        "What have we got in this folder?",
        "Mind showing me what files exist here?",
        "Hey, what's sitting in this directory?",
        "ls",  # Keep one direct command for baseline
        "Would you mind listing what we have here?",
        "Could you show me the files in this location?",
    ],
    TestCategories.COMPLEX: [
        "I've got some project files somewhere in this folder, can you show me what's there?",
        "Need to check my homework directory, what files do we have?",
        "Been working on some documents, can you list them for me?",
        "My backup folder should have some files, can you check?",
        "What is in my code directory",
    ],
}

RM_COMMANDS = {
    TestCategories.BASIC: [
        "I need to get rid of report.txt",
        "Can you help me remove document.md?",
        "Let's remove notes.txt",
        "Need to clean up some files",
        "Would you help me remove something?",
        "Got to delete this file",
    ],
    TestCategories.COMPLEX: [
        "There's this config file with database stuff I need to get rid of",
        "Help me clean up these old API key files",
        "Need to remove some sensitive data files",
        "Got an old password file that needs to be deleted",
        "There are some project notes I don't need anymore",
    ],
}

PWD_COMMANDS = {
    TestCategories.BASIC: [
        "Mind telling me where we are?",
        "Could you show me my current location?",
        "Which directory am I in right now?",
        "What's our current position in the system?",
        "Help me figure out where I'm working from",
        "pwd",  # Keep one direct command
        "Can you tell me which folder we're in?",
        "Show me my place in the directory tree",
        "What's my current working location?",
    ],
    TestCategories.COMPLEX: [
        "Need the full directory path for this documentation I'm writing",
        "Got to know exactly where in the system I'm working",
        "Can you show me the complete path structure to here?",
        "Need to copy my current location for this config setup",
    ],
}

NANO_COMMANDS = {
    TestCategories.BASIC: [
        "I need to make some changes to report.txt",
        "Let's work on document.md for a bit",
        "Time to start a new file called notes.txt",
        "Got to update config.yml",
        "Want to write something new",
        "Need to make some text changes",
        "Let's create something",
    ],
    TestCategories.COMPLEX: [
        "Time to update those database settings in the config",
        "Need to make some changes to where I keep the API stuff",
        "Got to update where I keep all those passwords",
        "Should probably revise those project notes",
    ],
}

CAT_COMMANDS = {
    TestCategories.BASIC: [
        "What's written in this file?",
        "Can you read this out for me?",
        "Show me content of work log",
        "What does this file contain?",
        "show me what is in this file with meeting notes"
    ],
    TestCategories.COMPLEX: [
        "Need to check what Facebook details I saved here",
        "Can you show me what passwords I stored in this file?",
        "Got to check what API keys I put in here",
        "Print content of file with database settings ",
        "Need to verify these configuration details",
    ],
    TestCategories.EDGE: [
        "Hey, what's this file about?",
        "Could you peek inside notes.txt for me?",
        "What's the story with this file?",
        "Mind reading through this for me?",
    ],
}


def flatten_commands(command_dict):
    """Flatten nested command dictionary into list of (query, expected) tuples"""
    result = []
    for category, commands in command_dict.items():
        for cmd in commands:
            result.append((cmd, command_dict.get("command_type", "unknown")))
    return result


# Combine all test cases with proper command types
ALL_TEST_CASES = (
    [(cmd, "ls") for category in LS_COMMANDS.values() for cmd in category]
    # + [(cmd, "pwd") for category in PWD_COMMANDS.values() for cmd in category]
    + [(cmd, "nano") for category in NANO_COMMANDS.values() for cmd in category]
    + [(cmd, "cat") for category in CAT_COMMANDS.values() for cmd in category]
    + [(cmd, "rm") for category in RM_COMMANDS.values() for cmd in category]
)


@pytest.fixture(autouse=True)
def setup():
    """Initialize the commands collection before each test"""
    initialize_commands(COMMAND_LIST)


def create_test_group(command_type, commands_dict):
    """Create a test group for a specific command type"""

    @pytest.mark.parametrize(
        "query,expected_command",
        [(q, command_type) for category in commands_dict.values() for q in category],
    )
    def test_function(query, expected_command):
        response = COMMANDS_COLLECTION.query(query_texts=[query], n_results=1)
        command = response["ids"][0][0]
        assert command is not None, f"Command not found for query: {query}"
        assert (
            command == expected_command
        ), f"Query: {query}\nExpected: {expected_command}\nGot: {command}"

    return test_function


# Create separate test functions for each command type
test_ls_commands = create_test_group("ls", LS_COMMANDS)
# test_pwd_commands = create_test_group("pwd", PWD_COMMANDS)
test_nano_commands = create_test_group("nano", NANO_COMMANDS)
test_cat_commands = create_test_group("cat", CAT_COMMANDS)


def print_test_summary(results):
    """Print a beautiful summary of test results with proper table sizing"""
    console = Console()
    console_width = console.width or 100
    table_width = min(console_width - 4, 100)

    table = Table(
        title="Command Recognition Test Results",
        show_header=True,
        header_style="bold",
        show_lines=True,  # Add lines between rows for better readability
        width=table_width,
    )
    query_width = table_width - 35  # Reserve space for other columns
    table.add_column("Query", style="cyan", width=query_width, no_wrap=False)
    table.add_column("Expected", style="green", width=10, justify="center")
    table.add_column("Got", style="yellow", width=10, justify="center")
    table.add_column("Status", style="bold", width=8, justify="center")
    passed = 0
    failed = 0
    sorted_results = sorted(results, key=lambda x: (x[3], x[1]))
    for query, expected, actual, status in sorted_results:
        status_text = "✓" if status else "✗"
        table.add_row(
            query, expected, actual, status_text, style=None if status else "red"
        )
        if status:
            passed += 1
        else:
            failed += 1
    console.print(table)
    console.print(f"\n[green]Passed: {passed}[/green] | [red]Failed: {failed}[/red]")

    return passed, failed


def test_all_commands_with_summary(capsys):
    """Run all tests and generate a beautiful summary"""
    results = []

    for query, expected_command in ALL_TEST_CASES:
        response = COMMANDS_COLLECTION.query(query_texts=[query], n_results=1)
        actual_command = response["ids"][0][0]
        status = actual_command == expected_command
        results.append((query, expected_command, actual_command, status))

    # Print our custom formatted results
    passed, failed = print_test_summary(results)

    # Assert all tests passed
    assert failed == 0, f"{failed} tests failed"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

# how to add src to path in windows
# $env:PYTHONPATH += ";E:\FutureOS\futureOS\src"
