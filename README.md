# MSME AI Cash-Flow Reconciler

**AI-powered cash-flow reconciliation tool for Indian MSMEs.**

Matches UPI transactions with invoices and GST data to detect mismatches, estimate working capital needs, and provide actionable cash-flow insights.

## The Problem

Indian MSMEs (Micro, Small, and Medium Enterprises) often struggle with fragmented financial data:

- UPI payments arrive in bank accounts without clear references
- Invoices are tracked in spreadsheets or simple tools
- GST filings require accurate reconciliation of taxable supplies
- Cash-flow visibility is poor, leading to delayed payments, working capital shortages, and compliance risks

Manual matching is time-consuming and error-prone, especially with high transaction volumes.

## The Solution

This tool provides a practical starting point for an AI-assisted cash-flow system:

1. **Ingest** sample or real UPI transaction data, invoice records, and GST summaries
2. **Match** transactions to invoices using amount, date proximity, and reference patterns
3. **Flag** mismatches, unreconciled items, and potential GST discrepancies
4. **Estimate** short-term working capital needs based on outstanding receivables and payables
5. **Surface** simple insights (e.g., average collection period, cash gap)

The current implementation is a lightweight Python prototype using rule-based matching + basic heuristics (easily extensible with ML models for better matching).

## Usage

### Prerequisites
- Python 3.9+
- No external dependencies for the starter script (uses only the standard library)

### Run the demo
```bash
python reconciler.py
```

The script includes sample data representing a typical small Indian business (retail/wholesale MSME). It will:
- Load sample UPI transactions and invoices
- Perform matching
- Print a reconciliation report
- Estimate working capital requirements

### Extending the tool
- Replace sample data with CSV/Excel exports from your bank, UPI app, or accounting software
- Integrate GST portal data or GSTR-1/3B summaries
- Add fuzzy matching, NLP on narration fields, or an LLM layer for smarter classification
- Connect to real bank APIs (where available) or accounting systems

## Why this matters for Indian MSMEs

- **Cash-flow visibility**: Know exactly what is matched vs. outstanding
- **Faster collections**: Identify unpaid invoices linked to received UPI payments
- **GST readiness**: Reduce errors before filing
- **Working capital planning**: Simple estimate of funds needed in the next 15–30 days
- **Founder-friendly**: Lightweight, open, and easy to customize

## Roadmap (ideas)
- CSV/Excel import/export
- GST invoice matching (HSN, tax rates)
- Simple dashboard (Streamlit or Gradio)
- Integration with popular Indian accounting tools
- AI model for narration-based matching

## License
MIT — feel free to use, modify, and build upon this for real MSME fintech products.

---

Built as a practical demo of AI cash-flow systems for Indian MSMEs.
