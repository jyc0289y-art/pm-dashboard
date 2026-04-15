# HighLink 프로젝트 지침

## 세션 번호(P번호/루트번호) 작성 가이드

이 프로젝트는 **P18 (HighLink)** 프로젝트이다. 회사 PC 등 전역 CLAUDE.md가 없는 환경에서도 아래 규칙에 따라 세션 번호를 부여·관리할 수 있다.

### P번호 체계

- **형식**: `P18.{순번}{정책태그}`
- **순번**: `memory/sessions/registry.md`의 마지막 순번 + 1
- **정책 태그**: `w` = Worker LLM 위임, `c` = 컨텍스트 포크 시스템
- **현재 기본 태그**: `wc` (Worker + Context fork)

**예시**: P18.1wc → P18.2wc → P18.3wc → ...

### 에이전트 서브세션

Agent 도구로 생성된 서브세션은 부모 세션의 하위 계층:
```
P18.3wc        ← 메인 세션
P18.3.1wc      ← 에이전트 서브세션 1
P18.3.2wc      ← 에이전트 서브세션 2
```
서브세션은 메인 세션 순번 공간을 점유하지 않음.

### 새 세션 시작 프로토콜

1. `memory/sessions/registry.md` 확인
2. 다음 순번 부여 (예: 마지막이 P18.3wc이면 → P18.4wc)
3. **첫 응답에서 안내**: "이 세션 번호: `[P18.Nwc]` — 사이드바 제목에 붙여주세요"
4. registry에 신규 항목 추가
5. `memory/sessions/P18.Nwc.md` 세션지침 파일 생성

### 컨텍스트 포크

사용자가 "P18.Xwc 포크해줘" 요청 시:
1. `memory/sessions/P18.Xwc.md` 읽기
2. 포크 체인: 직전 세션 전체 로드, 2단계 이상은 핵심만
3. 현재 세션 번호를 다음 순번으로 부여
4. 컨텍스트 요약 보고 후 작업 재개

### 세션지침 표준 구조

```markdown
# P18.{N}wc — {제목}
## 메타데이터
- 생성: YYYY-MM-DD
- 포크원: P18.{N-1}wc 또는 없음
- 자식: {자식 목록}
## 작업 요약 (3~5줄)
## 주요 결과물 (파일명 + 한줄 설명)
## 핵심 결정사항
## 다음 작업을 위한 컨텍스트
```

### 세션 마무리

1. 세션지침 최종 갱신
2. registry 상태를 "종료"로 업데이트
3. 총평 작성 (의의, 정량 요약, 제언, 교훈)

### 파일 구조

```
memory/sessions/
├── registry.md        ← 전체 세션 목록 + 포크 관계
└── P18.{N}wc.md       ← 개별 세션지침
```

### 회사 PC 작업 위임 체계

- 맥에서 의뢰서/지시서를 `docs/requests/`에 작성 → Git 푸시
- 회사 PC에서 Git 풀 → Claude Code로 실행 → 결과 커밋·푸시
- **보안**: API 키, 인증정보는 코드/문서에 절대 미포함. `.streamlit/secrets.toml` 등 로컬 설정 파일로만 관리

## 프로젝트 개요

- **HighLink**: 고속도로 AI 관제 시스템
- **P번호**: P18 (P18.{N}wc)
- **최신 세션**: P18.6wc (2026-04-11)
- **현재 Phase**: Phase 1 (2단계 차종 분류기 통합 완료)
- **서버**: 회사 PC (RTX 4060), Streamlit + Cloudflare Tunnel
- **핵심 스택**: YOLOv8 + EfficientNet-B0 + Streamlit + gRPC
- **선행연구**: GO 판정 (파트너 경유 관납 모델, PM.3wc)

## 현재 상태 (2026-04-11 기준)

### 완료된 작업
- Phase 0 MPS 벤치마크 + Phase 1 2단계 분류기 통합
- Streamlit 대시보드 + Cloudflare Tunnel 원격 접속
- MJPEG Solution 1 (Tornado 핸들러 통합, `tornado_mjpeg.py`)
- F3 테스트 3건 완료 (pedestrian_dashcam, highway_bicycle, highway_tunnel_cctv)
- F3 bicycle 과감지 수정 (IoU 중복 억제 + confidence threshold)
- 보안 수정: DB 비밀번호 환경변수화 (`.streamlit/secrets.toml`)
- Streamlit 알림 UI (REQ-003) + 용어 통일 (REQ-004)
- ultralytics 패키지 설치 + secrets.toml 생성 (PM.14wc)

### 미해결 이슈
- MJPEG Solution 1 실전 테스트 (회사 PC에서 원격 접속 확인)
- 실전 ITS CCTV 테스트 (P18.3wc-REQ-002)
- PM.2wc-REQ-001: F3 과감지 추가 수정 (bbox 겹침 중복)

## 주요 파일 구조
```
app/streamlit/
├── app.py              ← Streamlit 메인 앱
├── tornado_mjpeg.py    ← MJPEG Tornado 핸들러 (ISS-001 해결)
├── .streamlit/secrets.toml  ← 비밀번호/DB 설정 (Git 제외)
engine/
├── detector/           ← YOLOv8 차량 탐지
├── classifier/         ← EfficientNet-B0 차종 분류
├── tracker/            ← 객체 추적
├── event_rules/        ← F1/F2/F3 룰엔진
data/test_results/      ← F3 테스트 결과 MP4
docs/requests/          ← 회사 PC 작업 의뢰서
```
