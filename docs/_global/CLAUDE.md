# Claude 글로벌 지침

**필수: 새 세션 시작 시 `~/.claude/registries/{P번호}.md`를 읽고 P번호를 부여하여 첫 응답에서 안내하라. 상세 → "세션 컨텍스트 포크 시스템" 섹션 참조.**
**⚠️ 레지스트리 SSOT (2026-04-16 이관)**: iCloud 내 `{프로젝트}/memory/sessions/registry.md`는 더 이상 SSOT가 아니며 MOVED stub만 남아 있다. 실제 SSOT는 `~/.claude/registries/{P번호}.md` (iCloud 외부, 동기화 지연 없음). 새 세션 등록/조회는 반드시 이 경로를 사용하라.

## Worker(부하 LLM) 활용 규칙

Worker(Ollama/Gemini CLI)로 토큰 효율 향상 → 같은 요금제 내 처리량 극대화. 품질 훼손 금지.
**핵심 원칙**: 사실 확인(요약/추출)은 위임 OK, 사실 생성(새 내용)은 Claude 검수 필수.
→ **상세 규칙**: `~/.claude/instructions/worker_rules.md` 참조
→ **실시간 데이터(항공권/환율 등)**: `~/.claude/instructions/realtime_data.md` 참조

## 콘텐츠 무단 누락 금지 (Content Preservation Rule)

기존 결과물(보고서, 문서, 코드 등)을 수정·업데이트할 때, **사용자가 명시적으로 삭제/제거를 요청하지 않은 기존 콘텐츠는 절대 누락시키지 않는다.**

### 원칙
1. **추가는 자유, 삭제는 허가제**: 새로운 콘텐츠 추가는 자유롭게 가능하나, 기존 콘텐츠의 삭제·축약·생략은 사용자의 명시적 요청이 있을 때만 허용
2. **섹션 교체 시 전수 확인**: 기존 섹션을 새 내용으로 교체할 때, 교체 전 섹션에 포함된 모든 정보 항목이 새 섹션에도 존재하는지 확인
3. **의심스러우면 유지**: 특정 콘텐츠의 포함 여부가 불확실하면 포함하는 쪽을 선택

### 적용 범위
- HTML/PDF 보고서, 문서 파일
- 코드 파일의 기존 기능·주석
- 데이터 파일의 기존 항목

### 위반 시
- 누락이 발견되면 즉시 복원 (새 콘텐츠를 유지하면서 누락분 추가)
- "이전 버전에는 있었는데 왜 빠졌냐"는 피드백 = 이 규칙 위반

## 자율개발모드

사용자가 "자율개발모드" 요청 시 질문 없이 스스로 판단하여 기능 구현·버그 수정·개선을 진행.
→ **상세 규칙**: `~/.claude/instructions/autonomous_dev.md` 참조

## 함정 관리 시스템 (TRAP)

프로젝트 제작 과정에서 겪은 시행착오를 **TRAP-NNN** 번호로 관리하여 같은 실수 반복을 방지한다.
- **기록 위치**: `{프로젝트}/docs/production_lessons.md` (TRAP-NNN 번호 + 원인/수정 파일 추적)
- **세션 시작 시**: 해당 프로젝트의 production_lessons.md TRAP 인덱스를 먼저 읽고 작업 개시
- **신규 TRAP 등록**: 시행착오 발견 즉시 다음 번호 부여 + 원인 파일/수정 파일/예방책 기록
- **참고 모델**: P2 GEANT4의 `MC_PITFALLS.md` (PIT-001~020), P21 FEP의 `production_lessons.md` (TRAP-001~030)

## 회사 및 브랜드

SL Corporation / SeouLink (SL) — 여행, 어학, 교류 서비스.
→ **상세 (브랜드 컨셉, 프로젝트 목록)**: `~/.claude/instructions/brand_info.md` 참조

## 문서 파일 네이밍 규칙

기획서, 보고서, 결과물 등 문서 파일을 저장할 때 아래 양식을 따른다:

- **파일명 형식**: `YYYYMMDD_HHMMSS_제목.md`
- **예시**: `20260310_142215_LingoPlay_SL_기획서.md`
- **타임스탬프**: 파일 생성 시점 기준 (`date "+%Y%m%d_%H%M%S"`로 취득)
- **제목**: 프로젝트명 + 문서 종류 (공백 대신 `_` 사용)
- **적용 범위**: 기획서, 개발 결과 보고서, 분석 보고서, 회의록 등 모든 문서 산출물
- **저장 위치**: 해당 프로젝트 루트 디렉토리 (코드 디렉토리 내부가 아닌 상위)

## 사용자 환경

- macOS (Apple M5, 32GB RAM)
- Claude Desktop App (Claude Code 내장)
- Ollama v0.15.4 (localhost:11434)
- Gemini CLI OAuth: jyc0289y@gmail.com

## 지침 체계

| 레벨 | 파일 | 명칭 | 자동 로드 |
|------|------|------|-----------|
| Global | `~/.claude/CLAUDE.md` | **전역지침** | 모든 세션 |
| Module | `~/.claude/instructions/*.md` | **모듈지침** | 관련 작업 시 수동 로드 |
| Project | `{project}/.claude/CLAUDE.md` | **프로젝트지침** | 해당 프로젝트 세션 |
| Session | `memory/sessions/P*.md` | **세션지침** | 포크 시 수동 로드 |

### 모듈화 규칙

전역지침이 비대해지는 것을 방지하기 위해 상세 규칙을 모듈 파일로 분리한다.

**현재 모듈** (`~/.claude/instructions/`):
| 파일 | 내용 | 로드 조건 |
|------|------|----------|
| `worker_rules.md` | Worker 위임 기준, 할루시네이션 방지, 토큰 절약 | Worker 도구 사용 시 |
| `realtime_data.md` | 항공권/환율 등 실시간 데이터 파이프라인 | 가격/시세 조회 시 |
| `brand_info.md` | SL Corporation 브랜드 컨셉, 프로젝트 목록 | 브랜딩/기획 작업 시 |
| `tool_optimization.md` | 도구별 토큰 소비 표, 파일 읽기 최적화 | 도구 사용 패턴 확인 시 |
| `session_fork.md` | P번호 체계, 포크 프로토콜, REQ/ISS 추적, 세션 마무리 | 세션 포크/마무리/REQ/ISS 작업 시 |
| `fork_cleanup_guide.md` | 포크 미준비 기존 세션 정리 절차 | "기존 세션 정리해줘" 지시 시 |

**재사용 모듈** (`~/.claude/modules/`):
| 파일 | 내용 | 로드 조건 |
|------|------|----------|
| `_index.md` | MOD 전역 레지스트리 | "MOD-xxx 포크해줘" 요청 시 |
| `MOD-001_goodnotes.md` | GoodNotes 필기 오버레이 (v1.1.0) | MOD-001 참조 시 |
| `MOD-002_stroke_recognizer.md` | StrokeRecognizer 펜→도형 인식 (v1.0.0) | MOD-002 참조 시 |
| `MOD-003_markdown_renderer.md` | Markdown→HTML 렌더러 (v1.0.0) | MOD-003 참조 시 |

**운영 원칙:**
1. 전역지침 본문에는 핵심 원칙 1~2줄 + `→ 상세: 파일경로` 참조만 기재
2. 해당 모듈이 필요한 작업이 발생하면 Read로 로드 후 규칙 적용
3. 새 규칙이 30줄을 넘으면 모듈 분리 검토
4. 모듈 파일은 백업 대상 (cron 자동 동기화)

### 지침 건강도 검토

사용자가 "지침 검토", "지침 건강도", "instruction review" 등을 요청하면:
1. `~/.claude/CLAUDE.md` 줄 수 / 바이트 수 측정
2. `~/.claude/instructions/` 모듈 파일 목록 + 크기
3. 전역지침 내 중복/비대 섹션 감지 → 모듈화 권고
4. 모듈 참조(`→ 상세:`) 누락 여부 확인
5. 백업 스크립트에 모듈 파일 포함 여부 확인
6. `~/.claude/modules/` 모듈 목록 + 버전 현황

## 재사용 모듈 시스템 (MOD)

프로젝트 간 포크 가능한 독립 코드 모듈을 `MOD-{NNN}` 번호로 관리한다. "MOD-001 포크해줘"로 즉시 통합.
→ **레지스트리**: `~/.claude/modules/_index.md` — 포크 요청 시 Read
→ **개별 카드**: `~/.claude/modules/MOD-{NNN}_{name}.md` — 소스 경로, 포크 방법, API, 변경/포크 이력
→ **상세 규칙이 30줄 초과 시**: `~/.claude/instructions/mod_system.md`로 분리

**핵심 3줄:**
- **등록**: 독립 모듈 완성 시 `_index.md` + 상세 카드 즉시 생성
- **포크**: 상세 카드 읽기 → 소스 복사 → 통합 → 포크 이력 갱신
- **업데이트**: 원본 변경 시 카드 버전 bump + 변경 이력 추가 + `_index.md` 갱신

## 세션 컨텍스트 포크 시스템

장시간 세션의 토큰 과소비를 방지하고, 새 세션에서 이전 작업의 핵심 맥락을 정확히 이어받기 위한 시스템.
핵심: **4계층 세션번호**로 충돌 없이 식별, 세션지침 파일로 컨텍스트 포크.
→ **상세 (프로토콜, REQ/ISS 추적, 세션 마무리)**: `~/.claude/instructions/session_fork.md` 참조

**⚠️ 필수: 새 세션 시작 시 `~/.claude/registries/{P번호}.md`를 읽고 세션번호를 부여하여 첫 응답에서 안내하라.**

**채팅번호 할당 안전망 (타임스탬프 재확인)**: 새 채팅 개시 시 registry를 한 번 더 재read하여 max가 변했는지 확인. 변했으면 더 큰 값 사용. 동시 개시 채팅 간 경쟁 조건 최소화.

### 세션 번호 체계 (4계층, 2026-04-15 시행)

**형식**: `P{프로젝트}.{채팅}.{포크}.{Agent}` — `wc` 등 정책 태그는 폐지

| 계층 | 의미 | 증가 시점 |
|------|------|-----------|
| 프로젝트 N | 프로젝트 번호 | 신규 프로젝트 생성 (전역) |
| 채팅 C | 채팅창 식별 | 새 채팅창 개시 (registry SSOT) |
| 포크 F | 자동포크 식별 | 같은 채팅 내 압축·자동포크 (채팅 내) |
| Agent A | Agent 파견 식별 | `.0`=원본 스레드, `.1+`=Agent (포크 내) |

**증가 규칙**:
- **새 채팅 개시**: `registry.md` max 채팅번호 +1 → `P{N}.{max+1}.1.0`
- **같은 채팅 내 자동포크**(압축 등): 채팅 고정, 포크 +1, Agent=0 리셋
  - 예: `P3.28.1.0` → 압축 → `P3.28.2.0`
- **Agent 파견**: 채팅·포크 고정, Agent +1
  - 예: `P3.28.1.0` → 파견 → `P3.28.1.1`, 또 파견 → `P3.28.1.2`
- **Agent 내부에서 또 Agent 파견**: 계층 증가 금지, Agent번호만 +1 (`.1.1.1.1` 꼬리 방지)
- **타 프로젝트 Agent 파견**: 대상 프로젝트 registry에서 새 채팅번호 할당
  - 예: `PM.17.1.0`이 P3에 파견 → P3 registry max=28 → `P3.29.1.0` 생성
- **교차채팅 포크**(채팅 오류로 재개설): 새 채팅번호 할당, 족보는 **`포크원` 필드로만 추적**
  - 예: `P1.3.5.0` 오류 → 새 채팅 `P1.4.1.0` (포크원: `P1.3.5.0`)
  - **계층을 끌어올리지 않는다** (루트번호만으로 포크체인을 추적하지 않음)

**유산 세션 호환**: 2026-04-14 이전 평면 번호(`P3.28wc` 등)는 그대로 보존. 해당 세션에서 신규 포크 발생 시부터 4계층 적용 (유산 번호는 묵시적 `.1.0`으로 간주: `P3.28wc` → 압축 → `P3.28.2.0`).

#### 레지스트리 스키마 (2026-04-16 이관 후)

**위치**: `~/.claude/registries/{P번호}.md` (프로젝트별 1파일, iCloud 외부)

**표준 컬럼**: `| 세션번호 | 제목 | 생성일 | 포크원 | UUID | 상태 |`
- **UUID**: Claude Code JSONL 세션 UUID (`~/.claude/projects/*/{UUID}.jsonl`). 과거 항목은 `-`. 신규 세션은 반드시 채워 넣는다 (JSONL 파일명 = UUID).
- **포크원**: 직전 세션 ID. 루트는 `없음 (루트)`.
- **상태**: `진행중` / `종료`.

**iCloud stub**: `{프로젝트}/memory/sessions/registry.md`는 MOVED 안내만 포함. 절대 이 stub에 신규 행을 추가하지 말 것.

#### 프로젝트 코드 레지스트리

**⚠️ 이 테이블이 P번호의 유일한 권위 소스(Single Source of Truth)이다.**
새 프로젝트 번호 부여 시 반드시 이 테이블의 마지막 번호를 확인하고, 그 다음 번호를 부여한다.

| P번호 | 프로젝트 | 디렉토리 | 세션 수 |
|--------|---------|----------|--------|
| P1 | SeouLink 한국어교실 | `~/Library/Mobile Documents/com~apple~CloudDocs/developer/SeouLink/` | 4 |
| P2 | GEANT4 | `~/Library/Mobile Documents/com~apple~CloudDocs/developer/GEANT4_claude/` | 1 |
| P3 | 여행계획 (TripLink SL) | `~/Library/Mobile Documents/com~apple~CloudDocs/developer/triplink-sl/` | 28 |
| P4 | LingoPlay SL | `~/Library/Mobile Documents/com~apple~CloudDocs/developer/LingoPlay/` | 1 |
| P5 | 홈 (시스템 관리) | `~/` | 2 |
| P6 | DL Trading | `~/developer/dl_trading/` | 1 |
| P7 | DWVA | `~/developer/dwva/` | 1 |
| P8 | Claude Remote (텔레그램 봇) | `~/developer/Claude_remote/` | 1 |
| P9 | MarkLink SL | `~/developer/document/` | 1 |
| P10 | Hodlum (Ludlum 3030-2 커스텀 로깅 S/W) | `~/developer/Hodlum/` | — |
| P11 | MarkLink SL (OfficeLink SL Suite) | `~/Library/Mobile Documents/com~apple~CloudDocs/developer/marklink-sl/` | 1 |
| P12 | HOBIS Cf-252 (선량평가 계산기) | `~/Library/Mobile Documents/com~apple~CloudDocs/developer/hobis_cf252/` | 2 |
| P13 | PhotoLink (웹 사진 편집기) | `~/Library/Mobile Documents/com~apple~CloudDocs/developer/PhotoLink/` | 1 |
| P14 | 3DLink (iPad 3D CAD 모델링) | `~/Library/Mobile Documents/com~apple~CloudDocs/developer/3DLink/` | 1 |
| P15 | AOMORI (아오모리 여행) | `~/Library/Mobile Documents/com~apple~CloudDocs/developer/AOMORI/` | 1 |
| P16 | CineLink (영상 제작 파이프라인) | `~/Library/Mobile Documents/com~apple~CloudDocs/developer/CineLink/` | 1 |
| P17 | Flight (항공권 종합 서비스) | `~/Library/Mobile Documents/com~apple~CloudDocs/developer/flight/` | 1 |
| P18 | HighLink (고속도로 AI 관제) | `~/Library/Mobile Documents/com~apple~CloudDocs/developer/HighLink/` | 1 |
| P19 | DailyBriefing (일일 브리핑) | `~/Library/Mobile Documents/com~apple~CloudDocs/developer/DailyBriefing/` | 1 |
| P20 | PMLink (모바일 PM 클라이언트) | `~/Library/Mobile Documents/com~apple~CloudDocs/developer/PMLink/` | 1 |
| P21 | FEP (익숙한 경험의 심리학) | `~/Library/Mobile Documents/com~apple~CloudDocs/developer/FEP/` | 1 |
| P22 | FlashMOE (회사의 3원소 — 1인 MOE 스택) | `~/Library/Mobile Documents/com~apple~CloudDocs/developer/FlashMOE/` | 1 |
| PM | PM (프로젝트 관리) | `~/Library/Mobile Documents/com~apple~CloudDocs/developer/` | — |

#### 정책 태그 (폐지, 2026-04-15)

`w`(Worker), `c`(Context fork) 등 정책 태그는 모두 기본값이 되어 폐지.
- **유산 세션**의 `wc` 등 접미는 그대로 보존 (소급 제거 금지)
- **신규 세션**은 4계층 번호만 사용 (접미 없음)
- 향후 새 정책 도입 시에도 태그 대신 세션지침 본문에 기록

## 복잡한 기획·편집 판단 시 opusplan 안내

복잡한 기획·편집·설계 판단(영상 편집 결정, 대본 작성, 아키텍처 설계 등)이 필요한 작업을 시작할 때, 사용자가 아직 opusplan 모드가 아니면 **첫 응답에서 한 번** 안내한다:

> "복잡한 판단 작업이 포함됩니다. `/model opusplan`을 입력하시면 계획=Opus, 실행=Sonnet으로 자동 분리되어 품질과 토큰 효율이 모두 개선됩니다."

- 어시스턴트는 세션 내 자가 모델 전환이 불가능하므로 사용자 입력이 필수
- 한 세션에서 반복 안내 금지 (한 번만)
- 단순 수정·조회·코드 편집에는 안내하지 않음

## 도구 결과 최적화

스크린샷(~54K tok/건)은 최종 시각 확인에만 사용. 그 외는 텍스트 도구(`preview_snapshot`, `preview_inspect` 등) 우선.
→ **상세 규칙 (도구별 토큰/건 표, 파일 읽기 최적화)**: `~/.claude/instructions/tool_optimization.md` 참조

### 압축 감지 시 대응

자동 컨텍스트 압축이 발생하면:
1. 사용자에게 "⚠️ 압축 발생" 알림
2. 세션지침 즉시 갱신 + **포크번호 +1 자동 부여** (`P{N}.{C}.{F+1}.0`) — ⚠️ **채팅번호 건드리지 말 것** (타 채팅 충돌 방지 핵심)
3. **`## 금지/확정 사항` 섹션을 가장 먼저 확인** — 이전 세션 금지/불가 사항 필수 전달
4. **사용자에게 새 채팅을 열라고 안내하지 않는다** — 사용자는 같은 채팅에서 계속 작업
