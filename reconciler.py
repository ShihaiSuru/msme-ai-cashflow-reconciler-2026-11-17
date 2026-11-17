#!/usr/bin/env python3
"""
MSME AI Cash-Flow Reconciler - Starter Demo
============================================

Practical prototype for Indian MSMEs:
- Matches UPI / bank transactions against invoices
- Flags unreconciled items
- Estimates short-term working capital needs
- Highlights potential GST-related mismatches

Uses only the Python standard library.
Sample data is included so the script runs immediately.

Usage:
    python reconciler.py
"""

from datetime import datetime, timedelta
from collections import defaultdict
import json

# ---------------------------------------------------------------------------
# Sample data (typical small Indian retail / wholesale MSME)
# ---------------------------------------------------------------------------

# UPI / bank credit transactions (inflows)
upi_transactions = [
    {"id": "UPI001", "date": "2026-11-10", "amount": 25000.00, "narration": "UPI/NEFT from Sharma Traders INV-1042", "type": "credit"},
    {"id": "UPI002", "date": "2026-11-12", "amount": 18500.00, "narration": "PhonePe payment from customer", "type": "credit"},
    {"id": "UPI003", "date": "2026-11-13", "amount": 42000.00, "narration": "RTGS from Gupta Enterprises", "type": "credit"},
    {"id": "UPI004", "date": "2026-11-15", "amount": 9800.00, "narration": "UPI payment received", "type": "credit"},
    {"id": "UPI005", "date": "2026-11-16", "amount": 31000.00, "narration": "NEFT from Patel & Sons against INV-1055", "type": "credit"},
]

# Outstanding / recent invoices (receivables)
invoices = [
    {"invoice_no": "INV-1042", "date": "2026-11-08", "customer": "Sharma Traders", "amount": 25000.00, "gst_amount": 4500.00, "status": "sent"},
    {"invoice_no": "INV-1048", "date": "2026-11-09", "customer": "Local Customer", "amount": 18500.00, "gst_amount": 3330.00, "status": "sent"},
    {"invoice_no": "INV-1051", "date": "2026-11-11", "customer": "Gupta Enterprises", "amount": 42000.00, "gst_amount": 7560.00, "status": "sent"},
    {"invoice_no": "INV-1055", "date": "2026-11-14", "customer": "Patel & Sons", "amount": 31000.00, "gst_amount": 5580.00, "status": "sent"},
    {"invoice_no": "INV-1058", "date": "2026-11-15", "customer": "Mehta Stores", "amount": 15750.00, "gst_amount": 2835.00, "status": "sent"},  # still open
]

# Simple payables sample (for working capital calc)
payables = [
    {"supplier": "Raw Material Supplier", "due_date": "2026-11-20", "amount": 18000.00},
    {"supplier": "Logistics Partner", "due_date": "2026-11-25", "amount": 6500.00},
]

# ---------------------------------------------------------------------------
# Matching logic
# ---------------------------------------------------------------------------

def parse_date(d):
    return datetime.strptime(d, "%Y-%m-%d")

def match_transactions(transactions, invoices, date_window_days=5):
    """
    Rule-based matching:
    1. Exact amount match + invoice number in narration (highest confidence)
    2. Exact amount + date proximity
    3. Approximate amount (within 1%) + date proximity (lower confidence)
    """
    matched = []
    unmatched_tx = []
    unmatched_inv = list(invoices)  # start with all invoices unmatched

    for tx in transactions:
        if tx["type"] != "credit":
            continue

        best_match = None
        best_score = 0
        tx_date = parse_date(tx["date"])

        for inv in unmatched_inv:
            inv_date = parse_date(inv["date"])
            date_diff = abs((tx_date - inv_date).days)

            # Score based on rules
            score = 0
            reason = []

            # Exact amount
            if abs(tx["amount"] - inv["amount"]) < 1.0:
                score += 50
                reason.append("exact amount")

            # Invoice number in narration
            if inv["invoice_no"].lower() in tx["narration"].lower():
                score += 40
                reason.append("invoice ref in narration")

            # Date proximity
            if date_diff <= date_window_days:
                score += 20 - (date_diff * 2)
                reason.append(f"date within {date_diff}d")

            # Customer name partial match
            if any(word.lower() in tx["narration"].lower() for word in inv["customer"].split()):
                score += 10
                reason.append("customer name hint")

            if score > best_score and score >= 50:  # minimum threshold
                best_score = score
                best_match = (inv, score, ", ".join(reason))

        if best_match:
            inv, score, reason = best_match
            matched.append({
                "transaction": tx,
                "invoice": inv,
                "confidence": score,
                "reason": reason,
            })
            unmatched_inv.remove(inv)
        else:
            unmatched_tx.append(tx)

    return matched, unmatched_tx, unmatched_inv

def estimate_working_capital(unmatched_invoices, payables, days_ahead=30):
    """
    Simple working capital estimate:
    - Expected inflows from open invoices (assume 70% collection within window)
    - Known payables due in the window
    - Net cash gap
    """
    today = datetime(2026, 11, 17)
    horizon = today + timedelta(days=days_ahead)

    expected_inflows = sum(inv["amount"] for inv in unmatched_invoices) * 0.70
    expected_outflows = sum(
        p["amount"] for p in payables
        if parse_date(p["due_date"]) <= horizon
    )

    net_gap = expected_outflows - expected_inflows
    return {
        "expected_inflows_30d": round(expected_inflows, 2),
        "expected_outflows_30d": round(expected_outflows, 2),
        "estimated_cash_gap": round(max(net_gap, 0), 2),
        "notes": "Assumes 70% collection rate on open invoices. Adjust based on historical data."
    }

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 70)
    print("MSME AI Cash-Flow Reconciler  |  Demo Run")
    print("Date: 2026-11-17  |  Sample Indian MSME data")
    print("=" * 70)

    matched, unmatched_tx, unmatched_inv = match_transactions(upi_transactions, invoices)

    print(f"\n✅ Matched transactions: {len(matched)}")
    print("-" * 70)
    for m in matched:
        print(f"  {m['transaction']['id']}  →  {m['invoice']['invoice_no']}  "
              f"(₹{m['invoice']['amount']:,.0f})  [conf: {m['confidence']}]  {m['reason']}")

    print(f"\n⚠️  Unmatched UPI credits: {len(unmatched_tx)}")
    for tx in unmatched_tx:
        print(f"  {tx['id']}  ₹{tx['amount']:,.0f}  {tx['date']}  |  {tx['narration'][:50]}")

    print(f"\n⚠️  Open / unmatched invoices: {len(unmatched_inv)}")
    for inv in unmatched_inv:
        print(f"  {inv['invoice_no']}  ₹{inv['amount']:,.0f}  {inv['customer']}  (GST: ₹{inv['gst_amount']:,.0f})")

    # Working capital estimate
    wc = estimate_working_capital(unmatched_inv, payables)
    print("\n" + "=" * 70)
    print("WORKING CAPITAL ESTIMATE (next 30 days)")
    print("=" * 70)
    print(f"  Expected inflows (70% of open invoices):  ₹{wc['expected_inflows_30d']:,.0f}")
    print(f"  Expected outflows (due payables):          ₹{wc['expected_outflows_30d']:,.0f}")
    print(f"  Estimated cash gap to cover:              ₹{wc['estimated_cash_gap']:,.0f}")
    print(f"  Note: {wc['notes']}")

    print("\n" + "=" * 70)
    print("Next steps for production use:")
    print("  • Import real bank/UPI CSV exports")
    print("  • Pull invoice data from your accounting tool")
    print("  • Add GST rate / HSN validation")
    print("  • Replace rules with ML or LLM-based matching")
    print("=" * 70)

if __name__ == "__main__":
    main()
