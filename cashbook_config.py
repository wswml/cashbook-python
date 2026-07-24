"""Cashbook 统一配置加载器 — 所有脚本的唯一配置入口

项目结构:
    ~/cashbook/
      ├── cashbook_config.py   ← 本文件
      ├── config.json
      ├── password.json        (不提交 git)
      ├── bin/jz               (CLI 快捷记账)
      ├── jz_import.py         (批量导入)
      ├── module/jz.py         (账单解析)
      ├── module/app/          (Xposed 模块源码)
      └── server/              (FastAPI 服务端)
"""
import json
import os

# 项目根目录 = 本文件所在目录
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

def _load():
    with open(os.path.join(PROJECT_ROOT, "config.json"), encoding="utf-8") as f:
        cfg = json.load(f)
    # password.json 可能不存在（首次 clone 后需从 password.json.example 复制）
    pwd_path = os.path.join(PROJECT_ROOT, "password.json")
    if os.path.exists(pwd_path):
        with open(pwd_path, encoding="utf-8") as f:
            pwd = json.load(f)
    else:
        pwd = {}
    return cfg, pwd

_cfg, _pwd = _load()

# ── 服务器 ──
SERVER_HOST = _cfg["server"]["host"]
SERVER_PORT = _cfg["server"]["port"]
SERVER_URL = f"http://{SERVER_HOST}:{SERVER_PORT}"
SSH_HOST  = SERVER_HOST
SSH_USER  = _cfg["server"]["ssh_user"]

# ── 认证 ──
ADMIN_USER = _pwd.get("cashbook_admin", {}).get("username", "")
ADMIN_PASS = _pwd.get("cashbook_admin", {}).get("password", "")

# ── 账本 ──
DEFAULT_BOOK_ID = _cfg["books"]["default"]["book_id"]

# ── AI ──
_ds = _pwd.get("deepseek", {})
DEEPSEEK_KEY   = _ds.get("api_key", "")
DEEPSEEK_MODEL = _ds.get("model", "deepseek-chat")

# ── 路径 ──
# 项目内路径（相对项目根）
JZ_PARSER    = os.path.join(PROJECT_ROOT, "module", "jz.py")

# Android 绝对路径（不可改为相对 — 系统存储/app数据目录）
CSV_OUTPUT   = _cfg["local_paths"]["csv_output"]
WECHAT_LOG   = _cfg["local_paths"]["wechat_log"]
ALIPAY_DB    = _cfg["local_paths"]["alipay_db"]
ALIPAY_TMP   = _cfg["local_paths"]["alipay_tmp"]
ALIPAY_LAST  = _cfg["local_paths"]["alipay_last_id"]

# ── 分类 ──
EXPENSE_CATS   = _cfg["categories"]["expense"]
INCOME_CATS    = _cfg["categories"]["income"]
REFUND_KEYWORDS = _cfg["categories"]["refund_keywords"]
DEFAULT_CAT    = _cfg["categories"]["default"]

# ── Token 缓存 ──
TOKEN_FILE = os.path.expanduser("~/.jz_token")
