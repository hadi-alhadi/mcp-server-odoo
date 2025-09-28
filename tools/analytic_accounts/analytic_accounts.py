from typing import Optional, Dict, Any, List
from mcp.server.fastmcp import Context
from odoo_client import get_odoo_client
from logger import info, success, warning, error, debug


def get_analytic_accounts_api(account_type: Optional[str] = None, limit: int = 50):
    """
    Fetches analytic accounts (account.analytic.account) for API endpoint.
    
    Parameters:
    - account_type: Type of analytic account to retrieve
    - limit: Maximum number of records to return (default: 50)
    """
    debug(f"🔍 API endpoint /mcp/odoo/analytic_accounts called with type: {account_type}")
    client = get_odoo_client()

    # Initialize domain with no filters
    domain = []

    # Add account_type filter if provided
    if account_type:
        domain.append(["group_id.name", "ilike", account_type])

    records = client.search_read(
        model="account.analytic.account",
        domain=domain,
        fields=["name", "code", "partner_id", "group_id", "company_id", "active", "balance", "plan_id", "root_plan_id"],
        limit=limit
    )
    success(f"✅ Returning {len(records)} analytic accounts")
    return {"records": records}


def get_analytic_accounts(
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
    debug("🔍 Environment Configuration Check")
    # Get Odoo client directly instead of from context
    odoo = get_odoo_client()
    info("✅ Odoo client initialized")

    # Initialize domain with no filters
    domain = []

    # Add account_type filter if provided
    if account_type:
        domain.append(["group_id.name", "ilike", account_type])
        info(f"🔍 Filtering for analytic account type: {account_type}")

    try:
        debug(f"🔍 Executing analytic accounts search with type: {account_type}")
        results = odoo.search_read(
            model="account.analytic.account",
            domain=domain,
            fields=["name", "code", "partner_id", "group_id", "company_id", "active", "balance", "plan_id", "root_plan_id"],
            limit=limit
        )
        success(f"✅ Retrieved {len(results)} analytic accounts")
        return {"success": True, "result": results}
    except Exception as e:
        error(f"❌ Error retrieving analytic accounts: {str(e)}")
        return {"success": False, "error": str(e)}