# Portfolio Backend

This project is the backend of my portfolio, developed with FastAPI.

## Prerequisites

- Python 3.11+
- FastAPI
- uv for Python package and environment management. (https://docs.astral.sh/uv/)
- Ruff

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/***.git
    cd ***
    ```

General Workflow
By default, the dependencies are managed with uv, go there and install it.

From ./backend/ you can install all the dependencies with:

    ```
    $ uv sync
    ```
Then you can activate the virtual environment with:

$ source .venv/bin/activate
Make sure your editor is using the correct Python virtual environment, with the interpreter at backend/.venv/bin/python.

## Usage

1. Start the server:

    ```bash
    uv run fastapi dev
    ```

2. Access the interactive API documentation at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) or [http://127.0.0.1:8000/redocs](http://127.0.0.1:8000/redocs).

## Static Analysis

To analyze the code with Ruff, run the following command:

```bash
ruff .
```

## Project Structure

```
portfolio-backend/
├── app/
│   ├── main.py
│   ├── routers/
│   └── models/
├── tests/
├── requirements.txt
└── README.md
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.