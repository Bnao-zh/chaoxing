# -*- coding: utf-8 -*-
import os.path
import re
from typing import Optional

import requests

from api.config import GlobalConst as gc


def _normalize_account(account: Optional[str]) -> Optional[str]:
    if account is None:
        return None
    account = str(account).strip()
    return account or None


def _sanitize_account_for_filename(account: str) -> str:
    sanitized = re.sub(r"[^A-Za-z0-9_.-]", "_", account)
    sanitized = sanitized.strip("._")
    return sanitized or "default"


def get_cookies_path(account: Optional[str] = None, for_read: bool = True) -> str:
    account = _normalize_account(account)
    if not account:
        return gc.COOKIES_PATH

    account_cookies_path = f"cookies_{_sanitize_account_for_filename(account)}.txt"
    return account_cookies_path


def save_cookies(session: requests.Session, account: Optional[str] = None):
    cookies_path = get_cookies_path(account=account, for_read=False)
    buffer = ""
    with open(cookies_path, "w") as f:
        for k, v in session.cookies.items():
            buffer += f"{k}={v};"
        buffer = buffer.removesuffix(";")
        f.write(buffer)


def use_cookies(account: Optional[str] = None) -> dict:
    cookies_path = get_cookies_path(account=account, for_read=True)
    if not os.path.exists(cookies_path):
        return {}

    cookies = {}
    with open(cookies_path, "r") as f:
        buffer = f.read().strip()
        for item in buffer.split(";"):
            item = item.strip()
            if not item or "=" not in item:
                continue
            k, v = item.split("=", 1)
            cookies[k] = v

    return cookies
