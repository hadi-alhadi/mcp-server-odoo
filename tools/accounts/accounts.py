from typing import Optional, Dict, Any, List
from mcp.server.fastmcp import Context
from odoo_client import get_odoo_client
from logger import info, success, warning, error, debug


def get_accounts(account_type: Optional[str] = None, include_zero_balance: bool = False, limit: int = 100):
    """
    Fetches accounts (account.account) for API endpoint.
    
    Parameters:
    - account_type: Optional filter for specific account types
    - include_zero_balance: Parameter kept for API compatibility but not used
    - limit: Maximum number of records to return (default: 100)
    """
    debug(f"🔍 API endpoint /mcp/odoo/accounts called with type: {account_type}")
    client = get_odoo_client()

    # Initialize domain with no filters
    domain = []

    # Add account_type filter if provided
    if account_type:
        domain.append(["account_type", "=", account_type])

    # Note: We can't filter by balance as it's not a directly accessible field
    # include_zero_balance parameter is kept for API compatibility

    records = client.search_read(
        model="account.account",
        domain=domain,
        fields=["code", "name", "account_type", "company_id", "currency_id", "reconcile"],
        limit=limit
    )
    success(f"✅ Returning {len(records)} accounts")
    return {"records": records}


def get_chart_of_accounts(
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
    debug("🔍 Environment Configuration Check")
    # Get Odoo client directly instead of from context
    odoo = get_odoo_client()
    info("✅ Odoo client initialized")

    # Initialize domain with no filters
    domain = []

    # Add account_type filter if provided
    if account_type:
        domain.append(["account_type", "=", account_type])
        info(f"🔍 Filtering for account type: {account_type}")

    # Note: We can't filter by balance as it's not a directly accessible field

    try:
        debug(f"🔍 Executing chart of accounts search with type: {account_type}")
        results = odoo.search_read(
            model="account.account",
            domain=domain,
            fields=["code", "name", "account_type", "company_id", "currency_id", "reconcile"],
            limit=limit
        )
        success(f"✅ Retrieved {len(results)} accounts")
        return {"success": True, "result": results}
    except Exception as e:
        error(f"❌ Error retrieving chart of accounts: {str(e)}")
        return {"success": False, "error": str(e)}