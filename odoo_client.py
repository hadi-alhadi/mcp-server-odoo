import os
import re
import socket
import sys
import urllib.parse
import xmlrpc.client
from logger import info, success, warning, error, debug


class OdooClient:
    def __init__(self, url, db, username, password):
        info("🏗️ Initializing Odoo client...")
        if not re.match(r"^https?://", url):
            url = f"http://{url}"
        url = url.rstrip("/")

        self.url = url
        self.db = db
        self.username = username
        self.password = password
        self.uid = None

        debug(f"🔌 Setting up XML-RPC connection to {url}")
        self._common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
        self._models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
        self._connect()

    def _connect(self):
        info("🔄 Connecting to Odoo server...")
        self.uid = self._common.authenticate(self.db, self.username, self.password, {})
        if not self.uid:
            error("❌ Odoo authentication failed")
            raise ValueError("Authentication failed")
        success("✅ Odoo authentication successful")

    def search_read(self, model, domain=[], fields=None, limit=10):
        debug(f"🔍 Executing search_read on model: {model}")
        result = self._models.execute_kw(
            self.db,
            self.uid,
            self.password,
            model,
            "search_read",
            [domain],
            {"fields": fields, "limit": limit}
        )
        success(f"✅ Retrieved {len(result)} records from {model}")
        return result


def get_odoo_client():
    info("🔧 Creating Odoo client from environment variables")
    return OdooClient(
        url=os.environ["ODOO_URL"],
        db=os.environ["ODOO_DB"],
        username=os.environ["ODOO_USERNAME"],
        password=os.environ["ODOO_PASSWORD"]
    )
