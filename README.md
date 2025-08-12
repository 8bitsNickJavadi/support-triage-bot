# Customer Support Triage Bot

A multi-step graph-based customer support system with human-in-the-loop approval using LangGraph, OpenAI, and FAISS vector search.

## Features

- **Automated Ticket Classification**: LLM-powered categorization into billing, account, technical, or other
- **Customer Enrichment**: CRM lookup by email/name from CSV database
- **FAQ Retrieval**: Vector-based search through knowledge base documents
- **Draft Generation**: Context-aware reply drafting using customer data and FAQ passages
- **Human Approval Loop**: Review and revision workflow with feedback incorporation
- **Multi-format Knowledge Base**: Supports both PDF and Markdown FAQ documents

## Project Structure

```
support-triage-bot/
├── data/
│   ├── customers.csv          # CRM-like customer database
│   └── faq.md                 # Knowledge base (FAQ)
├── nodes/
│   ├── ingest_faq_node.py     # Build/load vector index from KB
│   ├── classify_node.py       # LLM ticket categorization
│   ├── enrich_node.py         # CRM lookup by name/email
│   ├── retrieve_node.py       # Top-k FAQ chunk retrieval
│   ├── draft_node.py          # LLM draft reply generation
│   ├── approval_node.py       # Human approval checkpoint
│   └── revise_node.py         # Incorporate reviewer feedback
├── graph.py                   # LangGraph workflow orchestration
├── run_cli.py                 # CLI interface for approval loop
├── environment.yaml           # Conda environment specification
├── .env                       # Environment variables (API keys)
└── README.md                  # This file
```

## Setup Instructions

### 1. Environment Setup

Create and activate the conda environment:

```bash
conda env create -f environment.yaml
conda activate support-triage-bot
```

### 2. API Keys

Edit the `.env` file and add your OpenAI API key:

```bash
OPENAI_API_KEY=sk-your-actual-openai-api-key-here
LANGCHAIN_TRACING_V2=true
```

### 3. Knowledge Base

The project includes a sample FAQ in `data/faq.md`. You can:
- Replace it with your own FAQ content
- Add PDF files to the `data/` directory
- The system will automatically index all `.md` and `.pdf` files

### 4. Customer Database

Update `data/customers.csv` with your customer information. The format is:
```csv
customer_id,name,email,tier,balance,product
1,Jane Smith,jane@example.com,Gold,120,Pro
```

## Usage

Run the interactive CLI:

```bash
python run_cli.py
```

### Workflow

1. **Enter Ticket Information**: Provide ticket text, customer name (optional), and email (optional)
2. **Automatic Processing**: The system will:
   - Classify the ticket category
   - Look up customer information
   - Retrieve relevant FAQ passages
   - Generate a draft reply
3. **Human Review**: Review the draft and either:
   - Approve it (y)
   - Request changes with feedback (n)
   - Quit the approval loop (q)
4. **Revision Loop**: If changes are requested, the system will revise the draft based on your feedback
5. **Finalization**: Once approved, the final reply is displayed

### Sample Interaction

```
=== New Ticket ===
Enter a new support ticket:
Ticket text: I can't log into my account and need help resetting my password
Customer name (optional): Jane Smith
Customer email (optional): jane@example.com

--- DRAFT REPLY ---
Hello Jane,

I understand you're having trouble logging into your account. As a Gold tier customer, I'm happy to help you reset your password quickly.

Here are the steps to reset your password:
1. Go to the login page and click "Forgot Password"
2. Enter your email address (jane@example.com)
3. Check your email for a reset link
4. Follow the instructions in the email
5. Create a new strong password

The reset process should take just a few minutes. If you don't receive the reset email within 5 minutes, please check your spam folder.

Thank you for being a valued Gold customer. Let me know if you need any further assistance!

Best regards,
Customer Support Team

Approve draft? (y = approve / n = request changes / q = quit): y

=== Finalized Reply ===
[Final reply displayed]
```

## System Architecture

### Graph Flow

```
User ticket → Classify → Enrich (CRM) → Retrieve FAQ → Draft reply → Human approval
                                                                           ↓
                                                              Reviewer feedback → Revise
```

### Node Functions

- **ingest_faq_node**: Builds FAISS vector index from knowledge base files
- **classify_node**: Categorizes tickets using GPT-3.5-turbo
- **enrich_node**: Looks up customer data from CSV by email/name matching
- **retrieve_node**: Finds relevant FAQ passages using vector similarity
- **draft_node**: Generates contextual reply using customer tier and FAQ info
- **approval_node**: Pauses workflow for human review
- **revise_node**: Incorporates feedback and regenerates reply

### Key Features

- **Conditional Routing**: Approval decisions route to either completion or revision
- **Revision Limits**: Maximum 3 revisions per ticket to prevent infinite loops
- **Customer Tier Awareness**: Replies are customized based on customer subscription level
- **Vector Caching**: FAQ index is built once and reused for performance
- **Graceful Fallbacks**: Handles missing customer data and empty FAQ results

## Customization

### Adding New Categories

Edit `nodes/classify_node.py` to add new ticket categories:

```python
if label not in {"billing","account","technical","support","other"}:
    label = "other"
```

### Modifying Prompts

Update the prompt templates in `draft_node.py` and `revise_node.py` to change the tone or structure of generated replies.

### Extending Customer Data

Add new columns to `customers.csv` and reference them in the draft generation prompt for more personalized responses.

## Troubleshooting

### Common Issues

1. **Missing API Key**: Ensure your OpenAI API key is set in `.env`
2. **Import Errors**: Verify all dependencies are installed with `conda list`
3. **Empty FAQ Index**: Check that files exist in `data/` directory
4. **Customer Lookup Fails**: Verify email/name matching in CSV file

### Debug Mode

Enable LangChain tracing by setting `LANGCHAIN_TRACING_V2=true` in your `.env` file to see detailed execution logs.

## Learning Objectives

This project demonstrates:

- **LangGraph Orchestration**: Multi-step workflow with conditional edges
- **Vector Retrieval**: FAISS-based semantic search over documents
- **Human-in-the-Loop**: Interactive approval and revision workflows
- **State Management**: Persistent state across graph execution steps
- **CRM Integration**: Simple database lookup and enrichment
- **Prompt Engineering**: Context-aware LLM response generation

## Next Steps

Consider extending the project with:

- Web interface instead of CLI
- Database integration (PostgreSQL/MongoDB)
- Email integration for automatic ticket ingestion
- Analytics dashboard for ticket trends
- Multi-language support
- Sentiment analysis for ticket prioritization
