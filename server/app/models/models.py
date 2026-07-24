"""SQLAlchemy 数据模型 - 像素级复刻 Cashbook Prisma Schema"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text
from sqlalchemy.sql import func
from app.models.database import Base


class SystemSetting(Base):
    """系统设置"""
    __tablename__ = "system_settings"

    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    description = Column(Text)
    keywords = Column(String(255))
    version = Column(String(50))
    open_register = Column(Boolean, default=False)
    create_date = Column(DateTime, default=func.now())
    update_by = Column(DateTime, default=func.now())


class User(Base):
    """用户表"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False, unique=True)  # 唯一索引
    password = Column(String(255), nullable=False)
    name = Column(String(100))
    email = Column(String(255))
    create_date = Column(DateTime, default=func.now())


class Book(Base):
    """账本表"""
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(String(100), nullable=False, index=True)
    book_name = Column(String(255), nullable=False)
    share_key = Column(String(255))
    share_key_expires = Column(DateTime)  # shareKey 过期时间
    user_id = Column(Integer, nullable=False, index=True)
    budget = Column(Float, default=0)
    create_date = Column(DateTime, default=func.now())


class BookMember(Base):
    """账本成员表"""
    __tablename__ = "book_members"

    id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(String(100), nullable=False, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    role = Column(String(20), default="member")  # owner | member
    joined_at = Column(DateTime, default=func.now())


class Flow(Base):
    """流水表"""
    __tablename__ = "flows"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False, index=True)
    book_id = Column(String(100), nullable=False, index=True)
    day = Column(String(20), nullable=False)
    flow_type = Column(String(50))  # 收入、支出、不计收支
    industry_type = Column(String(100))  # 行业分类
    pay_type = Column(String(100))  # 支付方式
    money = Column(Float)
    name = Column(String(255))
    description = Column(Text)
    invoice = Column(String(500))  # 小票图片路径
    origin = Column(String(255))  # 流水来源
    attribution = Column(String(100))  # 流水归属
    eliminate = Column(Integer, default=0)  # 0未平账 1已平账 -1忽略


class Budget(Base):
    """预算表"""
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(String(100), nullable=False)
    user_id = Column(Integer, nullable=False)
    month = Column(String(20))
    budget = Column(Float)
    used = Column(Float)


class Receivable(Base):
    """应收/借出表"""
    __tablename__ = "receivables"

    id = Column(Integer, primary_key=True, autoincrement=True)
    occur_id = Column(Integer)
    actual_id = Column(Integer)
    book_id = Column(String(100), nullable=False)
    user_id = Column(Integer, nullable=False)
    name = Column(String(255))
    description = Column(Text)
    occur_day = Column(String(20))
    expect_day = Column(String(20))
    actual_day = Column(String(20))
    money = Column(Float)
    status = Column(Integer, default=0)


class FixedFlow(Base):
    """固定流水/定时记账"""
    __tablename__ = "fixed_flows"

    id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(String(100), nullable=False)
    user_id = Column(Integer, nullable=False)
    month = Column(String(20))
    money = Column(Float)
    name = Column(String(255))
    description = Column(Text)
    flow_type = Column(String(50))
    industry_type = Column(String(100))
    pay_type = Column(String(100))
    attribution = Column(String(100))


class TypeRelation(Base):
    """类型映射关系（CSV导入用）"""
    __tablename__ = "type_relations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    book_id = Column(String(100), nullable=False)
    source = Column(String(255))
    target = Column(String(255))
