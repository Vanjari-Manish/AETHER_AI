import logging
from sqlalchemy.orm import Session
from app.database.connection import engine, SessionLocal
from app.models.base import Base
from app.models.auth_models import Organization, User, Role, Permission
from app.models.grid_models import GridAsset, Policy, PolicyVersion, PolicyExecution, Incident
from app.models.system_models import Notification, Report, AuditLog, ActivityLog, SystemSetting
from app.models.digital_twin_models import Substation, Bus, TransmissionLine, Transformer, Generator, Load, Switch
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


        # 5. Seed Digital Twin entities if they don't exist
        from app.models.digital_twin_models import Substation, Bus, TransmissionLine, Transformer, Generator, Load, Switch
        from app.models.system_models import AuditLog

        if not db.query(Substation).first():
            logger.info("Seeding digital twin topology data...")
            
            # Substations
            sierra = Substation(
                name="Sierra Substation",
                description="Primary transmission substation located near Sierra range.",
                latitude=39.5296,
                longitude=-119.8138,
                metadata_json={"voltage_class_kv": 138.0}
            )
            reno = Substation(
                name="Reno Substation",
                description="Distribution substation serving Reno city center.",
                latitude=39.5272,
                longitude=-119.8219,
                metadata_json={"voltage_class_kv": 138.0}
            )
            tahoe = Substation(
                name="Tahoe Substation",
                description="Substation connecting Tahoe hydro generation and battery units.",
                latitude=39.0968,
                longitude=-120.0324,
                metadata_json={"voltage_class_kv": 138.0}
            )
            db.add_all([sierra, reno, tahoe])
            db.flush()  # To populate IDs
            
            # Buses
            sierra_bus_a = Bus(
                name="Sierra Bus A",
                description="Main 138kV bus Sierra Substation",
                base_kv=138.0,
                substation_id=sierra.id
            )
            sierra_bus_b = Bus(
                name="Sierra Bus B",
                description="Medium voltage 13.8kV bus Sierra Substation",
                base_kv=13.8,
                substation_id=sierra.id
            )
            reno_bus_a = Bus(
                name="Reno Bus A",
                description="Main 138kV bus Reno Substation",
                base_kv=138.0,
                substation_id=reno.id
            )
            tahoe_bus_a = Bus(
                name="Tahoe Bus A",
                description="Main 138kV bus Tahoe Substation",
                base_kv=138.0,
                substation_id=tahoe.id
            )
            db.add_all([sierra_bus_a, sierra_bus_b, reno_bus_a, tahoe_bus_a])
            db.flush()
            
            # Transmission Lines
            line_sierra_reno = TransmissionLine(
                name="Sierra-Reno Line 1",
                description="138kV transmission line connecting Sierra and Reno",
                from_bus_id=sierra_bus_a.id,
                to_bus_id=reno_bus_a.id,
                r_pu=0.01,
                x_pu=0.05,
                b_pu=0.02,
                rating_mva=100.0
            )
            line_sierra_tahoe = TransmissionLine(
                name="Sierra-Tahoe Line 1",
                description="138kV transmission line connecting Sierra and Tahoe",
                from_bus_id=sierra_bus_a.id,
                to_bus_id=tahoe_bus_a.id,
                r_pu=0.02,
                x_pu=0.08,
                b_pu=0.03,
                rating_mva=100.0
            )
            db.add_all([line_sierra_reno, line_sierra_tahoe])
            db.flush()
            
            # Transformers
            transformer_sierra = Transformer(
                name="Sierra XFMR 1",
                description="138kV/13.8kV step-down transformer at Sierra Substation",
                from_bus_id=sierra_bus_a.id,
                to_bus_id=sierra_bus_b.id,
                r_pu=0.005,
                x_pu=0.04,
                rating_mva=50.0
            )
            db.add(transformer_sierra)
            db.flush()
            
            # Generators
            gen_sierra = Generator(
                name="Sierra Gas Gen",
                description="Thermal generation unit located at Sierra Substation",
                bus_id=sierra_bus_a.id,
                type="thermal",
                capacity_mw=150.0,
                p_mw=60.0,
                q_mvar=15.0
            )
            gen_tahoe = Generator(
                name="Tahoe Hydro Gen",
                description="Hydroelectric turbine unit at Tahoe Substation",
                bus_id=tahoe_bus_a.id,
                type="hydro",
                capacity_mw=50.0,
                p_mw=30.0,
                q_mvar=5.0
            )
            db.add_all([gen_sierra, gen_tahoe])
            db.flush()
            
            # Loads
            load_reno = Load(
                name="Reno Town Load",
                description="Reno municipal power load center",
                bus_id=reno_bus_a.id,
                p_mw=80.0,
                q_mvar=20.0
            )
            load_sierra = Load(
                name="Sierra Local Load",
                description="Sierra local distribution industrial load",
                bus_id=sierra_bus_b.id,
                p_mw=15.0,
                q_mvar=4.0
            )
            db.add_all([load_reno, load_sierra])
            db.flush()
            
            # Switches
            switch_sierra = Switch(
                name="Sierra Line Breaker",
                description="Breaker switch for Sierra-Reno Line at Sierra Bus",
                line_id=line_sierra_reno.id,
                bus_id=sierra_bus_a.id,
                state="closed"
            )
            switch_tahoe = Switch(
                name="Tahoe Line Breaker",
                description="Breaker switch for Sierra-Tahoe Line at Tahoe Bus",
                line_id=line_sierra_tahoe.id,
                bus_id=tahoe_bus_a.id,
                state="closed"
            )
            db.add_all([switch_sierra, switch_tahoe])
            db.flush()
            
            # Audit Logs (Deterministic recent events for Phase 3.1)
            # Find admin user ID to associate
            admin_user_obj = db.query(User).filter(User.email == admin_email).first()
            admin_id = admin_user_obj.id if admin_user_obj else None
            
            events = [
                AuditLog(user_id=admin_id, action="substation.create", details="Substation 'Sierra Substation' created", status="success"),
                AuditLog(user_id=admin_id, action="substation.create", details="Substation 'Reno Substation' created", status="success"),
                AuditLog(user_id=admin_id, action="substation.create", details="Substation 'Tahoe Substation' created", status="success"),
                AuditLog(user_id=admin_id, action="generator.connect", details="Generator 'Tahoe Hydro Gen' connected to bus 'Tahoe Bus A'", status="success"),
                AuditLog(user_id=admin_id, action="line.update", details="Transmission line 'Sierra-Reno Line 1' updated parameters", status="success"),
                AuditLog(user_id=admin_id, action="asset.validation", details="Digital Twin asset validation passed: 15/15 rules valid", status="success"),
                AuditLog(user_id=admin_id, action="db.sync", details="Digital Twin topology synchronized with physical EMS database", status="success"),
            ]
            db.add_all(events)
            logger.info("Deterministic digital twin topology data seeded.")

        db.commit()
        logger.info("Database seeding completed successfully.")
    except Exception as e:
        db.rollback()
        logger.error(f"Critical error during database seeding: {e}")
        raise e
    finally:
        db.close()
