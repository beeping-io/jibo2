# 🤖 Jibo2 — Robot Social Inteligente

> Resurrección open source del robot social Jibo (2017) convertido en plataforma comunitaria con IA moderna, marketplace de skills, apps móviles e integración con el ecosistema Beeping.

---

## 1. 📋 Información básica

| Campo | Valor |
|---|---|
| **Nombre** | Jibo2 |
| **Tag** | `[J2] 🤖 Jibo2 — Robot Social Inteligente` |
| **Versión inicial** | `0.0.0` |
| **Fecha de inicio** | 2026-04-17 |
| **Owner** | Alfred Rivas (`alfred@beeping.io`) |
| **Organización Linear** | Beeping |
| **Licencia** | Apache 2.0 |
| **Estado** | 🟧 early_development |

## 2. 🎯 Qué es

Jibo2 es un proyecto de ingeniería inversa y desarrollo open source para **resucitar un robot social Jibo (2017, versión comercial)** cuyos servidores fueron desconectados en 2019, transformándolo en un **asistente robótico personal con IA moderna** y **plataforma comunitaria**.

Inspirado en la Jibo Research Platform del MIT Media Lab pero desarrollado de forma independiente, Jibo2 aspira a ser la **base open source** que la comunidad pueda reutilizar para resucitar sus propios Jibos, extenderlos con skills propias y construir comportamientos sociales avanzados.

## 3. 🏆 Objetivo medible

> **"Jibo2 responde al wake-word, mantiene una conversación hablada fluida con personalidad, y se mueve de forma expresiva en respuesta al contexto — validado en una demo de 5 minutos con un humano en el mismo cuarto."**

Con sub-objetivos por fase:

1. 🔓 **Root shell** obtenido en el Tegra K1 + firmware completo dumped.
2. 🤖 **ROS2** controlando los 3 ejes + LCD + audio + cámara + touch.
3. 🗣️ **Pipeline conversacional E2E** funcionando con latencia < 2s.
4. 🏪 **Marketplace de skills** operativo con 3 skills de referencia publicadas.
5. 📱 **Apps iOS + Android** (Flutter) en beta.
6. 🌍 **Comunidad activa** con documentación, Discord, blog y contribuidores externos.

## 4. 🚧 Restricciones clave

- 🔒 **Hardware fijo**: un único Jibo (NVIDIA Tegra K1, ~2GB RAM, Linux/Buildroot). No se puede cambiar el SoC.
- 🔓 **Exploit one-shot**: Fusée Gelée requiere poner el SoC en RCM mode y flashear payload — cuidado extremo para no brickear.
- 💾 **Reversibilidad obligatoria**: backup completo de firmware antes de tocar nada + procedimiento de restore documentado.
- 🌐 **Sin dependencia cloud obligatoria**: al menos una ruta funcional offline (degradación progresiva si se cae internet).
- 🔊 **Latencia E2E**: < 2s desde fin-de-habla humana a inicio-de-habla Jibo2.
- 🏠 **Red local**: Jibo2 vive en LAN WiFi + interfaz `http://jibo2.local`.
- 👤 **Solo-developer**: branch protection con self-merge (`gh pr merge --admin`).
- 💸 **Presupuesto APIs acotado**: límite mensual configurable + modo degradado offline.

## 5. 🌍 Entorno y distribución

| Aspecto | Detalle |
|---|---|
| **Dev environment** | macOS (darwin) + conexión al Jibo por USB/Ethernet/WiFi |
| **Runtime del robot** | Tegra K1 (posiblemente + host companion RPi5/NUC si onboard no aguanta) |
| **Backend / backoffice** | Firebase (Firestore, Functions, Storage, Auth, FCM, Analytics, Crashlytics, Perf, Remote Config, App Check, Dynamic Links, Hosting, App Distribution, Test Lab, Vertex AI, ML Kit) |
| **Web frontend** | Next.js desplegado en Firebase Hosting |
| **Apps móviles** | Flutter → iOS + Android (una base, dos builds) |
| **Distribución** | Open source público en GitHub (Apache 2.0) |
| **Package registries** | GitHub Releases (fallback), pub.dev (Flutter packages), PyPI (agente Python) |

## 6. ✅ Alcance (qué incluye)

### Hardware & sistema
- 🔓 Exploit Fusée Gelée + obtención de root shell
- 💾 Dump completo de firmware + mapeo de hardware
- 🚑 Procedimiento de recovery / restore documentado
- 🐧 Linux/Buildroot baseline funcional

### Robótica
- ⚙️ ROS2 + rosbridge controlando 3 ejes + LCD circular + audio + cámara + touch
- 🎛️ Drivers individuales por subsistema
- 🌉 Interfaz web local `http://jibo2.local`

### Voice + AI
- 🎙️ Pipeline STT → LLM → TTS end-to-end con streaming
- 🔬 **Benchmarks exhaustivos**:
  - **LLM**: Claude (Opus/Sonnet/Haiku) · OpenAI · Gemini · Groq · Llama local · Vertex AI
  - **TTS**: ElevenLabs · OpenAI TTS · Google Cloud TTS · Cartesia · Piper local · **Skywalker** (modelo específico)
  - **STT**: Whisper local · Deepgram · AssemblyAI · OpenAI Whisper API
- 🤖 **Dual-stack agente**: provider independiente + plataforma AI Agents de Beeping
- 🎯 Wake-word detection
- 🎚️ Voice Activity Detection (VAD)

### Expresiones y comportamiento
- 🎭 LCD expression system (mocks → real) sincronizado con visemas
- 💃 Movement patterns library
- 👂 Sound source localization + head tracking
- 👤 Face detection + person recognition (ML Kit)

### Marketplace
- 🧩 Skills SDK Python + plugin architecture
- ⌨️ CLI `jibo2-cli` (new-skill, publish, install)
- 🗄️ Registry (Firestore + Cloud Functions + Storage)
- 🔐 Skill signing + sandbox
- 🔄 Versioning + auto-update
- 📦 3 skills de referencia (timer, weather, music)

### Frontend web
- 🏪 Marketplace público (landing, search, skill pages, reviews)
- 👨‍💻 Developer portal (publicar, gestionar skills)
- 👀 **Admin backoffice** (robots, users, skills, métricas, moderación, billing)
- 🔑 Firebase Auth (Google/Apple/GitHub)

### Apps móviles (Flutter)
- 📡 Pairing vía **ultrasonido (Beeping SDK)** — sin QR, sin BT
- 🎙️ Push-to-talk
- 📸 Envío de foto al robot → mostrar en LCD
- 🎥 Live camera view
- 🕹️ Remote control (movement + expressions)
- 🛒 Browse + install skills
- 🔔 Push notifications (FCM)
- ⚙️ Settings + perfiles multi-usuario

### Beeping integration
- 📡 Pairing robot↔app por ultrasonido
- 🔑 Auth token exchange vía ultrasonido
- 📤 Send-to-robot (foto/URL/mensaje)
- 🎯 Ultrasonic skill activation

### Comunidad
- 🌐 Website `jibo2.dev`
- 📚 Docs (Docusaurus)
- 📝 Blog (dev updates + RE content)
- 💬 Discord server
- 🗣️ Forum / GitHub Discussions
- 🗺️ Public roadmap
- 📊 Status page
- 📧 Newsletter
- 🏆 Hackathons + bounties

## 7. ❌ Qué NO incluye

- ❌ Movilidad (Jibo2 no tiene ruedas)
- ❌ Reconocimiento emocional avanzado (más allá de presencia/no-presencia, sonrisa/seriedad)
- ❌ Multi-robot sync (cada Jibo2 es autónomo)
- ❌ Certificaciones formales (CE, FCC, HIPAA) — proyecto personal/comunitario
- ❌ Persistencia cross-device del estado (cada Jibo2 vive en su robot físico)
- ❌ App móvil con funcionalidad sin robot conectado (el robot es el producto)
- ❌ Integraciones HomeKit / Matter en v1 (diferidas)

## 8. 🔄 Cambios de alcance

- Cualquier cambio de scope (añadir/eliminar fase o milestone, ajustar story points, recalibrar velocidad) dispara una entrada en `docs/ROADMAP_CHANGELOG.md` con trigger `"Scope change"` o `"Velocity recalibration"`.
- El scope v1 está congelado en este documento. Cambios requieren decisión explícita documentada.

## 9. 🧭 Principios de producto

1. **♻️ Reversibilidad**: cualquier paso de hardware debe ser revertible. Backup antes que acción.
2. **📡 Offline-first para lo crítico**: Jibo2 sigue vivo sin internet (degradado pero funcional).
3. **🔍 Observabilidad extrema**: logs detallados en debug, métricas siempre, Crashlytics + Perf Monitoring desde día 1.
4. **📊 Benchmark-driven**: decisiones de API/modelo basadas en datos, no en marketing.
5. **🎨 UX antes que backend**: pantallas mock primero, luego conectar.
6. **🧪 Tests estrictos**: lint 0 warnings, tests verdes antes de cerrar tarea.
7. **🍽️ Dogfooding**: usar Beeping, Skywalker y AI Agents en un producto físico real.
8. **🌍 Open source desde día 1**: cada commit público, roadmap público, docs públicas.
9. **🤝 Comunidad primero**: diseñar APIs + SDK para terceros, no solo para nosotros.
10. **🧠 Personalidad coherente**: Jibo2 tiene carácter propio, no es un chatbot plano.

## 10. 🔁 Flujo principal

1. 💤 **Standby**: pantalla con ojo dormido, logging mínimo.
2. 👂 **Wake-word detectado** → gira cabeza hacia fuente del sonido (localización).
3. 📝 **Listening**: STT streaming, expresión "atento" en LCD.
4. 🧠 **Thinking**: LLM procesa transcript + historial + contexto del robot.
5. 🗣️ **Speaking**: TTS streaming, visemas sincronizados, LCD expresivo, movimiento contextual.
6. 🧩 **Skill invocation** (opcional): si el LLM invoca una skill, ejecuta + retorna.
7. 💤 **Vuelta a standby** tras N segundos de silencio.

### Flujos secundarios
- 📱 Usuario envía foto desde la app → Jibo2 la muestra en LCD + comenta.
- 🔊 Pairing nuevo dispositivo vía ultrasonido (Beeping).
- 🔄 Auto-update de skills desde marketplace.
- 🎥 Owner abre live camera feed desde la app.

## 11. ⚠️ Estados y errores

| Estado | Descripción |
|---|---|
| `booting` | Arranque del robot, health checks |
| `standby` | Esperando wake-word |
| `listening` | Transcribiendo voz |
| `thinking` | LLM procesando |
| `speaking` | TTS + movimiento |
| `skill_running` | Ejecutando skill |
| `offline` | Sin internet, modo degradado |
| `error` | Error recuperable (mostrado en LCD) |
| `recovery_mode` | Estado crítico, intervención manual requerida |
| `updating` | OTA en curso |

## 12. 📐 Requisitos no funcionales

- 🕐 **Latencia E2E** < 2s (wake-word → inicio habla)
- 🔊 **Audio** sin cortes ni clipping audibles
- 📊 **100% de interacciones logueadas** en modo debug
- 🧪 **Coverage > 70%** en código Python del agente y del SDK
- 💾 **Persistencia local** de historial de conversación (SQLite on-device)
- 🔒 **Recovery documentado** + backup firmware obligatorio
- 📱 **Apps** funcionan en iOS ≥ 15 y Android ≥ 10
- 🌐 **Backoffice** carga en < 2s en 4G
- 🚀 **CI** < 10 min por build
- 🔐 **Secretos** nunca en repo (Firebase Secret Manager / Remote Config encriptado)

## 13. 🛠️ Stack técnico

| Capa | Tecnología |
|---|---|
| **Exploit** | ShofEL2-for-T124, fusee-launcher.py |
| **OS robot** | Linux/Buildroot (existente, posible kernel custom) |
| **Robótica** | ROS2 Humble + rosbridge_suite |
| **Agente** | Python 3.12 + provider-abstraction layer |
| **LLM providers** | Claude SDK, OpenAI, Gemini, Groq, Llama (Ollama), Vertex AI |
| **TTS providers** | ElevenLabs, OpenAI, Google Cloud TTS, Cartesia, Piper, Skywalker |
| **STT providers** | Whisper local, Deepgram, AssemblyAI, OpenAI Whisper |
| **Audio** | PortAudio / sounddevice |
| **DB on-device** | SQLite |
| **Backend** | Firebase (Firestore, Functions, Storage, Auth, FCM, Analytics, Crashlytics, Perf, Remote Config, App Check, Dynamic Links, Hosting, App Distribution, Test Lab, Vertex AI, ML Kit) |
| **Backoffice web** | Next.js 14 + TypeScript + Tailwind + Firebase SDK |
| **Marketplace web** | Next.js 14 + TypeScript + Tailwind |
| **Apps móviles** | Flutter (iOS + Android) |
| **Docs** | Docusaurus 3 |
| **Packaging Python** | uv + ruff strict |
| **CI/CD** | GitHub Actions + Firebase App Distribution |
| **Monorepo** | Turborepo (web) + separate repos (Python agent, Flutter app) |

## 14. 🧱 Componentes principales

1. **`jibo2-robot`** — Agente Python on-device (ROS2 nodes + voice pipeline + skills runtime).
2. **`jibo2-skills-sdk`** — SDK Python para que devs escriban skills.
3. **`jibo2-cli`** — CLI dev tool (new-skill, publish, install, test).
4. **`jibo2-firmware-tools`** — Scripts de exploit + dump + recovery.
5. **`jibo2-backoffice`** — Next.js admin (robots, users, skills review, métricas).
6. **`jibo2-marketplace`** — Next.js público (browse skills, developer portal).
7. **`jibo2-app`** — Flutter (iOS + Android).
8. **`jibo2-docs`** — Docusaurus.
9. **`jibo2-functions`** — Cloud Functions (publish pipeline, auth triggers, moderación).

## 15. 🔌 Integraciones externas

- **🔊 Beeping Platform** (propia) — pairing + send-to-robot + auth via ultrasonido
- **🌌 Skywalker** (propia) — voice stack como candidato de benchmark
- **🤖 AI Agents** (propia) — plataforma multi-agente como provider alternativo
- **🔥 Firebase** (Google) — backend completo
- **🧠 Anthropic Claude** — provider LLM primario
- **OpenAI · Google AI · Groq · Meta Llama** — providers alternativos
- **ElevenLabs · Cartesia · Deepgram · AssemblyAI** — voice providers
- **GitHub** — hosting código, OAuth, releases
- **Apple / Google OAuth** — login apps

## 16. 🎯 Decisiones técnicas

### Decisiones tomadas
- ✅ **Flutter** para apps (una base → iOS + Android)
- ✅ **Firebase** como backend universal
- ✅ **Next.js** para backoffice + marketplace
- ✅ **ROS2 Humble** para capa robótica
- ✅ **Python 3.12** para agente on-device
- ✅ **Apache 2.0** como licencia
- ✅ **Nombre** = `Jibo2`

### Decisiones pendientes (se resolverán en ejecución)
- ⏳ ¿Agente corre onboard en Tegra K1 o host companion (RPi5/NUC)?
- ⏳ ¿Kernel Buildroot existente suficiente o se recompila custom?
- ⏳ ¿ROS2 compila nativo para ARMv7 del Tegra K1 o se containeriza?
- ⏳ ¿Wake-word engine? (Porcupine, OpenWakeWord, Snowboy fork...)
- ⏳ ¿Modelo Skywalker específico para el benchmark? (se concreta en Phase 4)

## 17. 👥 Usuarios target

### Primarios
- 👤 **Alfred Rivas** (owner, developer principal, dogfood user)

### Secundarios
- 👨‍👩‍👧 **Familia + amigos** del owner (usuarios cotidianos del Jibo2 físico)

### Comunidad
- 🛠️ **Developers** que quieran resucitar su propio Jibo siguiendo la guía
- 🧩 **Skill developers** que publiquen extensions en el marketplace
- 🔬 **Researchers** interesados en social robotics / HRI
- 📺 **Content creators** (YouTube, blog) interesados en el proceso de RE

## 18. 📈 Métricas de éxito

### Técnicas
- ⏱️ **Latencia E2E** (wake-word → habla): p50 < 2s, p95 < 3s
- 🎯 **Wake-word accuracy**: > 95% TPR, < 1/hora FPR
- 🚀 **Uptime del robot**: > 99% mensual
- 🧪 **Test coverage**: > 70%
- 🟢 **CI green rate**: > 95%

### Producto
- 📦 **Skills publicadas** en marketplace: ≥ 20 al cierre del v1
- 👥 **Robots registrados** (otros Jibos resucitados por la comunidad): ≥ 5 en 6 meses post-launch
- 💬 **Interacciones/día** (owner): ≥ 20
- 📱 **Downloads** apps móviles: ≥ 500 en 3 meses post-launch

### Comunidad
- ⭐ **GitHub stars** org: ≥ 1000 en 6 meses
- 💬 **Discord members** activos: ≥ 100
- 📝 **Contribuidores** externos con PR mergeado: ≥ 10
- 📺 **Visualizaciones** blog/YouTube del proceso de RE: ≥ 50k

## 19. 🔥 Riesgos y mitigaciones

| Riesgo | Severidad | Mitigación |
|---|---|---|
| 🧱 **Brickeo del Jibo** | 🔴 Crítica | Backup completo firmware antes de cualquier flash. Procedimiento recovery. Segunda unidad "cold spare" recomendada. |
| 🐌 **Tegra K1 insuficiente** | 🟠 Alta | Fallback a host companion (RPi5/NUC) desde la Phase 2. Arquitectura preparada desde día 1. |
| 💸 **Costes APIs descontrolados** | 🟠 Alta | Límite mensual configurable + modo offline degradado. Benchmark de costes en Phase 4. |
| 🔌 **Piezas HW irremplazables** | 🟠 Alta | Documentar interfaces para que terceros reemplacen piezas. Catalogar en Phase 1. |
| 📜 **Issues legales RE** | 🟡 Media | No publicar blobs con copyright. Documentar procedimientos sin distribuir firmware. Apache 2.0 con disclaimers. |
| 🧑‍💻 **Solo-developer fatigue** | 🟡 Media | Milestones granulares, QA humano frecuente, roadmap realista con 20% margen, comunidad desde día 1. |
| 🌍 **Comunidad no despega** | 🟡 Media | Contenido atractivo (RE en YouTube), docs impecables, hackathons, primeros skills "wow", bounties. |
| 🔊 **Skywalker inmaduro en voice** | 🟢 Baja | Benchmark compara, si Skywalker pierde se usa provider externo y se mejora Skywalker en su proyecto. |

## 20. 📅 Timeline

> 13 fases · ~60 milestones · ~32 semanas (~8 meses) de trabajo concentrado.
> Inicio: **2026-04-17** · Fin estimado (con 20% margen): **~2026-12-15**.

### Orden lógico global
Setup → Tests → CI/CD → UX mocks → Logging → Funcionalidad → Tests automáticos → QA humano → Scripts documentados.

### Fases

| # | Fase | Semanas | Entregable | Versión |
|---|---|---|---|---|
| 0 | 🏗️ Foundation | 0-1 | Dev env + testing infra + logging + Firebase bootstrap | 0.1.0 |
| 1 | 🔓 Reverse Engineering | 1-4 | Root shell + firmware dumped + recovery doc | 0.2.0 |
| 2 | ⚙️ ROS2 Robotics Stack | 4-8 | Drivers controlando todos los subsistemas | 0.3.0 |
| 3 | 🖼️ Web Backoffice (mocks → real) | 6-10 | Admin dashboard controlando robot | 0.4.0 |
| 4 | 🗣️ Voice Pipeline + Benchmarks | 8-14 | E2E < 2s con multi-provider | 0.5.0 |
| 5 | 😊 Expressions + Behavior | 12-16 | LCD + movimientos sincronizados con voz | 0.6.0 |
| 6 | 🔌 Skills Marketplace Backend | 14-18 | SDK + CLI + Firestore registry + 3 skills | 0.7.0 |
| 7 | 🌐 Marketplace Frontend | 16-20 | Next.js marketplace público + dev portal | 0.8.0 |
| 8 | 📱 iOS App (Flutter) | 18-24 | TestFlight beta | 0.9.0 |
| 9 | 🤖 Android App (Flutter) | 22-28 | Google Play internal testing | 0.10.0 |
| 10 | 🔊 Beeping Integration | 20-26 | Pairing + send-to-robot ultrasónico | 0.11.0 |
| 11 | 🌍 Community Platform | 22-30 | Website + docs + Discord + blog | 0.12.0 |
| 12 | 🚀 Launch Prep | 28-32 | Beta program + security + marketing | 0.13.0 |
| 13 | 👀 Admin Backoffice completo | 14-20 | Moderación + billing + remote config | (integrado en 3) |

Los milestones granulares de cada fase se crearán en Linear en el Paso 7 de `/worktree-init`.

---

## 🔗 Referencias

- **Linear project** (se creará): Jibo2
- **GitHub repo**: pendiente de crear
- **Roadmap vivo**: `docs/ROADMAP.md`
- **Historial roadmap**: `docs/ROADMAP_CHANGELOG.md`
- **Memoria proyecto**: `MEMORY.md`
- **Convenciones**: `CLAUDE.md`

## 📜 Historial de este documento

| Fecha | Cambio |
|---|---|
| 2026-04-17 | Creación inicial vía `/worktree-init`. |
