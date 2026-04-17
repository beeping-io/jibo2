# 📅 Jibo2 — ROADMAP Changelog

> Historial completo de cambios en `docs/ROADMAP.md`.
> Mantenido automáticamente por el CLI: cada vez que el ROADMAP cambia,
> se añade una nueva entrada al inicio de la sección **History** con el
> diff versus la versión anterior.

---

## 🎯 Snapshot actual

- **Fecha de inicio del proyecto**: 2026-04-17
- **Fecha fin estimada (con 20% margen)**: 2026-12-15
- **Velocidad asumida**: 8 story points / día
- **Estado global**: ✅ En tiempo
- **Última actualización**: 2026-04-17 (trigger: J2-5 closed · F0:M1 at 100% · 8/72 F0)

| #   | Milestone                      | Story points | Inicio est. | Fin est.   | Estado |
| --- | ------------------------------ | ------------ | ----------- | ---------- | ------ |
| F0  | 🏗️ Foundation                  | ~45          | 2026-04-17  | 2026-04-26 | ✅     |
| F1  | 🔓 Reverse Engineering         | ~100         | 2026-04-27  | 2026-05-20 | ✅     |
| F2  | ⚙️ ROS2 Robotics Stack         | ~115         | 2026-05-18  | 2026-06-19 | ✅     |
| F3  | 🖼️ Web Backoffice              | TBD          | 2026-06-01  | 2026-07-03 | ✅     |
| F4  | 🗣️ Voice Pipeline + Benchmarks | TBD          | 2026-06-15  | 2026-08-04 | ✅     |
| F5  | 😊 Expressions + Behavior      | TBD          | 2026-07-13  | 2026-08-14 | ✅     |
| F6  | 🔌 Skills Marketplace Backend  | TBD          | 2026-07-27  | 2026-08-28 | ✅     |
| F7  | 🌐 Marketplace Frontend        | TBD          | 2026-08-10  | 2026-09-11 | ✅     |
| F8  | 📱 iOS App Flutter             | TBD          | 2026-08-24  | 2026-10-16 | ✅     |
| F9  | 🤖 Android App Flutter         | TBD          | 2026-09-21  | 2026-11-13 | ✅     |
| F10 | 🔊 Beeping Integration         | TBD          | 2026-09-07  | 2026-10-23 | ✅     |
| F11 | 🌍 Community Platform          | TBD          | 2026-09-21  | 2026-11-27 | ✅     |
| F12 | 🚀 Launch Prep                 | TBD          | 2026-10-26  | 2026-12-11 | ⚠️     |
| F13 | 👀 Admin Backoffice (paralelo) | TBD          | 2026-07-27  | 2026-09-11 | ✅     |

---

## 📜 History

### [2026-04-17] — Closed J2-5 · 🎉 Milestone F0:M1 complete

**Trigger**: J2-5 closed · 2 SP delivered · **Milestone F0:M1 🛠️ Dev environment + toolchain → 100%**
**Net delta global**: 0 días (M1 cerrado dentro de su ventana estimada)
**Nueva fecha fin estimada**: 2026-12-15 (sin cambio)
**Nuevo estado global**: ✅ (sin cambio)

#### Milestone closed

- **F0:M1 🛠️ Dev environment + toolchain**: 5/5 tasks · 8 SP consumed.

#### Notas

F0 total progress: 8/72 SP (~11%). Velocidad acumulada en la sesión: 8 SP (J2-1 to J2-5) — alineado con la velocidad asumida de 8 SP/día.

Siguientes milestones en F0: M2 (testing), M3 (logging), M4 (secrets), M5 (Firebase), M6 (analytics/crashlytics/perf).

### [2026-04-17] — Closed J2-4 (🎯 Flutter SDK install + doctor docs)

**Trigger**: J2-4 closed · 2 SP delivered
**Net delta global**: 0 días
**Nueva fecha fin estimada**: 2026-12-15 (sin cambio)
**Nuevo estado global**: ✅ (sin cambio)

#### Notas

F0:M1 ahora 4/5 tasks completed (80%). F0 total: 6/72 SP (~8%). Docs-only task — QA postponed to F8:M54 cuando el subproyecto Flutter se scaffolde.

### [2026-04-17] — Closed J2-3 (💻 VSCode recommended extensions)

**Trigger**: J2-3 closed · 1 SP delivered (first task with human QA approval)
**Net delta global**: 0 días
**Nueva fecha fin estimada**: 2026-12-15 (sin cambio)
**Nuevo estado global**: ✅ (sin cambio)

#### Notas

F0:M1 ahora 3/5 tasks completed (60%). F0 total: 4/72 SP (~5%).
Primera tarea que pasa por Human QA Checkpoint con aprobación explícita del owner (banner de recomendaciones + formato al guardar verificados).

### [2026-04-17] — Closed J2-2 (🪝 Install pre-commit + hook install)

**Trigger**: J2-2 closed · 2 SP delivered
**Net delta global**: 0 días (ritmo esperado)
**Nueva fecha fin estimada**: 2026-12-15 (sin cambio)
**Nuevo estado global**: ✅ (sin cambio)

#### Adelantados / Retrasados / Sin cambio

- Todas las fases (F0 – F13): sin cambio.

#### Notas

F0:M1 ahora 2/5 tasks completed (40%). F0 total: 3/72 SP (~4%).
Velocidad observada en esta sesión: J2-1 (1 SP) + J2-2 (2 SP) = 3 SP en ~25 min, ritmo por encima de la asunción de 8 SP/día.

### [2026-04-17] — Closed J2-1 (🐍 Install uv + verify Python 3.12)

**Trigger**: J2-1 closed · 1 SP delivered
**Net delta global**: 0 días (dentro de lo planeado; F0 tenía holgura)
**Nueva fecha fin estimada**: 2026-12-15 (sin cambio)
**Nuevo estado global**: ✅ (sin cambio)

#### Adelantados

- Ninguno (task pequeña, impacto no medible a nivel de fase)

#### Retrasados

- Ninguno

#### Sin cambio

- F0 – F13 (todas mantienen fechas objetivo)

#### Cambios de estado de riesgo

- Ninguno

#### Notas

Primera task cerrada del proyecto. Velocidad observada: 1 SP en una sesión — consistente con la velocidad asumida de 8 SP/día. F0:M1 ahora 1/5 tasks completed (20%).

### [2026-04-17] — Initial ROADMAP creation

**Trigger**: `/worktree-init` bootstrap
**Estado global inicial**: ✅ En tiempo
**Fecha fin estimada**: 2026-12-15

Primera iteración del roadmap de Jibo2. Contexto:

- 14 fases (F0 – F13), 96 milestones (M1 – M96) definidos en `docs/PRODUCTO.md`.
- Proyecto en Linear `🤖 Jibo2` creado con todos los milestones.
- Tareas granulares de F0-F2 creadas (M1-M20, 89 tasks totales, J2-1 a J2-89).
- Tareas de F3-F13 se generarán cuando cada fase arranque en `/worktree-start`.
- F10 (Beeping) y F13 (Admin Backoffice) corren en paralelo y no extienden la línea crítica.
- Velocidad asumida: 8 story points/día. Margen de riesgo: +20%.

Scope incluido:

- 🔓 Ingeniería inversa del Jibo (Fusée Gelée + firmware dump + recovery).
- ⚙️ Stack robótico ROS2 completo.
- 🗣️ Voice pipeline con benchmarks multi-provider (Claude / OpenAI / Gemini / Groq / Llama / Vertex AI para LLM; ElevenLabs / OpenAI / Google / Cartesia / Piper + Skywalker para TTS; Whisper / Deepgram / AssemblyAI / OpenAI para STT).
- 🔌 Marketplace de skills (SDK + CLI + Firestore registry + 3 skills de referencia).
- 🌐 Marketplace frontend + admin backoffice (Next.js).
- 📱 Apps iOS + Android (Flutter) con Beeping ultrasonic pairing.
- 🌍 Comunidad (website, docs, Discord, blog, hackathons).
- 🚀 Launch (beta, security audit, hardware kit, marketing).

Snapshot inicial — ver tabla al inicio del documento.

**Próxima actualización**: automática al cerrar la primera tarea en `/worktree-start`.
