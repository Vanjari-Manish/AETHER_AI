import logging
from sqlalchemy.orm import Session
from app.database.connection import engine, SessionLocal
from app.models.base import Base
from app.models.auth_models import Organization, User, Role, Permission
from app.core.security import get_password_hash

logger = logging.getLogger("gpo.db")

def init_db():
    """
    Initialize database schema tables dynamically and seeds default system parameters,
    roles, permissions, default organization and default superuser.
    """
    logger.info("Initializing database tables...")
    try:
        # Create all tables registered under the declarative metadata Base
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables verified/created successfully.")
    except Exception as e:
        logger.error(f"Critical error creating database tables: {e}")
        raise e

    db: Session = SessionLocal()
    try:
        # 1. Seed Permissions
        permissions_data = {
            "dashboard:view": "Clearance to view the operational telemetry dashboard.",
            "grid:view": "Read-only access to view grid asset topology models.",
            "grid:control": "Permission to run breaker controls or trigger switches.",
            "assets:view": "Access to view physical grid assets inventory.",
            "assets:manage": "Access to create, update, or remove physical grid assets.",
            "policies:view": "Access to view central compiled safety boundary policies.",
            "policies:compile": "Access to compile policy rules syntax files.",
            "policies:deploy": "Access to deploy compiled policy versions to edge substation RTUs.",
            "reports:view": "Access to view generated system operations & compliance reports.",
            "reports:create": "Clearance to generate operations and compliance report logs.",
            "settings:view": "Clearance to view basic system parameters and configurations.",
            "admin:view": "Global administration permissions check."
        }

        seeded_perms = {}
        for name, desc in permissions_data.items():
            perm = db.query(Permission).filter(Permission.name == name).first()
            if not perm:
                perm = Permission(name=name, description=desc, status="active")
                db.add(perm)
                db.flush()
                logger.info(f"Seeded permission: {name}")
            seeded_perms[name] = perm

        # 2. Seed Roles and associate permissions
        roles_permissions_map = {
            "Super Admin": list(permissions_data.keys()),
            "Grid Administrator": [
                "dashboard:view", "grid:view", "grid:control", "assets:view",
                "assets:manage", "policies:view", "policies:compile", "settings:view"
            ],
            "Operations Engineer": [
                "dashboard:view", "grid:view", "grid:control", "assets:view",
                "policies:view", "settings:view"
            ],
            "Policy Analyst": [
                "dashboard:view", "grid:view", "policies:view", "policies:compile",
                "policies:deploy", "reports:view", "reports:create"
            ],
            "Viewer": [
                "dashboard:view", "reports:view"
            ]
        }

        seeded_roles = {}
        for role_name, perms in roles_permissions_map.items():
            role = db.query(Role).filter(Role.name == role_name).first()
            if not role:
                role = Role(name=role_name, description=f"{role_name} security profile.", status="active")
                db.add(role)
                db.flush()
                logger.info(f"Seeded role: {role_name}")
            
            # Map permissions
            for p_name in perms:
                p_obj = seeded_perms[p_name]
                if p_obj not in role.permissions_list:
                    role.permissions_list.append(p_obj)
            seeded_roles[role_name] = role

        # 3. Seed Default Organization
        default_org = db.query(Organization).filter(Organization.name == "GPO Corp").first()
        if not default_org:
            default_org = Organization(
                name="GPO Corp",
                description="Grid Policy Orchestrator Global Operations",
                status="active"
            )
            db.add(default_org)
            db.flush()
            logger.info("Seeded default organization: GPO Corp")

        # 4. Seed Default Admin User
        admin_email = "admin@gpo.gov"
        admin_user = db.query(User).filter(User.email == admin_email).first()
        if not admin_user:
            admin_pwd = "admin"
            admin_user = User(
                email=admin_email,
                password_hash=get_password_hash(admin_pwd),
                full_name="Super Admin",
                organization="GPO Corp",
                role="Super Admin",
                organization_id=default_org.id,
                status="active"
            )
            admin_user.roles_list.append(seeded_roles["Super Admin"])
            db.add(admin_user)
            db.flush()
            logger.info(f"Seeded default Super Admin user: {admin_email}")

        db.commit()
        logger.info("Database seeding completed successfully.")
    except Exception as e:
        db.rollback()
        logger.error(f"Critical error during database seeding: {e}")
        raise e
    finally:
        db.close()
