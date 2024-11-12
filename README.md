# futureOS

futureOS is a command-line interface (CLI) tool for managing and executing various shell commands with enhanced features. It leverages advanced libraries like `chromadb`, `langchain`, and `rich` to provide a powerful and user-friendly experience.

![image](https://github.com/user-attachments/assets/d22be02b-33d5-4c18-a516-05e6bc3715c7)
![image](https://github.com/user-attachments/assets/f96f1e3d-baed-42e0-b647-289e7e0d77d4)


## Features

- Execute shell commands with natural language queries.
- Enhanced command matching using embeddings.
- Rich output formatting with `rich`.
- Logging with `loguru`.

## Installation

To install futureOS, ensure you have Python 3.12 or higher and use the `uv` packaging tool:

```sh
uv install futureos
```

## Usage

After installation, you can start the CLI by running:

```sh
python -m futureos
```

### Available Commands

- `help`: Show help for all commands or a specific command.
- `exit`/`quit`: Exit the shell.

### Example

```sh
$ python -m futureos
Type 'help' for available commands

$ /home $ ls
# Lists the files in the current directory

$ /home $ cat /home/finances.csv
# Displays the content of the file 'finances.csv'
```

### Test results

![image](https://github.com/user-attachments/assets/07b223fe-5d99-439f-9d23-178ae7ec39fe)


## Contributing

Contributions are welcome! Please open an issue or submit a pull request on GitHub.

## License

This project is licensed under the MIT License.
