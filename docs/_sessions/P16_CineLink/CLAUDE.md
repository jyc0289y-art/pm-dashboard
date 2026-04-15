# CineLink 프로젝트지침

## 프로젝트 개요
- **목적**: AI 영상 제작 파이프라인 (촬영→편집→배포 자동화)
- **P번호**: P16 (P16.{N}wc)
- **최신 세션**: P16.3wc (2026-04-10)
- **브랜드**: CineLink SL
- **선행연구**: GO 판정 (에이전시 모델, CAGR 42%, PM.4wc)

## 기술 스택
- **전사**: Whisper (미설치 — Phase 1 블로커)
- **편집**: FFmpeg 8.0.1 + Python 자동화
- **색보정**: LUT 파일 (미확보 — Phase 2 블로커)
- **TTS**: Typecast API 또는 Edge TTS (미확인)
- **에이전트**: `.claude/agents/` 에 5종 서브에이전트 정의

## 파이프라인 Phase
| Phase | 작업 | 상태 |
|-------|------|------|
| Phase 1 | 음성 전사 + 자막 생성 | 🔴 Whisper 미설치 |
| Phase 2 | 색보정 (LOG→Rec.709) | 🔴 LUT 미확보 |
| Phase 3 | 컷 편집 자동화 | ⚪ 미착수 |
| Phase 4 | BGM/효과음 배치 | ⚪ 미착수 |
| Phase 5 | 최종 렌더링 + 배포 | ⚪ 미착수 |

## 세션 관리
- registry: `memory/sessions/registry.md`
- 포크 시 `P16.{N}wc` 형식

## 현재 단계 (2026-04-11 기준)
- P16.1wc: 파이프라인 가이드 검토 + 프로젝트 시작
- P16.2wc: 서브에이전트 확인 + 스캐폴딩 보완
- P16.3wc: 환경 점검 (Whisper/LUT 블로커 발견)

## 즉시 해결 필요
1. **Whisper 설치**: `pip install openai-whisper` 또는 `brew install whisper`
2. **LUT 파일 확보**: 카메라에 따른 LOG→Rec.709 LUT
3. **첫 영상 프로젝트(C-6) 셋업**: AOMORI(P15) 소재 활용

## 디렉토리 구조
```
CineLink/
├── .claude/agents/     ← 5종 서브에이전트
├── _template/          ← 프로젝트 템플릿
├── shared/
│   ├── luts/           ← LUT 파일 (비어있음)
│   └── fonts/          ← 폰트
├── brand/
│   └── brand-guide.md  ← 브랜드 가이드
└── memory/sessions/    ← 세션 관리
```

## 사업화 방향 (PM.4wc 선행연구)
- AI 영상 편집 시장: $1.6B→$9.3B (2025→2030, CAGR 42%)
- 에이전시 모델: 월 $10K~$40K 잠재력
- SeouLink 채널 수익화 우선 → 외부 클라이언트 확장
