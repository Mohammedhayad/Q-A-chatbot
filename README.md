# AI Question & Answering System

A modular Streamlit chat application powered by Google's Gemini API. It keeps
conversation history in the current Streamlit session so users can ask
follow-up questions.

## Features

- Streamlit chat interface with separate user and assistant messages.
- Multi-turn conversation history in `st.session_state`.
- Configurable Gemini model and response temperature.
- Gemini client and API calls encapsulated in a service.
- Clear-conversation button, loading indicator, and friendly error messages.
- Tests that mock Gemini and do not make network calls.

## Architecture

The Streamlit UI coordinates configuration, prompt management, and the Gemini
service. `settings.py` loads and validates environment settings. The service
initializes the Gemini client, sends system instructions and conversation
history, and returns answer text. Logging records application events without
logging API keys or full conversations.

## Project structure

```text
.
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py
│   ├── prompts/
│   │   ├── __init__.py
│   │   └── qa_prompt.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── gemini_service.py
│   └── utils/
│       ├── __init__.py
│       └── logging_config.py
├── tests/
│   ├── __init__.py
│   ├── test_config.py
│   └── test_gemini_service.py
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
├── streamlit_app.py
└── run.sh
```

## Requirements

- Python 3.10 or newer.
- A Gemini API key.

Check the Python version:

```sh
python --version
```

On some systems, use `python3` instead of `python`.

## Configure Gemini

Copy `.env.example` to `.env`:

macOS/Linux:

```sh
cp .env.example .env
```

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Windows Command Prompt:

```bat
copy .env.example .env
```

Set your Gemini API key in `.env`:

```dotenv
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-3.8-flash
TEMPERATURE=0.2
```

`GEMINI_API_KEY` is required. `GEMINI_MODEL` defaults to
`gemini-3.8-flash`, and `TEMPERATURE` defaults to `0.2` (valid range: 0–2).
The app reads these exact uppercase environment variable names. It does not
read OpenAI settings.

## Create and activate a virtual environment

From the project root, create the virtual environment:

```sh
python -m venv .venv
```

Activate it:

macOS/Linux:

```sh
source .venv/bin/activate
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Windows Command Prompt:

```bat
.venv\Scripts\activate.bat
```

## Install dependencies

With the virtual environment active:

```sh
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Run the Streamlit application

Run from the project root with the virtual environment active and `.env`
configured:

```sh
python -m streamlit run streamlit_app.py
```

`streamlit_app.py` ensures the project root is available for package imports.
The terminal displays the local browser URL. On macOS/Linux you can also run
`./run.sh`.

Submit a question in the chat input, ask follow-ups, or select **Clear
Conversation** in the sidebar to reset the current session.

## Run tests

Tests use a mocked Gemini client and need neither a real API key nor network
access:

```sh
python -m pytest
```

## Example questions

- “Explain photosynthesis in simple terms.”
- “What are the main differences between lists and tuples in Python?”
- “Suggest a three-day itinerary for visiting Kyoto.”
- “Summarize your previous answer as three bullet points.”

## Troubleshooting

- **Gemini API key is missing:** Confirm `.env` is in the project root and
  contains a non-empty `GEMINI_API_KEY`.
- **Invalid key or permission error:** Verify the key is valid and enabled for
  the Gemini API.
- **Model unavailable:** Set `GEMINI_MODEL` to a model available to your API
  key.
- **Invalid temperature:** Set `TEMPERATURE` to a number between `0` and `2`.
- **`ModuleNotFoundError: No module named 'app'`:** Launch
  `streamlit_app.py` from the project root using the command above, not
  `app/main.py` directly.
- **Missing commands or imports:** Activate `.venv` and reinstall dependencies
  with `python -m pip install -r requirements.txt`.

## Security

- `.env` is ignored by Git. Never commit it or put a real key in
  `.env.example`.
- Do not put API keys in source code, logs, or UI.
- Questions and conversation history are sent to Google's Gemini API. Do not
  submit sensitive information unless you are permitted to do so.
- Revoke or rotate the API key if it is exposed.

## Stop and deactivate

Stop Streamlit with **Ctrl+C** in its terminal. Deactivate the virtual
environment with:

```sh
deactivate
```

## Future enhancements

- Add configurable limits for retained conversation history.
- Add deployment and production secret-management guidance.
- Add UI-level tests for chat interactions.
