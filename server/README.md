# Cashbook Python

> 像素级复刻 Cashbook 记账本的 Python 版本
> 技术栈：FastAPI + SQLAlchemy + MySQL + Jinja2 + Docker

## 快速开始

```bash
# 1. 解压并进入目录
cd cashbook-python

# 2. 启动服务（Docker Compose）
docker-compose up -d

# 3. 访问
# http://localhost:9090
```

## 功能

- ✅ 用户注册/登录
- ✅ 创建账本
- ✅ 生成 shareKey 邀请共享
- ✅ 通过 shareKey 加入账本
- ✅ 账本成员管理（列表、移除）
- ✅ 记账（收入/支出/不计收支）
- ✅ 消费日历看板
- ✅ 数据分析图表（ECharts）
- ✅ 月度统计
- ✅ 预算管理
- ✅ CSV 导入（支付宝/微信）
- ✅ Docker 部署

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端 | FastAPI |
| ORM | SQLAlchemy |
| 数据库 | MySQL 8.0 |
| 前端 | Jinja2 + 纯 CSS/JS |
| 图表 | ECharts |
| 部署 | Docker Compose |

## API 文档

启动后访问：http://localhost:9090/docs

## 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| DATABASE_URL | mysql+pymysql://... | MySQL 连接串 |
| SECRET_KEY | your-secret-key | JWT 密钥 |
| ACCESS_TOKEN_EXPIRE_DAYS | 7 | Token 过期天数 |

## 数据库模型

- users - 用户表
- books - 账本表
- book_members - 账本成员表
- flows - 流水表
- budgets - 预算表
- receivables - 应收/借出表
- fixed_flows - 固定流水表
- type_relations - 类型映射表

## 共享账本机制

1. 用户A创建账本 → 生成 shareKey
2. 用户A分享 shareKey 给用户B
3. 用户B输入 shareKey → 加入账本
4. 系统为用户B复制 Book 记录 + 写入 BookMember 表
5. 所有成员通过 bookId 共享流水数据

## 开发

```bash
# 本地开发
pip install -r requirements.txt
python main.py

# 数据库迁移
alembic revision --autogenerate -m "xxx"
alembic upgrade head
```

## License

MIT
