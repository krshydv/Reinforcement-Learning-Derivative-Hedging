from sqlalchemy import select, func
import structlog
from app.db.session import AsyncSessionLocal
from app.db.models import Role, Permission, RolePermission, User, UserRole, Portfolio, Position, PortfolioSnapshot
from app.services.auth_service import pwd_context
from app.core.config import settings

DEFAULT_PERMISSIONS = [
    "access",
    "user:create",
    "user:read",
]

ADMIN_ROLE = "admin"
USER_ROLE = "user"


class SeedService:
    async def seed(self) -> None:
        async with AsyncSessionLocal() as session:
            logger = structlog.get_logger()
            existing_roles = await session.execute(select(Role))
            roles = {role.name: role for role in existing_roles.scalars().all()}
            for role_name in [ADMIN_ROLE, USER_ROLE]:
                if role_name not in roles:
                    role = Role(name=role_name)
                    session.add(role)
                    roles[role_name] = role

            existing_permissions = await session.execute(select(Permission))
            permissions = {perm.name: perm for perm in existing_permissions.scalars().all()}
            for perm_name in DEFAULT_PERMISSIONS:
                if perm_name not in permissions:
                    perm = Permission(name=perm_name)
                    session.add(perm)
                    permissions[perm_name] = perm

            await session.flush()

            for perm_name in DEFAULT_PERMISSIONS:
                perm = permissions[perm_name]
                for role_name in [ADMIN_ROLE, USER_ROLE]:
                    role = roles[role_name]
                    existing_link = await session.execute(
                        select(RolePermission).where(
                            RolePermission.role_id == role.id,
                            RolePermission.permission_id == perm.id,
                        )
                    )
                    if existing_link.scalar_one_or_none() is None:
                        session.add(RolePermission(role_id=role.id, permission_id=perm.id))

            await session.flush()

            if settings.admin_email and settings.admin_password:
                if len(settings.admin_password) > 72:
                    logger.warning("admin_password_too_long", max_length=72)
                    await session.commit()
                    return
                admin_email = settings.admin_email.lower()
                admin_exists = await session.execute(
                    select(User).where(User.email == admin_email)
                )
                admin_user = admin_exists.scalar_one_or_none()
                if not admin_user:
                    admin_user = User(
                        email=admin_email,
                        hashed_password=pwd_context.hash(settings.admin_password),
                        is_active=True,
                    )
                    session.add(admin_user)
                    await session.flush()
                admin_role = roles[ADMIN_ROLE]
                existing_role = await session.execute(
                    select(UserRole).where(
                        UserRole.user_id == admin_user.id,
                        UserRole.role_id == admin_role.id,
                    )
                )
                if existing_role.scalar_one_or_none() is None:
                    session.add(UserRole(user_id=admin_user.id, role_id=admin_role.id))

                await self._seed_demo_portfolio(session, admin_user.id)

            await session.commit()

    async def _seed_demo_portfolio(self, session, user_id: str) -> None:
        existing = await session.execute(select(Portfolio).where(Portfolio.user_id == user_id))
        if existing.scalars().first():
            return
        portfolio = Portfolio(user_id=user_id, name="Hedging Book")
        session.add(portfolio)
        await session.flush()
        session.add(PortfolioSnapshot(portfolio_id=portfolio.id, value=1_250_000.0, pnl=42_500.0))
        demo_positions = [
            ("SPY", 1200.0, 512.4),
            ("QQQ", -400.0, 438.2),
            ("IWM", 800.0, 201.6),
            ("TLT", -250.0, 92.3),
        ]
        for symbol, quantity, avg_price in demo_positions:
            session.add(Position(portfolio_id=portfolio.id, symbol=symbol, quantity=quantity, avg_price=avg_price))

    async def has_users(self) -> bool:
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(func.count(User.id)))
            return result.scalar_one() > 0
