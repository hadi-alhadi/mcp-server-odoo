from typing import Optional, Dict, Any, List
from mcp.server.fastmcp import Context
from odoo_client import get_odoo_client
from logger import info, success, warning, error, debug


def get_account_moves():
    """
    Fetches recent account moves for API endpoint.
    """
    debug("🔍 API endpoint /mcp/odoo/accounting called")
    client = get_odoo_client()
    records = client.search_read(
        model="account.move",
        domain=[["state", "=", "posted"]],
        fields=["name", "date", "journal_id", "amount_total"],
        limit=10
    )
    success(f"✅ Returning {len(records)} account moves")
    return {"records": records}


def get_recent_journal_entries(
    ctx: Context,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    limit: int = 20
) -> Dict[str, Any]:
    """
    Fetches recent journal entries (account.move) for AI analysis.
    Allows optional filtering by date.
    """
    debug("🔍 Environment Configuration Check")
    # Get Odoo client directly instead of from context
    odoo = get_odoo_client()
    info("✅ Odoo client initialized")

    domain = [["state", "=", "posted"]]
    if start_date:
        domain.append(["date", ">=", start_date])
    if end_date:
        domain.append(["date", "<=", end_date])

    try:
        debug(f"🔍 Executing journal entries search with date range: {start_date} to {end_date}")
        results = odoo.search_read(
            model="account.move",
            domain=domain,
            fields=["name", "date", "move_type", "amount_total", "journal_id", "partner_id"],
            limit=limit
        )
        success(f"✅ Retrieved {len(results)} journal entries")
        return {"success": True, "result": results}
    except Exception as e:
        error(f"❌ Error retrieving journal entries: {str(e)}")
        return {"success": False, "error": str(e)}