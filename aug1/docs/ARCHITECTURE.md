# Grid Policy Orchestrator (GPO)
## Technical Architecture Specification

*   **Version:** v1.0.0
*   **Status:** Approved
*   **Owner:** Principal Software Architect / AI Systems Architect
*   **Phase:** Phase 0.7
*   **Last Updated:** July 22, 2026
*   **Purpose:** Blueprint outlining overall microservices design, multi-agent AI loops, simulation pipelines, database stacks, and deployment perimeters.

---

## Table of Contents
*   [1. Architecture Overview](#1-architecture-overview)
    *   [1.1 Overall Architecture Style](#11-overall-architecture-style)
    *   [1.2 High-Level System Overview](#12-high-level-system-overview)
    *   [1.3 Design Principles](#13-design-principles)
    *   [1.4 Major Subsystems](#14-major-subsystems)
    *   [1.5 Architectural Goals](#15-architectural-goals)
*   [2. Frontend Architecture](#2-frontend-architecture)
    *   [2.1 Overall Frontend Structure](#21-overall-frontend-structure)
    *   [2.2 Module Organization](#22-module-organization)
    *   [2.3 State Management Strategy](#23-state-management-strategy)
    *   [2.4 Routing Strategy](#24-routing-strategy)
    *   [2.5 Component Organization](#25-component-organization)
    *   [2.6 Data Flow](#26-data-flow)
    *   [2.7 Authentication Flow](#27-authentication-flow)
    *   [2.8 Error Handling Strategy](#28-error-handling-strategy)
*   [3. Backend Architecture](#3-backend-architecture)
    *   [3.1 Service Organization](#31-service-organization)
    *   [3.2 Business Logic Layer](#32-business-logic-layer)
    *   [3.3 API Layer](#33-api-layer)
    *   [3.4 Background Jobs](#34-background-jobs)
    *   [3.5 File Processing](#35-file-processing)
    *   [3.6 Logging & Auditing](#36-logging--auditing)
    *   [3.7 Configuration Management](#37-configuration-management)
    *   [3.8 Error Handling](#38-error-handling)
*   [4. AI Architecture](#4-ai-architecture)
    *   [4.1 Multi-Agent Architecture](#41-multi-agent-architecture)
    *   [4.2 Agent Responsibilities](#42-agent-responsibilities)
    *   [4.3 Agent Communication](#43-agent-communication)
    *   [4.4 Orchestrator](#44-orchestrator)
    *   [4.5 Memory Strategy](#45-memory-strategy)
    *   [4.6 RAG Integration](#46-rag-integration)
    *   [4.7 Explainability](#47-explainability)
    *   [4.8 Human Approval Workflow](#48-human-approval-workflow)
    *   [4.9 Hallucination Mitigation Strategy](#49-hallucination-mitigation-strategy)
*   [5. Simulation Architecture](#5-simulation-architecture)
    *   [5.1 Digital Twin](#51-digital-twin)
    *   [5.2 Simulation Engine](#52-simulation-engine)
    *   [5.3 Scenario Execution](#53-scenario-execution)
    *   [5.4 Optimization Pipeline](#54-optimization-pipeline)
    *   [5.5 Policy Evaluation](#55-policy-evaluation)
    *   [5.6 Result Generation](#56-result-generation)
*   [6. Database Architecture](#6-database-architecture)
    *   [6.1 Transactional Database (PostgreSQL)](#61-transactional-database-postgresql)
    *   [6.2 Vector Database (Qdrant)](#62-vector-database-qdrant)
    *   [6.3 Cache Layer (Redis)](#63-cache-layer-redis)
    *   [6.4 File Storage](#64-file-storage)
    *   [6.5 Backup Strategy](#65-backup-strategy)
    *   [6.6 Data Lifecycle](#66-data-lifecycle)
*   [7. Deployment Architecture](#7-deployment-architecture)
    *   [7.1 Development Environment](#71-development-environment)
    *   [7.2 Testing & Staging Environment](#72-testing--staging-environment)
    *   [7.3 Production Environment](#73-production-environment)
    *   [7.4 CI/CD Overview](#74-cicd-overview)
    *   [7.5 Monitoring & Logging](#75-monitoring--logging)
    *   [7.6 Scalability & High Availability](#76-scalability--high-availability)
*   [8. Security Architecture](#8-security-architecture)
    *   [8.1 Authentication & Authorization](#81-authentication--authorization)
    *   [8.2 Role-Based Access Control (RBAC)](#82-role-based-access-control-rbac)
    *   [8.3 API & Secret Security](#83-api--secret-security)
    *   [8.4 Encryption](#84-encryption)
    *   [8.5 Audit Logging](#85-audit-logging)
    *   [8.6 Input Validation & Secure AI](#86-input-validation--secure-ai)
*   [9. Cross-Cutting Concerns](#9-cross-cutting-concerns)
*   [10. Recommended Technology Stack](#10-recommended-technology-stack)
*   [11. Related Documents](#11-related-documents)
*   [12. Revision History](#12-revision-history)

---

## 1. Architecture Overview

### 1.1 Overall Architecture Style
GPO implements a hybrid architecture combining **Event-Driven Microservices** with a **Distributed Multi-Agent Consensus System**. High-frequency SCADA/EMS data streams and rule evaluation logs are handled asynchronously via an event-driven control plane, while core database transactions, simulations, and user admin views utilize clean service boundaries.

### 1.2 High-Level System Overview
GPO is structured into three primary operational tiers:
1.  **Observability & Management Plane (Frontend):** A role-based operator dashboard displaying active topology maps, simulation configurations, compiled policies, and audit logs.
2.  **Orchestration & Verification Plane (Backend Services):** Service modules handling user sessions, database entries, scenario compilations, simulations, and the verification compiler.
3.  **Autonomous Edge Control Plane (Multi-Agent Swarm):** Software agents deployed on substation RTUs (Remote Terminal Units) or substation edge nodes. These agents negotiate locally in real-time, governed by compiled policy constraints, to stabilize voltage, balance loads, and manage DERs.

### 1.3 Design Principles
*   **Decoupled Governance:** Separate policy definition (compiled central control) from local operational execution (distributed edge agents).
*   **Asynchronous Commits:** Leverage event streams for telemetry and agent logs to prevent database write blocks.
*   **Fail-Safe Default:** If communication breaks down or the policy engine becomes unavailable, edge nodes default to hard-wired physical safety configurations.
*   **Mathematically Verified Boundaries:** Every action proposed by agents is verified against compiled safety rules before physical relays receive commands.

### 1.4 Major Subsystems
*   **Policy Studio & Compiler:** Converts human-authored regulations (e.g., NERC rules) into numeric logic files.
*   **Multi-Agent Coordination Hub:** Orchestrates consensus loops and manages communication between active edge agents.
*   **Digital Twin & Simulation Engine:** An emulated grid network environment used to verify policy updates against simulated contingency events.
*   **Audit Logger & Compliance Engine:** Immutable log system recording all configurations, user actions, and agent decisions.
*   **Gateway Interface & SCADA Adapters:** Translates industrial protocols (DNP3, Modbus, IEC 61850) into internal JSON formats.

### 1.5 Architectural Goals
*   **Sub-Second Latency:** Complete agent consensus and policy checks within 400 milliseconds.
*   **Fault Tolerance:** Prevent complete grid control failures if individual agents or communication links drop offline.
*   **Scale:** Support up to 100,000 active DER agents per utility control zone.
*   **Strict Security:** Ensure 100% compliance with NERC CIP physical and cybersecurity perimeters.

---

## 2. Frontend Architecture

### 2.1 Overall Frontend Structure
The GPO frontend is designed as a **Single Page Application (SPA)** utilizing modular rendering compartments. The UI is client-side rendered (CSR) to guarantee instant transitions and layout changes.

### 2.2 Module Organization
The frontend is divided into independent modules organized by domain concerns:
*   `core/` (Standard layouts, navbar, sidebar, app wrapper, authentication screens).
*   `dashboard/` (KPI displays, notification widgets, negotiation list layouts).
*   `topology/` (GIS map interfaces, interactive single-line vector canvas).
*   `policy/` (Text editor inputs, compiler output screens).
*   `simulation/` (Sandbox settings, scenario builders, timeline graphs).
*   `shared/` (Generic buttons, inputs, tables, status indicators, badges).

### 2.3 State Management Strategy
GPO splits application state into three distinct layers:
1.  **Global View State:** Tracks user sessions, theme configurations, notification badges, and UI settings. Managed using a centralized client-side store (e.g., Redux or Zustand).
2.  **Telemetry Data Cache:** High-frequency, real-time grid values (Hz, MW, Volts) updating at sub-second intervals. Cached in memory using client-side buffers to prevent screen lagging.
3.  **Server Cache / Query State:** Manages CRUD operations for policies, logs, settings, and user lists, using asynchronous query managers (e.g., React Query) to handle caching and background updates.

### 2.4 Routing Strategy
*   **Hash-Based Routing:** Uses hash paths (e.g., `#/topology?node=substation-4a`) to avoid collision with backend APIs and simplify deployment in offline intranet configurations.
*   **Route Guards:** Synchronous security checks validating the user's role before mounting restricted screens (e.g., only Administrators can access `#/administration`).

### 2.5 Component Organization
Components follow the Atomic Design model:
*   *Atoms:* Standard buttons, badges, labels, inputs, status indicators.
*   *Molecules:* Search bars, KPI cards, form fields.
*   *Organisms:* Data tables, timeline feeds, the topology schematic canvas.
*   *Templates/Pages:* Unified layouts (Dashboard view, Settings view).

### 2.6 Data Flow
The frontend enforces a strict **Unidirectional Data Flow**:
1.  User triggers action (e.g., click breaker override button).
2.  Component dispatches action request to the controller / state manager.
3.  State manager sends API request to the backend server.
4.  API returns updated data; client-side store updates state.
5.  Views listen to state changes and re-render affected elements.

### 2.7 Authentication Flow
1.  User enters credentials on the login screen.
2.  Gateway verifies credentials and returns a secure JSON Web Token (JWT) containing role clearances.
3.  Client stores the token in memory (session storage) to protect against CSRF attacks.
4.  Subsequent API calls include the JWT in the Authorization header.
5.  If the token expires or validation fails, the routing system redirects the user to the login screen.

### 2.8 Error Handling Strategy
*   **Boundary Catching:** Visual compartments are wrapped in error boundaries. If a telemetry widget fails, it collapses into a clear error state without crashing the main application dashboard.
*   **Global Interceptor:** A centralized API client interceptor catches network connection drops, showing a modal connection warning to the operator.

---

## 3. Backend Architecture

### 3.1 Service Organization
The backend is structured into microservices communicating via an API Gateway. Services are containerized and deployed in isolated nodes.

```
                  +--------------------------+
                  |       API GATEWAY        |
                  +-------------+------------+
                                |
        +-----------------------+-----------------------+
        |                       |                       |
+-------+-------+       +-------+-------+       +-------+-------+
|  AUTH SERVICE |       | POLICY SERVICE|       | SIM SERVICE   |
+-------+-------+       +-------+-------+       +-------+-------+
        |                       |                       |
        +-----------------------+-----------------------+
                                |
                  +-------------+------------+
                  |    SCADA / EMS CONNECTOR |
                  +--------------------------+
```

### 3.2 Business Logic Layer
Encapsulates domain operations. It evaluates data against mathematical grid models, schedules simulation runs, compiles policy syntax files, and records audit logs.

### 3.3 API Layer
Exposes RESTful endpoints for CRUD tasks (saving policies, pulling history logs) and WebSockets for real-time telemetry streaming (pushing Hz/MW metrics to active dashboards).

### 3.4 Background Jobs
Managed using a queue framework (e.g., Celery, Redis). Tasks include:
*   Generating compliance report archives (PDF/CSV compilation).
*   Executing simulation scenario trials.
*   Pushing configuration updates to physical edge nodes.

### 3.5 File Processing
Handles ingestion of NERC CIP XML logs, CAD drawings of grid topologies, and compiled `.yaml` policy configurations. Uploaded files are verified, parsed, and logged.

### 3.6 Logging & Auditing
All logs write to a centralized stdout/stderr stream captured by log aggregators. Audit logs are written to database tables with cryptographic checksum verification to prevent tampering.

### 3.7 Configuration Management
Configuration variables (database credentials, SCADA endpoints, key limits) are loaded from system environment variables at startup, adhering to Twelve-Factor App guidelines.

### 3.8 Error Handling
The backend uses standard HTTP status codes:
*   `400 Bad Request` for validation failures (contains structured error details).
*   `401 Unauthorized` / `403 Forbidden` for role clearance checks.
*   `422 Unprocessable Entity` for syntax compile failures.
*   `500 Internal Server Error` displays a generic support ID to the user while logging the full traceback to system files.

---

## 4. AI Architecture

GPO implements a Multi-Agent Decision Intelligence System governed by central compliance rules.

```
       +---------------------------------------------+
       |             CENTRAL POLICY ENGINE           |
       |  (NERC Safety & Regulatory Constraints)     |
       +----------------------+----------------------+
                              | Enforces Rules
                              v
       +---------------------------------------------+
       |             ORCHESTRATOR AGENT              |
       |  (Consensus & Path Allocation Governance)   |
       +-------+-----------------------------+-------+
               |                             |
     Negotiates|                     Negotiates|
               v                             v
+--------------+-------------+     +----------+--------------+
|      SUBSTATION AGENT A    |     |      SUBSTATION AGENT B |
| (Edge Load/Voltage control)|     | (Edge Load/Voltage control)|
+----------------------------+     +----------------------------+
```

### 4.1 Multi-Agent Architecture
*   **Orchestrator Agent:** Manages global consensus, monitors regional capacity limits, and resolves coordination conflicts between substation agents.
*   **Substation Agents:** Control localized devices (breakers, line switches). They communicate with adjacent substation agents to balance local voltage variations.
*   **DER Agents:** Located at active generation sites (wind farms, battery arrays). They manage local supply in response to substation queries.

### 4.2 Agent Responsibilities
Agents monitor local metrics, negotiate capacity trades with adjacent nodes during contingency events, and calculate compliance paths using the local policy compiler.

### 4.3 Agent Communication
Agents communicate asynchronously using a lightweight message broker (e.g., RabbitMQ, gRPC). Communication protocols are optimized to prevent packet delays on low-bandwidth utility networks.

### 4.4 Orchestrator
The central Orchestrator manages agent configurations, validates agent identities, and ensures agent negotiations reach consensus during grid contingencies.

### 4.5 Memory Strategy
*   *Short-Term Memory:* Local node parameters and adjacent node statuses stored in in-memory databases (e.g., Redis).
*   *Long-Term Memory:* Historical negotiation traces, event sequences, and outcomes logged to relational databases for future analysis.

### 4.6 RAG Integration
A Retrieval-Augmented Generation (RAG) module parses natural-language utility regulations (e.g., FERC, NERC CIP files) stored in a vector database. This helps operators query the exact safety rule supporting a compiled policy.

### 4.7 Explainability
Every agent decision is logged with a trace containing:
1.  Trigger event (e.g., `Overload on Feeder 4`).
2.  Alternative paths evaluated.
3.  Active policy constraint applied (e.g., `Prohibit load shedding on Hospital node`).
4.  Final decision output (e.g., `Dispatch Battery BESS-1`).

### 4.8 Human Approval Workflow
For non-critical operations (e.g., daily solar curtailments), agent proposals are pushed to the operator's dashboard as a Recommendation Card. The action is held in queue until manually approved. Critical actions (e.g., sub-second sags) execute autonomously but log detailed trace summaries immediately.

### 4.9 Hallucination Mitigation Strategy
GPO does not rely on generative models for real-time control actions. Decisions are calculated using deterministic optimization logic and verified against compiled safety boundaries, eliminating AI hallucination risks.

---

## 5. Simulation Architecture

The simulation engine allows operators to safely test policy rules against grid contingency models in an emulated environment.

### 5.1 Digital Twin
The Digital Twin models physical grid assets (buses, lines, generation parameters, line resistance, maximum capacities) in a clean software database.

### 5.2 Simulation Engine
Calculates power flows and grid dynamics in real-time, executing contingency models (lightning strikes, generation drops) to test system resilience.

### 5.3 Scenario Execution
1.  Scenario Builder passes configuration parameters to the simulator.
2.  The simulator configures the digital twin grid state.
3.  Simulated grid faults are introduced.
4.  Active agents coordinate to resolve the fault under the target ruleset.
5.  Data logs are exported to analytics databases.

### 5.4 Optimization Pipeline
Calculates optimal power flow paths during contingencies, balancing restoration speed against line capacity limits.

### 5.5 Policy Evaluation
Every simulated agent action is evaluated by the policy engine. If an action violates a safety constraint (e.g., overloading a line), the simulator flags the violation and stops the run.

### 5.6 Result Generation
At the end of a simulation run, GPO generates a detailed report summary comparing baseline metrics with simulated outcomes (restoration times, voltage levels).

---

## 6. Database Architecture

GPO utilizes a multi-tier database structure to optimize transactional speed, data security, and analytics queries.

```
       +---------------------------------------------+
       |             CENTRAL DATABASE GATEWAY        |
       +----+-------------------+----------------+---+
            |                   |                |
            v                   v                v
+-----------+-----------+ +-----+-----+ +--------+--------+
|  POSTGRESQL (Primary) | | QDRANT    | | REDIS          |
|  Transactional data,  | | Vector DB | | Cache, short   |
|  user records, logs   | | RAG data  | | agent memory   |
+-----------------------+ +-----------+ +-----------------+
```

### 6.1 Transactional Database (PostgreSQL)
Acts as the central repository. Stored data includes user records, security roles, policy metadata, log records, and node statuses. PostgreSQL provides the ACID compliance necessary to manage grid configurations securely.

### 6.2 Vector Database (Qdrant)
Stores vector embeddings of natural-language utility regulations and NERC compliance guidelines. Enables semantic lookup and RAG queries for policy drafting.

### 6.3 Cache Layer (Redis)
Caches API queries, stores active WebSocket connections, and manages short-term agent memory.

### 6.4 File Storage
Policy configurations, CAD schematics, and generated PDF compliance reports are saved in secure object storage.

### 6.5 Backup Strategy
Transactional databases run continuous replication to secondary standby instances. Daily encrypted snapshot backups are compiled and stored in offsite utility perimeters.

### 6.6 Data Lifecycle
*   *Hot Data (0 - 30 days):* Deployed in primary transactional tables and cache layers.
*   *Warm Data (30 - 365 days):* Moved to compressed database instances for analytics and audit queries.
*   *Cold Data (>365 days):* Archived in read-only compressed storage files to meet NERC retention requirements.

---

## 7. Deployment Architecture

GPO is deployed in containerized environments, ensuring rapid scaling and compatibility with local utility hardware.

### 7.1 Development Environment
Engineers deploy code locally using container runtimes (e.g., Docker Desktop, Minikube). Telemetry is emulated using mock SCADA generators.

### 7.2 Testing & Staging Environment
Hosts automated CI/CD pipeline tests. Includes integration testing against simulated grid engines, validation testing, and compliance checks.

### 7.3 Production Environment
Deployed in high-availability clusters (e.g., Kubernetes). Containers are isolated in secure namespaces with restricted API gateway perimeters.

### 7.4 CI/CD Overview
1.  Developers push updates to version control.
2.  CI pipelines run unit checks, lint verification, and security scanning.
3.  Docker images are compiled, scanned for vulnerabilities, and saved to secure registers.
4.  CD pipelines update Kubernetes deployments with rolling updates to ensure zero downtime.

### 7.5 Monitoring & Logging
System load, memory usage, API performance, and container logs are aggregated using standard tools (e.g., Prometheus, Grafana, ELK stack).

### 7.6 Scalability & High Availability
Services run in multi-replica configurations behind load balancers. Kubernetes automatically scales pods during high-frequency telemetry events.

---

## 8. Security Architecture

GPO follows a zero-trust architecture model, complying with NERC CIP requirements.

### 8.1 Authentication & Authorization
Uses corporate Single Sign-On (SSO) systems integrated with Active Directory. User actions require MFA verification.

### 8.2 Role-Based Access Control (RBAC)
Provides fine-grained permission mapping:
*   *Operator:* View telemetry, trigger overrides, acknowledge alerts.
*   *Engineer:* View metrics, run simulations, edit policy files.
*   *Compliance Officer:* Deploy policies, download audit reports.
*   *Administrator:* Manage users, view audit logs.

### 8.3 API & Secret Security
External communication channels are encrypted using TLS 1.3. API requests require valid signatures. System secrets are loaded dynamically from vault systems.

### 8.4 Encryption
Data is encrypted in transit using TLS 1.3 and at rest using AES-256 keys.

### 8.5 Audit Logging
All operator actions, policy updates, and breaker overrides are logged to encrypted, append-only database tables with cryptographic checksum verification.

### 8.6 Input Validation & Secure AI
API payloads are validated against strict schemas to prevent injection attacks. AI models are isolated, and agent outputs are validated by deterministic compilers before physical execution.

---

## 9. Cross-Cutting Concerns

*   **Scalability:** The platform scales horizontally, managing growing DER counts by isolating agent calculations to regional edge nodes.
*   **Reliability:** Central control plane drops do not disrupt local safety loops; edge agents default to localized safety configurations.
*   **Performance:** Telemetry data loops are processed in memory using Redis cache layers to ensure fast dashboard updates.
*   **Maintainability:** De-coupled microservices and clear interface schemas allow independent updates of individual modules.
*   **Observability:** Real-time metrics are exported to Grafana dashboards, providing full visibility into system health.
*   **Fault Tolerance:** Active node clusters run inside auto-healing Kubernetes nodes. If a container fails, a replica is initialized instantly.
*   **Disaster Recovery:** Offsite database backups and secondary cloud instances ensure recovery targets are met during catastrophic outages.

---

## 10. Recommended Technology Stack

| Architecture Layer | Recommended Technology | Strategic Rationale |
| :--- | :--- | :--- |
| **Frontend Framework** | **React & TypeScript** | Component-driven architecture, robust type safety, large ecosystem. |
| **Styling** | **CSS Modules & Vanilla CSS** | Ensures maximum layout performance and prevents library bloat. |
| **Backend Engine** | **Python (FastAPI)** | High performance, native support for async processes, rich AI libraries. |
| **AI Orchestration** | **LangChain & gRPC** | Structured tool management, asynchronous communication. |
| **Simulation Core** | **PowerModels.jl (Julia)** | Industrial math performance, fast solver speeds. |
| **Primary Database** | **PostgreSQL** | Trusted transactional database with full ACID compliance. |
| **Vector Database** | **Qdrant** | High performance vector lookups for RAG compliance checks. |
| **Caching & Broker** | **Redis & RabbitMQ** | Sub-millisecond read/writes, reliable event processing. |
| **Authentication** | **Auth0 / Keycloak** | Standard OIDC/OAuth2 protocols with Active Directory integration. |
| **Cloud Deployment**| **Kubernetes (EKS / GKE)** | High-availability container orchestration and scaling. |
| **Observability** | **Prometheus & Grafana** | Industry-standard metric collection and dashboard overlays. |

---

## 11. Related Documents
*   [Product Vision](PRODUCT_VISION.md)
*   [Database & Schema Design](DATABASE_DESIGN.md)
*   [API Specification Contract](API_SPEC.md)
*   [Screen Inventory & Flow Catalog](SCREEN_CATALOG.md)
*   [Reusable Component Library](COMPONENT_LIBRARY.md)

---

## 12. Revision History

| Version | Date | Description | Author |
| :--- | :--- | :--- | :--- |
| v1.0.0 | July 22, 2026 | Initial Release for Phase 0 | Principal Software Architect |
