# Sukhshum Vaishnavi // Software Engineer

<p align="center">
  <picture>
    <source media="(prefers-reduced-motion: reduce)" srcset="assets/matrix-portrait.png">
    <img src="assets/matrix-portrait.gif" alt="Matrix Developer Silhouette Animation" width="280">
  </picture>
</p>

<p align="center">
  <img src="assets/terminal-banner.gif" alt="Terminal Initialization Sequence" width="680">
</p>

<p align="center">
  <a href="https://github.com/Sukhshum2628?tab=repositories"><img src="https://img.shields.io/badge/GitHub-Sukhshum2628-0b0f10?style=for-the-badge&logo=github&logoColor=55e6a5" alt="GitHub"></a>
  <a href="https://www.linkedin.com/in/sukhshum-vaishnavi/"><img src="https://img.shields.io/badge/LinkedIn-Connect-0b0f10?style=for-the-badge&logo=linkedin&logoColor=66d9ef" alt="LinkedIn"></a>
  <a href="https://sukhshum-portfolio.vercel.app/"><img src="https://img.shields.io/badge/Portfolio-Live_Site-0b0f10?style=for-the-badge&logo=vercel&logoColor=55e6a5" alt="Portfolio"></a>
  <a href="mailto:sukhsham2628@gmail.com"><img src="https://img.shields.io/badge/Email-Contact_Me-0b0f10?style=for-the-badge&logo=gmail&logoColor=66d9ef" alt="Email"></a>
</p>

---

## $ neofetch --engineer sukhshum

```bash
sukhshum@github-workstation
---------------------------
NAME        : Sukhshum Vaishnavi
ROLE        : Software Engineer
SPECIALTIES : Distributed Systems, Multiplayer Networking, AI & ML, Systems Programming
STACK_CORE  : C++17 / Python / TypeScript / Node.js / Docker
METHODOLOGY : Deterministic Simulation, Host Authority, Frozen Architecture & Contracts
UPTIME      : Building low-latency backends, game engine integrations, and AI pipelines
STATUS      : Developing STALKER-MP & exploring distributed architectures
```

> Software Engineer specializing in distributed backends, multiplayer networking frameworks, and AI-assisted cloud platforms. I focus on building resilient, deterministic systems—from server-authoritative netcode for monolithic game engines to production-grade ML inference services.

---

## 🎮 Flagship Project: STALKER-MP

### Persistent Multiplayer Framework for the X-Ray Engine
**Repository:** [github.com/Sukhshum2628/STALKER-MP](https://github.com/Sukhshum2628/STALKER-MP)  
**Status:** Sprint-by-sprint frozen architecture; engine-free unit-tested core; integration verified on MT engine baseline.

```
       [ Client A ]              [ Client B ]
             \                        /
       (Client Requests)        (Client Requests)
               \                    /
         ┌──────▼──────────────────▼──────┐
         │     HOST-AUTHORITATIVE ZONE    │
         │  ----------------------------  │
         │  • EngineFrameBridge (Seq)     │
         │  • FrameDispatcher Pipeline    │
         │  • World & EntityRegistry      │
         │  • A-Life Online/Offline Bubbles│
         │  • Deterministic Snapshotting  │
         │  • UDP Platform Networking     │
         └────────────────────────────────┘
```

STALKER-MP is a modular multiplayer framework layered directly on top of the X-Ray Monolith engine (S.T.A.L.K.E.R. Anomaly) without forking or rewriting the upstream engine. It introduces a persistent, shared Zone while preserving the native single-player A-Life simulation.

#### Architectural Pillars
- **Preserve Before Replace:** Reuses vanilla engine systems (ALife, spawn machinery, pathfinding) rather than duplicating them.
- **Host Authority:** Clients request; the host decides. Clients never own persistent world state.
- **One World, One A-Life Simulation:** Single authoritative world where online and offline entity transitions are host-driven.
- **Deterministic Pipeline:** Strict per-frame ordering (`World 100` → `EntityRegistry 200` → `PlayerLifecycle 250` → `Bubble 300` → `Transition 350` → `Snapshot 400` → `Networking 900`).
- **Strict Architectural Boundaries:** Exactly one translation unit touches engine headers (`EngineAdapters.cpp`), and exactly one touches OS network sockets (`PlatformSockets.cpp`).
- **Engine ABI Contract (ADR-007):** Exception-free, RTTI-free, iostream-free engine-linked units using deterministic value outcomes (`core::Expected<T>`).

**Tech:** `C++17`, `Visual Studio 2022`, `GCC`, `GoogleTest`, `UDP`, `X-Ray Monolith Engine`

---

## 💼 Featured Engineering Projects

### 🏗️ ConstructIQ — AI-Assisted Construction Planning System
**Repository:** [github.com/Sukhshum2628/ConstructIQ](https://github.com/Sukhshum2628/ConstructIQ)  
*AI-Assisted Construction Planning & Resource Intelligence System (B.Tech CSE Capstone)*

- **CAD-to-Estimate QTO:** Automated `.DXF` geometric parser (`ezdxf`) computing physical material quantities (cement, bricks, steel) and labor-days according to CPWD quantity takeoff formulas.
- **Execution Intelligence:** Geofenced GPS logging and automated weather gating (Open-Meteo) locking weather-sensitive site tasks.
- **Anomaly Detection & Predictive ML:** Z-score material consumption anomaly analysis, cost overrun risk classification via an **XGBoost** model (AUC 0.82), and localized RAG query assistant utilizing ChromaDB and NVIDIA NIM.
- **Tech Stack:** `Python`, `FastAPI`, `Flutter 3.x`, `XGBoost`, `ChromaDB`, `NVIDIA NIM (Llama 3.1)`, `Firebase`

### 🚨 EduSafe — AI-Powered Disaster Preparedness Platform
**Repository:** [github.com/Sukhshum2628/Edusafe-Platform](https://github.com/Sukhshum2628/Edusafe-Platform)  
*Emergency Drill & Institutional Safety Command Platform*  
**Live Admin Demo:** [edusafe-613b7.web.app](https://edusafe-613b7.web.app) *(Guest Access Available)*

- **Physics-Based Drill Verification:** Evaluates device accelerometer G-forces and GPS displacement vectors to verify "Drop, Cover, and Hold On" compliance and real evacuation movements.
- **AI Vision Verification:** Integrates Google Gemini 2.5 Flash for camera-verified safety gear inspections.
- **Real-Time Emergency Broadcasting:** Synchronized Socket.IO engine to broadcast real-time global alarms, high-vibration alerts, and dynamic muster point routing.
- **Tech Stack:** `Node.js`, `Express`, `React 19`, `TypeScript`, `React Native (Expo)`, `Socket.IO`, `MongoDB`, `Gemini 2.5 Flash API`, `Tailwind CSS`

### 📝 Flask Blog — AI-Enhanced Publishing Platform
**Repository:** [github.com/Sukhshum2628/Flask-Blog-Website](https://github.com/Sukhshum2628/Flask-Blog-Website)  
*Performance-Optimized Publishing Engine with Asynchronous AI Capabilities*

- **Non-blocking AI Pipeline:** Offloads LLM research and content analysis to background workers via `ThreadPoolExecutor` to maintain high concurrency on constrained runtimes.
- **AI Writing Suite:** Research synthesis using Tavily web search, visual draft diff inspection, and real-time SSE streaming Q&A.
- **Caching & Security:** MongoDB-backed summarization cache to eliminate redundant inference calls, alongside `Flask-Limiter` rate limiting and secure HTTP response headers.
- **Tech Stack:** `Python 3.12`, `Flask`, `MongoDB Atlas`, `Llama 3.1 8B (NVIDIA NIM)`, `Tavily API`, `Bootstrap 5`, `Gunicorn`

---

## 🛠️ Technical Stack

```
[SYSTEM LANGUAGES]      C++17  •  Python  •  TypeScript  •  JavaScript  •  SQL
[BACKEND & APIS]        Node.js  •  Express  •  FastAPI  •  Flask  •  Socket.IO  •  RESTful APIs
[DATABASES & CACHING]   MongoDB  •  MySQL  •  ChromaDB (Vector)  •  Firebase RTDB / Firestore
[CLOUD & DEVOPS]        Docker  •  AWS  •  GitHub Actions (CI/CD)  •  Linux / Bash  •  Vercel
[AI & MACHINE LEARNING] NVIDIA NIM  •  Gemini API  •  XGBoost  •  LangChain  •  ezdxf CAD Engine
[FRONTEND & CLIENT]     React 19  •  React Native (Expo)  •  Flutter  •  Tailwind CSS  •  Vite
[TESTING & ARCH]        GoogleTest  •  Architecture Decision Records (ADR)  •  MSVC / GCC
```

---

## 📊 GitHub Telemetry

<p align="center">
  <a href="https://github.com/Sukhshum2628">
    <img src="https://streak-stats.demolab.com/?user=Sukhshum2628&theme=matrix&hide_border=true&background=0b0f10&ring=55e6a5&fire=66d9ef&currStreakLabel=55e6a5" alt="GitHub Contribution Streak">
  </a>
</p>

<p align="center">
  <img src="https://ghchart.rshah.org/55e6a5/Sukhshum2628" alt="GitHub Contribution Activity Chart">
</p>

### Automated Contribution Grid Snake

<!-- The contribution snake is generated automatically via GitHub Actions (.github/workflows/generate-snake.yml) -->
<p align="center">
  <img src="https://raw.githubusercontent.com/Sukhshum2628/Sukhshum2628/output/github-contribution-grid-snake.svg" alt="GitHub Contribution Snake" onerror="this.src='https://ghchart.rshah.org/55e6a5/Sukhshum2628';">
</p>

---

## 📡 Terminal Transmission / Contact

```bash
$ cat << 'EOF' > transmission.txt
-----------------------------------------------------------------
Name      : Sukhshum Vaishnavi
Email     : sukhsham2628@gmail.com
LinkedIn  : https://www.linkedin.com/in/sukhshum-vaishnavi/
Portfolio : https://sukhshum-portfolio.vercel.app/
Location  : India (IST / UTC+5:30)
Status    : Open to engineering roles, distributed systems, & systems collaborations
-----------------------------------------------------------------
EOF
```

<p align="center">
  <a href="mailto:sukhsham2628@gmail.com"><img src="https://img.shields.io/badge/Email-sukhsham2628%40gmail.com-0b0f10?style=flat-square&logo=gmail&logoColor=55e6a5" alt="Email"></a>
  <a href="https://www.linkedin.com/in/sukhshum-vaishnavi/"><img src="https://img.shields.io/badge/LinkedIn-sukhshum--vaishnavi-0b0f10?style=flat-square&logo=linkedin&logoColor=66d9ef" alt="LinkedIn"></a>
  <a href="https://sukhshum-portfolio.vercel.app/"><img src="https://img.shields.io/badge/Portfolio-sukhshum--portfolio-0b0f10?style=flat-square&logo=vercel&logoColor=55e6a5" alt="Portfolio"></a>
</p>
