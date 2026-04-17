# CineLink 프로젝트지침

## 프로젝트 개요
- **목적**: AI 영상 제작 파이프라인 (기획→촬영→편집→배포 자동화)
- **P번호**: P16
- **최신 세션**: P16.3wc (2026-04-17) — 발전방향 확정 + Phase A 기반 정비 완료
- **브랜드**: CineLink SL (SL Corporation → SeouLink → CineLink 내부 엔진)
- **선행연구**: GO 판정 (에이전시 모델, CAGR 42%, PM.4wc)

## 발전방향 정본
⭐ **정본 문서**: `20260417_012751_CineLink_발전방향.md` (프로젝트 루트)
→ **옵션 1 → 옵션 2 → 옵션 3 진화 로드맵**: CapCut 전담(현재) → 이원 병행 → CineLink 전담

## 3층 아키텍처
```
[1] Claude Code (두뇌)       — Skills, Commands, CLAUDE.md 채널별 규칙
[2] CineLink (전처리·후처리)  — ffmpeg_lib.py, TTS, Whisper
[3] CapCut (최종 조립)       — Phase 6, Phase D에서 CineLink로 이관 예정
```

## 기술 스택
- **FFmpeg**: 8.0.1 ✅ (표준 라이브러리: `cinelink/shared/scripts/ffmpeg_lib.py`)
- **ffprobe**: ✅, **jq**: ✅
- **전사**: Whisper ❌ (Phase C 진입 시 faster-whisper 설치)
- **색보정**: LUT ❌ (Phase C 진입 시 확보)
- **TTS**: Typecast (TEREV 한국어) / 거지맵은 현장 오디오 / Edge TTS 백업
- **Agent (루트 전역)**: `.claude/agents/` 5종 (frame-analyzer, transcript-processor, ffmpeg-runner, narration-writer, editor-judge)

## 채널 구조
```
cinelink/channels/
├── terev/      — 기술혁명 연대기 (한국어, 다큐 톤, Typecast TTS)
├── ggeoji/     — 거지맵 (일본어, 현장 오디오, Phase C 활성화)
└── _shared/    — 공용 Commands·Skills (srt-translate, publish-metadata 등)
```

## CL-TRAP 시스템
- **카탈로그**: `cinelink/docs/production_lessons.md` (CL-TRAP-001~011, FEP→CineLink 이관)
- **표준 함수**: `cinelink/shared/scripts/ffmpeg_lib.py` (11개, 8개 즉시 사용 + 3개 Phase B용)
- **게이트**: `ffmpeg-runner` Agent가 명령 생성 전 자동 확인
- **⚠️ 새 실패 발견 시 즉시 CL-TRAP-012+ 추가** (이론 단계 정체 방지)

## AI 청각 한계 보완 (핵심 원칙)
- AI는 오디오를 **직접 들을 수 없다** → 대본 기반 타이밍 추정은 구조적 편차
- 해결: **CL-TRAP-010 `snap_manifest_to_silence()`** — `ffmpeg silencedetect`로 발화 구간 감지 → auto-snap
- FEP 검증: 21/21 (100%) 정합 달성
- 유사 한계(시각=프레임 샘플링, 색각=히스토그램) 동일 패턴으로 보완

## 진화 로드맵 (Phase A 완료 시점 기준)

| Phase | 옵션 | 상태 | 특징 |
|-------|------|------|------|
| A | 기반 정비 | ✅ 완료 (P16.3wc) | docs·ffmpeg_lib·channels 스캐폴딩 |
| B | 옵션 1 | 🟡 진입 대기 | CapCut 전담 + 연구라인 선행 (B10) |
| C | 옵션 2 | ⚪ | 이원 병행, Whisper/LUT 확보 |
| D | 옵션 3 | ⚪ | CapCut 의존성 제거, 완전 자동화 |

### Phase B → C 전환 조건
- ✅ `ffmpeg_lib.py` 11개 함수 단위 테스트 통과
- ✅ TEREV EP01~EP03 완성 (CapCut)
- ✅ B10 합성 연구 vs CapCut 품질 비교
- ✅ 새 CL-TRAP 3건 추가 또는 "현행 11개로 충분" 확정

## 세션 관리
- **레지스트리 SSOT**: `~/.claude/registries/P16.md` (2026-04-16 이관)
- **iCloud stub**: `memory/sessions/registry.md` (MOVED 안내만)
- **번호 체계**:
  - 유산: `P16.Nwc` (2026-04-14 이전, 보존)
  - 신규: 4계층 `P16.{채팅}.{포크}.{Agent}`
- **세션지침**: `memory/sessions/P16.{N}wc.md` 또는 4계층

## 즉시 해결 필요
1. ~~Whisper 설치~~ → Phase C 진입 시 (TEREV 파일럿은 우회 가능)
2. ~~LUT 파일 확보~~ → Phase C 진입 시
3. **첫 실전 영상**: TEREV EP01 파일럿 (2~3분, Typecast TTS)

## 디렉토리 구조
```
CineLink/
├── .claude/
│   ├── CLAUDE.md              ← 이 파일
│   └── agents/                ← 5종 Agent (전역)
├── 20260417_012751_CineLink_발전방향.md  ← 정본
├── capcut-claude-hybrid-strategy.md       ← 참조 입력
├── cinelink/
│   ├── docs/                  ← TRAP·표준·아키텍처 문서
│   ├── channels/              ← TEREV·거지맵·_shared
│   ├── shared/scripts/        ← ffmpeg_lib.py, ffmpeg-presets.sh
│   ├── projects/_template/    ← 에피소드 단위 작업 원자
│   └── ...
└── memory/sessions/
```

## 사업화 방향 (PM.4wc 선행연구)
- AI 영상 편집 시장: $1.6B→$9.3B (2025→2030, CAGR 42%)
- 에이전시 모델: 월 $10K~$40K 잠재력
- SeouLink 채널 수익화 우선 → 외부 클라이언트 확장

## 금지/확정 사항
- ❌ `-shortest` FFmpeg 플래그 사용 (CL-TRAP-001)
- ❌ `drawtext`로 한글/일본어 (CL-TRAP-006)
- ❌ concat 직전 오디오 파라미터 미검증 (CL-TRAP-003)
- ❌ 대본 기반 manifest 타이밍을 silencedetect auto-snap 없이 최종 사용 (CL-TRAP-010)
- ✅ 모든 FFmpeg 호출은 `ffmpeg_lib.py` 경유
- ✅ CL-TRAP 새 실패는 즉시 카탈로그 추가
- ✅ 채널 작업은 채널 `.claude/CLAUDE.md` 오버라이드 준수
