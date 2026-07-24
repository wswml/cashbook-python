"""通用工具函数"""
import uuid
import random
import string


def get_uuid(length: int = 8) -> str:
    """生成指定长度的随机字符串"""
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choices(chars, k=length))


def generate_book_id(user_id: int) -> str:
    """生成账本ID: userId-随机串"""
    return f"{user_id}-{get_uuid(8)}"


def generate_share_key(user_id: int, book_db_id: int) -> str:
    """生成分享密钥: userId + bookDbId + 随机串"""
    return f"{user_id}{book_db_id}{get_uuid(8)}"


def success(data=None, message="success"):
    """统一成功响应格式"""
    return {
        "code": 200,
        "message": message,
        "data": data
    }


def error(message="error", code=400):
    """统一错误响应格式"""
    return {
        "code": code,
        "message": message,
        "data": None
    }
