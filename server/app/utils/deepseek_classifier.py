"""DeepSeek 分类模块 - 语义分析兜底分类
==========================================
调用 DeepSeek Chat API 对规则未覆盖的交易进行语义分类。
API key 从环境变量 DEEPSEEK_API_KEY 读取，未配置时自动降级。
"""
import json
import logging
import os
import urllib.request
import urllib.error

logger = logging.getLogger(__name__)

# ── 配置 ──
DEEPSEEK_API_URL = os.getenv(
    "DEEPSEEK_API_URL",
    "https://api.deepseek.com/chat/completions"
)
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")  # V3
REQUEST_TIMEOUT = int(os.getenv("DEEPSEEK_TIMEOUT", "15"))
MAX_RETRIES = int(os.getenv("DEEPSEEK_MAX_RETRIES", "3"))

# 可选分类列表（必须与 rule_engine.py 一致）
CATEGORIES = [
    "餐饮", "交通", "购物", "通讯", "住房",
    "娱乐", "医疗", "教育", "转账", "理财",
    "工资", "还款", "其他",
]

SYSTEM_PROMPT = (
    "你是一个账单分类助手。请根据交易描述，从以下分类中选择最合适的一个：\n\n"
    f"可选分类：{', '.join(CATEGORIES)}\n\n"
    "规则：\n"
    "1. 必须且只能从上述分类中选择\n"
    "2. 只返回分类名称，不要任何解释、标点或多余文字\n"
    "3. 如果确实无法判断，返回\"其他\"\n"
    "4. 输出格式：纯文本，只有一个中文词"
)


def _build_user_message(merchant: str, amount: float, date: str, note: str = "") -> str:
    return (
        f"交易描述：商户「{merchant}」"
        f"{f'，备注「{note}」' if note else ''}"
        f"，金额 {amount} 元"
        f"{f'，日期 {date}' if date else ''}"
    )


def is_available() -> bool:
    """检查 DeepSeek API 是否已配置"""
    return bool(DEEPSEEK_API_KEY)


def deepseek_classify(
    merchant: str,
    amount: float,
    date: str,
    note: str = "",
) -> str:
    """调用 DeepSeek API 进行分类

    Args:
        merchant: 商户名/交易对方
        amount: 交易金额
        date: 交易日期 (YYYY-MM-DD)
        note: 备注/商品名

    Returns:
        分类名称，API 不可用时返回 "其他"
    """
    if not DEEPSEEK_API_KEY:
        logger.debug("DEEPSEEK_API_KEY 未配置，跳过 API 调用")
        return "其他"

    payload = {
        "model": DEEPSEEK_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": _build_user_message(merchant, amount, date, note)},
        ],
        "temperature": 0.1,
        "max_tokens": 16,
    }

    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        DEEPSEEK_API_URL,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        },
        method="POST",
    )

    last_error = None
    for attempt in range(MAX_RETRIES):
        try:
            with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                content = result["choices"][0]["message"]["content"].strip()

                # 验证返回的分类是否合法
                category = _validate(content)
                if category:
                    return category
                else:
                    logger.warning(f"DeepSeek 返回非法分类: {content!r}，降级为其他")
                    return "其他"

        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < MAX_RETRIES - 1:
                import time
                wait = 2 ** attempt
                logger.warning(f"DeepSeek 限流，{wait}s 后重试 ({attempt+1}/{MAX_RETRIES})")
                time.sleep(wait)
                continue
            last_error = f"HTTP {e.code}: {e.reason}"
            break
        except (urllib.error.URLError, OSError, json.JSONDecodeError,
                KeyError, IndexError) as e:
            last_error = str(e)
            if attempt < MAX_RETRIES - 1:
                import time
                wait = 2 ** attempt
                logger.warning(f"DeepSeek 请求失败，{wait}s 后重试 ({attempt+1}/{MAX_RETRIES}): {e}")
                time.sleep(wait)
                continue
            break

    logger.error(f"DeepSeek API 调用失败 ({MAX_RETRIES}次): {last_error}")
    return "其他"


def _validate(category: str) -> str | None:
    """验证分类是否在允许列表中"""
    for c in CATEGORIES:
        if category == c:
            return c
    return None
