import json
import sys
from mcp.server.fastmcp import Context
from typing import Optional, Dict, Any, List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from mcp.server.fastmcp import FastMCP

from odoo_client import get_odoo_client
from logger import info, success, warning, error, debug, divider
from tools import (
    get_accounts, get_chart_of_accounts,
    get_invoices_api, get_invoices,
    get_journals_api, get_journals,
    get_partners_api, get_partners,
    get_account_moves, get_recent_journal_entries
)


mcp = FastMCP(
    "Odoo MCP Server",
)
info("🎯 Odoo Accounting MCP Server initialized")


app = FastAPI(title="Odoo Accounting MCP Server")

# CORS (Claude Desktop needs this)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # loosen for local dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
info("🌐 FastAPI app configured with CORS middleware")


@app.get("/mcp/odoo/accounting")
def get_account_moves_endpoint():
    return get_account_moves()


@app.get("/mcp/odoo/invoices")
def get_invoices_endpoint(invoice_type: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None, limit: int = 20):
    return get_invoices_api(invoice_type, start_date, end_date, limit)


@app.get("/mcp/odoo/accounts")
def get_accounts_endpoint(account_type: Optional[str] = None, include_zero_balance: bool = False, limit: int = 100):
    return get_accounts(account_type, include_zero_balance, limit)


@app.get("/mcp/odoo/partners")
def get_partners_endpoint(partner_type: Optional[str] = None, limit: int = 50):
    return get_partners_api(partner_type, limit)


@app.get("/mcp/odoo/journals")
def get_journals_endpoint(journal_type: Optional[str] = None, limit: int = 20):
    return get_journals_api(journal_type, limit)


@app.get("/mcp/odoo/analytic_accounts")
def get_analytic_accounts_endpoint(account_type: Optional[str] = None, limit: int = 50):
    return get_analytic_accounts_api(account_type, limit)



@mcp.tool(description="🎯 Get recent journal entries for AI audit")
def get_recent_journal_entries_wrapper(
    ctx: Context,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    limit: int = 20
) -> Dict[str, Any]:
    """
    Fetches recent journal entries (account.move) for AI analysis.
    Allows optional filtering by date.
    """
    return get_recent_journal_entries(ctx, start_date, end_date, limit)


@mcp.tool(description="📄 Get invoices and bills for AI analysis")
def get_invoices_wrapper(
    ctx: Context,
    invoice_type: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    limit: int = 20
) -> Dict[str, Any]:
    """
    Fetches invoices and bills (account.move) for AI analysis.

    Parameters:
    - invoice_type: Type of invoice to retrieve. Options:
      - "customer_invoices" for Customer Invoices (move_type = 'out_invoice')
      - "vendor_bills" for Vendor Bills (move_type = 'in_invoice')
      - "credit_notes" for Credit Notes (move_type = 'out_refund' or 'in_refund')
      - If not specified, returns all types
    - start_date: Optional start date filter (format: YYYY-MM-DD)
    - end_date: Optional end date filter (format: YYYY-MM-DD)
    - limit: Maximum number of records to return (default: 20)
    """
    return get_invoices(ctx, invoice_type, start_date, end_date, limit)


@mcp.tool(description="📊 Get chart of accounts for AI analysis")
def get_chart_of_accounts_wrapper(
    ctx: Context,
    account_type: Optional[str] = None,
    include_zero_balance: bool = False,
    limit: int = 100
) -> Dict[str, Any]:
    """
    Fetches chart of accounts (account.account) for AI analysis.

    Parameters:
    - account_type: Optional filter for specific account types. Common types include:
      - "asset_receivable" for Receivable Accounts
      - "asset_cash" for Bank & Cash Accounts
      - "asset_current" for Current Assets
      - "asset_non_current" for Non-current Assets
      - "liability_payable" for Payable Accounts
      - "liability_current" for Current Liabilities
      - "equity" for Equity Accounts
      - "income" for Income Accounts
      - "expense" for Expense Accounts
      - If not specified, returns all account types
    - include_zero_balance: Parameter kept for API compatibility but not used (balance field not available)
    - limit: Maximum number of records to return (default: 100)
    """
    return get_chart_of_accounts(ctx, account_type, include_zero_balance, limit)


@mcp.tool(description="👥 Get partners for AI analysis")
def get_partners_wrapper(
    ctx: Context,
    partner_type: Optional[str] = None,
    limit: int = 50
) -> Dict[str, Any]:
    """
    Fetches partners (res.partner) for AI analysis.

    Parameters:
    - partner_type: Type of partners to retrieve. Options:
      - "customer" for Customers (customer_rank > 0)
      - "vendor" for Vendors (supplier_rank > 0)
      - If not specified, returns all partners
    - limit: Maximum number of records to return (default: 50)
    """
    return get_partners(ctx, partner_type, limit)


@mcp.tool(description="📒 Get journals for AI analysis")
def get_journals_wrapper(
    ctx: Context,
    journal_type: Optional[str] = None,
    limit: int = 20
) -> Dict[str, Any]:
    """
    Fetches journals (account.journal) for AI analysis.

    Parameters:
    - journal_type: Type of journal to retrieve. Common types include:
      - "sale" for Sales Journals
      - "purchase" for Purchase Journals
      - "cash" for Cash Journals
      - "bank" for Bank Journals
      - "general" for Miscellaneous Operations Journals
      - If not specified, returns all journal types
    - limit: Maximum number of records to return (default: 20)
    """
    return get_journals(ctx, journal_type, limit)


@mcp.tool(description="📊 Get analytic accounts for AI analysis")
def get_analytic_accounts_wrapper(
    ctx: Context,
    account_type: Optional[str] = None,
    limit: int = 50
) -> Dict[str, Any]:
    """
    Fetches analytic accounts (account.analytic.account) for AI analysis.

    Parameters:
    - account_type: Type of analytic account to retrieve. This can be used to filter by:
      - Project names
      - Cost centers
      - Department names
      - Any other grouping used in your Odoo instance
      - If not specified, returns all analytic accounts
    - limit: Maximum number of records to return (default: 50)
    """
    return get_analytic_accounts(ctx, account_type, limit)


def main():
    divider()
    info("🚀 Starting Odoo MCP FastAPI server...")
    divider()
    uvicorn.run(app, host="0.0.0.0", port=8002)
