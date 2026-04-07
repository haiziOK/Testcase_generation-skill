# Test Case Generation Skill

A Claude Code skill that generates Excel test cases from design documents, existing test case graphs, and test experience summary graphs.

## Features

- **Document Processing**: Parses design documents in TXT, PDF, and DOCX formats
- **LLM-Powered Generation**: Uses local Ollama or OpenAI to generate comprehensive test cases
- **Excel Output**: Creates professionally formatted Excel files with test cases
- **Interactive Prompts**: Guides users through the generation process
- **Extensible Architecture**: Modular design for easy extension

## MVP Status

Currently implements basic functionality:
- ✅ Text document parsing (.txt files)
- ✅ LLM integration with Ollama
- ✅ Excel test case generation
- ✅ Interactive command-line interface
- ✅ Skill structure and documentation

## Prerequisites

1. **Python 3.9+**
2. **Ollama** (optional, for local LLM)
   - Install from [ollama.com](https://ollama.com)
   - Pull a model: `ollama pull gemma3:4b` (or any other model)

## Installation

### Option 1: Use as standalone Python tool

1. Clone or copy this directory
2. Create virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Option 2: Install as Claude Code skill (manual)

1. Copy the entire `Testcase_generation` directory to your Claude Code skills folder:
   - Windows: `%USERPROFILE%\.claude\plugins\cache\anthropic-agent-skills\document-skills\b0cbd3df1533\skills\`
   - Or consult Claude Code documentation for skill installation

2. Restart Claude Code

## Usage

### As a standalone tool

```bash
# Generate test cases from a design document
python scripts/main.py --document examples/sample_design.txt --output test_cases.xlsx

# Interactive mode
python scripts/main.py --interactive

# With custom parameters
python scripts/main.py --document design.txt --output output.xlsx --max-cases 10
```

### As a Claude Code skill

Once installed, invoke via:
- `Skill("Testcase_generation")` in Claude Code
- Follow interactive prompts

## Configuration

### LLM Settings

By default, the skill uses Ollama with `gemma3:4b` model. To change:

1. Edit `scripts/llm_client.py`:
   ```python
   class LLMClient:
       def __init__(self, base_url: str = "http://localhost:11434", model: str = "your-model"):
   ```

2. Or set environment variables (future enhancement)

### Document Parsing

Supported formats:
- `.txt` - plain text (fully implemented)
- `.pdf` - PDF documents (stub implementation)
- `.docx` - Word documents (stub implementation)

## Project Structure

```
Testcase_generation/
├── SKILL.md                    # Skill definition
├── LICENSE.txt                 # MIT License
├── README.md                   # This file
├── requirements.txt            # Python dependencies
├── scripts/                    # Core implementation
│   ├── __init__.py
│   ├── main.py                 # CLI entry point
│   ├── document_parser.py      # Document parsing
│   ├── llm_client.py          # LLM integration
│   ├── testcase_generator.py   # Test case generation
│   └── excel_writer.py        # Excel file creation
├── examples/                   # Sample files
│   ├── sample_design.txt
│   └── test_cases.xlsx        # Generated example
└── tests/                      # Test suite (future)
```

## Development

### Adding New Features

1. **PDF/DOCX Support**: Implement parsing in `document_parser.py`
2. **Graph Integration**: Add graph processing modules
3. **Additional LLM Providers**: Extend `llm_client.py`
4. **Enhanced Excel Formatting**: Improve `excel_writer.py`

### Running Tests

```bash
# Install test dependencies
pip install pytest

# Run tests
pytest tests/
```

## Limitations

- **MVP Only**: Currently supports only text documents
- **LLM Dependency**: Requires Ollama or similar LLM service
- **Graph Support**: Not yet implemented (planned for Phase 3)
- **Error Handling**: Basic error handling implemented

## Future Enhancements

1. **Phase 2**: PDF and DOCX document support
2. **Phase 3**: JSON/GraphML graph integration
3. **Phase 4**: Test experience learning and optimization
4. **Phase 5**: API exposure and CI/CD integration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Implement changes
4. Add tests
5. Submit pull request

## License

MIT License - see LICENSE.txt for details.

## Acknowledgments

- Built with inspiration from Anthropic's document skills
- Uses Ollama for local LLM inference
- Leverages openpyxl for Excel file creation