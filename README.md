# 🛠️ GitTextLab

**AI-Powered Python Code Analysis and Visualization Tool**

GitTextLab is a sophisticated Python application that analyzes GitHub repositories, providing comprehensive code insights, function analysis, optimization suggestions, and interactive visualizations. Built with Streamlit and powered by local LLM integration, it offers detailed code quality assessments and actionable recommendations for Python projects.

## ✨ Features

### 🔍 **Code Analysis**
- **Automated Repository Scanning**: Recursively analyzes all Python files in any public GitHub repository
- **Function Extraction**: Identifies and extracts all functions with their metadata (line numbers, complexity, arguments)
- **Module Dependencies**: Tracks and visualizes imported modules and libraries
- **Code Quality Assessment**: AI-powered evaluation of code structure and best practices

### 🤖 **AI-Powered Insights**
- **Function Explanations**: Detailed descriptions of what each function does
- **Optimization Suggestions**: AI-generated recommendations for code improvements
- **Error Detection**: Identifies potential bugs, edge cases, and bad practices
- **Project Scoring**: Overall code quality assessment (0-100 scale)

### 📊 **Interactive Visualizations**
- **Function Usage Charts**: Pie charts showing most frequently used function names
- **Module Dependency Graphs**: Visual representation of imported libraries
- **Quality Score Bars**: Color-coded project quality indicators
- **Responsive Design**: Theme-aware interface that adapts to light/dark modes

### 🎨 **Modern UI/UX**
- **Streamlit-Based Interface**: Clean, professional web application
- **Gradient Styling**: Beautiful color schemes with smooth transitions
- **Collapsible Sections**: Organized display of analysis results
- **Real-time Processing**: Live updates during analysis

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- Local LLM server (LM Studio or Ollama) running on `localhost:1234`

### Setup

1. **Clone the repository:**
```bash
git clone https://github.com/eeclk/GitTextLab.git
cd GitTextLab
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up local LLM server:**
   - Install [LM Studio](https://lmstudio.ai/) or [Ollama](https://ollama.ai/)
   - Load a coding-focused model (recommended: CodeLlama, DeepSeek-Coder)
   - Start the server on `localhost:1234`

4. **Run the application:**
```bash
streamlit run main.py
```

## 📦 Dependencies

```python
streamlit>=1.25.0
requests>=2.31.0
matplotlib>=3.7.0
numpy>=1.24.0
astor>=0.8.1
```

## 🎯 Usage

### Basic Analysis

1. **Launch the application:**
   ```bash
   streamlit run main.py
   ```

2. **Enter repository details:**
   - GitHub username (e.g., `microsoft`)
   - Repository name (e.g., `vscode`)

3. **Configure analysis options:**
   - ✅ Function optimization suggestions
   - ✅ Error detection and analysis
   - ✅ Visualization charts

4. **Start analysis** and view results in real-time

### Advanced Features

#### **Optimization Analysis**
Enable optimization suggestions to receive AI-generated code improvements:
```python
# Example output:
# Original function complexity: 15 lines
# Suggested optimization: Use list comprehension instead of loops
# Performance improvement: ~40% faster execution
```

#### **Error Detection**
Activate error checking to identify potential issues:
- Syntax errors and logical flaws
- Missing error handling
- Edge case vulnerabilities
- Performance bottlenecks

#### **Project Scoring**
Get comprehensive quality assessment based on:
- **Code Readability (25%)**: Variable names, comments, docstrings
- **Structure & Organization (20%)**: File organization, function layout
- **Functional Correctness (25%)**: Code functionality, logical flow
- **Error Handling & Security (15%)**: Try-catch blocks, input validation
- **Module Usage & Efficiency (15%)**: Library selection, algorithm efficiency

## 🏗️ Project Structure

```
GitTextLab/
├── main.py                    # Streamlit application entry point
├── analysis/
│   ├── function_analysis.py   # Function extraction and parsing
│   ├── github_analysis.py     # Repository analysis logic
│   ├── shared.py             # LLM integration and utilities
│   └── visualization.py      # Chart generation and plotting
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

### Core Components

#### **main.py**
- Streamlit UI configuration
- User input handling
- Results display and formatting
- Responsive CSS styling

#### **analysis/function_analysis.py**
```python
def extract_functions_code(code):
    """Extracts functions with metadata from Python code"""
    # Returns: name, args, docstring, line numbers, complexity
```

#### **analysis/github_analysis.py**
```python
def analyze_github_repository(username, repo_name, options):
    """Main analysis pipeline for GitHub repositories"""
    # Handles API calls, file processing, and result aggregation
```

#### **analysis/shared.py**
```python
def analyze_function_with_llama(function_code):
    """LLM-powered function analysis and explanation"""
    # Integrates with local LLM server for AI insights
```

#### **analysis/visualization.py**
```python
def create_function_chart(analysis_results):
    """Generates interactive charts for analysis results"""
    # Creates matplotlib visualizations
```

## 🔧 Configuration

### LLM Server Setup

The application expects a local LLM server running on `localhost:1234`. Configure your LLM server with:

```python
# Default configuration in shared.py
ENDPOINT = "http://localhost:1234/v1/chat/completions"
MODEL = "deepseek-coder:6.7b"  # Recommended
TEMPERATURE = 0.2  # For consistent results
```

### Supported Models
- **DeepSeek-Coder**: Best for code analysis
- **CodeLlama**: Good for optimization suggestions
- **GPT-4**: Premium option for advanced insights

## 📈 Output Formats

### JSON Export
Analysis results are automatically saved as JSON:
```json
{
  "source_file": "example.py",
  "file_summary": "AI-generated file overview",
  "functions": [
    {
      "name": "function_name",
      "lineno": 42,
      "length": 15,
      "complexity": 8,
      "explanation": "AI explanation",
      "optimization": "Improvement suggestions",
      "error_check": "Potential issues"
    }
  ]
}
```

### Visual Reports
- **PNG Charts**: Function usage and module dependency graphs
- **Interactive Widgets**: Expandable sections with detailed analysis
- **Progress Indicators**: Real-time analysis progress

## 🎨 Customization

### Styling
Modify the CSS in `main.py` to customize the appearance:
```python
# Theme variables
--bg-gradient-start: #667eea
--bg-gradient-end: #764ba2
--text-primary: #212529
```

### Analysis Options
Extend functionality by modifying analysis parameters:
```python
# In github_analysis.py
functions = extract_functions_code(code)
for func in functions[:10]:  # Analyze first 10 functions
    # Add custom analysis logic here
```

## 🔒 Security & Privacy

- **No Data Storage**: Analysis results are only stored locally
- **Public Repositories Only**: Only analyzes publicly accessible GitHub repositories
- **Local LLM**: All AI processing happens on your machine
- **No API Keys**: No external AI service dependencies

## 🐛 Troubleshooting

### Common Issues

**LLM Connection Error:**
```bash
❌ LLM Hatası: Connection refused
```
**Solution:** Ensure your local LLM server is running on `localhost:1234`

**Repository Not Found:**
```bash
Bu repository'de Python dosyası bulunamadı!
```
**Solution:** Verify the repository exists and contains Python files

**Analysis Timeout:**
```bash
Fonksiyon analiz hatası: timeout
```
**Solution:** Large repositories may take time; consider analyzing smaller projects first

### Performance Tips

1. **Start with smaller repositories** (< 50 files)
2. **Use faster LLM models** for quicker analysis
3. **Disable optimization/error checking** for basic analysis
4. **Close other applications** to free up system resources

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Submit a pull request with a clear description

### Development Setup
```bash
# Install development dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/

# Format code
black . --line-length 88
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Streamlit** for the excellent web framework
- **AST Module** for Python code parsing
- **Matplotlib** for visualization capabilities
- **Local LLM Community** for making AI accessible

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/eeclk/GitTextLab/issues)
- **Discussions**: [GitHub Discussions](https://github.com/eeclk/GitTextLab/discussions)
- **Email**: [Contact the author](mailto:ee.clk61l@gmail.com)

---

<div align="center">

**⭐ Star this repository if GitTextLab helped you analyze your code!**

Made with ❤️ by [eeclk](https://github.com/eeclk)

</div>
