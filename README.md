# Teclusion

A collection of Python scripts demonstrating various OpenAI API capabilities including natural language processing, image analysis, audio transcription, and structured data extraction.

## Features

- **Chat Interface**: Interactive chat with conversation history
- **Image Processing**: Capture, analyze, and generate images
- **Audio Transcription**: Convert audio files to text
- **Structured Data Extraction**: Parse natural language into structured JSON
- **Home Automation**: JSON parser for home automation commands

## Setup

### Prerequisites

- Python 3.12 or higher
- [uv](https://docs.astral.sh/uv/) package manager

### Installation

1. **Install uv** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd teclusion
   ```

3. **Install dependencies**:
   ```bash
   uv sync
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```
   
   Edit the `.env` file and replace the placeholder values with your actual API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Usage

Run any script using uv:

```bash
uv run <script_name>.py
```

## Scripts

### 🤖 Chat & Conversation

#### `main.py`
Interactive chat interface with conversation persistence.
- **Features**: Load existing chats, save chat history, currency conversion parsing
- **Usage**: `uv run main.py`
- **Functionality**: Creates a conversational interface that can parse natural language into currency conversion JSON

#### `recap.py`
Home automation command parser with continuous interaction.
- **Features**: JSON schema validation, home automation equipment control
- **Usage**: `uv run recap.py`
- **Functionality**: Parses natural language commands into structured JSON for controlling home devices (lights, AC, fans, water motor)

### 🎯 Structured Data Extraction

#### `structured-currency.py`
Single-use currency conversion parser.
- **Features**: Converts natural language to currency conversion JSON
- **Usage**: `uv run structured-currency.py`
- **Schema**: `from` (currency code), `to` (currency code), `amount` (number)

#### `structured-hotel-menu.py`
Restaurant menu parser from text files.
- **Features**: Extracts restaurant information and dishes from menu text
- **Usage**: `uv run structured-hotel-menu.py`
- **Input**: Reads from `inputs/menu.txt`
- **Schema**: Restaurant name, dishes with prices, categories, and ingredients

#### `structured-visiting-card.py`
Business card information extractor from images.
- **Features**: OCR and structured extraction from business card images
- **Usage**: `uv run structured-visiting-card.py`
- **Schema**: Name, phone, email, company, address, position, qualification

#### `structured-event.py`
Event information parser from images.
- **Features**: Extracts event details including speakers from event flyers/images
- **Usage**: `uv run structured-event.py`
- **Schema**: Title, subtitle, company, address, date, time, speakers array

### 📸 Image Processing

#### `capture-img.py`
Real-time image capture and analysis.
- **Features**: Webcam capture, base64 encoding, image analysis
- **Usage**: `uv run capture-img.py`
- **Functionality**: Captures image from webcam and analyzes visiting cards

#### `gen-image.py`
AI image generation.
- **Features**: Generate images from text prompts
- **Usage**: `uv run gen-image.py`
- **Output**: Saves generated images to `generated/` directory

#### `image.py`
Image analysis from uploaded files.
- **Features**: Analyze pre-uploaded images using file IDs
- **Usage**: `uv run image.py`
- **Functionality**: Analyzes books and other content from images

### 🎵 Audio Processing

#### `transcription.py`
Audio file transcription.
- **Features**: Convert audio files to text
- **Usage**: `uv run transcription.py`
- **Input**: Reads from `inputs/sample.m4a`
- **Functionality**: Transcribes audio content to text

## Project Structure

```
teclusion/
├── captured/          # Webcam captured images
├── chats/            # Saved chat conversations (JSON)
├── generated/        # AI-generated images
├── images/           # Image assets
├── inputs/           # Input files (audio, text)
├── main.py           # Main chat interface
├── capture-img.py    # Image capture and analysis
├── gen-image.py      # Image generation
├── image.py          # Image analysis
├── recap.py          # Home automation parser
├── structured-*.py   # Structured data extractors
├── transcription.py  # Audio transcription
├── .env.example      # Environment variables template
└── pyproject.toml    # Project dependencies
```

## Dependencies

- **openai**: OpenAI API client
- **opencv-python**: Computer vision and image processing
- **python-dotenv**: Environment variable management
- **pandas**: Data manipulation (if needed)
- **requests**: HTTP client for API calls

## API Models Used

- **gpt-4o**: Main conversation and analysis model
- **gpt-4.1-mini**: Lightweight model for specific tasks
- **gpt-4.1-nano**: Ultra-lightweight model for simple parsing
- **gpt-image-1**: Image generation model
- **gpt-4o-mini-transcribe**: Audio transcription model

## Notes

- All scripts require a valid OpenAI API key
- Image processing scripts may require camera permissions
- Audio transcription requires compatible audio file formats
- Generated content is saved to respective directories
- Chat histories are persisted as JSON files

## Contributing

Feel free to contribute by adding new scripts or improving existing functionality. Each script demonstrates different aspects of the OpenAI API capabilities.