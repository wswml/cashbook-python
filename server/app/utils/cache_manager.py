"""缓存管理 - 避免重复调用外部分类 API
========================================
缓存键: MD5(商户名_备注)
缓存值: 分类名称
持久化: JSON 文件
"""
import hashlib
import json
import os
import logging

logger = logging.getLogger(__name__)


class ClassificationCache:
    """分类缓存"""

    def __init__(self, cache_file: str = "classification_cache.json"):
        self.cache_file = cache_file
        self._cache: dict[str, str] = {}
        self._dirty = False
        self._load()

    def _key(self, merchant: str, note: str = "") -> str:
        """生成缓存键"""
        raw = f"{merchant}_{note}"
        return hashlib.md5(raw.encode("utf-8")).hexdigest()

    def _load(self):
        """从文件加载缓存"""
        if not os.path.exists(self.cache_file):
            self._cache = {}
            return

        try:
            with open(self.cache_file, "r", encoding="utf-8") as f:
                self._cache = json.load(f)
            logger.info(f"缓存已加载: {len(self._cache)} 条")
        except (json.JSONDecodeError, OSError) as e:
            logger.warning(f"缓存文件损坏，重建空缓存: {e}")
            self._cache = {}

    def _save(self):
        """持久化到文件"""
        try:
            os.makedirs(os.path.dirname(self.cache_file) or ".", exist_ok=True)
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump(self._cache, f, ensure_ascii=False, indent=2)
            self._dirty = False
        except OSError as e:
            logger.error(f"缓存写入失败: {e}")

    def get(self, merchant: str, note: str = "") -> str | None:
        """查询缓存

        Returns:
            命中返回分类名称，未命中返回 None
        """
        k = self._key(merchant, note)
        return self._cache.get(k)

    def set(self, merchant: str, category: str, note: str = ""):
        """写入缓存并持久化"""
        k = self._key(merchant, note)
        if self._cache.get(k) != category:
            self._cache[k] = category
            self._dirty = True
            self._save()

    def get_stats(self) -> dict:
        """返回缓存统计信息"""
        return {
            "total": len(self._cache),
            "file": self.cache_file,
        }
