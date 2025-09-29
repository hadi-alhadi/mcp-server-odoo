# 🐍 Odoo MCP Server

This project provides a **lightweight, experimental Model Context Protocol (MCP) server** for integrating with **Odoo** via XML-RPC.  
It is primarily designed for use with [Claude Desktop](https://claude.ai), enabling AI tools to query and analyze a wide range of Odoo accounting data.  

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95.0+-00a393.svg)](https://fastapi.tiangolo.com/)

## 📑 Table of Contents

- [Overview](#-odoo-mcp-server)
- [What is MCP?](#-what-is-mcp)
- [Key Features](#-key-features)
- [Project Architecture](#-project-architecture)
- [Setup Guide](#️-setup-guide)
- [Environment Variables](#-environment-variables)
- [Tools Directory](#-tools-directory)
- [API Documentation](#-api-documentation)
- [Claude Desktop Integration](#-claude-desktop-integration)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

### 🔍 Example: Claude Detecting MCP Tool

![MCP Tool Preview](assets/mcp_tool_preview.png)

## 🤖 What is MCP?

The **Model Context Protocol (MCP)** is a standardized interface that allows AI assistants like Claude to interact with external tools and data sources. MCP enables Claude to:

- Access real-time data from your Odoo instance
- Perform complex queries on your accounting data
- Analyze financial information without manual data entry
- Provide insights based on your actual business data

This server implements the MCP specification to create a bridge between Claude and your Odoo ERP system.

## 🚀 Key Features

- **Secure Odoo Connection**: Connect to your Odoo instance using environment variables or a configuration file.  
- **Accounting Data Access**: Retrieve and analyze essential records, including:  
  - **Journals & Entries** – access both journal configurations (sales, purchase, bank, cash, etc.) and their corresponding posted entries for audits and reporting  
  - **Invoices & Bills** – customer invoices, vendor bills, and credit notes  
  - **Chart of Accounts** – account hierarchy, balances, and classifications  
  - **Partners** – customer and vendor profiles with contact details  
  - **Analytic Accounts** – project and cost center data for financial analysis  
- **Claude AI Integration**: Fully supports the Model Context Protocol (MCP) for seamless use with Claude Desktop.  
- **RESTful API**: Powered by FastAPI, offering simple and reliable endpoints.  
- **Flexible Configuration**: Customize settings easily via environment variables or Claude Desktop.  

## 🏗️ Project Architecture

The project consists of several key components that work together:

- **main.py**: Entry point that initializes the MCP server and handles the stdio communication
- **server.py**: Implements the MCP protocol and defines the API endpoints
- **odoo_client.py**: Manages the XML-RPC connection to Odoo and provides methods for data retrieval
- **tools/**: Directory containing modules for different Odoo data types:
  - **accounts/**: Chart of accounts and account balances
  - **analytic_accounts/**: Project and cost center data
  - **invoices/**: Customer invoices and vendor bills
  - **journals/**: Journal configurations and entries
  - **moves/**: Accounting moves and entries
  - **partners/**: Customer and vendor information

The server uses FastAPI for the REST endpoints and the MCP protocol for communication with Claude Desktop.

---

## 🏗️ Setup Guide

Follow these steps to set up and run the Odoo Accounting MCP Server:

### 1. 📅 Clone the Repository

```bash
git clone https://github.com/hadi-alhadi/mcp-server-odoo.git
cd mcp-server-odoo
```

### 2. 🔧 Configure Environment Variables

Create a `.env` file in the project's root directory and populate it with your Odoo connection details:

```ini
ODOO_URL=http://localhost:8069
ODOO_DB=your_db_name
ODOO_USERNAME=your_odoo_user_name
ODOO_PASSWORD=your_odoo_password
```

See the [Environment Variables](#-environment-variables) section for more details.

### 3. 🏗️ Set Up Virtual Environment

It's recommended to use a virtual environment to manage project dependencies:

```bash
python -m venv .venv
```

Activate it:

```bash
# Windows
.\.venv\Scripts\activate

# Unix/Mac
source .venv/bin/activate
```

### 4. 📁 Install Dependencies

Install the required Python packages from the `requirements.txt` file:

```bash
python -m pip install -r requirements.txt
```

### 5. 🚀 Run the Server (optional, not required)

Start the MCP server using the main Python script:

```bash
python main.py
```

The server will typically start and be accessible at `http://localhost:8000`.

## 🔧 Environment Variables

The following environment variables can be configured in your `.env` file or directly in the Claude Desktop configuration:

| Variable | Required | Description | Default |
|----------|----------|-------------|---------|
| `ODOO_URL` | Yes | Base URL of your Odoo instance | - |
| `ODOO_DB` | Yes | Database name | - |
| `ODOO_USERNAME` | Yes | Username for authentication | - |
| `ODOO_PASSWORD` | Yes | Password for authentication | - |
| `ODOO_PORT` | No | Custom port if not using standard HTTP/HTTPS ports | 80/443 |
| `ODOO_PROTOCOL` | No | Protocol to use (http or https) | http |

## 📁 Tools Directory

The `tools/` directory contains specialized modules for different Odoo data types:

- **accounts/**: Functions for retrieving account information and chart of accounts
- **analytic_accounts/**: Functions for accessing analytic accounting data
- **invoices/**: Methods for querying customer invoices and vendor bills
- **journals/**: Tools for accessing journal configurations and entries
- **moves/**: Functions for retrieving accounting moves and entries
- **partners/**: Methods for accessing customer and vendor information

Each module provides specific functions that are exposed through the API endpoints.

## 🔌 API Documentation

The server exposes the following API endpoints:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/accounts` | GET | Retrieve chart of accounts |
| `/invoices` | GET | Get customer invoices and vendor bills |
| `/journals` | GET | Access journal configurations |
| `/partners` | GET | Retrieve customer and vendor information |
| `/moves` | GET | Get accounting moves and entries |
| `/recent_entries` | GET | Retrieve recent journal entries |

All endpoints return JSON responses and support filtering via query parameters.

---

## 🔌 Claude Desktop Integration

You don't need to manually run the MCP server when using Claude Desktop. Instead, configure Claude Desktop to manage the server lifecycle.

Update your `claude_desktop_config.json` file with the following configuration (adjust the paths and Odoo credentials as necessary):

```json
{
  "mcpServers": {
    "odoo": {
      "command": "/path/to/repo/mcp-server-odoo/.venv/bin/python",
      "cwd": "/path/to/repo/mcp-server-odoo",
      "args": ["/path/to/repo/mcp-server-odoo/main.py"],
      "env": {
        "ODOO_URL": "http://localhost:8069",
        "ODOO_DB": "your_db",
        "ODOO_USERNAME": "admin",
        "ODOO_PASSWORD": "your_password"
      }
    }
  }
}
```

## 🔧 Troubleshooting

### Common Issues

1. **Connection Errors**:
   - Verify your Odoo server is running and accessible
   - Check that your credentials in the `.env` file are correct
   - Ensure your network allows connections to the Odoo server

2. **Authentication Failures**:
   - Confirm your Odoo username and password are correct
   - Verify the database name is correct

3. **Missing Data**:
   - Ensure your Odoo user has sufficient permissions to access the requested data
   - Check that the modules for the data you're requesting are installed in Odoo

### Debugging

If you encounter issues, you can enable more detailed logging by setting the `DEBUG` environment variable to `True`.

## 🤝 Contributing

Contributions to the Odoo MCP Server are welcome! Here's how you can contribute:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes**
4. **Run tests** to ensure your changes don't break existing functionality
5. **Submit a pull request**

Please follow the existing code style and include appropriate documentation for new features.

---

## 📁 License

This project is licensed under the MIT License.
