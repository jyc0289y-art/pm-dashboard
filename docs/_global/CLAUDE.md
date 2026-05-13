# Claude 글로벌 지침

**필수: 새 세션 시작 시 `~/.claude/registries/{P번호}.md`를 읽고 P번호를 부여하여 첫 응답에서 안내하라. 상세 → "세션 컨텍스트 포크 시스템" 섹션 참조.**
**⚠️ 레지스트리 SSOT (2026-04-16 이관)**: iCloud 내 `{프로젝트}/memory/sessions/registry.md`는 더 이상 SSOT가 아니며 MOVED stub만 남아 있다. 실제 SSOT는 `~/.claude/registries/{P번호}.md` (iCloud 외부, 동기화 지연 없음). 새 세션 등록/조회는 반드시 이 경로를 사용하라.

## ⚠️ Google Apps Script 작업 — clasp 필수 (P31에서 도출, 2026-05-13)

Google Sheets / Docs / Forms / Slides의 **Apps Script 코드를 작성·수정·실행하는 작업이 발생하면 즉시 `~/.claude/instructions/clasp_workflow.md` 로드 후 그 워크플로를 따른다.**

- ❌ 금지: Apps Script 편집기에 코드 복붙(Cmd+A→Cmd+V), Chrome MCP로 메뉴 자동 클릭, 사용자 클립보드·키보드 점유
- ✅ 필수: `clasp push`로 디스크 ↔ Apps Script 자동 동기화. 함수 실행은 onOpen + PropertiesService 멱등 플래그 패턴
- 적용 키워드 (자동 트리거): "Apps Script", "구글 시트 코드", "스프레드시트 자동화", "createMenu", "onOpen", "setFormula", ".gs 파일", "google.script.run"

위반 시 P31에서 누적된 비효율(메뉴 클릭당 5~80초, 1500줄 복붙, 시스템 차단) 재발.

## Worker(부하 LLM) 활용 규칙

Worker(Ollama/Gemini CLI)로 토큰 효율 향상 → 같은 요금제 내 처리량 극대화. 품질 훼손 금지.
**핵심 원칙**: 사실 확인(요약/추출)은 위임 OK, 사실 생성(새 내용)은 Claude 검수 필수.
→ **상세 규칙**: `~/.claude/instructions/worker_rules.md` 참조
→ **실시간 데이터(항공권/환율 등)**: `~/.claude/instructions/realtime_data.md` 참조

## 사용자 검수 요청 사전 검증 의무 (Pre-QA Self-Validation)

> **추가 일자**: 2026-05-06 (사용자 지시: "내 노동력을 줄이기 위해 시스템 만들고 있는데 의미없는 검수 요청은 노동력 낭비. 검수가 의미있는지 사전 검토")

**사용자에게 검수 요청 알림을 보내기 전에 다음 5개 게이트 모두 자동 통과해야 한다. 하나라도 실패 시 재처리 → 재검증 → 통과 후 알림 발송.**

### 게이트 G1 — 산출물 최신성
- 산출물 timestamp가 모든 입력 자산의 마지막 수정 시점 **이후**여야 함
- 검사: `산출물.mtime > max(입력자산들.mtime)`
- 위반 시: "재빌드 안 됨" 자동 감지 → 빌드 트리거

### 게이트 G2 — 자동 결함 검출 통과
영상/이미지에 다음을 자동 검사:
- **OCR 결함 텍스트**: 영상 프레임 샘플 5~10개 OCR → 한글/일본/중국 텍스트 발견 시 fail (의도된 자막 제외)
- **moov atom 위치**: 파일 시작 부분 (faststart 적용됨)
- **코덱 호환성**: H.264 baseline/main + AAC + yuv420p
- **빈 프레임**: 검정/단색 프레임이 0.5초 이상 연속되면 검토 트리거
- **자막 동기화**: 자막 timing이 audio 발화와 ±200ms 이내

### 게이트 G3 — 이전 사용자 지적 반영 확인
- 프로젝트의 `USER_FEEDBACK_HISTORY.md` 또는 동등 문서에서 미해결 지적 모두 ✅ 처리됨 확인
- 미반영 지적 발견 시: 검수 요청 차단 + 처리 후 재시도

### 게이트 G4 — 변화 발생
- 이전 빌드 대비 정량 지표 또는 시각 변화 측정 (`qa_build_compare.py` 결과)
- 변화량이 임계 이하 (예: 정량 diff ≤ 1%, 시각 변화 없음) → 검수 의미 없음 → 차단

### 게이트 G5 — AI 한계 명시
검수 페이지에 다음 박스 의무 표시:
- ❌ AI 측정 불가 항목 (오디오 청취/영상 재생 관찰/시청자 정서/맥락 흐름)
- ✅ AI 검증 가능 항목 (정량/정지 프레임/timestamp 매칭)
- 사용자가 어디에 노동력을 써야 하는지 명확히

### 위반 시
- 사용자에게 알림 발송 금지
- 자동 재처리 (재빌드/재생성/재정렬)
- 게이트 재실행 → 통과 후에만 알림
- 같은 게이트가 2회 실패 시 사용자에게 "이 게이트 자동 해결 불가, 가이드 필요" 보고

### 위반 사례 (격상 계기)
P21 FEP 2026-05-06: 한글 깨진 일러스트 4개 재생성 후 빌드 안 한 상태에서 사용자에게 검수 페이지 표시 → 사용자가 옛 영상 보면서 "한글 안 지워졌다" 다시 지적 → 노동력 낭비. G1 위반.

---

## 사용자 검수 요청 의무 (User Verification Interface Rule)

> **추가 일자**: 2026-04-17 (사용자 지시: "프로젝트 중단 원인은 직접 검증 요청 단계 — HTML로 게시하고 클릭 피드백")

**시각/청각 산출물(영상·이미지·HTML·문서)을 사용자에게 검수 요청할 때 텍스트 묘사로만 끝내지 않는다. 반드시 사용자가 클릭/선택으로 피드백을 줄 수 있는 인터페이스를 제공한다.**

### 규칙 1: 검수 페이지 자동 생성 의무
검수 대상이 **영상·이미지·다층 시각물**인 경우, 다음을 포함한 단일 HTML 페이지를 생성한다:
- 산출물 직접 재생/표시 (HTML5 video, img tag)
- **같은 시점 / 같은 좌표 비교** (PREV vs NEW 그리드)
- **시점별/항목별 체크리스트** (good/needs-fix/critical 라디오 + 자유 코멘트)
- **피드백 복사 버튼** → 구조화 텍스트(JSON/Markdown)를 클립보드로 → 사용자가 채팅창에 붙여넣기 가능

### 규칙 2: 표준 위치
- HTML 산출물: `{프로젝트}/docs/qa_review/qa_{YYYYMMDD_HHMMSS}_{설명}.html`
- 의존 자산(프레임 이미지·복사 영상): 같은 디렉토리 또는 `{ts}_assets/` 하위
- **단일 폴더로 자가완결** (브라우저로 열면 외부 의존 없이 동작)

### 규칙 3: 글로벌 스크립트
- `~/.claude/scripts/generate_qa_page.py` 사용 (없으면 P21 FEP `EP01_forced_compliment/qa_review_page.py` 참조)
- 입력: NEW/PREV 영상 경로 + 비교 시점 리스트 + 체크리스트 항목
- 출력: 단일 HTML 페이지 + 자동 브라우저 오픈 (`open` 명령)

### 규칙 4: 사용자 피드백 형식
HTML 페이지의 "피드백 복사" 버튼은 다음 형식의 텍스트를 클립보드에 넣는다:
```markdown
## QA 피드백 — {빌드명}
- 115s 03_validation: ✅ 정상 / 🟡 위치 어색 / 🔴 자막 가림
- 280s 다층 자막: 🟡 Type D와 Type F 겹침
- 자유 코멘트: ...
```
사용자가 이를 채팅창에 붙여넣으면 AI가 즉시 항목별 수정 진행.

### 규칙 5: 텍스트만의 검수 요청 금지
- ❌ "확인해주세요", "괜찮은지 봐주세요" 만 보내고 작업 종료
- ✅ HTML 페이지 경로 + `open` 명령 + 체크리스트 항목 미리보기 함께 제공

### 위반 시
- 사용자가 직접 검증을 위해 매번 텍스트 설명을 읽고 별도로 영상을 재생해야 함 → 검증 비용 증가 → 프로젝트 진척 저하

## 산출물 보존 + 개선 평가 의무 (Build Output Preservation & Comparison Rule)

> **추가 일자**: 2026-04-17 (P21 FEP에서 누적된 "이전 빌드 덮어쓰여 개선 평가 불가" 문제로 격상)

### 규칙 1: 산출물 파일명에 타임스탬프 필수
**반복 빌드/생성 가능한 산출물(영상, 이미지, 보고서, 모델, 빌드 아티팩트 등)은 반드시 타임스탬프 접두사를 포함한다.**
- 형식: `YYYYMMDD_HHMMSS_{설명}.{확장자}`
- 적용 대상:
  - 영상 빌드 (`output/20260417_014924_EP01_v3_lp_bubble.mp4`)
  - 이미지/일러스트 (`v3_layers/...`)
  - 분석 보고서, 측정 결과 JSON
  - 모델 체크포인트, 데이터셋 스냅샷
  - 컴파일된 바이너리 (반복 가능한 것)
- **금지**: 같은 파일명으로 덮어쓰기 (`output.mp4`, `result.json` 등 고정명)
- **예외**: 임시 작업 파일(`/tmp/*`), 캐시(`__pycache__`), 의존성 잠금(`package-lock.json`)

### 규칙 2: 개선 작업 후 비교 평가 의무
**"개선됨" 또는 "고침"이라고 보고하기 전에 반드시 다음을 수행:**

1. **이전 산출물 보존 확인**: 이전 버전이 같은 디렉토리에 보존되어 있는지 확인. 없으면 즉시 사용자에게 보고하고 작업 중단.
2. **정량 비교 측정**: 사용 가능한 객관적 지표로 이전 vs 현재 측정값 표 작성
   - 영상: 길이, 크기, 씬 수, 자막 수, 측정 가능한 품질 지표
   - 코드: 테스트 통과율, 성능 벤치마크, LOC, 복잡도
   - 데이터: 샘플 수, 정확도, 손실값
3. **시각/청각 검증** (해당 시): 같은 위치(타임스탬프/좌표)에서 이전 vs 현재 샘플 추출
4. **회귀 항목 명시**: 개선 항목 + **퇴보/유지 항목**도 빠짐없이 보고

### 규칙 3: "개선됨" 선언 유예
- AI(Claude)는 오디오 청취 불가, 영상 재생 관찰 불가, 사용자 체감 추정 불가
- 따라서 정량 지표가 좋아져도 **"개선됨"이라 단정하지 말고 "개선 시도"로만 표기**
- 사용자 시각/청각 검증 통과 후에만 "개선 확인" 으로 격상
- **위반 시 즉시 정정**: 같은 메시지 안에서 "개선됨 → 개선 시도" 로 표현 변경

### 규칙 4: 실패 패턴 추적
**같은 카테고리의 비교 평가 실패가 2회 발생하면**:
- 즉시 해당 프로젝트의 TRAP 시스템에 등록 + 전역지침 갱신
- 자동화 스크립트로 격상 (예: 빌드 후 자동 비교 보고서 생성)

### 위반 사례 (P21 FEP, 2026-04-16~17)
- 8회 이상의 EP.01 빌드를 진행했으나 **각 빌드 간 정량 비교 보고서 부재**
- "100% 정합" 같은 지표 자만 → 사용자 체감 "전혀 안맞음"
- 이전 빌드는 타임스탬프 파일명 덕에 우연히 보존되었으나 **비교 평가 절차 자체가 없었음**

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

## 함정 관리 시스템 (TRAP) — 강제 이행

> **2026-04-17 강화**: 25개 프로젝트 감사 결과 16개(64%) 미이행 → 강제 규칙으로 격상

프로젝트 제작 과정에서 겪은 시행착오를 **TRAP-NNN** 번호로 관리하여 같은 실수 반복을 방지한다.

### 1. 표준 위치 (필수)
`{프로젝트루트}/docs/production_lessons.md` — 또는 타임스탬프 변형 (`YYYYMMDD_HHMMSS_*_TRAP_*.md`)
- 두 형식 다 OK이나 **반드시 `docs/` 하위에 위치**
- 리네임 시 원래 파일을 stub으로 남기고 새 파일 경로 안내 (P21 FEP 사례 참조)

### 2. 신규 프로젝트 생성 시 자동 스캐폴딩 (필수)
새 P{N} 프로젝트 디렉토리 생성 시 PM 또는 사용자 지시로 **반드시 함께 생성**:
```
{프로젝트}/docs/production_lessons.md  # 빈 TRAP 인덱스 + 표준 스키마 헤더
```
스캐폴드 템플릿: `~/.claude/instructions/trap_template.md` (없으면 P21 FEP 참조)

### 3. 프로젝트지침 CLAUDE.md 명시 의무
각 프로젝트의 `.claude/CLAUDE.md`에 **TRAP 파일 경로를 명시적으로 기록**:
```markdown
## ⚠️ TRAP 함정 관리 시스템 (필수 참조)
> 매 세션 시작 시 + 새 Phase 진입 시 `{프로젝트}/docs/production_lessons.md` 먼저 확인
```

### 4. 세션 시작 시 의무
- 해당 프로젝트의 TRAP 파일 인덱스를 먼저 읽고 작업 개시
- 신규 시행착오 발견 즉시 다음 번호 부여 + 원인 파일/수정 파일/예방책 기록
- 같은 카테고리 TRAP 2회 이상 재발 시 **접근 자체 교체** (TRAP-041 교훈)

### 5. 정기 감사 (PM 또는 분기별)
사용자 지시 또는 PM 정기 검사로 전체 프로젝트 TRAP 이행 상태 점검:
```bash
# 감사 스크립트 (글로벌)
~/.claude/scripts/audit_trap_compliance.py
```
미이행 발견 시 자동 스캐폴딩 + 사용자 보고

### 6. 표준 스키마
| 필드 | 설명 |
|------|------|
| TRAP-NNN | 순차 번호 (전 프로젝트 공통, 카테고리 무관) |
| 발견 일시 | 발견 날짜·시각 |
| 발견 Phase | 작업 단계 |
| 원인 파일 | 문제 발생한 파일 경로 |
| 수정 파일 | 해결을 위해 수정한 파일 경로 |
| 증상 | 사용자/시스템에서 보이는 문제 |
| 원인 | 근본 원인 분석 |
| 해결 | 적용한 수정 |
| 예방책 | 같은 실수 재발 방지 방법 |
| 상태 | ✅/🟡/🔴 |

### 7. 참고 모델 (실제 사용 중)
- **P21 FEP** `docs/20260415_092337_FEP_영상제작_TRAP_관리시스템.md` (TRAP-001~046, 49KB) — **메인 참고**
- P18 HighLink `docs/production_lessons.md` (12KB)
- P16 CineLink `cinelink/docs/production_lessons.md` (16KB)
- ⚠️ 이전 지침의 "P2 GEANT4 MC_PITFALLS.md" 참고 모델은 실제로는 파일 부재 — 사실 오류 정정 (2026-04-17)

### 8. 위반 시
- 미이행 프로젝트는 PM 정기 감사에서 자동 스캐폴딩 트리거
- "이전에 같은 함정 빠졌는데 또 빠짐" → 즉시 TRAP 등록 + 글로벌 지침 격상 검토
- 이행률 50% 미만 시 글로벌 지침 추가 강화 (자동화 도입 등)

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
| **`ai_limits_and_measurement.md`** ⚠️ | **AI 구조적 한계 + 반복 실수 패턴 금지 + 측정 기반 개선 원칙** | **멀티미디어/영상/오디오/타이밍/시각 품질 작업 필수** |
| **`disaster_recovery.md`** 🛡 | **재해 복구 표준 — 모든 P 프로젝트 공통 mirror·복원·worktree 패턴 (`~/.claude/` 자산은 iCloud·GitHub 자동 동기화 안 됨)** | **신규 P 프로젝트 시작 + 맥북 교체·복원 + worktree 운영 시 수동 로드** |
| **`clasp_workflow.md`** 📜 | **Google Apps Script 작업 표준 — clasp 기반 (코드 푸시·실행·멱등 패턴). 메뉴 클릭·복붙 자동화 금지** | **Google Sheets/Docs/Forms/Slides에 Apps Script 작성·수정·배포 작업 시 필수 로드** |

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

**⚠️ CWD 검증 절차 (PM.18 오부여 교훈, 2026-04-17 추가)**:
1. CWD를 프로젝트 레지스트리 테이블의 경로와 **정확히 일치** 여부로 대조 (prefix 일치만으로 판단 금지)
2. **완전 일치**: 해당 P번호 사용
3. **하위 경로** (등록 프로젝트의 서브폴더이지만 그 자체는 미등록): 사용자에게 선택지 제시하고 답변 대기
   - (a) 새 프로젝트로 등록 (다음 빈 P번호 부여)
   - (b) 상위 {P번호}의 임시 작업공간으로 진행
   - (c) 임시 세션 (번호 미부여)
4. **부모 `.claude/CLAUDE.md`의 자동 로드는 범위 표식일 뿐 소속 확정이 아님** — CWD가 레지스트리 경로와 정확 일치할 때만 그 프로젝트 세션으로 간주
5. 위반 사례: 2026-04-17 TEREV 폴더에서 세션 시작했으나 부모 PM 지침 자동 로드를 근거로 PM.18.1.0 오부여 → P25.1.1.0으로 소급 정정

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
| P23 | DEX (탈중앙화 거래소 트레이딩 봇) | `~/Library/Mobile Documents/com~apple~CloudDocs/developer/DEX/` | 1 |
| P24 | Dstream (SKT 데이터쉐어링 우회 시스템) | `~/Dstream/` | 2 |
| P25 | TEREV (기술혁명 연대기 — 콘텐츠 기획) | `~/Library/Mobile Documents/com~apple~CloudDocs/developer/TEREV/` | 1 |
| P26 | MOAT / 大思惟齋 (장기 사유·학습·연구 대화 아카이브) | `~/Library/Mobile Documents/com~apple~CloudDocs/developer/MOAT/` | 1 |
| P27 | CardioLink (심혈관 모니터링 — 지속 ECG + 1인가구 안전망) | `~/Library/Mobile Documents/com~apple~CloudDocs/developer/CardioLink/` | 1 |
| P28 | HornetLink (장기체공 Tailsitter 드론 — 군·관급 기술의 민간 민주화) | `~/Library/Mobile Documents/com~apple~CloudDocs/developer/HornetLink/` | 1 |
| P29 | AutoLink (업무 자동화 + 웹 대시보드 서비스) | `~/Library/Mobile Documents/com~apple~CloudDocs/developer/AutoLink/` | 1 |
| P30 | SeouLink Game (한국어교실 비주얼노벨 게임화) | `~/Library/Mobile Documents/com~apple~CloudDocs/developer/SeouLink_Game/` | 1 |
| P31 | HJ Safety Sheet 개선 (호진산업기연 안전관리현황통합파일 데이터 구조 혁신) | `~/Library/Mobile Documents/com~apple~CloudDocs/developer/HJ/` | 1 |
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
