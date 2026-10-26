# JARVIS — Local LLM Voice Assistant

A Python voice and text assistant powered by a locally running Ollama model. It can answer questions, use facts you choose to save, retrieve relevant lines from a local knowledge file, and perform a small set of allowlisted desktop and web actions.

## Features

- Local LLM responses through Ollama (default model: `llama3`).
- Voice input with SpeechRecognition and spoken output with pyttsx3.
- `--text` mode for machines without audio hardware.
- Persistent JSON memory with explicit remember, review, and clear commands.
- Lightweight retrieval from a local `knowledge.txt` file.
- Time, date, and battery responses; allowlisted app and website opening; encoded web and YouTube searches.
- No arbitrary shell execution or voice-triggered shutdown/restart.

## Requirements

- Python 3.10 or newer.
- [Ollama](https://ollama.com/download), running locally.
- A downloaded Ollama model, for example `llama3`.
- For voice mode, a working microphone and speaker. Speech recognition uses Google's online recognition service.

## Setup

```bash
git clone https://github.com/nanda9121/Ai-assistant-using-LLM.git
cd Ai-assistant-using-LLM
python -m venv .venv
```

Activate the environment:

```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

```bash
# macOS / Linux
source .venv/bin/activate
```

Install Python packages and prepare the model:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
ollama pull llama3
```

Start Ollama if it is not already running, then launch JARVIS:

```bash
python main.py
```

For text-only interaction:

```bash
python main.py --text
```

Type `help` to see built-in commands. Type `exit` or `quit` to close text mode; say one of the exit phrases in voice mode.

## Configuration

Copy `.env.example` to `.env` and set any overrides in your shell or use your preferred environment-file loader. The project does not automatically load `.env`.

| Variable | Default | Purpose |
| --- | --- | --- |
| `OLLAMA_URL` | `http://localhost:11434/api/generate` | Ollama generate endpoint |
| `OLLAMA_MODEL` | `llama3` | Installed model name |
| `OLLAMA_TIMEOUT` | `60` | Request timeout in seconds |
| `ASSISTANT_SPEECH_RATE` | `165` | Text-to-speech rate |
| `ASSISTANT_LISTEN_TIMEOUT` | `5` | Seconds to wait for speech to start |
| `ASSISTANT_PHRASE_LIMIT` | `15` | Maximum seconds per spoken phrase |
| `ASSISTANT_MEMORY_FILE` | `memory.json` beside `main.py` | Optional memory-file location |
| `ASSISTANT_KNOWLEDGE_FILE` | `knowledge.txt` beside `main.py` | Optional knowledge-file location |

On Windows, microphone support may require installing a compatible PyAudio wheel if the requirements install reports that PyAudio is unavailable. Text mode does not need audio devices.

## Memory and local knowledge

- Say `remember that ...` to save a fact.
- Ask `what do you remember` to review saved context.
- Say `clear memory` to restore the empty defaults.
- Add one knowledge item per line to `knowledge.txt`. This file is ignored by Git so personal notes are not committed.
- Memory is stored locally in `memory.json`, which is also ignored by Git.

## Tests

The tests use only Python's standard library and mock external services:

```bash
python -m unittest discover -s tests -v
```

## Troubleshooting

- **Cannot connect to Ollama:** start Ollama, confirm `ollama list` shows the configured model, and check `OLLAMA_URL`.
- **Model not found:** run `ollama pull <model-name>` using the configured `OLLAMA_MODEL`.
- **Microphone unavailable:** check OS microphone permissions and audio drivers, or run `python main.py --text`.
- **Speech recognition unavailable:** voice transcription needs an internet connection; the local LLM itself runs through Ollama.
