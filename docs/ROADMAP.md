# 📅 Jibo2 — ROADMAP

> Documento vivo. Cada tarea cerrada en `/worktree-start` dispara:
> (1) recálculo de las fechas siguientes (cascade de adelantos/retrasos),
> (2) nueva entrada en `docs/ROADMAP_CHANGELOG.md` con el diff,
> (3) commit conjunto de ambos ficheros.

---

## 🎯 Snapshot actual

- **Fecha de inicio del proyecto**: 2026-04-17
- **Fecha fin estimada (con 20% margen)**: ~2026-12-15
- **Velocidad asumida**: 8 story points / día (single-dev en sesiones profundas)
- **Margen de riesgo aplicado**: +20% sobre la estimación cruda
- **Estado global**: ✅ En tiempo
- **Última actualización**: 2026-04-17 (trigger: J2-4 closed · +2 SP, total 6/72 F0)

## 📊 Métricas del roadmap

- **Fases totales**: 14 (F0 – F13)
- **Milestones totales**: 96 (M1 – M96)
- **Tareas iniciales creadas**: 89 (F0-F2 = M1-M20). Resto se genera por fase cuando arranca.
- **Story points estimados F0-F2**: ~260 pts (suma de estimates de tasks creadas)
- **Solo developer**: Alfred Rivas

## 🗓️ Tabla de fases

| #   | Fase                           | Milestones | Inicio est. | Fin est. (raw) | Fin est. (+20%) | Estado               |
| --- | ------------------------------ | ---------- | ----------- | -------------- | --------------- | -------------------- |
| F0  | 🏗️ Foundation                  | M1-M6      | 2026-04-17  | 2026-04-24     | 2026-04-26      | ✅                   |
| F1  | 🔓 Reverse Engineering         | M7-M12     | 2026-04-27  | 2026-05-15     | 2026-05-20      | ✅                   |
| F2  | ⚙️ ROS2 Robotics Stack         | M13-M20    | 2026-05-18  | 2026-06-12     | 2026-06-19      | ✅                   |
| F3  | 🖼️ Web Backoffice              | M21-M26    | 2026-06-01  | 2026-06-26     | 2026-07-03      | ✅                   |
| F4  | 🗣️ Voice Pipeline + Benchmarks | M27-M36    | 2026-06-15  | 2026-07-24     | 2026-08-04      | ✅                   |
| F5  | 😊 Expressions + Behavior      | M37-M42    | 2026-07-13  | 2026-08-07     | 2026-08-14      | ✅                   |
| F6  | 🔌 Skills Marketplace Backend  | M43-M48    | 2026-07-27  | 2026-08-21     | 2026-08-28      | ✅                   |
| F7  | 🌐 Marketplace Frontend        | M49-M53    | 2026-08-10  | 2026-09-04     | 2026-09-11      | ✅                   |
| F8  | 📱 iOS App Flutter             | M54-M62    | 2026-08-24  | 2026-10-02     | 2026-10-16      | ✅                   |
| F9  | 🤖 Android App Flutter         | M63-M72    | 2026-09-21  | 2026-10-30     | 2026-11-13      | ✅                   |
| F10 | 🔊 Beeping Integration         | M73-M77    | 2026-09-07  | 2026-10-16     | 2026-10-23      | ✅                   |
| F11 | 🌍 Community Platform          | M78-M85    | 2026-09-21  | 2026-11-13     | 2026-11-27      | ✅                   |
| F12 | 🚀 Launch Prep                 | M86-M90    | 2026-10-26  | 2026-11-27     | 2026-12-11      | ⚠️ (margen ajustado) |
| F13 | 👀 Admin Backoffice (paralelo) | M91-M96    | 2026-07-27  | 2026-09-04     | 2026-09-11      | ✅                   |

**Fin estimado global (con margen)**: ~2026-12-15

> **Nota sobre F13**: corre en paralelo a F6-F7, no extiende la línea crítica.
> **Nota sobre F10**: corre en paralelo a F9 (Android), no extiende la línea crítica.

## 🎯 Hitos clave

- 🔓 **Root shell + firmware dumped** → fin de F1 (~2026-05-20)
- 🤖 **ROS2 controlando todo el hardware** → fin de F2 (~2026-06-19)
- 🗣️ **Conversación E2E < 2s latencia** → fin de F4 (~2026-08-04)
- 🏪 **Marketplace con 3 skills publicadas** → fin de F6 (~2026-08-28)
- 📱 **iOS + Android betas activas** → fin de F9 (~2026-11-13)
- 🌍 **Website + Docs + Discord live** → fin de F11 (~2026-11-27)
- 🚀 **Launch público** → fin de F12 (~2026-12-15)

## 📈 Estado por fase (detalle)

### F0 — 🏗️ Foundation (2026-04-17 → 2026-04-26)

- M1: 🛠️ Dev environment + toolchain (5 tasks)
- M2: 🧪 Testing infrastructure (4 tasks)
- M3: 📊 Logging framework (4 tasks)
- M4: 🔐 Secrets + config management (4 tasks)
- M5: 🔥 Firebase project bootstrap (6 tasks)
- M6: 📈 Analytics + Crashlytics + Perf (5 tasks)

### F1 — 🔓 Reverse Engineering (2026-04-27 → 2026-05-20)

- M7: 📋 Hardware documentation (4 tasks)
- M8: 💾 Firmware backup procedure (5 tasks)
- M9: ⚡ Fusée Gelée exploit + root shell (5 tasks)
- M10: 🔍 Firmware dump + análisis (4 tasks)
- M11: 🧩 Kernel + drivers mapping (4 tasks)
- M12: 🚑 Recovery procedure (5 tasks)

### F2 — ⚙️ ROS2 Robotics Stack (2026-05-18 → 2026-06-19)

- M13: 🐧 Linux/Buildroot baseline (4 tasks)
- M14: 🤖 ROS2 cross-compile decision (5 tasks)
- M15: 🎛️ Motor control driver (5 tasks)
- M16: 🖥️ LCD driver (4 tasks)
- M17: 🎙️ Audio I/O driver (4 tasks)
- M18: 📸 Camera driver (4 tasks)
- M19: 👆 Touch sensor driver (3 tasks)
- M20: 🌉 rosbridge + web local baseline (5 tasks)

### F3-F13 — Scope definido en Linear

Tareas granulares se generarán al iniciar cada fase via `/worktree-start`.
Los 96 milestones ya existen en Linear con sus fechas target.

## ⚠️ Riesgos que pueden mover fechas

| Riesgo                             | Impacto potencial                | Mitigación                                   |
| ---------------------------------- | -------------------------------- | -------------------------------------------- |
| 🧱 Brickeo del Jibo                | F1-F2 bloqueadas indefinidamente | Backup + recovery procedure (M8 + M12)       |
| 🐌 Tegra K1 no aguanta ROS2 nativo | F2 +1-2 sem (host companion)     | Evaluación en M14                            |
| 💸 API costs explotan              | F4 paused hasta caps             | Benchmark-driven + Remote Config caps        |
| 🔌 Hardware irremplazable roto     | Proyecto bloqueado               | Spare unit recomendada antes de F1           |
| 🧑‍💻 Solo-dev fatigue                | Timeline +30% si hay parón       | Milestones cortos, QA checkpoints frecuentes |

## 🔗 Referencias

- **Linear project**: `🤖 Jibo2` (id `576a6eda-953d-4ead-8c07-790bed54ce32`)
- **Linear team**: `Jibo2` (key `J2`)
- **GitHub repo**: https://github.com/beeping-io/jibo2
- **Producto**: `docs/PRODUCTO.md`
- **Histórico de cambios del roadmap**: `docs/ROADMAP_CHANGELOG.md`
