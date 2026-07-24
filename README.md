# Cashbook

微信/支付宝账单自动记账系统。Android 端 Xposed 模块抓取 → 本地解析导出 → 服务端 FastAPI 入库 → Web 看板。

## 项目结构

```
~/cashbook/
├── bin/jz                     # CLI 快捷记账（SSH 调服务器 API）
├── jz_import.py               # 批量导入管道（本地 csv → scp → 服务器 API）
├── cashbook_config.py         # 统一配置加载器
├── config.json                # 配置文件
├── password.json              # 密钥（不提交）
├── password.json.example      # 密钥模板
├── module/                    # Android 端
│   ├── jz.py                  # 账单解析引擎（messages.log → CSV）
│   └── app/                   # Xposed 模块源码（WechatReader）
│       └── src/main/java/com/nous/wechatreader/
│           ├── WechatReader.java       # 主 Hook 入口
│           ├── MessageWriter.java      # 消息写入 messages.log
│           └── DailyExportReceiver.java # 每日导出广播
└── server/                    # 服务端
    ├── main.py                # FastAPI 入口（端口 9090）
    ├── app/
    │   ├── models/            # SQLAlchemy 模型
    │   ├── routers/           # API 路由（记账/账本/预算/导入）
    │   ├── utils/             # 工具
    │   │   ├── classifier.py        # 分类调度器
    │   │   ├── rule_engine.py       # 关键词规则引擎
    │   │   ├── deepseek_classifier.py # DeepSeek AI 分类
    │   │   ├── cache_manager.py     # 分类缓存
    │   │   └── auth.py              # JWT 鉴权
    │   ├── static/            # 前端静态资源（图表/样式）
    │   └── templates/         # Jinja2 模板
    └── ecosystem.config.cjs   # PM2 配置
```

## 数据流

```
微信 App
  │  Xposed Hook (WechatReader.java)
  │  拦截 318767153 支付消息
  ▼
messages.log ──→ module/jz.py 解析 ──→ qianji.csv
                                          │
                                    jz_import.py
                                    scp → 服务器 API
                                          │
                                    /api/entry/import/qianji
                                    ├─ 四元组去重
                                    ├─ 规则引擎分类
                                    ├─ DeepSeek AI 兜底
                                    ▼
                                    MySQL
                                      │
                                    Web 看板 (ECharts)
```

## 部署

### 服务器

```bash
git clone https://github.com/wswml/cashbook-python.git /root/cashbook-python
cd /root/cashbook-python/server
pip install -r requirements.txt
cp .env.example .env        # 编辑填入实际密钥
pm2 start ecosystem.config.cjs && pm2 save
```

### 本地 Termux

```bash
git clone https://github.com/wswml/cashbook-python.git ~/cashbook
cd ~/cashbook
cp password.json.example password.json
# 编辑 password.json 填入服务器 IP、JWT token、DeepSeek key
```

## 日常使用

```bash
# 快捷记账
jz 15 早餐
jz r 200 报销      # r = 收入

# 批量导入（从 WechatReader 导出后）
python3 ~/cashbook/jz_import.py

# 服务器更新
ssh root@47.99.240.71 'cd /root/cashbook-python && git pull && pm2 restart cashbook'
```

## 分类策略

三级分类，按优先级：

1. **规则引擎** — 关键词匹配（地铁→交通、麦当劳→餐饮、超市→购物），零成本
2. **本地缓存** — 同类商户复用上次 API 结果，零成本
3. **DeepSeek AI** — 语义分析兜底，结果入缓存

规则覆盖约 80% 的交易，剩余 20% 由 AI 处理。

## 依赖

- Python 3.10+
- MySQL 8.0
- Android (Termux + root + LSPosed)
- DeepSeek API（可选）
