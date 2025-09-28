import sys
import datetime
import platform
import os
from enum import Enum, auto
from typing import Any, Optional

class LogLevel(Enum):
    INFO = auto()
    SUCCESS = auto()
    WARNING = auto()
    ERROR = auto()
    DEBUG = auto()

# ANSI color codes
class Colors:
    RESET = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"

def log(message: str, level: LogLevel = LogLevel.INFO, *args: Any, **kwargs: Any) -> None:
    """
    Log a message with timestamp, color, emoji, and source context.

    Args:
        message: The message to log
        level: The log level (INFO, SUCCESS, WARNING, ERROR, DEBUG)
        *args, **kwargs: Additional arguments to format the message with
    """
    if args or kwargs:
        message = message.format(*args, **kwargs)

    # Get current timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

    # Source context
    source = "odoo-mcp-server"

    # Select emoji and color based on log level
    level_info = {
        LogLevel.INFO: {"emoji": "🌐 ", "color": Colors.GREEN, "text": "INFO"},
        LogLevel.SUCCESS: {"emoji": "✅ ", "color": Colors.GREEN, "text": "INFO"},
        LogLevel.WARNING: {"emoji": "🚀 ", "color": Colors.YELLOW, "text": "WARN"},
        LogLevel.ERROR: {"emoji": "❌ ", "color": Colors.RED, "text": "ERROR"},
        LogLevel.DEBUG: {"emoji": "🔍 ", "color": Colors.BLUE, "text": "DEBUG"},
    }.get(level, {"emoji": "", "color": Colors.RESET, "text": "UNKNOWN"})

    # Format the log level with color
    colored_level = f"{level_info['color']}{level_info['text']}{Colors.RESET}"

    # Print the formatted message to stderr
    print(f"{timestamp} | {colored_level} | {source:<20} | {level_info['emoji']}{message}", file=sys.stderr)

# Utility functions for specialized logging
def divider(char: str = "=", length: int = 80) -> None:
    """Log a divider line."""
    info(char * length)

def log_startup_header() -> None:
    """Log the startup header with system information."""
    divider()
    info("🚀 ODOO MCP SERVER STARTING")
    divider()
    info("📅 Start time: {}", datetime.datetime.now().isoformat())
    info("🐍 Python version: {}", sys.version)
    info("📁 Working directory: {}", os.getcwd())
    info("🔧 Logging level: {}", 20)  # INFO level is 20
    divider()

def log_env_check(env_vars: dict) -> None:
    """Log environment variable check results."""
    info("🔍 Environment Configuration Check:")
    for key, value in env_vars.items():
        if value:
            if key.lower().endswith("password"):
                info("  ✅ {}: ***", key)
            else:
                info("  ✅ {}: {}", key, value)
        else:
            info("  ⚪ {}: Not set (optional)", key)

# Convenience functions for different log levels
def info(message: str, *args: Any, **kwargs: Any) -> None:
    """Log an informational message."""
    log(message, LogLevel.INFO, *args, **kwargs)

def success(message: str, *args: Any, **kwargs: Any) -> None:
    """Log a success message."""
    log(message, LogLevel.SUCCESS, *args, **kwargs)

def warning(message: str, *args: Any, **kwargs: Any) -> None:
    """Log a warning message."""
    log(message, LogLevel.WARNING, *args, **kwargs)

def error(message: str, *args: Any, **kwargs: Any) -> None:
    """Log an error message."""
    log(message, LogLevel.ERROR, *args, **kwargs)

def debug(message: str, *args: Any, **kwargs: Any) -> None:
    """Log a debug message."""
    log(message, LogLevel.DEBUG, *args, **kwargs)
