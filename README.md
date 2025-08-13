<div align="center">

# 🚀 Celeste API

### Unified HTTP API for Celeste — Capabilities, Models, Providers, and Streaming

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge&logo=opensourceinitiative&logoColor=white)](LICENSE)
[![Interface](https://img.shields.io/badge/Interface-REST_+_SSE-purple?style=for-the-badge&logo=fastapi&logoColor=white)](#-api-overview)
[![OpenAPI](https://img.shields.io/badge/OpenAPI-Available-85ea2d?style=for-the-badge&logo=openapi-initiative&logoColor=white)](/docs)

[![Try API](https://img.shields.io/badge/🚀_Try_API-OpenAPI_UI-0ea5e9?style=for-the-badge)](/docs)

</div>

---

## 🎯 Why Celeste API?

<div align="center">
  <table>
    <tr>
      <td align="center">🔌<br><b>Unified Gateway</b><br>Single HTTP surface for all providers</td>
      <td align="center">🔐<br><b>Secure Keys</b><br>Secrets remain server‑side</td>
      <td align="center">🌊<br><b>Streaming</b><br>SSE token-by-token responses</td>
      <td align="center">📦<br><b>Uploads</b><br>Images, Audio, PDFs via multipart</td>
    </tr>
  </table>
</div>

Backed by the Celeste Python libraries, this API exposes capability‑aware model discovery and normalized operations, returning consistent `AIResponse` JSON across providers.

## 🚀 Quick Start

```bash
# 1) Create a virtualenv and install
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .

# 2) Install Celeste subpackages (editable) so imports work locally
pip install -e ../celeste-core ../celeste-client ../celeste-image-generation \
  ../celeste-image-edit ../celeste-audio-intelligence ../celeste-document-intelligence \
  ../celeste-embeddings

# 3) Configure environment
cp .env.example .env

# 4) Run the API
uvicorn celeste_api.main:app --reload --port 8000

# Open the OpenAPI UI:
# http://localhost:8000/docs
```

<details>
<summary><b>Using UV (Alternative)</b></summary>

```bash
uv venv
source .venv/bin/activate
uv pip install -e .
uv pip install -e ../celeste-core ../celeste-client ../celeste-image-generation \
  ../celeste-image-edit ../celeste-audio-intelligence ../celeste-document-intelligence \
  ../celeste-embeddings
uvicorn celeste_api.main:app --reload --port 8000
```

</details>

## 🔧 Configuration

### 1️⃣ Create your environment file
```bash
cp .env.example .env
```

### 2️⃣ Add your API keys

<details>
<summary><b>🔑 API Key Setup</b></summary>

| Provider | Environment Variable | Get API Key |
|----------|----------------------|-------------|
| 🌈 **Gemini** | `GOOGLE_API_KEY` | [Google AI Studio](https://aistudio.google.com/app/apikey) |
| 🤖 **OpenAI** | `OPENAI_API_KEY` | [OpenAI Platform](https://platform.openai.com/api-keys) |
| 🌊 **Mistral** | `MISTRAL_API_KEY` | [Mistral Console](https://console.mistral.ai/) |
| 🎭 **Anthropic** | `ANTHROPIC_API_KEY` | [Anthropic Console](https://console.anthropic.com/) |
| 🤗 **Hugging Face** | `HUGGINGFACE_HUB_TOKEN` | [HF Settings](https://huggingface.co/settings/tokens) |
| 🦙 **Ollama** | `OLLAMA_HOST` (optional) | [Install Ollama](https://ollama.com/download) |
| 🖼️ **Stability AI** | `STABILITY_API_KEY` | [Stability AI](https://platform.stability.ai/) |
| 🎥 **Luma** | `LUMA_API_KEY` | [Luma AI](https://lumalabs.ai/) |

</details>

### 3️⃣ CORS
- `CORS_ALLOW_ORIGINS` (comma‑separated) defaults to `*` for local dev.

## 📚 API Overview

- Discovery
  - `GET /v1/health` — service health
  - `GET /v1/capabilities` — list of capability ids and labels
  - `GET /v1/providers` — list of providers
  - `GET /v1/models?capability=&provider=` — capability/provider‑filtered models (from registry)
- Text
  - `POST /v1/text/generate` — JSON body, returns `AIResponse`
  - `GET /v1/text/stream` — SSE stream of tokens
- Images
  - `POST /v1/images/generate` — JSON body
  - `POST /v1/images/edit` — multipart (image + prompt)
- Audio
  - `POST /v1/audio/transcribe` — multipart (audio)
- Documents
  - `POST /v1/documents/qa` — multipart (pdf) or JSON by reference
- Embeddings
  - `POST /v1/embeddings/generate` — JSON (single or batch)

## 🌊 Streaming (SSE)

- Event types: `delta`, `final`, `error` (usage events temporarily removed)
- Message shape (example):

```text
event: delta
data: {"content":"Hello"}

# usage event removed for now

event: final
data: {"content":"Hello world","is_final":true}
```

## 💻 Usage Examples

### Model discovery
```bash
curl "http://localhost:8000/v1/models?capability=image_generation&provider=google"
```

### Text generation
```bash
curl -X POST http://localhost:8000/v1/text/generate \
  -H 'Content-Type: application/json' \
  -d '{"provider":"openai","model":"gpt-4o-mini","prompt":"Write a haiku about the ocean"}'
```

### Streaming (SSE)
```bash
curl -N "http://localhost:8000/v1/text/stream?provider=openai&model=gpt-4o-mini&prompt=Hello"
```

## 🗺️ Roadmap

- [ ] Implement v1 endpoints for all capabilities
- [ ] SSE streaming for text/audio/doc
- [ ] Unified error envelope and usage reporting
- [ ] OpenAPI client generation for `celeste-ui`
- [ ] Auth (optional) and rate limiting

## 🌌 Celeste Ecosystem

| Package | Description | Status |
|---------|-------------|--------|
| 💻 **celeste-ui** | React/Next.js front‑end | 🔄 In Progress |
| 🧠 **celeste-client** | Text generation & chat | ✅ Available |
| 🎨 **celeste-image-generation** | Multi‑provider image gen | ✅ Available |
| ✏️ **celeste-image-edit** | Image editing | ✅ Available |
| 🎧 **celeste-audio-intelligence** | Audio processing | ✅ Available |
| 📄 **celeste-document-intelligence** | PDF/document QA | ✅ Available |
| 🔢 **celeste-embeddings** | Text embeddings | ✅ Available |

## 🤝 Contributing

We welcome contributions! Please see our Contributing Guide.

## 📄 License

This project is licensed under the MIT License - see the `LICENSE` file for details.

---

<div align="center">
  Made with ❤️ by the Celeste Team

  <a href="#-celeste-api">⬆ Back to Top</a>
</div>
