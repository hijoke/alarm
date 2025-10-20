# Alarm Android App (Scaffold)

This repository contains a Kotlin DSL-based Android project scaffold configured for:

- Jetpack Compose (Material 3)
- Hilt (DI)
- Room (local persistence)
- Retrofit + OkHttp (network)
- Kotlin Coroutines / Flow
- DataStore (Preferences)

Project configuration:
- Package: `com.hojoke.alarm`
- Min SDK 23 / Target SDK 35
- Kotlin/Java toolchain 17

Structure:
- app/src/main/java/com/hojoke/alarm
  - `AlarmApp.kt` — Hilt-enabled Application
  - `MainActivity.kt` — Compose entry point + preview
  - `di/` — Base DI modules for database, network, dispatchers, DataStore
  - `data/` — Room entities/DAO/DB and Retrofit API service
  - `ui/theme/` — Material 3 theme, typography, colors

Build: Gradle Kotlin DSL with version catalogs and CI-friendly gradle.properties.

Permissions included in AndroidManifest:
- SCHEDULE_EXACT_ALARM
- POST_NOTIFICATIONS
- WAKE_LOCK
- FOREGROUND_SERVICE

This is only a scaffold; add features, tests, and CI as needed.
