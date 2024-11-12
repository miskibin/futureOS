import pytest
from rich import print
from rich.table import Table
from rich.panel import Panel
from commands import get_command, COMMAND_LIST
from init.create_collections import initialize_commands, COMMANDS_COLLECTION


class TestCategories:
    """Test categories for better organization"""

    BASIC = "basic"
    COMPLEX = "complex"
    EDGE = "edge"


# Test data organized by command type and complexity
LS_COMMANDS = {
    TestCategories.BASIC: [
        "Show files in directory",
        "List contents of folder documents",
        "What is in the current directory",  # This should work with ls
        "Display files in downloads",
        "Show what's in this folder",
        "List all items in directory",
        "ls .",
        "Show me what files are here",
        "What files do I have?",
        "Display current folder contents",
    ],
    TestCategories.COMPLEX: [
        "I need to see what's in the folder with my project files",
        "Could you show me the contents of the directory containing my homework",
        "List everything inside the folder where I keep my documents",
        "What files are stored in the directory with my backups",
        "Show contents of the folder that has my code",
    ],
}

PWD_COMMANDS = {
    TestCategories.BASIC: [
        "where am i?",
        "What is the full path to my current directory?",
        "Show me the absolute path of where I am",
        "Print the path to my current location",
        "Display my current directory path",
        "pwd .",
        "Current location please",
        "List current path",
        "Show directory path",
    ],
    TestCategories.COMPLEX: [
        "I need to know the complete path to where I'm working right now",
        "Tell me the full directory structure to my current position",
        "What's the absolute filesystem path to this location",
        "I need the full path to include in my configuration file",
    ],
}

NANO_COMMANDS = {
    TestCategories.BASIC: [
        "Edit file report.txt",
        "Open file document.md in editor",
        "Create new file notes.txt",
        "Modify file config.yml",
        "I want to edit a file",
        "Open editor",
        "Create and edit new file",
    ],
    TestCategories.COMPLEX: [
        "I need to edit the configuration file with my database credentials",
        "Open the file containing my API keys in the editor",
        "Create a new file to store my AWS access keys",
        "Edit the text file where I keep my passwords",
        "I want to modify the file that has my project notes",
    ],
}

CAT_COMMANDS = {
    TestCategories.BASIC: [
        "Show file content",
        "Display file",
        "Read file",
        "Print file contents",
        "Show what's in file",
    ],
    TestCategories.COMPLEX: [
        "Show me the content of the file with my Facebook login",
        "Display the contents of the file containing my passwords",
        "I need to see what's written in my credentials file",
        "Read out the file where I stored my API keys",
        "Show me what's inside the configuration file with my database setup",
    ],
    TestCategories.EDGE: [
        "What does this file say",
        "Let me see inside this document",
        "Read out everything in this file",
        "Display all text from this document",
    ],
}

INDEX_COMMANDS = {
    TestCategories.BASIC: [
        "Rebuild the search index",
        "Reindex the file system",
        "Update the file index",
        "Regenerate the search index",
        "Rebuild file system index",
        "Need to rebuild the index",
        "Update search database",
    ],
    TestCategories.COMPLEX: [
        "The search seems slow, we need to rebuild the index",
        "Search isn't working well, please reindex everything",
        "I added new files manually, update the search index",
        "Regenerate indexes after adding new documents",
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
    + [(cmd, "pwd") for category in PWD_COMMANDS.values() for cmd in category]
    + [(cmd, "nano") for category in NANO_COMMANDS.values() for cmd in category]
    + [(cmd, "cat") for category in CAT_COMMANDS.values() for cmd in category]
    + [(cmd, "index") for category in INDEX_COMMANDS.values() for cmd in category]
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
test_pwd_commands = create_test_group("pwd", PWD_COMMANDS)
test_nano_commands = create_test_group("nano", NANO_COMMANDS)
test_cat_commands = create_test_group("cat", CAT_COMMANDS)
test_index_commands = create_test_group("index", INDEX_COMMANDS)


def print_test_summary(results):
    """Print a beautiful summary of test results"""
    table = Table(title="Command Recognition Test Results")
    table.add_column("Query", style="cyan", width=50)
    table.add_column("Expected", style="green")
    table.add_column("Result", style="blue")
    table.add_column("Status", style="bold")

    passed = 0
    failed = 0

    # Sort results by status (failed first) and then by query
    sorted_results = sorted(results, key=lambda x: (x[3], x[0]))

    for query, expected, actual, status in sorted_results:
        status_style = "green" if status else "red"
        status_text = "✓" if status else "✗"
        table.add_row(
            query[:47] + "..." if len(query) > 50 else query,
            expected,
            actual,
            status_text,
            style=None if status else "red",
        )
        if status:
            passed += 1
        else:
            failed += 1

    print(Panel(table, border_style="blue"))
    print(f"\n[green]Passed: {passed}[/green] | [red]Failed: {failed}[/red]")
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
