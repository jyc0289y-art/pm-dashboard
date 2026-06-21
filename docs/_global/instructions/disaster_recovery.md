# 재해 복구 표준 — 모든 P 프로젝트 공통 패턴

> **레벨**: 모듈 지침 (~/.claude/instructions/disaster_recovery.md)
> **로드 조건**: 맥북 소실 대비, 다른 PC 복원, mirror·worktree 운영 시 수동 로드
> **시행**: 2026-05-09 (P2.17.1.0 세션에서 정립, 사용자 명시 요청)
> **🛡 보험 사본 (자가완결 종합 기록)**: P2 `docs/20260509_122807_맥북소실대비_재해복구_표준_정립_종합기록.md` — 본 모듈이 ~/.claude/ 위치라 자동 동기화 안 됨에 대한 안전망 (본 모듈 본문 사본 + 모든 관련 자산 cross-reference 보존)

---

## 핵심 원칙

**사용자 홈(`~/.claude/`) 자산은 iCloud·GitHub 어디에도 자동 동기화 안 됨.**
맥북 소실 시 P 번호 시스템·세션 컨텍스트·도메인 메타·글로벌 지침 모두 누락 위험.

→ **모든 P 프로젝트는 다음 표준 인프라 보유 의무**:
1. `memory/_user_claude_mirror/` 디렉토리 (~/.claude/ 백업, git 추적)
2. `scripts/mirror_user_claude.sh` (양방향 sync 도구)
3. `docs/RECOVERY.md` (clean Mac 복원 가이드)
4. 정기 mirror 갱신 (수동 또는 cron)

> ⚠️ **알려진 실패 유형 — 조용한 백업 중단 (2026-06-17 P31 발견·복구)**: 전역 자산 백업용 cron(`claude_sync_runner.sh`)이
> **2026-03-28부터 ~2.5개월 silent failure**. 원인 = ① **cron 프로세스에 Full Disk Access 부재** →
> iCloud Drive(`~/Library/Mobile Documents/`) 쓰기 시 `cp: Operation not permitted`(EPERM),
> ② `set -euo pipefail` + 첫 대상 CLAUDE.md 실패 → 스크립트 전체 즉사(나머지 전부 미백업),
> ③ `registries/`(P번호 SSOT)가 애초에 백업 대상에서 누락.
> **해결 = 훅 기반 백업 전환**: `~/.claude/scripts/claude_home_backup.sh`(쓰기 probe + 실패 허용 집계 + registries 포함 + API 키 마스킹)를
> Stop(30분 throttle)·SessionEnd 훅에서 실행. 훅은 앱 컨텍스트라 iCloud 쓰기 가능(실측 확인).
> cron은 robust wrapper로 축소(FDA 있으면 보조, 없으면 probe에서 무해 종료). **헬스체크: `~/.claude/.cache/home_backup/status.txt`**.
> **교훈**: 백업은 *성공 로그의 최신성*을 주기 점검할 것 — silent failure가 가장 위험. (cron 동작 가정 금지)

---

## 1. 미러 대상 (모든 프로젝트 공통)

| 사용자 홈 경로 | 프로젝트 mirror 경로 | 비고 |
|---------------|---------------------|------|
| `~/.claude/registries/{P번호}.md` | `memory/_user_claude_mirror/registries_{P번호}.md` | P 번호 SSOT |
| `~/.claude/projects/{인코딩}/memory/MEMORY.md` | `memory/_user_claude_mirror/memory_MEMORY.md` | 자동 메모리 인덱스 |
| `~/.claude/projects/{인코딩}/memory/*.md` | `memory/_user_claude_mirror/{filename}.md` | 사용자 도메인 메타 등 |
| `~/.claude/CLAUDE.md` | `memory/_user_claude_mirror/global_CLAUDE.md` | 글로벌 지침 |
| `~/.claude/instructions/*.md` | `memory/_user_claude_mirror/instructions/` | 모듈 지침 (본 파일 포함) |
| `~/.claude/plans/{프로젝트 plan}` | `memory/_user_claude_mirror/plans/` | 활성 plan만 |

⚠️ **인코딩**: `~/.claude/projects/`는 프로젝트 디렉토리 절대 경로를 `-`로 인코딩 사용
예: `/Users/jyc/.../GEANT4_claude` → `-Users-jyc-Library-Mobile-Documents-com-apple-CloudDocs-GEANT4-claude`

---

## 2. 표준 mirror 스크립트 템플릿

각 프로젝트 루트에 `scripts/mirror_user_claude.sh`로 배치. 기준 구현은 P2 (`~/.../GEANT4_claude/scripts/mirror_user_claude.sh`) 참조.

### 모드
- **`--to-project`** (백업): `~/.claude/` → 프로젝트 mirror (정기 사용)
- **`--to-home`** (복원): mirror → `~/.claude/` (clean Mac 복원 시)
- **`--status`** (read-only): 차이만 확인
- **(default 양방향)**: mtime 비교로 더 최신을 유지

### 충돌 처리
- 양쪽 모두 변경 시 mtime 더 최신 우선 + 백업 (`.conflict.YYYYMMDD_HHMMSS`)
- 양쪽 같으면 skip
- 한쪽만 있으면 신규 복사

---

## 3. RECOVERY.md 템플릿 (clean Mac 복원 7단계)

```markdown
# 복구 가이드 — Clean Mac에서 본 프로젝트 완전 복원

## 1단계: iCloud 또는 GitHub clone
   옵션 A (iCloud Drive 자동, Apple ID 같으면)
   옵션 B (GitHub clone, PAT/SSH 키 필요)

## 2단계: ~/.claude/ 자산 복원
   ./scripts/mirror_user_claude.sh --to-home

## 3단계: 도메인 의존성 설치
   (프로젝트별: GEANT4 / Node.js / Python 등)

## 4단계: 보조 도구 (Qt5, brew 등)

## 5단계: 빌드

## 6단계: Smoke test
   (프로젝트별 검증 명령)

## 7단계: worktree 재생성 (선택)
```

---

## 4. mirror 갱신 시점 (의무 + 권장)

### 의무
- 새 P 번호 부여 시 (`~/.claude/registries/{P번호}.md` 갱신됨)
- 사용자 도메인 메타 수정 시 (`user_*.md` 갱신)
- 글로벌 지침 변경 시

### 권장
- 매 세션 마무리 시
- 큰 작업 단위 git commit 직전·직후
- cron 자동화 (예: 매일 18:00)

### Cron 예시
```bash
# crontab -e
0 18 * * * cd "$HOME/Library/Mobile Documents/com~apple~CloudDocs/{project}" && ./scripts/mirror_user_claude.sh --to-project >> /tmp/mirror.log 2>&1
```

---

## 5. 보안 원칙

- **모든 P repo는 private 권장** (사용자 도메인·세션 데이터 포함 가능)
- 정기 점검: `curl -s -o /dev/null -w "%{http_code}\n" https://github.com/<owner>/<repo>` → 404 OK / 200 노출
- mirror 디렉토리에 `.env`, credentials, API key 등 민감 파일 절대 포함 금지
- mirror 스크립트의 화이트리스트 방식으로 의도된 자산만 복사

---

## 6. 연결성 표준

각 프로젝트는 다음 cross-reference 보유:
- `memory/sessions/registry.md` (또는 SSOT) ↔ `memory/_user_claude_mirror/registries_{P}.md` (mirror)
- `memory/sessions/P{X}.md` (세션지침) ↔ git commit 메시지에 세션 번호 인용
- `memory/issues/_index.md` ↔ commit 메시지에 ISS-NNN 인용
- `docs/MC_PITFALLS.md` (또는 lessons_learned.md) ↔ commit 메시지에 PIT-NNN 인용
- `reports/test_reports/` ↔ TR-NNN 번호 cross-ref

→ 어떤 자산에서 시작해도 다른 자산으로 navigate 가능.

---

## 7. 신규 P 프로젝트 적용 절차

1. 프로젝트 디렉토리 생성
2. `git init` + GitHub private repo 연결
3. `mkdir -p memory/_user_claude_mirror`
4. `scripts/mirror_user_claude.sh` 복사 (기준 구현은 P2 참조)
   - 프로젝트 루트 + `~/.claude/projects/{인코딩}` 부분만 갱신
5. `docs/RECOVERY.md` 작성 (프로젝트별 도메인 의존성 추가)
6. 첫 mirror 실행: `./scripts/mirror_user_claude.sh --to-project`
7. git commit + push + tag (예: `v0.1-recovery-baseline`)

---

## 8. 검증 체크리스트

```bash
# 1. mirror 디렉토리 존재
ls memory/_user_claude_mirror/registries_{P}.md
ls memory/_user_claude_mirror/global_CLAUDE.md
ls memory/_user_claude_mirror/instructions/

# 2. mirror 스크립트 존재 + 실행 가능
ls -la scripts/mirror_user_claude.sh

# 3. RECOVERY.md 존재
ls docs/RECOVERY.md

# 4. private 보안
curl -s -o /dev/null -w "%{http_code}\n" https://github.com/{owner}/{repo}  # 404 OK

# 5. mirror 정상 작동
./scripts/mirror_user_claude.sh --status
```

위 모두 ✅이면 **재해 복구 표준 충족**.

---

## 9. 변경 이력

| 날짜 | 세션 | 변경 |
|------|------|------|
| 2026-05-09 | P2.17.1.0 | 본 모듈 신규 작성. 사용자 명시 요청으로 모든 P 프로젝트 공통 패턴 정립. P2 기준 구현 완료 (mirror_user_claude.sh + RECOVERY.md + memory/_user_claude_mirror/) |
| 2026-06-17 | P31 (HJ 정기검사 세션) | 전역 cron 백업이 2026-03-28부터 silent failure(FDA 부재 EPERM + set -e 즉사 + registries 누락)임을 발견·즉시 복구. 훅 기반 백업 `~/.claude/scripts/claude_home_backup.sh` 도입(Stop/SessionEnd), cron은 robust wrapper로 축소. 헬스체크 `~/.claude/.cache/home_backup/status.txt`. 「알려진 실패 유형」 콜아웃 추가 |
| 2026-06-17 (재검토) | P31 | 충분성 재검토로 7개 잔존 격차 발견·5개 즉시 보완: `modules/`·`plans/`·**비-iCloud 프로젝트**(`~/developer/*`·`~/Dstream`의 .claude/CLAUDE.md+memory/sessions) 백업 대상 추가(146→201개), `session_start.sh`에 **silent-failure 알람**(마지막 성공>48h 경고) + 세션시작 백업(3번째 트리거) 추가. 미해결 2건 = **iCloud 외(GitHub) 이중화 미설정**(전역지침 GitHub 사본은 P2 미러뿐, stale), ICRPlink 원격 없음 |
