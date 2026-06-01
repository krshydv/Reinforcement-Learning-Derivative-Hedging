"""init schema

Revision ID: 20260516_0001
Revises: 
Create Date: 2026-05-16 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = "20260516_0001"
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        "roles",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("name", sa.String(), nullable=False, unique=True),
    )
    op.create_table(
        "permissions",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("name", sa.String(), nullable=False, unique=True),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_table(
        "role_permissions",
        sa.Column("role_id", sa.String(), sa.ForeignKey("roles.id"), primary_key=True),
        sa.Column("permission_id", sa.String(), sa.ForeignKey("permissions.id"), primary_key=True),
    )
    op.create_table(
        "user_roles",
        sa.Column("user_id", sa.String(), sa.ForeignKey("users.id"), primary_key=True),
        sa.Column("role_id", sa.String(), sa.ForeignKey("roles.id"), primary_key=True),
    )
    op.create_table(
        "portfolios",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("user_id", sa.String(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_table(
        "positions",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("portfolio_id", sa.String(), sa.ForeignKey("portfolios.id"), nullable=False),
        sa.Column("symbol", sa.String(), nullable=False),
        sa.Column("quantity", sa.Float(), nullable=False),
        sa.Column("avg_price", sa.Float(), nullable=False),
    )
    op.create_table(
        "trades",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("portfolio_id", sa.String(), sa.ForeignKey("portfolios.id"), nullable=False),
        sa.Column("symbol", sa.String(), nullable=False),
        sa.Column("quantity", sa.Float(), nullable=False),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("side", sa.String(), nullable=False),
        sa.Column("executed_at", sa.DateTime(), nullable=False),
    )
    op.create_table(
        "portfolio_snapshots",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("portfolio_id", sa.String(), sa.ForeignKey("portfolios.id"), nullable=False),
        sa.Column("value", sa.Float(), nullable=False),
        sa.Column("pnl", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_table(
        "experiments",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("user_id", sa.String(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("algorithm", sa.String(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_table(
        "episodes",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("experiment_id", sa.String(), sa.ForeignKey("experiments.id"), nullable=False),
        sa.Column("reward", sa.Float(), nullable=False),
        sa.Column("length", sa.Integer(), nullable=False),
    )
    op.create_table(
        "market_states",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("experiment_id", sa.String(), sa.ForeignKey("experiments.id"), nullable=False),
        sa.Column("data", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_table(
        "rl_checkpoints",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("experiment_id", sa.String(), sa.ForeignKey("experiments.id"), nullable=False),
        sa.Column("path", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_table(
        "metrics",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("experiment_id", sa.String(), sa.ForeignKey("experiments.id"), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("value", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_table(
        "backtests",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("user_id", sa.String(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("metrics", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_table(
        "training_runs",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("user_id", sa.String(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("experiment_name", sa.String(), nullable=False),
        sa.Column("algorithm", sa.String(), nullable=False),
        sa.Column("timesteps", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_table(
        "audit_logs",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("user_id", sa.String(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("action", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

def downgrade() -> None:
    op.drop_table("audit_logs")
    op.drop_table("training_runs")
    op.drop_table("backtests")
    op.drop_table("metrics")
    op.drop_table("rl_checkpoints")
    op.drop_table("market_states")
    op.drop_table("episodes")
    op.drop_table("experiments")
    op.drop_table("portfolio_snapshots")
    op.drop_table("trades")
    op.drop_table("positions")
    op.drop_table("portfolios")
    op.drop_table("user_roles")
    op.drop_table("role_permissions")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
    op.drop_table("permissions")
    op.drop_table("roles")
