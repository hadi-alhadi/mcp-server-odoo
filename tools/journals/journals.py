from typing import Optional, Dict, Any, List
from mcp.server.fastmcp import Context
from odoo_client import get_odoo_client
from logger import info, success, warning, error, debug


def get_journals_api(journal_type: Optional[str] = None, limit: int = 20):
    """
    Fetches journals (account.journal) for API endpoint.
    
    Parameters:
    - journal_type: Type of journal to retrieve
    - limit: Maximum number of records to return (default: 20)
    """
    debug(f"🔍 API endpoint /mcp/odoo/journals called with type: {journal_type}")
    client = get_odoo_client()

    # Initialize domain with no filters
    domain = []

    # Add journal_type filter if provided
    if journal_type:
        domain.append(["type", "=", journal_type])

    records = client.search_read(
        model="account.journal",
        domain=domain,
        fields=["name", "type", "code", "active", "company_id", "currency_id", "default_account_id", "sequence"],
        limit=limit
    )
    success(f"✅ Returning {len(records)} journals")
    return {"records": records}


def get_journals(
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
    debug("🔍 Environment Configuration Check")
    # Get Odoo client directly instead of from context
    odoo = get_odoo_client()
    info("✅ Odoo client initialized")

    # Initialize domain with no filters
    domain = []

    # Add journal_type filter if provided
    if journal_type:
        domain.append(["type", "=", journal_type])
        info(f"🔍 Filtering for journal type: {journal_type}")

    try:
        debug(f"🔍 Executing journals search with type: {journal_type}")
        results = odoo.search_read(
            model="account.journal",
            domain=domain,
            fields=["name", "type", "code", "active", "company_id", "currency_id", "default_account_id", "sequence"],
            limit=limit
        )
        success(f"✅ Retrieved {len(results)} journals")
        return {"success": True, "result": results}
    except Exception as e:
        error(f"❌ Error retrieving journals: {str(e)}")
        return {"success": False, "error": str(e)}