# 🔒 Jibo2 — security operations

> Runbooks for rotating secrets, responding to leaks and auditing
> access. Every section is meant to be **executable** — a new
> engineer should be able to follow it step by step without guessing.

Reporting a vulnerability? See [`SECURITY.md`](../SECURITY.md) at the
repo root for the private disclosure policy.

## 🔁 Rotation policy

| Cadence        | Applies to                                         |
| -------------- | -------------------------------------------------- |
| **🟢 Annual**  | Low-risk keys, local dev automation                |
| **🟠 180 d**   | LLM / TTS / STT provider keys, Linear, Beeping     |
| **🔴 90 d**    | Firebase service accounts, OAuth client secrets    |
| **⚫ On event** | Robot SSH key, mobile app signing keys             |
| **🚨 Instant** | Any key known/suspected to be leaked or exfiltrated |

- **Owner:** Alfred Rivas (`alfred@beeping.io`) until the team grows.
- **Trackable:** every rotation opens a Linear issue tagged `security`
  with the rotation date + verification evidence (screenshot, curl
  output, etc.).
- **Windowed:** rotations are never performed on Friday afternoons
  nor within 48 h of a release unless triggered by an incident.

## 📋 Secret inventory

| Secret                                     | Criticality | Cadence    | Impact if leaked                           |
| ------------------------------------------ | ----------- | ---------- | ------------------------------------------ |
| Firebase service account (dev/staging/prod) | 🔴 critical | 90 d       | Full admin on the Firebase project         |
| OAuth client secrets (Google/Apple/GitHub) | 🔴 critical | 90 d       | Impersonation of the app / phishing vector |
| Robot SSH private key                      | 🔴 critical | On event   | Remote hijack of the physical Jibo2        |
| Anthropic API key                          | 🟠 high     | 180 d      | API cost + exfiltration of prompts         |
| OpenAI / Google / Groq / Vertex keys       | 🟠 high     | 180 d      | Same as Anthropic                          |
| ElevenLabs / Cartesia TTS keys             | 🟡 medium   | 180 d      | API cost                                   |
| Deepgram / AssemblyAI STT keys             | 🟡 medium   | 180 d      | API cost + transcripts access              |
| Beeping / Skywalker / AI Agents keys       | 🟠 high     | 180 d      | Ecosystem access                           |
| Linear API token                           | 🟡 medium   | 180 d      | Task/milestone manipulation                |
| iOS App Store Connect API key              | 🔴 critical | 365 d      | Malicious release                          |
| Android Play Store signing key             | 🔴 critical | On event   | Irrecoverable — plan carefully             |

## 🚨 Incident response (leak detected)

Triggered by: `gitleaks` alert, provider notification, manual review,
or third-party report.

### T+0 — Stop the bleed

1. **Confirm** the key is live. `curl` the provider's `me`/`identity`
   endpoint with the leaked key. Record the output.
2. **Revoke** the key at the provider. Every provider offers an
   immediate revocation action — do it before anything else:
   - Anthropic: console.anthropic.com → Settings → API keys → Revoke
   - OpenAI: platform.openai.com → API keys → Revoke
   - Google: console.cloud.google.com → IAM → Service accounts → Disable
   - Firebase: Project settings → Service accounts → Delete
   - Linear: linear.app → Settings → API → Revoke
3. **Do not delete the repo history** yet — you need it for post-mortem.

### T+5 min — Replace

4. Generate a new key at the provider.
5. Store it in **Firebase Secret Manager** (once J2-16 lands) or in your
   local `.env` for dev work. Never commit the new key.
6. Trigger a redeploy so running services pick it up. For serverless
   (Cloud Functions), roll the deployment. For the robot agent, SSH in
   and restart the service.

### T+30 min — Verify

7. Run the relevant service's health check. For LLM keys: one real
   inference. For Firebase: a Firestore read with the new service
   account.
8. Watch cost dashboards for abnormal activity from the old key window.
9. If any unexpected charges appear, open a support ticket with the
   provider and include the revocation timestamp.

### T+24 h — Post-mortem

10. Write a short post-mortem in `docs/postmortems/YYYY-MM-DD-<key>.md`
    using the template below.
11. Open a Linear issue for any follow-up hardening (extra detection,
    narrower scopes, shorter cadence).
12. Close the incident.

### Post-mortem template

```markdown
# Post-mortem: <secret> leaked on <date>

- **Severity:** 🔴 / 🟠 / 🟡
- **Detection:** how we found out + when
- **Exposure window:** earliest possible leak → revocation
- **Blast radius:** what the attacker could do
- **Root cause:** how the key escaped the vault
- **Immediate actions:** revoke, replace, redeploy (with timestamps)
- **Remediation:** guardrails added to prevent a repeat
- **Follow-ups:** Linear tasks opened
```

## 🔧 Per-secret runbooks

### 🔥 Firebase service account (critical)

1. Console: `Firebase console → Project settings → Service accounts`.
2. Click **Generate new private key**, download the JSON. Store it
   immediately in the team vault and delete the download.
3. In Google Cloud IAM, **disable** (don't delete yet) the previous
   service account credential — `Project → IAM & Admin → Service accounts
   → Keys → Disable`.
4. Update `GOOGLE_APPLICATION_CREDENTIALS` everywhere:
   - Local: new path in `.env`.
   - Cloud Functions: redeploy with the new secret injected.
   - Firebase Hosting CI: update the `FIREBASE_SERVICE_ACCOUNT` GitHub
     secret.
5. Verify: `firebase projects:list` succeeds with the new key.
6. After 24 h of clean metrics, **delete** the disabled old credential.

### 🧠 LLM provider keys (Anthropic / OpenAI / Gemini / Groq / Vertex)

1. Generate a new key at the provider console.
2. Update `jibo2-{env}` Firebase Secret Manager entry (`ANTHROPIC_API_KEY`
   etc.) once J2-16 lands. Until then, rotate via `.env` + redeploy.
3. Run `make test-cov` with the new key — no real outbound calls but the
   suite verifies imports.
4. Kick off one real inference with the robot agent, check Langfuse or
   the provider console for the request log.
5. Revoke the old key.

### 🔊 TTS + 🎤 STT provider keys

Same pattern as LLM keys. Verification step is one round-trip of
`synthesize("hello")` / `transcribe(wave)` against fixtures.

### 🐝 Beeping ecosystem keys (Beeping / Skywalker / AI Agents)

1. Rotate inside the Beeping org dashboard (Linear workspace Admin).
2. Update Firebase Secret Manager / `.env`.
3. Run one integration test per surface:
   - Beeping: app ↔ robot pairing with the new key.
   - Skywalker: one voice clip with the benchmarked model.
   - AI Agents: one agent turn via the `AIAgentsTracer` in F4:M36.

### 🤖 Robot SSH key (event-driven)

1. Generate a new ed25519 keypair: `ssh-keygen -t ed25519 -a 100 -f ~/.ssh/jibo2_new`.
2. From the current still-valid session, append the new pubkey to
   `/root/.ssh/authorized_keys` on the robot.
3. Verify you can SSH with the new key.
4. Remove the old pubkey from `authorized_keys`.
5. Update `JIBO2_SSH_KEY` path in `.env`.

### 📱 App signing keys

- **iOS**: App Store Connect API keys rotate annually. Generate new,
  update CI (`APP_STORE_CONNECT_API_KEY`), redeploy TestFlight build,
  revoke old.
- **Android**: the upload key is **irrecoverable**. Rotation requires
  a key upgrade with Google Play Console. **Plan carefully** — treat
  this as a mini-project, not a runbook.

### 📱 Linear API token

1. linear.app → Settings → API → Revoke existing token.
2. Generate a new one with the same scope.
3. Update it everywhere it's used: local `.env` `LINEAR_API_KEY`,
   `/worktree-*` scripts, any CI job that reads Linear.
4. Verify with `curl -H "Authorization: <new>" https://api.linear.app/graphql -d '{"query":"{viewer{name}}"}'`.

## 🧪 Rotation drill

Schedule one drill per quarter for a 🟠/🟡 secret to keep the runbook
fresh:

1. Pick a non-critical key (e.g. a Groq or ElevenLabs dev key).
2. Follow the per-secret runbook end-to-end in a timed session.
3. Update the runbook with anything that surprised you (commands that
   changed, new console navigation, etc.).
4. Keep the total drill time under 30 minutes. If you exceed that, the
   runbook has a step that deserves automation.

## 📊 Audit log expectations

Every rotation must leave:

- A **Linear issue** in `J2-` project tagged `security`, closed with:
  - Secret rotated, revocation timestamp, new key ID fingerprint.
  - Who performed the rotation.
  - Verification evidence (screenshot + one command output).
- A **commit** touching `.env.example` or `docs/security.md` if the
  rotation exposed any gap to fix.
- If prod: a **note in `docs/operations.md`** (when that exists) under
  a `Rotations` section.

No audit log entry ⇒ the rotation didn't happen. Hard rule.

## 🛡️ Defence in depth (reminders)

- `gitleaks` scans every PR + every commit on work branches (CI gate).
- `.env` is **always** gitignored; `.env.example` lives in the repo.
- Firestore + Storage rules default to **deny all** (J2-20, J2-21).
- Firebase **App Check** protects the client surfaces (M5, F0:M6).
- Dev + staging + prod live in **separate Firebase projects** — no
  cross-env credential sharing.
- Skill bundles will be **signed** in F6:M46; unsigned skills are
  rejected at install time.

## 🗓️ Rotation calendar

Automatically recalculated on each rotation; maintained by hand until
the automation task lands:

| Secret                              | Last rotated | Next due   |
| ----------------------------------- | ------------ | ---------- |
| _to be filled at first rotation_    | —            | —          |

When a rotation lands, prepend a row with the date + deadline so the
calendar stays up-to-date without extra effort.
