"""core/snowflake_client.py - Resilient Snowflake Live Client & Fallback Engine.

Connects to Snowflake using environment variables when provided (e.g. on Render),
and seamlessly falls back to high-fidelity local data if credentials are not set.
"""

import os
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

load_dotenv()

def get_snowflake_config() -> Dict[str, str]:
    """Retrieve sanitized Snowflake credentials from environment."""
    return {
        "account": os.getenv("SNOWFLAKE_ACCOUNT", "hf55215.ap-northeast-1.aws").strip(),
        "user": os.getenv("SNOWFLAKE_USER", "CHIRAG").strip(),
        "password": os.getenv("SNOWFLAKE_PASSWORD", "").strip(),
        "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH").strip(),
        "database": os.getenv("SNOWFLAKE_DATABASE", "SUPPLY_CHAIN_DB").strip(),
        "schema": os.getenv("SNOWFLAKE_SCHEMA", "CORE").strip(),
        "role": os.getenv("SNOWFLAKE_ROLE", "ACCOUNTADMIN").strip(),
    }

def has_live_credentials() -> bool:
    """Check if minimum live authentication credentials exist."""
    cfg = get_snowflake_config()
    return bool(cfg["password"] or os.getenv("SNOWFLAKE_PRIVATE_KEY_PATH"))

def execute_snowflake_query(query: str, params: Optional[Dict[str, Any]] = None) -> Optional[List[Dict[str, Any]]]:
    """
    Executes a SQL query against live Snowflake if credentials exist.
    Returns list of dict rows or None if unavailable.
    """
    if not has_live_credentials():
        return None

    try:
        import snowflake.connector
        cfg = get_snowflake_config()
        conn_params = {
            "account": cfg["account"],
            "user": cfg["user"],
            "warehouse": cfg["warehouse"],
            "database": cfg["database"],
            "schema": cfg["schema"],
            "role": cfg["role"],
        }
        if cfg["password"]:
            conn_params["password"] = cfg["password"]

        with snowflake.connector.connect(**conn_params) as conn:
            with conn.cursor(snowflake.connector.DictCursor) as cur:
                cur.execute(query, params or {})
                return cur.fetchall()
    except Exception as e:
        print(f"⚠️ Snowflake live query fallback (Error: {e})")
        return None
