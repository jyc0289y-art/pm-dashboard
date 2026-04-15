---
name: fork_cleanup_guide
description: 기존 포크 미준비 세션을 정리하는 절차 가이드 — 다른 세션의 Claude Code가 따라할 수 있음
type: project
---

# 기존 세션 포크 정리 가이드

다른 세션에서 Claude Code에게 "기존 포크준비 안된 세션들 정리해줘"라고 지시할 때 따라야 할 절차.

## 전제 조건

- `~/.claude/CLAUDE.md`의 "세션 컨텍스트 포크 시스템" 섹션을 숙지할 것
- 해당 프로젝트의 `memory/sessions/registry.md` 존재 확인

## 정리 절차

### 1단계: 현황 파악

```bash
# 프로젝트의 세션 레지스트리 확인
cat {project}/memory/sessions/registry.md

# 세션지침 파일 존재 여부 확인
ls {project}/memory/sessions/P*.md

# REQ 시스템 존재 여부 확인
ls {project}/memory/requirements/_index.md
```

**확인 사항:**
- registry에 등록되었지만 세션지침(.md)이 없는 세션
- registry에 미등록된 세션 (JSONL만 존재)
- REQ 인덱스 파일 부재 여부

### 2단계: 세션지침 소급 생성

세션지침이 없는 세션에 대해:

1. **JSONL 분석**: `~/.claude/projects/{project-path}/{uuid}.jsonl` 에서 해당 세션 대화 이력 확인
2. **결과물 분석**: 해당 세션에서 생성/수정된 파일 확인 (git log 또는 파일 타임스탬프)
3. **세션지침 작성**: 표준 구조에 따라 `memory/sessions/P{번호}.md` 생성

#### 세션지침 표준 구조

```markdown
# P{번호} — {제목}

## 메타데이터
- UUID: {앞8자}
- 생성: YYYY-MM-DD
- 포크원: {부모 P번호} 또는 없음 (루트)
- 자식: {자식 P번호 목록}

## 작업 요약
(3~5줄로 핵심 작업 기술)

## 주요 결과물
(파일명 + 한줄 설명, ✅/🟡/🔴 상태)

## 핵심 결정사항
(번호 매겨서 기술)

## 다음 작업을 위한 컨텍스트
### 즉시 해야 할 일
### 포크 가이드
### 기술 환경
```

### 3단계: REQ 시스템 초기화

`memory/requirements/_index.md`가 없으면 생성:

```markdown
# P{N} 요구사항 인덱스 — {프로젝트명}

## 요구사항 목록

| REQ ID | 내용 | 상태 | 기원 세션 | 현재 세션 |
|--------|------|------|-----------|-----------|

## 포크 캐리오버 이력
```

**REQ 번호 규칙:**
- 형식: `{기원세션}-REQ-{NNN}` (예: `P1.4wc-REQ-001`)
- 상태: 🔴 미착수 | 🟡 진행중 | 🟢 완료 | ⚪ 보류/취소
- 미완(🔴/🟡) REQ는 포크 시 자식 세션의 "현재 세션"으로 갱신

### 4단계: registry 업데이트

모든 세션이 registry에 반영되어야 함:
- 세션 목록 테이블에 행 추가
- 포크 트리에 계보 표시 (`← 포크원: P{부모}`)
- 세션지침 파일 현황 테이블 업데이트

### 5단계: 검증

- [ ] 모든 세션에 세션지침 파일 존재
- [ ] registry 세션 목록/포크 트리/세션지침 현황 3곳 모두 일치
- [ ] 미완 REQ가 있는 종료 세션 → 자식 세션으로 캐리오버 확인
- [ ] MEMORY.md에 sessions/registry.md, requirements/_index.md 링크 존재

## P1 프로젝트 참고 사항

- **JSONL 위치**: `~/.claude/projects/-Users-jyc-Library-Mobile-Documents-com-apple-CloudDocs-SeouLink------/`
- **UUID 매핑**: registry.md의 UUID(앞8자) 컬럼으로 JSONL 파일 매칭
- **P1.2wc UUID**: fc3b323c — 이 UUID로 시작하는 JSONL이 P1.2wc + P1.4wc 세션 (P1.4wc는 P1.2wc의 컨텍스트 압축 후 재개)

## 다른 프로젝트(P2~P10) 적용 시

1. 해당 프로젝트 디렉토리에서 Claude Code 실행
2. `memory/sessions/` 디렉토리 없으면 생성
3. 위 절차 1~5단계 실행
4. 프로젝트코드 레지스트리(`~/.claude/CLAUDE.md`)의 세션 수 갱신
