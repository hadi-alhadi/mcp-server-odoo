from typing import Optional, Dict, Any, List
from mcp.server.fastmcp import Context
from odoo_client import get_odoo_client
from logger import info, success, warning, error, debug


def get_invoices_api(invoice_type: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None, limit: int = 20):
    """
    Fetches invoices and bills (account.move) for API endpoint.
    
    Parameters:
    - invoice_type: Type of invoice to retrieve. Options:
      - "customer_invoices" for Customer Invoices
      - "vendor_bills" for Vendor Bills
      - "credit_notes" for Credit Notes
      - If not specified, returns all types
    - start_date: Optional start date filter (format: YYYY-MM-DD)
    - end_date: Optional end date filter (format: YYYY-MM-DD)
    - limit: Maximum number of records to return (default: 20)
    """
    debug(f"🔍 API endpoint /mcp/odoo/invoices called with type: {invoice_type}")
    client = get_odoo_client()

    # Base domain - only get posted documents
    domain = [["state", "=", "posted"]]

    # Add move_type filter based on invoice_type parameter
    if invoice_type == "customer_invoices":
        domain.append(["move_type", "=", "out_invoice"])
    elif invoice_type == "vendor_bills":
        domain.append(["move_type", "=", "in_invoice"])
    elif invoice_type == "credit_notes":
        domain.append(["move_type", "in", ["out_refund", "in_refund"]])

    # Add date filters if provided
    if start_date:
        domain.append(["date", ">=", start_date])
    if end_date:
        domain.append(["date", "<=", end_date])

    records = client.search_read(
        model="account.move",
        domain=domain,
        fields=["name", "date", "move_type", "amount_total", "journal_id", "partner_id", "invoice_date", "payment_state"],
        limit=limit
    )
    success(f"✅ Returning {len(records)} invoices/bills")
    return {"records": records}


def get_invoices(
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
    debug("🔍 Environment Configuration Check")
    # Get Odoo client directly instead of from context
    odoo = get_odoo_client()
    info("✅ Odoo client initialized")

    # Base domain - only get posted documents
    domain = [["state", "=", "posted"]]

    # Add move_type filter based on invoice_type parameter
    if invoice_type == "customer_invoices":
        domain.append(["move_type", "=", "out_invoice"])
        info("🔍 Filtering for Customer Invoices")
    elif invoice_type == "vendor_bills":
        domain.append(["move_type", "=", "in_invoice"])
        info("🔍 Filtering for Vendor Bills")
    elif invoice_type == "credit_notes":
        domain.append(["move_type", "in", ["out_refund", "in_refund"]])
        info("🔍 Filtering for Credit Notes")

    # Add date filters if provided
    if start_date:
        domain.append(["date", ">=", start_date])
    if end_date:
        domain.append(["date", "<=", end_date])

    try:
        debug(f"🔍 Executing invoice search with type: {invoice_type}, date range: {start_date} to {end_date}")
        results = odoo.search_read(
            model="account.move",
            domain=domain,
            fields=["name", "date", "move_type", "amount_total", "journal_id", "partner_id", "invoice_date", "payment_state"],
            limit=limit
        )
        success(f"✅ Retrieved {len(results)} invoices/bills")
        return {"success": True, "result": results}
    except Exception as e:
        error(f"❌ Error retrieving invoices: {str(e)}")
        return {"success": False, "error": str(e)}