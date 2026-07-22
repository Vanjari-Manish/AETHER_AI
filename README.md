# Grid Policy Orchestrator (GPO)
> Policy-Aware Multi-Agent Decision Intelligence Platform for Smart Grid Operations

Grid Policy Orchestrator (GPO) is a policy-governed multi-agent decision support platform designed for electrical transmission and distribution utility control rooms. The system automates localized grid stabilization, DER (Distributed Energy Resource) dispatch, and load-balancing operations at millisecond speeds. By enforcing safety boundaries through an executable policy compiler, GPO bridges the gap between autonomous edge actions and strict utility compliance standards, reducing operator alert fatigue and securing grid topology structures against outage contingencies.

---

## Vision
Our vision is to deliver a secure, self-healing grid control system where autonomous agents handle sub-second stability negotiations within strict policy boundaries, under the continuous oversight of utility control room dispatchers.

For the complete product strategy, target personas, and validation metrics, refer to [PRODUCT_VISION.md](PRODUCT_VISION.md).

---

## Features
*   **Multi-Agent AI:** Decentralized edge agent negotiation loops for regional balancing.
*   **Policy Engine:** Executable rules compiler that translates regulatory texts into system boundaries.
*   **Digital Twin:** Real-time electrical schematic visualization of grid asset connections.
*   **Grid Simulation:** Interactive scenario builder to test grid events under mock faults.
*   **Explainable AI:** Decision logs tracing the exact policy constraints applied by agents.
*   **Decision Support:** Recommendation feeds allowing operators to review non-critical agent actions.
*   **Analytics Dashboard:** Visual indicators monitoring system load patterns and trends.
*   **Role-Based Access Control:** Fine-grained API authorization mapping roles to actions.
*   **Enterprise Security:** Zero-trust architecture compliant with NERC CIP guidelines.
*   **Scenario Planning:** Toolsets to configure and clone reproducible grid contingencies.

---

## Technology Stack
GPO's decoupled microservices stack is optimized for high-volume telemetry ingestion and fast rule compiling:
*   **Frontend UI:** React and TypeScript leveraging high-density CSS variables.
*   **Backend API:** FastAPI (Python) executing asynchronous endpoints and WebSocket feeds.
*   **AI Orchestration:** LangChain and gRPC managing edge agent coordination logs.
*   **Grid Solver:** PowerModels.jl (Julia) calculating power flow states.
*   **Databases:** PostgreSQL (transactions, configs), Qdrant (vectors), and Redis (caching, agent memory).
*   **Deployment:** Containerized pipelines hosted in high-availability Kubernetes clusters.

For detailed interface paths and microservice mappings, see [ARCHITECTURE.md](ARCHITECTURE.md).

---

## Documentation

| Document File | Description |
| :--- | :--- |
| [PRODUCT_VISION.md](PRODUCT_VISION.md) | Product vision, target users, personas, and success metrics. |
| [BRAND_GUIDELINES.md](BRAND_GUIDELINES.md) | Visual identity, monospaced typography, and color palette definitions. |
| [DESIGN_SYSTEM.md](DESIGN_SYSTEM.md) | Core design system tokens, typography scales, and visual spacing rules. |
| [design-tokens.json](design-tokens.json) | Compiled JSON tokens for color, typography, borders, and margins. |
| [UX_GUIDELINES.md](UX_GUIDELINES.md) | UX guidelines, accessibility (WCAG AA), shortcuts, and error alerts. |
| [SCREEN_CATALOG.md](SCREEN_CATALOG.md) | Directory of all application views, user permissions, and dependencies. |
| [COMPONENT_LIBRARY.md](COMPONENT_LIBRARY.md) | Master inventory of all reusable visual and domain components. |
| [ARCHITECTURE.md](ARCHITECTURE.md) | System overview, module structures, and technology stack rationales. |
| [DATABASE_DESIGN.md](DATABASE_DESIGN.md) | Database schemas, indexing guidelines, lifecycles, and tables. |
| [API_SPEC.md](API_SPEC.md) | API endpoints, status codes, request schemas, and websocket flows. |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Code styling, branching models, conventional commits, and workflows. |
| [AI_DEVELOPMENT_GUIDE.md](AI_DEVELOPMENT_GUIDE.md) | System prompt templates, coding guidelines, and safety practices. |
| [ROADMAP.md](ROADMAP.md) | *Future Document:* Detailed multi-phase roadmap. |

---

## Repository Structure

```
aug1/
├── BRAND_GUIDELINES.md       # Color profiles and brand attributes
├── PRODUCT_VISION.md         # Strategy, scopes, and target personas
├── DESIGN_SYSTEM.md          # Visual tokens and typography hierarchies
├── design-tokens.json        # Compiled design parameters schema
├── UX_GUIDELINES.md          # Accessibility rules and standard alerts
├── SCREEN_CATALOG.md         # Directory of views and permission maps
├── COMPONENT_LIBRARY.md      # UI components and domain assets
├── ARCHITECTURE.md           # System components and stack definitions
├── DATABASE_DESIGN.md        # Database schema specifications
├── API_SPEC.md               # API endpoints contract
├── CONTRIBUTING.md           # Git branching and conventional commits
├── AI_DEVELOPMENT_GUIDE.md   # Prompt templates and safety guidelines
└── README.md                 # Project landing page
```

---

## Development Workflow
All developments in the codebase follow a structured integration sequence:

```
[Documentation & Spec Alignment]
               │
               ▼
[System Architecture & API Mappings]
               │
               ▼
[Code Implementation & Local Style Compliance]
               │
               ▼
[Automated Tests Verification (Unit/Integration)]
               │
               ▼
[CI/CD Verification & Production Deployments]
```

---

## Getting Started
To set up GPO for local development, follow these high-level steps:
1.  **Clone Repository:** Access the repository inside the secure corporate firewall.
2.  **Install Prerequisites:** Verify that local containers (Docker), Python, Node, and Julia environments are installed.
3.  **Local Environment Configuration:** Copy the template variables file into a local `.env` configuration.
4.  **Launch Dependencies:** Start local database containers (Postgres, Redis, Qdrant) using container setups.
5.  **Initialize Services:** Launch backend FastAPI workers, simulation solvers, and frontend dev servers.
6.  **Verify Setup:** Access the local address and verify connections using system health endpoints.

---

## Contribution
GPO follows a structured branching strategy (`main`, `development`, `feature/*`, `bugfix/*`). Pull requests require two approvals and passing tests. 

For commit conventions, code formatting grids, and test specifications, refer to [CONTRIBUTING.md](CONTRIBUTING.md).

---

## AI Development
AI-assisted coding is encouraged but must follow GPO's security, formatting, and structural constraints. All model prompts and verification workflows must conform to the rules in [AI_DEVELOPMENT_GUIDE.md](AI_DEVELOPMENT_GUIDE.md).

---

## Roadmap
Core GPO milestones are divided into multi-phase steps:
*   *Phase 0 (Planning):* Complete system specifications and architecture (Current).
*   *Phase 1 (Core Services):* Compile backend engines and DNP3/Modbus adapters.
*   *Phase 2 (Consensus Engine):* Implement multi-agent negotiation logic.
*   *Phase 3 (Dashboard UI):* Build the React frontend using design tokens.

Refer to `docs/ROADMAP.md` for detailed milestone schedules.

---

## Security & License
*   **Security:** This software controls electrical grid infrastructure and complies with NERC CIP cybersecurity perimeters. Vulnerabilities must be reported to `security@gpo.utility.org`.
*   **License:** Proprietary - Licensed for Internal Utility Use Only.

---

## Maintainers
*   **GPO core team** (`gpo-core-devs@gpo.utility.org`)
