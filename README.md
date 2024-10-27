# ChatGPT and LangChain: The Complete Developer's Masterclass

This project is part of the "ChatGPT and LangChain: The Complete Developer's Masterclass" course. It demonstrates how to use LangChain to generate code snippets using OpenAI's language model.

## Prerequisites

- Python 3.7+
- Pipenv for managing dependencies

## Setup

1. Install dependencies:

   ```sh
   pipenv install
   ```

2. Create a `.env` file based on the `.env.example` file and add your OpenAI API key:

   ```sh
   cp .env.example .env
   ```

3. Activate the virtual environment:
   ```sh
   pipenv shell
   ```

## Usage

To run the project, execute the following command:

```sh
python main.py --task "<your-task>" --language "<your-language>"
```

## License

This project is licensed under the MIT License.
