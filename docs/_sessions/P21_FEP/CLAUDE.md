# P21 FEP (Familiar Experience Psychology) 프로젝트지침

## 정체성

- **P번호**: P21
- **프로젝트명**: FEP (Familiar Experience Psychology)
- **채널명**: 일상속 경험들의 심리학
- **슬로건**: 당연하다고 넘긴 순간, 거기에 심리학이 있었습니다.
- **디렉토리**: `~/Library/Mobile Documents/com~apple~CloudDocs/developer/FEP/`

## 채널 컨셉

- 누구나 겪어봤지만 아무도 분석하지 않은 일상 에피소드를 심리학적으로 해부
- **시네마틱 심리극** — 영화적 연출 + 심리학 해설의 융합 (정보 강의 X)
- AI 일러스트(ComfyUI + FLUX Kontext Dev) + TTS 내레이션 + 캐릭터 대사 조합
- 톤: 장난스럽지만 핵심은 정확하게
- 타겟: 한국어 화자, 2030세대

## 영상 연출 원칙 (v2 — 시네마틱 오버홀)

### 영상 규격
- **롱폼**: 10~15분 (3막 드라마 구조, 기존 5분 정보전달에서 확대)
- **쇼츠**: 1~3분 (극적 연출 포함, 기존 15~25초에서 확대)
- **쇼츠 편수**: 5편 (롱폼 검수 후 별도 각본)

### 핵심 연출 철학
1. **Show, Don't Tell**: 심리학 개념을 먼저 설명하지 않는다. 장면으로 보여주고, 시청자가 "왜 그렇지?"라고 느낀 순간에 해설이 들어온다
2. **침묵의 힘**: 대사 사이의 정적(0.5~1초)이 불편함을 체감시킨다. 빽빽한 해설로 채우지 않는다
3. **반복과 변주**: 핵심 대사가 에피소드 내에서 반복되되, 매번 다른 맥락과 감정으로
4. **시점 전환**: 같은 상황을 여러 인물 시점으로 보여주며 입체적 해석
5. **감정 아크**: 가벼움(코미디) → 불편함(서스펜스) → 통찰(카타르시스) → 여운(성찰)
6. **감정 잔상 (Emotional Residue)**: 각 파트 종료 후 1~2초 정적 + 일러스트 홀드. 다음 파트로 서두르지 않는다
7. **대비의 원칙**: 밝은 직후에 어둡게, 유머 직후에 진지하게. 감정 고저차가 클수록 임팩트

### 구조 패턴
- 3막 구조: 프롤로그(훅) → 1막(상황 설정) → 2막(시점별 심리 해부) → 3막(통찰+정리) → 에필로그(시청자 자기투영)
- 음성 구성: 내레이터(해설) + 캐릭터 대사(대화/내면 독백)
- BGM 설계: 감정 전환점마다 음악 톤 변화, 정적의 전략적 활용
- 일러스트 연출: 정지 장면이더라도 구도/조명/색감으로 감정 전달 (카메라 무빙 집착 X)

### 감정 곡선 설계
- 에피소드마다 감정 곡선 차트를 먼저 설계한 후 각본 작성
- 5단 감정 설계: ① 일상의 균열 → ② 불편의 자각 → ③ 내면의 폭풍 → ④ 조용한 항복/반전 → ⑤ 거울 앞의 나
- 비트(정적) 시간 명시: 감정이 무거운 전환점일수록 정적을 길게

### 캐릭터 대사 가이드
- 캐릭터는 단순 선역/악역이 아닌 입체적 인물
- 내면 독백: 시청자가 자기 목소리로 느끼게
- 대사 딜레이: 진심이 아닌 대답은 0.2~0.3초 딜레이로 표현

### 듀얼 그림체 시스템 (Dual Art Style)
> 크레용 신짱처럼 상황에 따라 그림체를 전환하여 감정 임팩트를 극대화한다.

- **스타일 A (SD 귀여운체)**: 2.5등신, 둥글고 귀여운 비율 — 기존 캐릭터 시트 기반
  - **용도**: 일상/코믹/가벼운 장면, 프롤로그, 에필로그, 쇼츠
  - **생성**: 캐릭터 시트(스타일 A) img2img 참조 + 흰 배경 → 알파 추출
  - **느낌**: 친근, 유머, 시청자 친화적
- **스타일 B (시네마틱 리얼체)**: 6-7등신, 웹툰 비율 — txt2img 생성
  - **용도**: 진중한/감정적/서스펜스 장면, 2막 심리 해부, 내면 독백
  - **생성**: 캐릭터 시트(스타일 B) img2img 참조 + 그린 스크린 → 크로마키 알파
  - **느낌**: 성숙, 몰입, 시네마틱

**전환 규칙:**
1. 감정 곡선의 전환점에서 그림체 전환 — 갑자기 바뀌면 시청자가 "분위기 바뀌었다" 인지
2. 같은 씬 내 전환 금지 — 씬 단위로 스타일 결정
3. 스타일 A→B 전환은 감정이 무거워질 때, B→A는 가벼워질 때
4. 각본에 `[스타일: A]` 또는 `[스타일: B]` 태그로 씬별 스타일 지정
5. 한 에피소드 내 스타일 전환 2~4회가 적당 (너무 잦으면 산만)

**파일 체계:**
- `characters/style_A/` — 기존 캐릭터 시트 기반 (img2img + 흰 배경 제거)
- `characters/style_B/` — 시네마틱 캐릭터 시트 기반 (img2img + 그린 스크린)
- `v3_layers/characters/` — 합성용 포즈 (style_A_, style_B_ 접두사로 구분)
- `v3_layers/alphas/` — 알파 추출 결과 (스타일 무관, 같은 폴더)

## 시리즈 구조

- 남자 주인공 **민준**(캐릭터 B)을 중심으로 주변인물과의 에피소드를 매회 심리학적 해석
- 영상 제목 구조: **[___의 심리학] — [훅/부제]**
- 롱폼(10~15분) + 쇼츠 5편(1~3분) 세트 제작

## 시리즈 고정 캐릭터

- **민준** (캐릭터 B): 시리즈 전체 고정 주인공. `FEP/characters/char_B_minjun.png`

## 기술 스택

- **일러스트**: ComfyUI + FLUX Kontext Dev (로컬, MacBook Apple Silicon)
- **TTS 초안**: edge-tts (ko-KR-InJoonNeural)
- **TTS 최종**: Typecast
- **영상 편집**: FFmpeg + Python (build_video_v3.py — LP+말풍선 통합)
- **텍스트 오버레이**: Pillow 기반 (FFmpeg drawtext 불가)
- **작업 환경**: Claude Code

## 파일 구조 규칙

- 시리즈 공용 캐릭터 시트: `FEP/characters/`
- 에피소드별 폴더: `FEP/EP{NN}_{영문명}/`
- 에피소드별 캐릭터: `EP{NN}/characters/`
- 일러스트 세이프 존: 핵심 요소를 중앙 세로 1/3에 배치 (9:16 쇼츠 크롭 대비)

### 에셋 오염 방지 체계 (Asset Isolation)

> **⚠️ 기존 에셋과 신규 에셋은 물리적으로 완전 격리한다.**

#### 1. 격리 디렉토리 원칙
```
EP01_forced_compliment/
├── scenes/              # ← 기존 v1/v2 (절대 건드리지 않음)
├── output/              # ← 기존 (절대 건드리지 않음)
├── v3_layers/           # ← 신규 레이어 기반 에셋 (격리됨)
│   ├── _meta/           # 생성 로그, 버전 정보
│   ├── locations/       # 장소 마스터 + 변형
│   ├── characters/      # 캐릭터 포즈 (솔리드 bg)
│   ├── alphas/          # 알파 추출 결과
│   ├── scenes/          # 씬별 합성 결과
│   └── lp/              # LivePortrait 영상
```

#### 2. 파일명 규칙 (타임스탬프 필수)
```
{YYYYMMDD}_{HHMMSS}_{type}_{id}_{detail}.png

예시:
20260414_010530_loc_living_room_master.png
20260414_010845_char_subin_standing_front.png
20260414_011200_char_subin_standing_front_alpha.png
20260414_012000_comp_S03_final.png
```

- **모든 생성 파일에 타임스탬프 접두사 필수** — 동일 에셋 재생성 시에도 기존 파일 유지
- type 코드: `loc` (장소), `char` (캐릭터), `prop` (소품), `comp` (합성), `lp` (애니메이션)

#### 3. 생성 로그 (generation_log.json)
매 생성마다 아래 기록 → 재현성 + 추적성 확보:
```json
{
  "filename": "20260414_010530_loc_living_room_master.png",
  "type": "location",
  "prompt": "...",
  "seed": 12345,
  "steps": 20,
  "cfg": 3.5,
  "resolution": "1344x768",
  "comfyui_prompt_id": "abc-123",
  "timestamp": "2026-04-14T01:05:30"
}
```

#### 4. 금지 사항
- ❌ 기존 `scenes/`, `output/` 디렉토리에 신규 파일 쓰기 금지
- ❌ 기존 파일 덮어쓰기/삭제 금지
- ❌ 타임스탬프 없는 파일명 생성 금지
- ❌ ComfyUI output 디렉토리에서 직접 사용 금지 — 반드시 v3_layers/로 복사 후 사용

## 현재 단계 (EP.01 — 강요된 칭찬의 심리학)

### v1 파이프라인 (완료 — 시네마틱 오버홀로 대체)
- ✅ Phase 0~7d: v1 제작 완료 (5분 정보전달 영상 + 쇼츠 7편 + BGM)
- ❌ v1은 시네마틱 오버홀(v2)로 대체됨

### v2 시네마틱 오버홀 (진행중)
- ✅ Phase 8a: 시네마틱 각본 v2 집필 (12~14분, 3막 드라마)
  - 파일: `EP01_forced_compliment/20260413_075604_EP01_시네마틱_각본.md`
  - 구조: 프롤로그 → 1막(상황) → 2막(민준/지우/수빈 시점) → 3막(정리) → 에필로그
  - 캐릭터 대사 + 내레이터 해설 혼합, 감정 곡선/BGM 디렉션 포함
  - 자막 주석 시스템(용어/주석/비교/라벨 4종) + 심리학 12/12 커버리지 검증 완료
- ✅ Phase 8a-2: 영상 연출 원칙 + TTS 감정 연출 전략 지침 반영
  - CLAUDE.md에 시네마틱 연출 원칙 7항 + TTS 후처리 전략 기록
  - Typecast 역량 분석: 70~80% 직접 가능, 나머지는 대사 분할+FFmpeg 후처리로 보완
- ✅ Phase 8b: 각본 사용자 검수 완료
  - 초벌 TTS 스크립트: `EP01_forced_compliment/generate_tts_v2.sh` (edge-tts, 16클립)
- ✅ Phase 8c: 쇼츠 v2 각본 (1~3분 × 5편) + BGM/SFX 설계
  - 쇼츠 각본: `EP01_forced_compliment/20260413_095251_EP01_쇼츠v2_각본.md`
  - BGM/SFX 설계: `EP01_forced_compliment/20260413_095251_EP01_BGM_SFX_설계.md`
  - Typecast 캐릭터 보이스 일관성 전략 → CLAUDE.md 재사용 시스템 #9에 기록
- ✅ Phase 8c-2: Typecast 보이스 캐스팅 준비
  - 4역할(내레이터/수빈/민준/지우) × 3후보 = 12명 선별 + 즐겨찾기 + 역할 메모 완료 (11/12, 시원 즐겨찾기 미표시 버그)
  - 후보 목록은 아래 "Typecast 보이스 캐스팅 후보" 섹션 참조
  - Typecast PRO 연간 플랜(₩35,000/월) 결정 — 주 2편 롱폼+쇼츠 기준 ~95분/월
- ✅ Phase 8d: v3 레이어 기반 일러스트 완성
  - 로케이션 8장 (5장 앰버→산뜻 자연광 재생성), 캐릭터 24장 (듀얼 스타일 A/B)
  - 알파 24장 (Flood Fill), 최종 씬 27장 (포트레이트 11 + 일반 14 + S-00 블랙 + S-02 타이틀)
  - `v3_composite_portrait.py` (auto_crop 기능 추가) + `v3_composite_scenes.py`
- ✅ Phase 8f: build_video_v2.py 프리뷰 빌드 완성
  - edge-tts 16클립 생성 (audio/longform_v2/, 644초=10.7분)
  - v3 씬 27장 → 16개 오디오 클립에 시간 분할 매핑
  - 스토리라인-시각 정합성 검토 완료 (아래 "정합성 검토 결과" 참조)
  - 프리뷰: `output/20260414_*_EP01_v2_preview.mp4` (11.0분, 1920×1080)
  - 숨쉬기 효과: OFF (BREATHING_INTENSITY=0.0)
  - 비트 클립: 24000Hz/mono (edge-tts와 일치, concat 호환)
- ✅ Phase 8d-2: LivePortrait 캐릭터 애니메이션 (눈/입 움직임)
  - Style B 캐릭터 18종 × 2 모션(talking/idle) = 36개 중 34개 성공 (94%)
  - 실패 2개: minjun_reaction (얼굴 미감지 → 브리딩 폴백)
  - LP 영상: 그린스크린(#00FF00) → FFmpeg chromakey로 실시간 합성
  - 출력: `v3_layers/lp/{timestamp}_alpha_B_{char}--{motion}.mp4`
- ⬚ Phase 8e: Typecast TTS 녹음 (감정별 분할 클립 + 후처리 타이밍)
  - 보이스 확정: 내레이터=대길, 수빈=지안, 민준=한준, 지우=진서
- 🟡 Phase 8e-2: 텍스트 오버레이 + 말풍선 합성 시스템
  - ComfyUI FLUX로 말풍선 5종(speech L/R/C + thought L/R) + 알파 생성 완료
  - ComfyUI FLUX로 천사 2종 + 악마 2종 캐릭터 + 알파 생성 완료
  - 콩이 포즈 8종 ComfyUI 생성 + 알파 완료
  - `build_video_v3.py` 통합 빌드: LP chromakey + 말풍선 오버레이 + 시간 페이드
  - S-06 프리뷰 완성 (`clips_v3/preview_S-06_FINAL.mp4`, 26.6초)
  - 말풍선 꼬리 방향: speaker_x_ratio 기반 자동 + 꼬리-캐릭터 정렬 오프셋 구현 완료
  - Pillow 텍스트 렌더링 품질 이슈 남아있음 → Typecast 단계 후 최종 조정 예정
  - 에셋: `assets/bubbles/`, `assets/angel/`, `assets/devil/`
- ⬚ Phase 8g: BGM/SFX 소싱 + 믹싱 (Pixabay + YouTube Audio Library)
- ⬚ Phase 8h: 영상 조립 + 최종 QA
- ⬚ Phase 8i: 업로드 준비

### 스토리라인-시각 정합성 검토 결과 (P21.7wc)
- ✅ S-00 블랙 스크린 추가 — 프롤로그 "질문 하나 할게요" 목소리만 긴장
- ✅ S-02 타이틀 카드 생성 — "강요된 칭찬의 심리학" 3막 진입 숨 고르기
- ✅ S-23 프롤로그 bookend — "세 사람의 심리" 언급 시 세 캐릭터 표시
- ✅ 01_siblings 비율 보정 — S-04(7%) S-05(22%) S-06(56%) 텍스트 비율 반영
- ✅ S-08 연속 59초→30초 완화 — 03_validation을 S-07+S-08 분할, 04_transition을 S-05로 교체
- ✅ S-07 콩이 auto_crop — 작은 캐릭터 투명 영역 자동 제거
- 🟡 S-12 자판기: 수빈 없음, "칭찬 버튼" 없음 — 텍스트 오버레이로 보완 예정
- 🟡 S-24 빈 의자: 네 번째 의자 지목 어려움 — 텍스트 오버레이로 보완 예정
- 🟡 S-25 CTA: 미생성 — Pillow로 생성 예정 (낮은 우선순위)

## 금지/확정 사항

- ❌ 정보 전달 강의 스타일 금지 — 시네마틱 심리극 연출 (Show, Don't Tell)
- ❌ 초보적 카메라 무빙(zoompan 등)에 대한 집착 금지 — 정지된 장면이더라도 구도/조명/색감으로 감정 전달
- ❌ 내레이터 단독 해설 금지 — 캐릭터 대사(대화/내면 독백) + 내레이터 해설 혼합 필수
- ❌ 캐릭터를 단순 선역/악역으로 그리지 않음 — 모든 캐릭터는 입체적 인물
- ✅ 롱폼 10~15분 (3막 드라마 구조), 쇼츠 1~3분 × 5편
- ✅ 감정 곡선 차트를 먼저 설계한 후 각본 작성
- ✅ 의도적 정적(비트)으로 감정 체감 시간 확보 — 빽빽한 해설 금지
- ✅ BGM은 감정 전환점마다 톤 변화 설계
- ✅ 듀얼 그림체: 스타일 A(SD 귀여운체) + 스타일 B(시네마틱 리얼체) — 감정 곡선에 따라 씬 단위 전환
- ❌ 같은 씬 내에서 그림체 전환 금지 — 씬 단위로만 결정
- ✅ 스타일 B 캐릭터 생성 시 캐릭터 시트(스타일 B) 참조 필수 — txt2img 단독 사용 시 캐릭터 일관성 붕괴
- ✅ 스타일 A 캐릭터 생성 시 캐릭터 시트(스타일 A) img2img 참조 + 흰 배경 제거
- ❌ **완성 씬 일괄 생성 금지 (EP.02~)** — 배경/캐릭터/소품을 독립 레이어로 생성 후 합성 (재사용 시스템 #5 참조)
- ❌ 복잡한 배경 위에서 rembg 캐릭터 분리 금지 — 솔리드 배경(#00FF00)에서 생성 후 추출
- ✅ 캐릭터는 솔리드 그린 배경 위에서 개별 생성 → 크로마키/rembg로 알파 추출
- ✅ 같은 장소 씬은 BG 마스터 1장에서 파생 (거실 5씬, 카페 5씬 등)
- ✅ 파일명: `FEP_{scene_id}_{layer}_{name}.png` (bg/char/prop/comp 구분)
- ✅ 에피소드 시작 시 장소 마스터 + 캐릭터 포즈 라이브러리 먼저 구축 후 씬 합성
- ❌ 장소 변형을 txt2img로 새로 생성 금지 — 마스터에서 Pillow 후처리 또는 img2img (denoise ≤ 0.3)
- ❌ 캐릭터 시트 없이 씬 생성 금지 — 반드시 캐릭터 레퍼런스 확보 후 씬 작업 시작
- ✅ 표정/포즈 변형은 img2img 우선 (denoise 0.3~0.5), 구조 변경 시에만 txt2img
- ❌ AI 일러스트에 텍스트/글자 직접 생성 금지 — Pillow 후처리 필수
- ❌ FP8 모델은 MPS(Apple Silicon)에서 사용 불가 — GGUF Q8 사용
- ❌ FFmpeg drawtext 필터 사용 불가 — Pillow 기반 오버레이 사용
- ❌ scene 프롬프트에 "dark/shadow/black" 직접 사용 금지 — AI가 검은 화면으로 해석 (scene_13 사례)
- ❌ `-shortest` 플래그만으로 싱크 제어 금지 — `-loop 1` + zoompan 조합에서 1~2초 오버런 발생, 반드시 `-t {duration}` 명시
- ❌ build_longform의 glob에 `_seg/_cut/_bcut` 임시 파일 포함 금지 — B컷 세그먼트 이중 concat으로 133초 부풀림 사고 발생
- ✅ **모든 출력물 파일명에 타임스탬프 필수**: `YYYYMMDD_HHMMSS_설명.확장자` (빌드 영상, 프리뷰, 클립, 롱폼 모두 적용 — 전후 관계 파악 + 덮어쓰기 방지)
- ✅ 다국어 전략: 단일 채널 + 멀티 오디오 + 번역 메타데이터 (채널 분리 X)
- ✅ 텍스트 오버레이는 manifest.json + Pillow 기반 후처리 (A=말풍선, B=생각풍선, C=심리학용어, D=킬링라인, E=구조라벨 — 5가지 타입 전체 구현)
- ✅ 말풍선/천사/악마 에셋은 ComfyUI FLUX로 생성 (Pillow 다각형 품질 부적합 확정)
- ✅ LP 영상은 그린스크린 → FFmpeg chromakey `0x30C010:0.12:0.02` 로 합성 (기존 0x40E810:0.25:0.08은 반투명/초록끼 → 폐기)
- ✅ 말풍선 위치는 PORTRAIT_RECIPES의 캐릭터 position 좌표 연동 (화자 머리 위 배치)
- ✅ 말풍선 꼬리 방향은 speaker_x_ratio 기반 자동 결정 (좌 < 0.5 → left, 우 ≥ 0.5 → right) + 꼬리-캐릭터 정렬 오프셋
- ✅ SPEAKER_NAME_MAP: 한국어 화자명 → 영어 alpha_pattern 키 변환 (수빈→subin, 민준→minjun, 지우→jiwoo)
- ✅ `build_video_v3.py`: LP chromakey + 말풍선 오버레이 + 시간 기반 페이드 통합 빌드
- ✅ LP portrait 전환 완료: S-10(단색BG+민준), S-16(카페+지우), S-17(카페+수빈+지우), S-21(침실+수빈) — 캐릭터 없는 배경 위 LP 합성
- ❌ LP를 기존 씬 이미지(캐릭터 baked-in) 위에 합성 금지 — 반드시 PORTRAIT_RECIPES로 캐릭터 없는 BG 구성 후 LP 오버레이
- ✅ 말풍선 에셋: `assets/bubbles/{speech,thought}_bubble_{left,right,center}_alpha.png`
- ✅ 천사/악마 에셋: `assets/{angel,devil}/{angel,devil}_character{,_left,_right}_alpha.png`
- ✅ 콩이 포즈 라이브러리: 8종 (`sitting_front/happy, crawling, reaching, sleeping, clapping, crying, looking_up`)
- ❌ Pillow 말풍선 생성은 품질 부적합 — ComfyUI 에셋만 사용
- ✅ 지우 보이스 리캐스팅 예정: 여성 → 변성기 전 소년 (성숙한 말투)
- ✅ 캐릭터 D 이름: 지우 (지호에서 변경, 중성적 외형 + 바지 착용)
- ✅ ComfyUI 실행: `cd ~/developer/ComfyUI && python main.py --listen 0.0.0.0 --port 8188`
- ✅ GGUF 모델: flux1-kontext-dev-Q8_0.gguf (UnetLoaderGGUF 노드 사용)
- ✅ HuggingFace 계정: Jinyjyc (토큰: [REDACTED])
- ✅ find_scene_image: `_alt` 파일 제외 필수 (macOS APFS glob 순서 비결정적)
- ✅ 수빈+아기 씬(scene_05): 마주보는 구도 → 쇼츠는 center 크롭 (split 불가)
- ❌ `--overlay` 빌드는 output/ 파일을 덮어씀 — 오버레이 영상은 반드시 별도 파일명으로 저장 (예: `_ko` 접미사)
- ❌ rembg 전경 분리는 머리카락 경계를 거칠게 잘라냄 — 패럴랙스에 rembg 단독 사용 금지, LivePortrait 사용 권장
- ❌ rembg는 거울 반사/말풍선 등 "전면 물체" 전체를 전경으로 분류 — 배경 요소까지 전경에 포함되는 문제
- ❌ onnxruntime-silicon==1.16.3은 현재 pip에서 설치 불가 — `onnxruntime` (일반)으로 대체
- ❌ LivePortrait named pkl 템플릿(wink.pkl 등)에 eye/lip 데이터 없음 — pipeline.py 패치 필수 (zeros 폴백)
- ❌ FFmpeg zoompan 필터는 비디오 입력과 호환 불가 — scale+crop 조합으로 미세 줌 대체
- ❌ LivePortrait는 단순한 만화체 얼굴 미감지 — 해당 씬은 브리딩 폴백
- ❌ B컷 세그먼트에 LivePortrait 적용 금지 — B컷은 별도 이미지이므로 메인 씬 LP 영상 사용 불가
- ✅ LivePortrait: 로컬(MPS) + 무료 + CLI 자동화 → 비치키 수준 애니메이션의 핵심 도구
- ✅ LivePortrait 실행: `PYTORCH_ENABLE_MPS_FALLBACK=1 python inference.py`
- ✅ LivePortrait 가중치: `~/developer/LivePortrait/pretrained_weights/` (HuggingFace KlingTeam/LivePortrait)
- ✅ LivePortrait 배치: 씬당 ~40-60초 (MPS), 14/15 성공률
- ✅ LP 클립 빌드: `-stream_loop -1` + `scale+crop` 미세줌 + `-t duration`
- ✅ Typecast PRO 연간 플랜: ₩35,000/월 — 주 2편 기준 최적
- ✅ BGM 소싱: Pixabay Music (무료, 상업적 이용 가능) + YouTube Audio Library (무료)
- ✅ 포트레이트 모드 합성 (Portrait Mode Compositing): 배경 위에 캐릭터를 정위치시키기 어려운 경우, 배경을 뒤에 깔고 캐릭터 상반신을 앞에 나열하는 방식 허용 (포켓몬스터/비주얼노벨 스타일). 배경과 캐릭터의 물리적 상호작용(의자에 앉기 등) 대신 감정 전달에 집중.
- ✅ 이미지 생성 시 합성 고려 필수: 캐릭터 생성 시 합성 대상(상반신 포트레이트 vs 전신 vs 환경 내 배치)을 사전 결정하고, 프롬프트에 프레이밍 명시 (예: "upper body portrait", "full body on green screen")
- ✅ Style A 알파 추출: Flood Fill 방식 사용 (가장자리 연결 흰색만 제거) — 글로벌 threshold는 흰 옷을 투명하게 만드는 문제 있음
- ✅ 크로마키 알파 추출 시 green spill 보정 필수 — 머리카락 갈라진 부분에 초록끼 잔류 → `despill_green()` 함수로 주변색 블렌딩 (기존 생성분은 수정 불필요, 향후 새 추출 시 자동 적용)

## ⚠️ TRAP 함정 관리 시스템 (필수 참조)

> **⚠️ 매 세션 시작 시 + 새 Phase 진입 시 반드시 아래 문서의 TRAP 인덱스를 먼저 읽을 것.**
> `FEP/docs/20260415_092337_FEP_영상제작_TRAP_관리시스템.md`
> (구 파일명: `docs/production_lessons.md` — 2026-04-16 리네임)
> — **TRAP-001~030**: 일러스트, 알파 추출, FFmpeg, LP, 말풍선, 대사 타이밍, 메모리 관련 시행착오 30건 + 절차 체크리스트
> — 각 TRAP에 **원인 파일/수정 파일/예방책** 기록 → 같은 함정 재진입 방지
> — 신규 시행착오 발견 시 즉시 다음 TRAP 번호 부여하여 등록 (TRAP-031~)

## 재사용 시스템 (에피소드 공용)

### 1. 브리딩 효과 (Breathing v6 — 랜덤 모션)
- **위치**: `build_video.py` → `ken_burns_filter()` + `BREATHING_INTENSITY`
- **원리**: 내부 2x 업스케일(3840×2160) + 복합 사인파(2개 주기 합성) + Lanczos 다운스케일
- **해결한 문제**: 정지 일러스트 어색함. v1(수전증)→v2(너무 미세)→v3(양자화)→v4/v5(해결)→v6(랜덤위상)
- **v6 추가**: 씬별 MD5 해시 기반 랜덤 위상/진폭 → 씬마다 다른 모션 패턴 (결정론적 재현 가능)
- **클램핑**: 수평 ±30px, 수직 ±24px 제한 → 구석 클로즈업 방지
- **인터렉티브**: `--breathing 1.5` CLI 옵션 또는 `BREATHING_INTENSITY` 상수 직접 수정 (0.0~3.0)
- **다음 에피소드**: 코드 수정 없이 자동 적용

### 2. B컷 시스템
- **위치**: `build_video.py` → `SCENE_BCUTS` 딕셔너리 + `_build_bcut_clip()`
- **원리**: 17초+ 긴 씬을 cut_at 비율로 분할, B컷 서브일러스트 삽입
- **폴백**: B컷 이미지 없으면 메인 이미지로 자동 대체
- **다음 에피소드**: `SCENE_BCUTS` 딕셔너리만 교체하면 됨

### 3. 쇼츠 멀티세그먼트 + 크롭 시스템
- **위치**: `build_video.py` → `SHORTS_CONFIG` (dict 리스트) + `build_shorts()`
- **멀티씬**: 각 쇼츠가 segments 리스트로 여러 씬 이미지를 시간 분할 표시
- **크롭 모드**: center / left / right (세그먼트별 독립 지정)
- **결정 기준**: 마주보는 구도→center, 좌우 분산→left+right 분할, 단일 인물→해당 방향
- **교훈**: 나레이션이 여러 상황 언급 시 반드시 멀티 씬 구성 (단일 이미지 사용 금지)

### 4. 텍스트 오버레이
- **위치**: `build_video.py` → `apply_text_overlays()` + Pillow
- **데이터**: `text_overlay_manifest.json` (씬별 오버레이 정의)
- **다국어**: `--lang ko|ja|en` 지원, 단일 manifest에서 `text_ko/ja/en` 키 분기

### 5. 레이어 분리 생성 원칙 (Layer-Based Generation, v2 이후 필수)

> **⚠️ 이 원칙은 EP.02부터 모든 일러스트 생성에 적용한다. 완성 씬 일괄 생성 방식은 폐기.**

#### 핵심 철학
씬을 완성 이미지로 한 번에 생성하지 않는다. **배경, 캐릭터, 소품을 독립 레이어로 생성**한 뒤 Pillow/FFmpeg로 합성한다. 이렇게 해야 캐릭터 애니메이션(LP), 패럴랙스, 재사용이 모두 자연스럽다.

#### 레이어 구조 (씬당)
```
layers/{scene_id}/
├── bg.png                    # 배경 (캐릭터 없는 환경)
├── char_{name}.png           # 캐릭터 (솔리드 배경 위)
├── char_{name}_alpha.png     # 캐릭터 (배경 제거, 투명)
├── char_{name}_lp.mp4        # 캐릭터 LP 애니메이션
├── prop_{item}.png           # 소품/전경 요소 (필요시)
├── shadow_{name}.png         # 캐릭터 그림자 (필요시)
└── comp.png                  # 합성 결과 (레퍼런스)
```

#### 생성 순서
1. **레퍼런스 합성 이미지** — 완성 구도를 먼저 txt2img로 생성 (위치/스케일/조명 기준)
2. **BG 레이어** — "same scene but completely empty, no characters, no people" 프롬프트
3. **캐릭터 레이어** — 각 캐릭터를 `solid bright green background (#00FF00)` 위에 개별 생성
   - 레퍼런스의 포즈/표정/조명 방향을 프롬프트에 명시
4. **알파 추출** — 솔리드 배경 → 크로마키 또는 rembg (솔리드 bg에서는 rembg 품질 우수)
5. **소품/FG** — 전경 요소가 있으면 별도 생성
6. **합성** — Pillow로 BG + 캐릭터(알파) + FG 레이어 합성

#### 프롬프트 규칙
- **BG**: `"...environment, empty room, no people, no characters, no figures, ..."`
- **캐릭터**: `"...character on solid bright green background #00FF00, full body visible, ..."`
- **조명 일치**: BG와 캐릭터 프롬프트에 동일한 조명 방향 명시 (예: "warm light from left side")
- **스케일 힌트**: 캐릭터 프롬프트에 프레임 내 비율 명시 (예: "waist up filling 60% of frame")

#### 합성 모드별 생성 전략 (EP.02~)

| 합성 모드 | 캐릭터 프롬프트 | 스케일/위치 | 적합 씬 |
|-----------|---------------|-----------|---------|
| **정위치 (Placed)** | "full body, standing/sitting in environment" | 환경 내 좌표 지정 | 단독 캐릭터 + 단순 배경 |
| **포트레이트 (Portrait)** | "upper body portrait, chest up, centered" | BG 전체 + 캐릭터 하단 30~50% 오버레이 | 대화 씬, 멀티캐릭터, 감정 클로즈업 |
| **풀 오버레이 (Full Overlay)** | 씬 전체를 한 이미지로 생성 (Style B) | scale=1.0, x=0, y=0 | 단독 캐릭터 클로즈업, 메타포 씬 |

**생성 전 체크리스트 (EP.02~)**:
1. 각본에서 씬별 합성 모드 결정 (정위치/포트레이트/풀오버레이)
2. 포트레이트 모드 씬 → 캐릭터를 "upper body, chest up" 프롬프트로 생성
3. 정위치 모드 씬 → 캐릭터를 "full body on solid green" + 환경 내 위치 명시
4. 풀 오버레이 씬 → Style B 캐릭터를 환경 포함하여 한 이미지로 생성

#### 파일명 규칙
```
FEP_{scene_id}_bg.png              # 배경
FEP_{scene_id}_char_{name}.png     # 캐릭터 (솔리드 bg)
FEP_{scene_id}_char_{name}_a.png   # 캐릭터 (알파)
FEP_{scene_id}_prop_{item}.png     # 소품
FEP_{scene_id}_comp.png            # 합성 결과
```

#### 재사용 이점
| 요소 | 재사용 범위 |
|------|-----------|
| 거실 BG | S-03/S-04/S-06/S-08/S-09 (같은 장소, 조명만 변경) |
| 카페 BG | S-15/S-16/S-17/S-18/S-19 |
| 수빈 캐릭터 (서있는 포즈) | S-04/S-06/S-11 |
| 민준 캐릭터 (소파) | S-03/S-08 |

#### 합성 시 주의사항
- **그림자**: 솔리드 bg 캐릭터에는 환경 그림자가 없음 → Pillow로 반투명 그림자 레이어 추가
- **엣지 페더링**: 알파 추출 후 가장자리 1~2px 페더링으로 자연스러운 합성
- **색감 통일**: 합성 후 전체 씬에 동일 컬러 그레이딩 적용 (레이어 간 색온도 차이 보정)
- **깊이 순서**: BG → 후경 소품 → 캐릭터 → 전경 소품 순서로 레이어링

#### rembg 재평가
- ❌ 이전: 복잡한 씬에서 캐릭터 분리 → 머리카락/반사 파괴 (폐기 판정)
- ✅ 변경: 솔리드 배경(#00FF00)에서 캐릭터 분리 → 깨끗한 알파 추출 (복원)
- 대안: OpenCV 크로마키 (`cv2.inRange` + `morphologyEx`) — 더 정밀한 제어 가능

#### EP.01 적용 범위
- EP.01은 이미 완성 씬 방식으로 대부분 생성 완료 → **EP.01은 기존 방식 유지**
- EP.02부터 레이어 분리 원칙 전면 적용
- EP.01의 LP 멀티캐릭터 오버레이(#11)는 기존 이미지에서 크롭 방식으로 진행

### 5-2. 에셋 일관성 시스템 (Asset Consistency System)

> **⚠️ 레이어 분리 생성(#5)의 핵심 전제. 일관성 없는 레이어는 합성해도 어색하다.**

#### A. 에셋 라이브러리 구조

```
FEP/assets/
├── locations/                     # 장소 마스터
│   ├── living_room/
│   │   ├── master.png             # 기준 배경 (캐릭터 없음)
│   │   ├── warm_afternoon.png     # 변형: 따뜻한 오후
│   │   ├── cold_desaturated.png   # 변형: 차가운 회상
│   │   ├── night_dim.png          # 변형: 밤
│   │   └── location.json          # 메타데이터
│   ├── cafe/
│   │   ├── master.png
│   │   ├── rainy_window.png
│   │   └── location.json
│   ├── bedroom_subin/
│   ├── hallway_jiwoo/
│   └── ...
├── characters/                    # 캐릭터 마스터 (듀얼 스타일)
│   ├── subin/
│   │   ├── ref_sheet_A.png        # 스타일 A 시트 (SD 귀여운체 2.5등신)
│   │   ├── ref_sheet_B.png        # 스타일 B 시트 (시네마틱 리얼체 6-7등신)
│   │   ├── style_A/               # 스타일 A 포즈 라이브러리
│   │   ├── style_B/               # 스타일 B 포즈 라이브러리
│   │   └── character.json         # 의상/외형 메타데이터 + 스타일 매핑
│   ├── minjun/
│   ├── jiwoo/
│   └── ...
└── props/                         # 공용 소품
    ├── coffee_cup.png
    ├── phone.png
    └── ...
```

#### B. 장소 마스터 시스템 (Location Master)

**원칙: 같은 장소의 모든 씬은 하나의 마스터 BG에서 파생한다.**

1. **마스터 생성**: 에피소드 기획 시 장소 목록 확정 → 장소당 1장 마스터 BG txt2img 생성
2. **변형은 후처리**: 시간대/분위기 변형은 마스터에서 Pillow 필터로 파생 (새로 생성 X)
   - 채도 감소 → 회상/내면 씬
   - 블루-그레이 톤 → 밤/우울 씬
   - 따뜻한 오렌지 → 오후 햇살 씬
   - 어둡게 + 단일 광원 → 밤 + 간접등 씬
3. **img2img 변형**: 구조 변경이 필요할 때만 (예: 창밖 비 추가) 마스터를 img2img 입력으로 사용
4. **카메라 앵글**: 같은 장소라도 와이드/미디엄/클로즈업 BG가 필요 → 마스터에서 크롭 또는 앵글별 생성

**location.json 구조:**
```json
{
  "id": "living_room",
  "name": "민준의 거실",
  "master": "master.png",
  "lighting_direction": "warm light from left window",
  "key_elements": ["beige sofa left-center", "side table with lamp right", "curtain left wall", "shelf back wall"],
  "character_positions": {
    "minjun_sofa": {"x": 0.3, "y": 0.6, "scale": 0.7, "pose": "sitting/lying"},
    "subin_standing": {"x": 0.6, "y": 0.5, "scale": 0.8, "pose": "standing"}
  },
  "variants": {
    "warm_afternoon": {"filter": "warm_orange +15%, brightness +10%"},
    "cold_desaturated": {"filter": "saturation -60%, blue_tint +20%"},
    "night_dim": {"filter": "brightness -50%, single_lamp_glow"}
  },
  "used_in_scenes": ["S-03", "S-04", "S-06", "S-08", "S-09"]
}
```

**EP.01 장소 맵 (예시):**

| 장소 ID | 장소명 | 사용 씬 | 변형 |
|---------|--------|---------|------|
| living_room | 민준의 거실 | S-03/04/06/08/09/11 | 따뜻한 오후, 차가운 회상, 압박 조명 |
| cafe | 카페 창가 | S-15/16/17/18/19 | 기본, 비 오는 창밖 |
| bedroom_subin | 수빈의 방 | S-21 | 밤 + 폰 빛 |
| hallway_jiwoo | 지우의 현관 | S-20 | 밤 + 간접등 |
| bathroom | 수빈의 욕실 | S-01 | 아침 햇살 |
| abstract | 추상/메타포 | S-12/13/14/19/22/24 | 씬별 독립 |

#### C. 캐릭터 마스터 시스템 (Character Master)

**원칙: 모든 캐릭터는 시리즈 공용 레퍼런스 시트를 기반으로 생성한다.**

1. **캐릭터 시트 생성**: 시리즈 시작 시 전 캐릭터 레퍼런스 시트 확보
   - 전신 정면 / 전신 측면 / 표정 변화 3~5종 / 의상 상세
   - 솔리드 배경(#00FF00) 위에 생성
2. **포즈 라이브러리**: 캐릭터별 기본 포즈를 사전 생성하여 재사용
   - 서기(정면/측면), 앉기, 클로즈업(다양한 표정)
   - 같은 포즈를 여러 씬에서 재사용 → 일관성 + 생성 비용 절감
3. **표정 변형**: 기본 포즈에서 표정만 변경이 필요할 때
   - img2img로 마스터 포즈 입력 + 표정 프롬프트 변경 → 체형/의상 유지하며 표정만 변화
4. **의상 추적**: 에피소드별 의상을 character.json에 기록

**character.json 구조:**
```json
{
  "id": "subin",
  "name": "수빈",
  "prompt_desc": "young Korean woman in her early 20s with long straight black hair, wearing a pastel pink cardigan over white top, confident bright expression with sparkling eyes",
  "fixed_features": ["long straight black hair", "sparkling eyes"],
  "episodes": {
    "EP01": {
      "outfit": "pastel pink cardigan over white top",
      "accessories": []
    }
  },
  "ref_sheet": "ref_sheet.png",
  "poses": ["standing_front", "sitting", "closeup_neutral", "closeup_happy", "closeup_vulnerable"]
}
```

#### D. 에셋 생성 워크플로우 (에피소드 시작 시)

```
① 각본 확정
    ↓
② 장소 목록 추출 + 캐릭터별 필요 포즈/표정 목록
    ↓
③ 장소 마스터 BG 생성 (장소당 1장) → assets/locations/
    ↓
④ 캐릭터 포즈 생성 (솔리드 bg) → assets/characters/
   - 기존 포즈 재사용 가능하면 스킵
   - 신규 포즈만 생성
    ↓
⑤ 장소 변형 생성 (후처리/img2img) → assets/locations/{id}/
    ↓
⑥ 씬별 합성 (BG변형 + 캐릭터포즈 + 소품) → layers/{scene_id}/comp.png
    ↓
⑦ LP 애니메이션 적용 → layers/{scene_id}/char_{name}_lp.mp4
```

#### E. 일관성 체크리스트 (씬 합성 전 검증)

| 항목 | 검증 방법 |
|------|----------|
| 조명 방향 | BG의 광원 방향과 캐릭터 그림자 방향 일치 |
| 캐릭터 스케일 | location.json의 character_positions 좌표/스케일 참조 |
| 의상 일치 | character.json의 현재 에피소드 outfit과 생성물 비교 |
| 소품 존재 | BG의 key_elements가 마스터와 동일한지 확인 |
| 색온도 통일 | 합성 후 전체 씬 컬러 그레이딩으로 레이어 간 차이 보정 |
| 얼굴 일관성 | 캐릭터 시트와 대조 (눈 색, 머리 길이, 얼굴형) |

#### F. img2img 활용 전략

txt2img은 매번 다른 결과 → 일관성 유지 어려움. **마스터 에셋이 확보되면 변형은 img2img 우선.**

| 용도 | 방식 | denoise 강도 |
|------|------|-------------|
| 표정 변경 (같은 포즈) | img2img + 표정 프롬프트 | 0.3~0.4 |
| 시간대 변경 (같은 장소) | img2img + 조명 프롬프트 | 0.2~0.3 |
| 의상 변경 (같은 캐릭터) | img2img + 의상 프롬프트 | 0.4~0.5 |
| 구조 변경 (창밖 비 추가 등) | img2img + 환경 프롬프트 | 0.5~0.6 |
| 완전 신규 | txt2img | 1.0 |

**ComfyUI img2img 워크플로우**: 기존 txt2img 워크플로우에서 `EmptyLatentImage` → `VAEEncode(입력이미지)` + `KSampler denoise < 1.0`으로 교체

### 5b. ComfyUI 일러스트 생성 + 수집 (레거시, EP.01용)
- **생성**: `generate_scenes.py` / `generate_scenes_v2.py` → ComfyUI API 호출
- **수집**: `collect_scenes.sh` → 최신 버전 자동 수집 + _alt 보존 + B컷 수집
- **캐릭터 상수**: `CHAR_SUBIN`, `CHAR_MINJUN`, `CHAR_JIWOO` — 의상/외형 일관성

### 6. 프롬프트 품질 교훈
- 워터마크 방지: "original artwork, no artist signature, no website url" 반드시 추가
- 어두운 톤: "darker/shadow/black" 대신 구체적 색상명("muted purple-gray") 사용
- 캐릭터 일관성: 상수(CHAR_*) 참조로 의상/머리 길이 불일치 방지
- 솔리드 배경 캐릭터: "solid bright green background #00FF00" — 크로마키/rembg 추출용

### 7. FFmpeg 파이프라인 교훈
- concat glob에 `_seg/_cut/_bcut` 임시 파일 포함 금지 (133초 부풀림 사고)
- `-shortest` 대신 반드시 `-t {duration}` 명시 (zoompan + loop 조합에서 1~2초 오버런)
- 오버레이 빌드: `--overlay` 플래그로 overlaid/ 이미지 우선 사용, 없으면 scenes/ 폴백

### 8. LivePortrait 애니메이션 (Lv3)
- **위치**: `build_video.py` → `find_liveportrait_video()` + `_build_liveportrait_clip()` + `--liveportrait` CLI
- **원리**: LivePortrait로 씬별 캐릭터 애니메이션 생성 → 루핑+스케일+미세줌으로 클립 통합
- **모션 매핑**: 씬의 감정/맥락에 맞는 드라이빙 템플릿(wink/shy/aggrieved/laugh/shake_face) + multiplier(0.20-0.35)
- **브리딩 합성**: LP 위에 BREATHING_INTENSITY×0.4 강도의 scale+crop 미세 줌 추가
- **폴백**: LP 영상 없는 씬(얼굴 미감지 등)은 자동으로 정지 이미지+브리딩 폴백
- **처리 시간**: 씬당 ~40-60초 (MPS), 배치 스크립트 `/tmp/fep_liveportrait_batch.py`
- **다음 에피소드**: SCENE_MOTION 딕셔너리만 교체 + 배치 실행

### 9. TTS 감정 연출 전략 (Typecast + 후처리)
- **원칙**: Typecast는 "감정별 원재료 생성기", 타이밍/정적/전환은 `build_video.py`에서 조립
- **대사 분할**: 감정이 바뀌는 지점마다 별도 클립으로 녹음 (예: 째려봄 클립 + 환한 미소 클립)
- **비트/정적**: Typecast에서 녹음하지 않음 → 클립 사이에 FFmpeg 무음 삽입 (각본의 초/비트 표기 참조)
- **내면 독백 vs 외부 대사**: 같은 보이스, "차분" 감정 + 느린 속도 → 후처리 미세 리버브로 구분
- **에너지 차이**: Typecast 감정 스타일 + 속도 슬라이더 조합
  - 최소 에너지 (민준 "응"): 속도 0.8x, 낮은 감정
  - 최대 에너지 (수빈 "나 예쁘지?"): 기쁨 감정, 속도 1.1x
- **ASMR/속삭임**: Typecast에 속삭임 스타일 없을 경우 → "차분" + 후처리 컴프레서/리버브
- **미세 딜레이** (0.2~0.3초 망설임): 대사를 분할 녹음 → FFmpeg에서 무음 삽입
- **초벌 확인**: edge-tts (`ko-KR-InJoonNeural`) 단일 보이스로 전체 흐름 프리뷰 → `generate_tts_v2.sh`
- **다음 에피소드**: 각본에 감정 디렉션 표기 → Typecast 클립 분할 가이드 + build_video.py 타이밍 가이드 양쪽으로 변환

#### Typecast 캐릭터 보이스 일관성 (시리즈 공용)
- **시리즈 고정 캐릭터는 에피소드 간 동일 보이스 캐스팅 유지 필수**
- 캐릭터별 보이스 ID를 확정 후 아래 테이블에 기록 → 다음 에피소드에서 자동 참조
- 내레이터도 시리즈 아이덴티티 → 동일 보이스 고정

| 역할 | Typecast 보이스 | 감정 기본값 | 속도 기본값 | 비고 |
|------|----------------|-----------|-----------|------|
| 내레이터 | **대길** (#다큐/리뷰) | 차분 | 1.0x | 시리즈 고정 |
| 수빈 | **지안** (#라디오/팟캐스트) | 기쁨 | 1.1x | 밝고 자신만만 |
| 민준 | **한준** (#라디오/팟캐스트) | 차분/낮음 | 0.8~0.9x | 건조하고 에너지 절약 |
| 지우 | **진서** (#다큐/리뷰) | 차분 | 0.9x | 밝으려고 노력하지만 지쳐있는 |

- EP.01에서 보이스 확정 시 이 테이블에 Typecast 보이스명/ID 기입
- 신규 에피소드의 신규 캐릭터도 같은 패턴으로 등록

#### Typecast 보이스 캐스팅 후보 (EP.01 선별, 사용자 최종 선택 대기)

| 역할 | 1순위 | 2순위 | 3순위 |
|------|-------|-------|-------|
| 내레이터 | 중현 (#낭독/오디오북) | 대길 (#다큐/리뷰) | 명일 (#기자/아나운서) |
| 수빈 | 지안 (#라디오/팟캐스트) | 다희 (#게임/애니) | 현주 (#낭독/오디오북) |
| 민준 | 한준 (#라디오/팟캐스트) | 시원 (#교육/강의) | 준상 (#다큐/리뷰) |
| 지우 | 주영 (#라디오/팟캐스트) | 진서 (#다큐/리뷰) | 소진 (#라디오/팟캐스트) |

- Typecast 즐겨찾기에 역할 메모 저장 완료 (시원만 즐겨찾기 미표시 버그, 검색으로 접근 가능)

### 11. LivePortrait 멀티캐릭터 (레이어 분리로 근본 해결)
- **EP.01 (레거시)**: 완성 씬에서 얼굴 크롭 → 개별 LP → FFmpeg overlay 합성 (차선책)
- **EP.02~ (레이어 분리)**: 캐릭터가 이미 독립 레이어 → LP 직접 적용 → BG 위에 합성
  - 크롭/좌표 매핑 불필요 — 캐릭터 전체 이미지에 LP 적용
  - 대사 타임라인에 따라 활성 캐릭터만 LP 영상, 나머지는 정지 이미지
  - BG + char_A(LP영상) + char_B(정지) → FFmpeg overlay
- **장점**: (1) 크롭 품질 손실 없음 (2) 캐릭터 전신 움직임 가능 (3) 합성 자유도 극대화

### 12. BGM/SFX 설계 전략 (시리즈 공용)
- **원칙**: BGM은 감정의 밑그림, 정적도 연출, 원형 구조 (프롤로그 테마 = 에필로그 테마)
- **메인 테마**: 시리즈 공용 피아노 단선율 → 매 에피소드 프롤로그/에필로그에서 변주 반복 (채널 아이덴티티)
- **트랙 구조**: 에피소드별 감정 곡선에 맞춰 BGM 트랙 ID 매핑 (BGM-A~Z)
- **BGM 소싱**: Pixabay Music (무료/상업적 이용 가능) + YouTube Audio Library (무료) + freesound.org SFX (CC0)
- **볼륨 레벨**: 대사 중 BGM -18~-22dB / 비트 중 -12~-15dB / 완전 정적은 소름 포인트에만
- **SFX 원칙**: 과하지 않게, 감정 전환점에만 포인트로 삽입 (자판기 동전음, 스트링 한 음, 현관문 등)
- **FFmpeg 믹싱**: 다중 레이어 (TTS + BGM + SFX + 무음) → `amix`/`amerge` 필터 합성
- **에피소드별 산출물**: `{EP}/BGM_SFX_설계.md` + 트랙 파일(`audio/bgm/`, `audio/sfx/`)
- **다음 에피소드**: 감정 곡선 차트 설계 → BGM 트랙 매핑 → SFX 포인트 지정 순서로 진행

### 10. 패럴랙스 효과 (Lv2 — 레이어 분리 생성으로 부활)
- **v1 (폐기)**: 완성 씬에서 rembg 분리 → 품질 최악
- **v2 (EP.02~)**: 레이어 분리 생성(#5) 덕분에 자연스러운 패럴랙스 가능
- **원리**: BG + 캐릭터(알파) + FG가 이미 분리됨 → 차등 움직임만 적용
- **구현**: BG는 느리게(0.3x), 캐릭터는 기본(1x), FG는 빠르게(1.5x) 이동
- **LP와 결합**: 캐릭터 레이어에 LP 애니메이션 적용 + 패럴랙스 동시 가능

## 작업일지 시스템

- **경로**: `FEP/worklog/YYYY-MM-DD.md`
- 세션 작업 시 주요 결정/완료 항목을 타임스탬프와 함께 기록
- 새 날짜 진입 시 새 MD 파일 생성
- `worklog/index.json` 업데이트: dates 배열에 날짜 추가, phases/assets/milestones 갱신
- **GitHub Pages 대시보드**: https://jyc0289y-art.github.io/FEP/
- **GitHub 레포**: https://github.com/jyc0289y-art/FEP
- 커밋: 세션 종료 시 worklog 변경사항 포함하여 푸시

### ⚠️ 매일 아침 브리핑 규칙
- **타이밍**: 사용자가 아침(새 세션 시작)에 접속하면 **첫 응답에서** 전날 작업일지 요약 + 오늘 예정 작업을 브리핑
- **형식**: 시각적 박스 + 진행률 바 (PM 보고 스타일)
- **내용**:
  1. 전날 완료 항목 (3~5줄 요약)
  2. 미완/이슈 항목
  3. 오늘 예정 작업 (우선순위 순)
  4. 전체 Phase 진행률
- **자동 갱신**: 세션 작업 종료 시 당일 worklog + index.json 즉시 갱신
- **배경**: 사용자는 전날 밤늦게 작업 → 다음날 아침 출근하며 점검하는 패턴

## 세션 운영 지침

- 이 프로젝트는 ComfyUI API 호출 + 대량 이미지/오디오 파일로 인해 **컨텍스트 소비가 매우 크다**
- **1 세션 = 1~2 Phase** 처리를 목표로 하고, 압축 전에 세션을 마무리할 것
- 세션 시작 시: `memory/sessions/registry.md` 확인 → P21.{N}wc 번호 부여
- 세션 종료 시: 세션지침 갱신 → 사용자에게 **새 채팅을 열어 포크**하도록 안내
- 압축 감지 시: 세션지침 즉시 갱신 → "⚠️ 컨텍스트 압축 — 새 채팅에서 P21.{N+1}wc로 이어갑니다" 안내
- ComfyUI 작업은 로컬 서버에서 독립 실행되므로, 세션 종료/네트워크 끊김과 무관하게 계속됨

## 애니메이션 품질 갭 — EP.02에서 재검토

현재 LP만으로는 비치키 수준 미달. EP.02 기획 시 아래 솔루션 비교 검토:
- **Kling AI**: 만화체 OK, image→video, ~$0.3/씬 (최우선 검토)
- **Runway Gen-3**: 유사 기능, 유료
- **Hedra/Hailuo**: 오디오 기반 토킹헤드, 만화체 지원 확인 필요
- **스타일 전환**: 반실사로 변경 시 LP+SadTalker 모두 작동
- **SadTalker**: `~/developer/SadTalker/` 설치 완료, 만화체 얼굴 미감지로 현재 사용 불가

## 라이선스 주의사항

- FLUX Kontext Dev: Non-Commercial License이나, 생성 이미지(Output) 상업적 사용 허용
- 채널 성장 시 BFL 상업 라이선스 전환 검토
- Typecast: 유료 플랜 상업적 이용 가능 여부 확인 필요
