from typing import Optional, Dict, Any, List
from mcp.server.fastmcp import Context
from odoo_client import get_odoo_client
from logger import info, success, warning, error, debug


def get_partners_api(partner_type: Optional[str] = None, limit: int = 50):
    """
    Fetches partners (res.partner) for API endpoint.
    
    Parameters:
    - partner_type: Type of partners to retrieve
    - limit: Maximum number of records to return (default: 50)
    """
    debug(f"🔍 API endpoint /mcp/odoo/partners called with type: {partner_type}")
    client = get_odoo_client()

    # Initialize domain with no filters
    domain = []

    # Add partner_type filter if provided
    if partner_type == "customer":
        domain.append(["customer_rank", ">", 0])
    elif partner_type == "vendor":
        domain.append(["supplier_rank", ">", 0])

    records = client.search_read(
        model="res.partner",
        domain=domain,
        fields=["name", "email", "phone", "mobile", "street", "city", "zip", "country_id", 
                "customer_rank", "supplier_rank", "company_id", "category_id", "user_id"],
        limit=limit
    )
    success(f"✅ Returning {len(records)} partners")
    return {"records": records}


def get_partners(
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
    debug("🔍 Environment Configuration Check")
    # Get Odoo client directly instead of from context
    odoo = get_odoo_client()
    info("✅ Odoo client initialized")

    # Initialize domain with no filters
    domain = []

    # Add partner_type filter if provided
    if partner_type == "customer":
        domain.append(["customer_rank", ">", 0])
        info("🔍 Filtering for Customers")
    elif partner_type == "vendor":
        domain.append(["supplier_rank", ">", 0])
        info("🔍 Filtering for Vendors")

    try:
        debug(f"🔍 Executing partners search with type: {partner_type}")
        results = odoo.search_read(
            model="res.partner",
            domain=domain,
            fields=["name", "email", "phone", "mobile", "street", "city", "zip", "country_id", 
                   "customer_rank", "supplier_rank", "company_id", "category_id", "user_id"],
            limit=limit
        )
        success(f"✅ Retrieved {len(results)} partners")
        return {"success": True, "result": results}
    except Exception as e:
        error(f"❌ Error retrieving partners: {str(e)}")
        return {"success": False, "error": str(e)}