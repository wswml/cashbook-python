# Cashbook

工业级记账系统 — 微信/支付宝账单自动抓取 + AI 分类 + Web 管理

## 架构

```
~/cashbook/
├── bin/jz                  # CLI 快捷记账
├── jz_import.py            # 批量导入管道
├── cashbook_config.py      # 统一配置加载器
├── config.json             # 配置文件（可提交 git）
├── password.json.example   # 密钥模板
├── password.json           # 实际密钥（不提交 git）
├── module/                 # 本地端
│   ├── jz.py               # 账单解析引擎
│   └── app/                # Xposed 模块源码 (WechatReader)
│       └── src/main/java/com/nous/wechatreader/
├── server/                 # 服务端
│   ├── main.py             # FastAPI 入口
│   ├── app/
│   │   ├── models/         # SQLAlchemy 模型
│   │   ├── routers/        # API 路由
│   │   ├── utils/          # 工具 (auth, classifier)
│   │   ├── static/         # 前端静态资源
│   │   └── templates/      # Jinja2 模板
│   └── ecosystem.config.cjs # PM2 配置
└── .gitignore
```

## 数据流

```
微信/支付宝 App → Xposed 模块抓取 → messages.log
                                      ↓
                              module/jz.py 解析
                                      ↓
                              qianji.csv
                                      ↓
                          jz_import.py (scp → API)
                                      ↓
                          服务器 FastAPI 导入
                           ├─ 四元组去重
                           ├─ 规则引擎分类
                           └─ DeepSeek AI 分类
                                      ↓
                                  MySQL
                                      ↓
                          Web 前端 (Vue/JS)
```

## 快速开始

### 首次 Clone

```bash
git clone https://github.com/wswml/cashbook-python.git ~/cashbook
cd ~/cashbook
cp password.json.example password.json
# 编辑 password.json 填入实际密钥
```

### 快捷记账

```bash
cd ~/cashbook && python3 -m bin.jz 15 早餐
# 或建立 alias: jz='python3 ~/cashbook/bin/jz'
```

### 批量导入

```bash
cd ~/cashbook && python3 jz_import.py
```

### 服务器部署

```bash
scp -r ~/cashbook/server/ root@your-server:/root/cashbook-python/
ssh root@your-server
cd /root/cashbook-python
pip install -r requirements.txt
# 编辑 ecosystem.config.cjs 填入实际密钥
pm2 start ecosystem.config.cjs && pm2 save
```

## 依赖

- Python 3.10+
- MySQL 8.0
- Android (Termux + root + LSPosed)
- DeepSeek API (可选，用于 AI 分类)

## License

MIT
