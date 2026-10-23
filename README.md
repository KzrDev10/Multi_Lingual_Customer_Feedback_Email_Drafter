# Customer Support System using LangChain
 
A small Python script that triages multilingual customer feedback with **LangChain** and **Google Gemini**. It detects the language, classifies sentiment, flags whether the customer needs a follow-up, summarizes the message in English, and, when follow-up is needed, drafts a polite reply in the customer's own language.
 
## Features
 
- **Language detection**: identifies the language of the incoming feedback
- **Sentiment analysis**: classifies feedback as `Positive`, `Negative`, or `Neutral`
- **Follow-up flag**: decides whether the feedback requires a response
- **English summary**: gives support staff a quick summary regardless of the original language
- **Auto-drafted apology**: generates a reply in the customer's native language when follow-up is required
- **Typed output**: uses a Pydantic schema with Gemini structured output, so results are predictable and easy to use downstream
## How it works
 
```
feedback text ──► prompt ──► Gemini (structured output) ──► FeedbackAnalysis
                                                              │
                                      requires_followup? ─────┤
                                           yes ──► Gemini drafts apology in the customer's language
                                           no  ──► "No action needed"
```
 
The structured result follows this schema:
 
| Field | Type | Description |
|---|---|---|
| `language` | `str` | Detected language of the feedback |
| `sentiment` | `"Positive" \| "Negative" \| "Neutral"` | Overall sentiment |
| `requires_followup` | `bool` | Whether the customer needs a reply |
| `english_summary` | `str` | English summary of the feedback |
 
## Getting started
 
### Prerequisites
 
- Python 3.10+
- A Google Gemini API key from [Google AI Studio](https://aistudio.google.com/)
### Installation
 
```bash
git clone https://github.com/KzrDev10/Customer_support_system_using_langchain.git
cd Customer_support_system_using_langchain
 
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
 
pip install langchain-google-genai langchain-core pydantic python-dotenv
```
 
### Configuration
 
Create a `.env` file in the project root:
 
```env
API_KEY=your_gemini_api_key_here
```
 
> Keep `.env` out of version control by adding it to `.gitignore`.
 
### Usage
 
```bash
python main.py
```
 
Example output for a feedback that needs follow-up:
 
```
Summary:
email_summary: Customer reports being charged $50 again after cancelling their subscription and requests an immediate refund.
Language: Japanese
Sentiment: Negative
Followup ?:  True
<polite apology drafted in Japanese>
```
 
For positive feedback with no action required:
 
```
Followup ?:  False
No action needed
```
 
### Trying other feedback
 
`main.py` includes sample messages in Spanish, French, Dutch, Japanese, German, and Portuguese (`test_esp`, `test_fra`, `test_dut`, `test_jap`, `test_ger`, `test_por`). To test a different one, replace `test_por` with another variable in the two places where it is passed to `invoke(...)`. Or add your own message and use it the same way.
 
## Project structure
 
```
.
├── main.py             # Analysis chain, structured output, and reply generation
├── requirements.txt    # Python dependencies
└── .env                # Your API key (not committed)
```
 
## Tech stack
 
- [LangChain](https://python.langchain.com/) (prompt templates, chains, output parsers)
- [langchain-google-genai](https://pypi.org/project/langchain-google-genai/) (Gemini integration)
- [Pydantic](https://docs.pydantic.dev/) (structured output schema)
- [python-dotenv](https://pypi.org/project/python-dotenv/) (environment variables)
## Getting help
 
Found a bug or have a question? Open an [issue](https://github.com/KzrDev10/Customer_support_system_using_langchain/issues).
 
## Maintainer
 
Maintained by [@KzrDev10](https://github.com/KzrDev10). Contributions are welcome: fork the repo, create a branch, and open a pull request.
 
## License
 
No license has been specified yet. Add a `LICENSE` file to define how others may use this project.
 
Claude finished the response
