from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, Integer, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class Role(Base):
    __tablename__ = "roles"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)

class Permission(Base):
    __tablename__ = "permissions"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)

class RolePermission(Base):
    __tablename__ = "role_permissions"
    role_id: Mapped[str] = mapped_column(String, ForeignKey("roles.id"), primary_key=True)
    permission_id: Mapped[str] = mapped_column(String, ForeignKey("permissions.id"), primary_key=True)

class UserRole(Base):
    __tablename__ = "user_roles"
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), primary_key=True)
    role_id: Mapped[str] = mapped_column(String, ForeignKey("roles.id"), primary_key=True)

class User(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Portfolio(Base):
    __tablename__ = "portfolios"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"))
    name: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Position(Base):
    __tablename__ = "positions"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    portfolio_id: Mapped[str] = mapped_column(String, ForeignKey("portfolios.id"))
    symbol: Mapped[str] = mapped_column(String)
    quantity: Mapped[float] = mapped_column(Float)
    avg_price: Mapped[float] = mapped_column(Float)

class Trade(Base):
    __tablename__ = "trades"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    portfolio_id: Mapped[str] = mapped_column(String, ForeignKey("portfolios.id"))
    symbol: Mapped[str] = mapped_column(String)
    quantity: Mapped[float] = mapped_column(Float)
    price: Mapped[float] = mapped_column(Float)
    side: Mapped[str] = mapped_column(String)
    executed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class PortfolioSnapshot(Base):
    __tablename__ = "portfolio_snapshots"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    portfolio_id: Mapped[str] = mapped_column(String, ForeignKey("portfolios.id"))
    value: Mapped[float] = mapped_column(Float)
    pnl: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Experiment(Base):
    __tablename__ = "experiments"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"))
    name: Mapped[str] = mapped_column(String)
    algorithm: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Episode(Base):
    __tablename__ = "episodes"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    experiment_id: Mapped[str] = mapped_column(String, ForeignKey("experiments.id"))
    reward: Mapped[float] = mapped_column(Float)
    length: Mapped[int] = mapped_column(Integer)

class MarketState(Base):
    __tablename__ = "market_states"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    experiment_id: Mapped[str] = mapped_column(String, ForeignKey("experiments.id"))
    data: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class RLCheckpoint(Base):
    __tablename__ = "rl_checkpoints"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    experiment_id: Mapped[str] = mapped_column(String, ForeignKey("experiments.id"))
    path: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Metric(Base):
    __tablename__ = "metrics"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    experiment_id: Mapped[str] = mapped_column(String, ForeignKey("experiments.id"))
    name: Mapped[str] = mapped_column(String)
    value: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Backtest(Base):
    __tablename__ = "backtests"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"))
    name: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"))
    action: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
