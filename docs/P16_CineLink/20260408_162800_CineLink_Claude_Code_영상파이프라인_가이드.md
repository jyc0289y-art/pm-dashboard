# CineLink — 영상 제작 파이프라인 가이드

> CineLink는 SL Corporation의 AI 기반 영상 제작 엔진이다. 소재 분석부터 편집·합성까지의 전 과정을 자동화하며, 완성된 콘텐츠는 SeouLink 브랜드로 배포한다.

---

## 브랜드 체계

```
SL Corporation
└── SeouLink (메인 브랜드: 한국문화를 세상에 연결)
    ├── CineLink (영상 제작 엔진: 이 프로젝트)
    └── 기타 ~~Link 서브 브랜드
```

**역할 분리:**
- **CineLink** = 제작 도구이자 내부 기술 브랜드. 소재 분석, 색보정, 편집, 나레이션, 합성, 미디어 라이브러리를 담당한다. 장기적으로 독립 애플리케이션으로 제품화한다.
- **SeouLink** = 대외 배포 브랜드. YouTube, Instagram, TikTok 등 플랫폼에서 시청자가 접하는 채널명이자 브랜드. 한국문화를 세상에 연결한다는 브랜드 스토리를 담는다.

**영상 크레딧 표기 규칙:**
- 엔딩 크레딧: `Produced with CineLink | SeouLink`
- 영상 설명(description): `© SL Corporation / SeouLink`
- 워터마크(선택): SeouLink 로고를 영상 우하단에 반투명 삽입

---

## 핵심 원칙

1. **분석이 먼저다.** 모든 편집 판단은 소재에 대한 충분한 분석 위에서 이루어진다. 프레임 추출 + 비전 분석 + 음성 전사를 통해 소재의 내용과 맥락을 먼저 이해한다.
2. **비파괴 작업 흐름.** 원본은 절대 수정하지 않는다. 모든 처리는 사본에 대해 수행하며, 중간 작업물은 고품질(CRF 18 이하)을 유지한다.
3. **단계별 검증.** 전체 소재에 적용하기 전에 반드시 2~3개 샘플로 소규모 테스트를 먼저 수행하여 파이프라인을 검증한다.
4. **맥락 기반 자동화.** Claude 비전이 영상/사진의 내용을 이해하고, 그 맥락에 맞는 보정·편집·나레이션·음악 선택 판단을 내린다.

---

## 환경 설정

### 필수 도구

```bash
# 영상/오디오 처리
brew install ffmpeg        # 핵심 미디어 처리 엔진
brew install imagemagick   # 이미지 보정

# Python 패키지
pip install Pillow         # 이미지 처리
pip install openai-whisper # 음성 전사 (로컬)

# 폰트 (텍스트 오버레이용)
# Noto Sans CJK 권장 — 한국어/일본어/중국어 지원
# https://fonts.google.com/noto/specimen/Noto+Sans+KR
```

### API 키 (나레이션 사용 시)

```bash
# 타입캐스트 TTS
export TYPECAST_API_KEY="..."
# 문서: https://typecast.ai/docs/ko/overview
# Python SDK: pip install typecast
# MCP 서버 연동도 지원

# ElevenLabs (영어 나레이션 시 대안)
export ELEVENLABS_API_KEY="..."
```

### 프로젝트 디렉토리 표준 구조

새 프로젝트를 시작할 때마다 `cinelink/projects/` 하위에 아래 구조를 생성한다.

```
cinelink/
├── projects/
│   └── [프로젝트명]/               # 예: 2025-ishigaki, 2026-aomori
│       ├── raw/                    # 원본 소재 (수정 금지)
│       │   ├── videos/
│       │   └── photos/
│       ├── luts/                   # LUT 파일
│       ├── audio/
│       │   ├── bgm/               # 배경음원
│       │   ├── sfx/               # 효과음
│       │   └── narration/         # 생성된 나레이션
│       ├── temp/                   # 중간 처리물
│       │   ├── analysis/          # 분석 결과 JSON
│       │   ├── frames/            # 추출된 프레임 (1fps)
│       │   ├── transcripts/       # 음성 전사 (SRT, TXT)
│       │   ├── graded/            # 색보정 완료 클립
│       │   ├── photos-processed/  # 보정 완료 사진
│       │   └── segments/          # 편집된 세그먼트
│       ├── output/                 # 최종 출력물
│       ├── LICENSE_LOG.md          # 에셋 저작권 기록
│       └── project-config.json     # 프로젝트 설정
├── brand/                          # SeouLink 브랜드 에셋
│   ├── seoulink-logo.png          # 로고 원본 (투명 배경)
│   ├── seoulink-watermark.png     # 워터마크용 (반투명)
│   ├── cinelink-credit.png        # 엔딩 크레딧용
│   └── brand-guide.md             # 색상 코드, 폰트, 사용 규칙
├── library/                        # 글로벌 미디어 라이브러리
│   ├── db/library.json            # 전체 인덱스
│   ├── people/                    # 등장인물 레지스트리
│   └── archive/                   # 프로젝트별 분석 아카이브
├── shared/                         # 프로젝트 공통 에셋
│   ├── luts/                      # 공용 LUT 파일
│   ├── fonts/                     # OFL 폰트 모음
│   └── templates/                 # 인트로/아웃트로 템플릿
└── README.md
```

**글로벌 미디어 라이브러리:**

프로젝트 완료 후 분석 결과를 `library/archive/`에 아카이빙한다. 소재가 누적될수록 인물·대사·장면을 크로스 프로젝트로 검색할 수 있는 자산이 된다. 상세 구조와 검색 방법은 "미디어 라이브러리 및 검색 시스템" 섹션을 참조한다.
```

### 프로젝트 설정 파일

각 프로젝트의 고유 설정을 `project-config.json`에 기록한다. 파이프라인의 모든 단계에서 이 파일을 참조한다.

```json
{
  "project_name": "프로젝트명",
  "description": "프로젝트 설명",
  "camera": {
    "model": "Canon EOS R6",
    "lens": "RF 28-70mm f/2.0 L USM",
    "log_profiles": ["clog", "clog3"],
    "color_space": "BT.709 / Cinema Gamut"
  },
  "output": {
    "resolution": "3840x2160",
    "fps": 29.97,
    "aspect_ratio": "16:9",
    "codec": "libx264",
    "target_duration_minutes": 5,
    "platform": "youtube"
  },
  "branding": {
    "watermark": true,
    "watermark_file": "../../brand/seoulink-watermark.png",
    "watermark_opacity": 0.3,
    "watermark_position": "bottom-right",
    "intro_template": "../../shared/templates/seoulink-intro.mp4",
    "credit_image": "../../brand/cinelink-credit.png",
    "credit_duration": 5,
    "credit_text": "Produced with CineLink | SeouLink | © SL Corporation",
    "description_footer": "Produced with CineLink by SeouLink\n© SL Corporation"
  },
  "narration": {
    "provider": "typecast",
    "language": "ko",
    "voice_id": "사용할_캐릭터_ID",
    "model": "ssfm-v30",
    "tone": "친근하고 자연스러운 구어체"
  },
  "mood": {
    "description": "전체 영상의 목표 분위기를 자유롭게 서술",
    "color_tone": "warm / cool / neutral",
    "bgm_style": "acoustic / lofi / cinematic / ambient"
  },
  "font": {
    "path": "/path/to/NotoSansKR-Regular.otf",
    "title_size": 60,
    "subtitle_size": 36,
    "color": "white",
    "border": true
  }
}
```

---

## Phase 1: 소재 분석

> 목표: 모든 소재의 기술적 속성과 내용을 파악하여 이후 모든 판단의 기반을 만든다.

### 1-1. 미디어 인벤토리 생성

모든 영상/사진 파일을 스캔하여 메타데이터를 추출한다.

```bash
# 영상
ffprobe -v quiet -print_format json -show_format -show_streams [파일]

# 사진 EXIF
exiftool [파일]   # 또는 Python Pillow의 Image.getexif()
```

각 파일에 대해 기록할 항목:
- 파일명, 파일 크기, 포맷
- 해상도, FPS, 코덱, 비트레이트 (영상)
- 색공간, 감마/전송 특성 (LOG 판별용)
- 촬영 일시 (타임라인 정렬용)
- GPS 좌표 (있는 경우)
- Duration (영상)

결과물: `temp/analysis/media_inventory.json`

### 1-2. LOG / 일반 프로파일 분류

영상 클립을 촬영 프로파일별로 자동 분류한다.

**1차 판별: 메타데이터 기반**
- ffprobe의 `color_transfer`, `color_primaries`, `color_range` 태그 확인
- 카메라별 LOG 프로파일 시그니처가 다르므로 project-config.json의 카메라 정보 참조

**2차 판별: 비전 분석 (메타데이터만으로 불충분한 경우)**
- 대표 프레임(10초 지점)을 추출하여 Claude 비전으로 분석
- LOG 영상은 플랫하고 채도가 낮으며 콘트라스트가 약함
- 히스토그램이 중간톤에 집중되어 있으면 LOG일 가능성 높음

```bash
ffmpeg -ss 00:00:10 -i [파일] -frames:v 1 -q:v 2 temp/frames/thumb_[번호].jpg
```

결과물: `temp/analysis/clip_classification.json`

### 1-3. 영상 내용 분석

각 클립의 내용을 이해한다.

**프레임 추출:**
```bash
# 1fps로 프레임 추출 (1초에 1장)
ffmpeg -i [파일] -vf "fps=1" temp/frames/[클립ID]_%04d.jpg
```

**음성 전사:**
```bash
ffmpeg -i [파일] -vn -acodec pcm_s16le -ar 16000 temp/frames/[클립ID]_audio.wav
whisper temp/frames/[클립ID]_audio.wav --language auto --model medium --output_format srt
```

**Claude 비전 분석:**
프레임을 배치(15장 단위)로 Claude 비전에 전달하여 분석한다. 서브에이전트를 사용하여 메인 컨텍스트를 보호한다.

각 클립에 대해 생성할 분석:
- 장면 설명 (무엇이 보이는지)
- 분위기/감정 태그
- 하이라이트 구간 (시각적으로 좋은 부분의 타임스탬프)
- 사용 불가 구간 (심한 흔들림, 의도치 않은 촬영 등)
- 현장음 특성 (대화, 환경음, 무음 등)

**토큰 비용 주의:**
- 1080p 프레임 1장 ≈ 1,600 토큰
- 10분 영상 1fps = 600프레임 ≈ 960K 토큰
- 반드시 분석 전에 토큰 비용을 추정하고 확인받을 것
- 긴 영상은 0.5fps 또는 0.2fps로 낮추거나, 구간을 지정하여 분석

결과물: `temp/analysis/content_analysis.json`

### 1-4. 사진 분석

사진도 동일하게 분석한다.

- EXIF 메타데이터 (촬영 일시, GPS, 카메라 설정)
- RAW(CR3 등) vs JPG 분류
- Claude 비전으로 내용 태깅 (풍경, 음식, 인물, 건축, 동물 등)
- 영상 타임라인의 어느 맥락에 어울리는지 매칭 후보 제안

결과물: `temp/analysis/photo_inventory.json`

---

## Phase 2: 색보정 및 톤 통일

> 목표: LOG/일반이 혼재된 소재를 통일된 색감으로 맞춘다.

### 2-1. LOG → Rec.709 변환

LOG 프로파일로 촬영된 클립에 적절한 변환 LUT를 적용한다.

**카메라별 대응표:**

| 카메라 | LOG 프로파일 | 권장 LUT |
|--------|-------------|----------|
| Canon EOS R시리즈 | C-Log, C-Log3 | Canon 공식 LUT 또는 CINECOLOR/Filmkit 무료 LUT |
| Sony A7 시리즈 | S-Log2, S-Log3 | Sony 공식 s709 LUT 또는 Bounce Color 무료 LUT |
| DJI 드론/액션캠 | D-Log, D-Log M | DJI 공식 Rec.709 LUT |
| Fujifilm | F-Log, F-Log2 | Fujifilm 공식 LUT |
| Panasonic | V-Log | Panasonic 공식 V-Log to V-709 LUT |
| GoPro | GoPro Color (플랫) | 일반적으로 별도 LUT 불필요, eq 필터로 조정 |

```bash
ffmpeg -i [LOG클립] \
  -vf "lut3d=[해당LUT파일].cube" \
  -c:v libx264 -crf 18 -c:a copy \
  temp/graded/[클립ID]_converted.mp4
```

**중요: LUT는 반드시 다른 모든 보정보다 먼저 적용해야 한다.**

### 2-2. 클립 간 톤 매칭

변환 완료 후에도 클립 간 밝기/채도/색온도 편차가 남을 수 있다.

1. **기준 클립 선정:** Claude가 모든 클립의 대표 프레임을 비교하여 노출과 색감이 가장 균형 잡힌 클립을 기준으로 선택한다.
2. **편차 분석:** 각 클립의 대표 프레임을 기준 클립과 비교하여 밝기/채도/색온도 보정량을 결정한다.
3. **보정 적용:**

```bash
ffmpeg -i [클립] \
  -vf "eq=brightness=[값]:contrast=[값]:saturation=[값]:gamma=[값],\
       colortemperature=temperature=[값]" \
  -c:v libx264 -crf 18 -c:a copy \
  temp/graded/[클립ID]_matched.mp4
```

eq 필터 파라미터 범위:
- brightness: -1.0 ~ 1.0 (0이 기본)
- contrast: 0.0 ~ 2.0 (1.0이 기본)
- saturation: 0.0 ~ 3.0 (1.0이 기본)
- gamma: 0.1 ~ 10.0 (1.0이 기본)
- colortemperature: 1000 ~ 12000 (6500이 일광)

### 2-3. 크리에이티브 룩 적용

프로젝트의 목표 분위기에 맞는 최종 룩을 적용한다. 두 가지 방법 중 선택:

**방법 A: 크리에이티브 LUT 적용**
- 사전 준비된 .cube LUT 파일을 전체 클립에 일괄 적용
- Lightroom/Photoshop에서 원하는 색감을 만든 뒤 HALD CLUT로 내보내 FFmpeg에서 사용 가능

**방법 B: FFmpeg 필터 조합으로 직접 구현**
- Claude가 project-config.json의 mood 설정을 참고하여 eq/curves/colorbalance 필터 파라미터를 결정

```bash
# 예: 따뜻한 여행 톤
-vf "eq=saturation=1.15:gamma=1.03,curves=vintage,colorbalance=rs=0.05:gs=-0.02:bs=-0.05"

# 예: 시네마틱 톤
-vf "eq=contrast=1.1:saturation=0.9,colorbalance=rs=0.03:bs=0.04,vignette=PI/4"

# 예: 청량한 톤
-vf "eq=saturation=1.2:brightness=0.02,colortemperature=temperature=7500"
```

---

## Phase 3: 사진 보정 및 가공

> 목표: 사진을 영상에 삽입할 수 있는 형태로 보정, 크롭, 모션 적용한다.

### 3-1. RAW 현상

RAW 파일(Canon CR3, Sony ARW 등)이 있는 경우 먼저 현상한다.

```bash
# darktable CLI
darktable-cli input.cr3 output.tiff

# 또는 dcraw
dcraw -w -T input.cr3
```

### 3-2. 자동 보정

Claude 비전으로 각 사진을 분석하고 보정 방향을 판단한다.

판단 기준:
- 노출: 어두우면 밝기 올림, 과노출이면 줄임
- 색온도: 실내/텅스텐은 따뜻하게, 그늘/흐린 날은 보정
- 채도: 영상 클립의 채도와 일관성 유지
- 선명도: 적절한 언샤프 마스크 적용

```bash
# ImageMagick
convert input.jpg \
  -brightness-contrast [값]x[값] \
  -modulate [밝기],[채도],[색조] \
  -unsharp 0x1+0.5+0 \
  output.jpg

# 또는 Python Pillow
python3 -c "
from PIL import Image, ImageEnhance
img = Image.open('input.jpg')
img = ImageEnhance.Brightness(img).enhance([값])
img = ImageEnhance.Contrast(img).enhance([값])
img = ImageEnhance.Color(img).enhance([값])
img = ImageEnhance.Sharpness(img).enhance([값])
img.save('output.jpg', quality=95)
"
```

### 3-3. 스마트 크롭

사진을 영상의 종횡비에 맞게 크롭한다. Claude 비전으로 주요 피사체 위치를 파악하여 중요한 부분이 잘리지 않도록 크롭 영역을 결정한다.

```bash
# 16:9 크롭 (오프셋은 Claude가 피사체 위치 기반으로 결정)
ffmpeg -i photo.jpg \
  -vf "crop=ih*16/9:ih:[x_offset]:0" \
  photo_cropped.jpg

# 9:16 세로형 (릴스/쇼츠용)
ffmpeg -i photo.jpg \
  -vf "crop=iw:iw*16/9:0:[y_offset]" \
  photo_vertical.jpg
```

### 3-4. Ken Burns 효과

정지 사진을 모션 클립으로 변환한다. 사진 내용에 따라 효과를 선택한다.

| 사진 유형 | 권장 효과 | 설명 |
|-----------|----------|------|
| 풍경 와이드 | 좌→우 또는 우→좌 패닝 | 공간감 전달 |
| 인물/음식 | 천천히 줌인 | 시선 집중 |
| 석양/탁 트인 풍경 | 줌아웃 | 점점 넓어지는 느낌 |
| 디테일 샷 | 줌인 후 정지 | 발견의 느낌 |

```bash
# 줌인
ffmpeg -loop 1 -i photo.jpg -t [초] \
  -vf "zoompan=z='min(zoom+0.001,1.3)':d=[프레임수]:s=[해상도]:fps=[fps]" \
  -c:v libx264 -pix_fmt yuv420p output.mp4

# 좌→우 패닝
ffmpeg -loop 1 -i photo.jpg -t [초] \
  -vf "zoompan=z='1.3':x='if(eq(on,1),0,x+2)':y='ih/2-(ih/zoom/2)':d=[프레임수]:s=[해상도]:fps=[fps]" \
  -c:v libx264 -pix_fmt yuv420p output.mp4

# 줌아웃
ffmpeg -loop 1 -i photo.jpg -t [초] \
  -vf "zoompan=z='if(eq(on,1),1.3,max(zoom-0.001,1.0))':d=[프레임수]:s=[해상도]:fps=[fps]" \
  -c:v libx264 -pix_fmt yuv420p output.mp4
```

---

## Phase 4: 나레이션 생성

> 목표: 영상 내용의 맥락에 맞는 나레이션 대본을 작성하고 AI 음성으로 생성한다.

### 4-1. 나레이션 대본 작성

Phase 1의 분석 결과를 기반으로 Claude가 나레이션 대본을 작성한다.

대본 작성 원칙:
- project-config.json의 narration.tone 설정을 따른다
- 영상/사진 분석에서 파악된 장면 맥락에 맞는 내용
- 장면별 2~3문장, 과하지 않은 분량
- 감정 태그를 함께 지정 (TTS 감정 파라미터용)

대본 형식:

```json
[
  {
    "scene_id": 1,
    "text": "나레이션 텍스트",
    "emotion": "excited | calm | awe | happy | sad | neutral | auto",
    "matched_clips": ["파일명"],
    "matched_photos": ["파일명"],
    "notes": "이 장면에서 나레이션이 끝나면 2초 여백"
  }
]
```

결과물: `temp/analysis/narration_script.json`

### 4-2. TTS 음성 생성

타입캐스트 API를 호출하여 나레이션 음성을 생성한다.

```python
import requests

def generate_tts(text, voice_id, emotion="auto", model="ssfm-v30", format="wav"):
    """
    타입캐스트 API 호출
    - model: ssfm-v30 (최신, 문맥 기반 감정 자동 적용)
    - emotion: auto(스마트 이모션), excited, calm, happy, sad 등
    - format: wav(편집용 고품질) 또는 mp3(최종 배포용)
    상세: https://typecast.ai/docs/ko/overview
    """
    pass
```

각 장면별 개별 파일로 저장: `audio/narration/scene_[번호].wav`

전체 나레이션을 순서대로 이어붙인 버전도 생성:

```bash
# concat
ffmpeg -f concat -safe 0 -i narration_list.txt -c copy audio/narration/full_narration.wav
```

### 4-3. TTS 대안

| 서비스 | 강점 | 언어 |
|--------|------|------|
| 타입캐스트 | 한국어 최고 품질, 감정 자동 적용, 500+ 캐릭터 | 한국어, 영어, 일본어 등 |
| ElevenLabs | 영어 최고 품질, 음성 클로닝 | 영어 중심, 다국어 지원 |
| OpenAI TTS | 간편한 API, 합리적 품질 | 다국어 |
| Edge TTS | 무료, 로컬 실행 가능 | 다국어 |

---

## Phase 5: 배경음악 및 효과음

> 목표: 영상의 분위기를 살리는 오디오 레이어를 구성한다.

### 5-1. 배경음원 소스

로열티프리 음원:
- Pixabay Music: https://pixabay.com/music/
- Free Music Archive: https://freemusicarchive.org/
- YouTube Audio Library: https://studio.youtube.com/channel/audio
- Uppbeat: https://uppbeat.io/

### 5-2. 음원 선택 가이드

project-config.json의 mood 설정과 Phase 1의 장면 분석을 기반으로 Claude가 적절한 음원 스타일을 제안한다.

장면 유형별 권장 BGM:
- 오프닝/이동: 경쾌하고 기대감 있는 톤
- 풍경/자연: 잔잔한 앰비언트, 어쿠스틱
- 액티비티/스포츠: 에너지 있는 일렉트로닉/팝
- 음식/카페: 가벼운 재즈, 보사노바
- 감성/석양: 서정적 피아노, 스트링
- 엔딩: 여운 있는 어쿠스틱

### 5-3. 효과음

- 장면 전환: whoosh, 짧은 임팩트
- 사진 등장: 셔터음, 슬라이드
- 텍스트 등장: 팝, 틱
- 환경음 보강: 파도, 바람, 새소리, 거리 소음 등

### 5-4. 오디오 믹싱 규칙

**볼륨 밸런스 기준:**
- 나레이션: 0dB (기준)
- BGM (나레이션 있을 때): -15dB ~ -20dB
- BGM (나레이션 없을 때): -6dB ~ -10dB
- 효과음: -6dB ~ -12dB
- 현장음: 장면에 따라 판단

**나레이션 구간 BGM 덕킹:**

```bash
# 간단한 볼륨 덕킹
ffmpeg -i bgm.mp3 \
  -af "volume=enable='between(t,[시작],[끝])':volume=0.15" \
  bgm_ducked.mp3

# 나레이션과 BGM 믹싱
ffmpeg -i bgm_ducked.mp3 -i narration.wav \
  -filter_complex "[0:a][1:a]amix=inputs=2:duration=first[aout]" \
  -map "[aout]" mixed.wav
```

**페이드 처리:**

```bash
# BGM 페이드인 (처음 3초) + 페이드아웃 (마지막 3초)
ffmpeg -i bgm.mp3 \
  -af "afade=t=in:st=0:d=3,afade=t=out:st=[종료시점-3]:d=3" \
  bgm_faded.mp3
```

---

## Phase 6: 최종 편집 및 합성

> 목표: 모든 소재를 타임라인에 배치하고 전환, 텍스트, 오디오를 합성하여 최종 영상을 출력한다.

### 6-1. 타임라인 설계

Phase 1의 분석 + Phase 4의 나레이션 대본을 기반으로 전체 타임라인을 구성한다.

```json
{
  "timeline": [
    {
      "order": 1,
      "type": "title",
      "duration": 3,
      "text": "타이틀 텍스트",
      "transition_in": "fade",
      "transition_out": "dissolve"
    },
    {
      "order": 2,
      "type": "video",
      "source": "파일명",
      "trim_start": "00:00:05",
      "trim_end": "00:00:17",
      "narration": "scene_01.wav",
      "transition_out": "xfade_1s"
    },
    {
      "order": 3,
      "type": "photo_montage",
      "photos": ["파일1", "파일2", "파일3"],
      "effect": "ken_burns",
      "duration_per_photo": 4,
      "narration": "scene_02.wav"
    }
  ]
}
```

### 6-2. 클립 트리밍

```bash
ffmpeg -i [원본] -ss [시작] -t [길이] \
  -c:v libx264 -crf 18 -c:a aac \
  temp/segments/seg_[번호].mp4
```

### 6-3. 전환 효과

```bash
# 크로스페이드 (가장 자연스러운 기본 전환)
ffmpeg -i clip1.mp4 -i clip2.mp4 \
  -filter_complex "xfade=transition=fade:duration=1:offset=[클립1길이-1]" \
  output.mp4

# 사용 가능한 전환 종류:
# fade, dissolve, wipeleft, wiperight, wipeup, wipedown
# slideright, slideleft, slideup, slidedown
# smoothleft, smoothright, smoothup, smoothdown
```

### 6-4. 텍스트 오버레이

```bash
# 중앙 타이틀
ffmpeg -i video.mp4 \
  -vf "drawtext=text='[제목]':fontsize=[크기]:fontcolor=[색]:\
       x=(w-text_w)/2:y=(h-text_h)/2:\
       enable='between(t,[시작],[끝])':\
       fontfile=[폰트경로]" \
  output.mp4

# 하단 자막 (장소명 등)
ffmpeg -i video.mp4 \
  -vf "drawtext=text='[텍스트]':fontsize=[크기]:fontcolor=white:\
       borderw=2:bordercolor=black:\
       x=50:y=h-80:\
       enable='between(t,[시작],[끝])':\
       fontfile=[폰트경로]" \
  output.mp4
```

**주의: 한국어/일본어/중국어 텍스트는 반드시 CJK 지원 폰트를 지정해야 한다.**

### 6-5. 전체 합성

```bash
# 1. 영상 클립들을 순서대로 연결
ffmpeg -f concat -safe 0 -i segment_list.txt \
  -c:v libx264 -crf 18 -c:a aac \
  temp/segments/video_assembled.mp4

# 2. 오디오 레이어 합성
ffmpeg -i temp/segments/video_assembled.mp4 \
       -i audio/narration/full_narration.wav \
       -i audio/bgm/main_bgm.mp3 \
  -filter_complex \
    "[0:a]volume=[현장음볼륨][orig];\
     [1:a]volume=1.0[narr];\
     [2:a]volume=[BGM볼륨][bgm];\
     [orig][narr][bgm]amix=inputs=3:duration=first[aout]" \
  -map 0:v -map "[aout]" \
  -c:v copy -c:a aac -b:a 192k \
  output/final.mp4
```

### 6-6. SeouLink 브랜딩 삽입

최종 합성된 영상에 SeouLink 브랜드 요소를 삽입한다. 브랜드 에셋은 `cinelink/brand/` 에서 참조한다.

**워터마크 (본편 전체):**

```bash
# 우하단에 SeouLink 로고 반투명 삽입
ffmpeg -i video.mp4 -i brand/seoulink-watermark.png \
  -filter_complex "[1:v]format=rgba,colorchannelmixer=aa=0.3[wm];\
                    [0:v][wm]overlay=W-w-20:H-h-20" \
  -c:v libx264 -crf 18 -c:a copy \
  output_watermarked.mp4
```

워터마크 투명도는 `aa=0.3` (30%)을 기본으로 하되, 장면에 따라 조정. 밝은 장면에서는 더 투명하게, 어두운 장면에서는 그대로.

**인트로 타이틀 (선택):**

`shared/templates/` 에 SeouLink 인트로 템플릿을 준비해두고 프로젝트명만 바꿔서 앞에 붙인다.

```bash
# 인트로 + 본편 연결
ffmpeg -i shared/templates/seoulink-intro.mp4 -i main_video.mp4 \
  -filter_complex "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]" \
  -map "[v]" -map "[a]" output.mp4
```

**엔딩 크레딧:**

본편 마지막에 크레딧 화면을 추가한다.

```bash
# 크레딧 이미지를 5초 클립으로 변환
ffmpeg -loop 1 -i brand/cinelink-credit.png -t 5 \
  -vf "fps=30,format=yuv420p" \
  -c:v libx264 credit_clip.mp4

# 본편 + 크레딧 연결 (크로스페이드)
ffmpeg -i main_video.mp4 -i credit_clip.mp4 \
  -filter_complex "xfade=transition=fade:duration=1.5:offset=[본편길이-1.5]" \
  output_with_credit.mp4
```

크레딧 표기 내용:
```
Produced with CineLink
SeouLink | SL Corporation
© 2026 SL Corporation
```

**영상 설명(description) 템플릿:**

각 플랫폼 업로드 시 아래 내용을 영상 설명 하단에 포함한다.

```
---
Produced with CineLink by SeouLink
© SL Corporation
```

### 6-7. 최종 인코딩

플랫폼별 권장 출력 설정:

| 플랫폼 | 해상도 | 코덱 | 비트레이트 | FPS |
|--------|--------|------|-----------|-----|
| YouTube 4K | 3840x2160 | H.264 | 35-45 Mbps | 29.97/59.94 |
| YouTube FHD | 1920x1080 | H.264 | 10-15 Mbps | 29.97/59.94 |
| Instagram 릴스 | 1080x1920 | H.264 | 10-15 Mbps | 30 |
| TikTok | 1080x1920 | H.264 | 10-15 Mbps | 30 |
| 일반 보관용 | 원본 해상도 | H.265 | CRF 20 | 원본 |

```bash
ffmpeg -i assembled.mp4 \
  -c:v libx264 -preset slow -crf [값] \
  -c:a aac -b:a 192k \
  -movflags +faststart \
  output/[프로젝트명]_final.mp4
```

`-movflags +faststart`는 웹 스트리밍 시 빠른 재생 시작을 위해 항상 포함한다.

---

## 미디어 라이브러리 및 검색 시스템

> 목표: Phase 1에서 생성된 분석 데이터와 중간생성물을 체계적으로 보관하여, 이후 프로젝트에서 인물·대사·장면·분위기 등으로 검색하고 재활용할 수 있는 미디어 라이브러리를 구축한다.

### 설계 원칙

- **모든 중간생성물을 보존한다.** 추출된 프레임, 전사 텍스트, 분석 JSON, 썸네일 등을 삭제하지 않고 구조화하여 보관한다.
- **프로젝트를 넘어 누적된다.** 개별 프로젝트의 분석 결과가 글로벌 라이브러리에 통합되어, 소재가 쌓일수록 검색 가능한 자산이 늘어난다.
- **사람이 확인·수정할 수 있다.** 자동 분석 결과는 JSON으로 저장되므로 사용자가 직접 열어서 태그를 수정하거나 보완할 수 있다.

### 글로벌 라이브러리 디렉토리

프로젝트 디렉토리와 별도로, 홈 디렉토리에 글로벌 미디어 라이브러리를 유지한다.

```
~/media-library/
├── db/
│   └── library.json           # 전체 인덱스 (또는 SQLite)
├── projects/
│   ├── 2025-ishigaki/         # 프로젝트별 분석 결과 아카이브
│   ├── 2026-aomori/
│   └── .../
├── people/                     # 등장인물 인덱스
│   └── people_registry.json
└── README.md
```

### 클립 단위 분석 레코드

Phase 1에서 각 클립을 분석할 때, 아래 형식으로 레코드를 생성하여 저장한다. 이 레코드가 라이브러리 검색의 기본 단위가 된다.

```json
{
  "clip_id": "2025-ishigaki_MVI_0023",
  "project": "2025-ishigaki",
  "source_file": "raw/videos/MVI_0023.mp4",
  "recorded_at": "2025-07-15T14:23:00+09:00",
  "gps": { "lat": 24.3336, "lng": 124.1557 },
  "location_name": "카바라 만",
  "duration": "00:02:15",
  "resolution": "3840x2160",
  "fps": 29.97,
  "profile": "clog3",

  "scenes": [
    {
      "scene_id": 1,
      "time_range": "00:00:00-00:00:45",
      "description": "에메랄드빛 바다 위로 보트가 지나가는 풍경. 멀리 산호초가 보임.",
      "mood": ["serene", "awe"],
      "tags": ["바다", "보트", "산호초", "풍경", "와이드"],
      "highlight": true,
      "thumbnail": "frames/2025-ishigaki_MVI_0023_scene01.jpg"
    },
    {
      "scene_id": 2,
      "time_range": "00:00:45-00:02:15",
      "description": "스노클링 중 수중 촬영. 열대어와 산호 클로즈업.",
      "mood": ["excited", "wonder"],
      "tags": ["수중", "스노클링", "열대어", "산호", "클로즈업"],
      "highlight": true,
      "thumbnail": "frames/2025-ishigaki_MVI_0023_scene02.jpg"
    }
  ],

  "people": [
    {
      "person_id": "person_jinnyeong",
      "appearances": [
        { "time_range": "00:00:10-00:00:30", "description": "보트 위에서 바다를 바라봄" },
        { "time_range": "00:01:00-00:01:45", "description": "스노클링 중" }
      ]
    }
  ],

  "dialogue": [
    {
      "time_range": "00:00:05-00:00:08",
      "speaker": "person_jinnyeong",
      "text": "와 여기 물 색깔 진짜 대박이다",
      "language": "ko",
      "emotion": "excited"
    },
    {
      "time_range": "00:01:50-00:01:55",
      "speaker": "unknown",
      "text": "あそこにウミガメがいますよ",
      "language": "ja",
      "emotion": "neutral"
    }
  ],

  "audio_characteristics": {
    "has_speech": true,
    "has_music": false,
    "ambient": "파도소리, 바람소리",
    "noise_level": "low"
  },

  "technical": {
    "stability": "stable",
    "exposure": "good",
    "focus": "sharp",
    "usable": true,
    "issues": []
  },

  "frames_dir": "projects/2025-ishigaki/frames/MVI_0023/",
  "transcript_file": "projects/2025-ishigaki/transcripts/MVI_0023.srt",
  "analysis_file": "projects/2025-ishigaki/analysis/MVI_0023_analysis.md"
}
```

### 등장인물 레지스트리

프로젝트를 넘어 인물을 추적하기 위한 글로벌 인물 인덱스.

```json
{
  "people": [
    {
      "person_id": "person_jinnyeong",
      "name": "진영",
      "relation": "self",
      "reference_photos": [
        "people/person_jinnyeong_ref01.jpg",
        "people/person_jinnyeong_ref02.jpg"
      ],
      "appearances": [
        {
          "project": "2025-ishigaki",
          "clips": ["MVI_0023", "MVI_0024", "MVI_0031"],
          "total_screen_time": "00:08:30"
        },
        {
          "project": "2026-aomori",
          "clips": ["MVI_0005", "MVI_0012"],
          "total_screen_time": "00:03:15"
        }
      ]
    },
    {
      "person_id": "person_friend_A",
      "name": "친구A",
      "relation": "friend",
      "reference_photos": ["people/person_friend_A_ref01.jpg"],
      "appearances": [
        {
          "project": "2025-ishigaki",
          "clips": ["MVI_0025", "MVI_0030"],
          "total_screen_time": "00:04:00"
        }
      ]
    }
  ]
}
```

인물 등록 과정:
1. Phase 1 분석 시 Claude 비전이 각 클립에서 인물을 감지한다
2. 처음 등장하는 인물은 대표 프레임을 캡처하여 `people/` 에 저장하고 임시 ID를 부여한다
3. 사용자가 이름과 관계를 수동으로 입력하여 레지스트리를 완성한다
4. 이후 프로젝트에서 동일 인물이 등장하면 참조 사진과 비교하여 매칭한다

### 보존해야 할 중간생성물 목록

| 생성물 | 저장 위치 | 용도 |
|--------|----------|------|
| 추출 프레임 (1fps JPG) | `projects/[프로젝트]/frames/[클립ID]/` | 장면 검색, 인물 매칭, 썸네일 |
| 대표 프레임 (장면당 1장) | `projects/[프로젝트]/frames/thumbnails/` | 빠른 브라우징, 타임라인 미리보기 |
| 음성 전사 (SRT) | `projects/[프로젝트]/transcripts/[클립ID].srt` | 대사 검색, 자막 재사용 |
| 음성 전사 (전체 텍스트) | `projects/[프로젝트]/transcripts/[클립ID].txt` | 전문 검색 |
| 프레임별 분석 (MD) | `projects/[프로젝트]/analysis/[클립ID]_frames.md` | 장면 내용 상세 확인 |
| 클립 분석 레코드 (JSON) | `projects/[프로젝트]/analysis/[클립ID].json` | 구조화 검색 |
| 프로젝트 전체 인덱스 | `projects/[프로젝트]/index.json` | 프로젝트 내 전체 소재 목록 |
| 인물 참조 사진 | `people/[인물ID]_ref[번호].jpg` | 인물 매칭 |
| 인물 레지스트리 | `people/people_registry.json` | 크로스 프로젝트 인물 검색 |
| 글로벌 인덱스 | `db/library.json` | 전체 라이브러리 검색 |

### 검색 쿼리 예시

라이브러리가 구축되면 Claude Code에 자연어로 질문하여 원하는 소재를 찾을 수 있다.

**인물 검색:**
```
"친구A가 등장하는 모든 클립을 찾아줘"
→ people_registry.json에서 person_friend_A의 appearances 조회
→ 해당 클립들의 time_range와 썸네일을 보여줌
```

**대사 검색:**
```
"이시가키 영상에서 '대박'이라는 단어가 나오는 장면을 찾아줘"
→ transcripts/ 디렉토리의 SRT 파일들을 grep
→ 해당 타임스탬프의 클립과 전후 맥락을 보여줌
```

**장면/분위기 검색:**
```
"석양이 나오는 모든 클립을 찾아줘"
→ 각 클립 JSON의 scenes[].tags에서 "석양" 검색
→ highlight 프레임과 함께 결과 표시

"감성적인 분위기의 바다 장면만 모아줘"
→ scenes[].mood에 "serene" 또는 "emotional" + tags에 "바다" 필터
```

**기술적 검색:**
```
"4K로 촬영한 안정적인 클립만 보여줘"
→ resolution이 3840x2160 + technical.stability가 "stable"인 클립 필터

"현장음이 깨끗한 대화 장면을 찾아줘"
→ audio_characteristics.has_speech가 true + noise_level이 "low"인 클립
```

**크로스 프로젝트 검색:**
```
"지금까지 촬영한 모든 영상에서 음식 장면만 모아줘"
→ 글로벌 library.json에서 tags에 "음식" 포함된 모든 장면을 프로젝트 횡단 검색
→ 음식 모음 하이라이트 영상 자동 제작 가능
```

**특정 클립에서 추출:**
```
"MVI_0023에서 친구A가 말하는 부분만 잘라줘"
→ 해당 클립의 people[].appearances + dialogue[].speaker 교차 조회
→ FFmpeg로 해당 time_range만 트리밍하여 출력
```

### 라이브러리 유지보수

**프로젝트 완료 후 아카이빙:**
```bash
# Phase 1 분석 결과를 글로벌 라이브러리에 통합
cp -r temp/analysis/ ../../library/archive/[프로젝트명]/analysis/
cp -r temp/frames/ ../../library/archive/[프로젝트명]/frames/

# 글로벌 인덱스 업데이트 (Claude Code가 수행)
# library/db/library.json에 새 프로젝트의 클립 레코드들을 추가
```

**수동 보정 권장 시점:**
- 인물 이름/관계 입력 (자동으로는 "person_001" 같은 임시 ID만 부여됨)
- 오인식된 장면 태그 수정
- 하이라이트 플래그 조정
- 사용 불가 구간 추가 표시

**용량 관리:**
- 추출 프레임이 가장 용량을 많이 차지함 (10분 1fps ≈ 600장 ≈ 300MB~1GB)
- 오래된 프로젝트의 프레임은 대표 프레임(장면당 1장)만 남기고 삭제 가능
- JSON/SRT/MD 파일은 용량이 작으므로 영구 보관
- 원본 영상은 별도 외장 드라이브에 보관하고, 라이브러리에는 경로만 기록

---

## 실행 체크리스트

```
□ cinelink/projects/[프로젝트명]/ 디렉토리 생성
□ project-config.json 작성 (카메라, 출력 설정, 분위기, 브랜딩 등)
□ 원본 소재를 raw/ 에 배치
□ 필요한 LUT 파일을 luts/ 에 배치 (또는 shared/luts/ 공용 참조)
□ 배경음원/효과음을 audio/ 에 배치 (라이선스 확인 완료된 것만)
□ 폰트 파일을 OFL 라이선스로 준비 (또는 shared/fonts/ 공용 참조)
□ SeouLink 브랜드 에셋 확인 (brand/ 폴더에 로고·워터마크·크레딧 있는지)
□ LICENSE_LOG.md 생성 및 기록 시작

□ Phase 1: 소재 스캔 및 분석
  □ 샘플 2~3개로 분석 파이프라인 테스트
  □ 전체 소재 분석 실행
  □ 분석 결과 확인 및 보완

□ Phase 2: 색보정
  □ LOG 변환 LUT 테스트 (샘플)
  □ 전체 LOG 클립 변환
  □ 톤 매칭
  □ 크리에이티브 룩 적용

□ Phase 3: 사진 처리
  □ RAW 현상 (해당 시)
  □ 보정 및 크롭
  □ Ken Burns 클립 생성

□ Phase 4: 나레이션
  □ 대본 작성 → 검토
  □ TTS 생성 → 청취 확인

□ Phase 5: 오디오
  □ BGM 선택
  □ 효과음 배치
  □ 덕킹 및 믹싱

□ Phase 6: 최종 합성
  □ 타임라인 설계 → 검토
  □ 편집 및 합성
  □ SeouLink 워터마크 삽입
  □ 엔딩 크레딧 삽입 (Produced with CineLink | SeouLink)
  □ 최종 인코딩 및 출력 확인

□ 라이브러리 아카이빙
  □ 분석 결과를 cinelink/library/archive/ 에 복사
  □ 등장인물 이름/관계 수동 입력
  □ 오인식 태그 수정
  □ 글로벌 인덱스(library/db/library.json) 업데이트

□ 배포
  □ 영상 설명(description)에 SeouLink 크레딧 + 출처 표기 포함
  □ 플랫폼별 업로드 (YouTube, Instagram, TikTok 등)
```

---

## 트러블슈팅

### FFmpeg 관련
- **LUT 적용 시 색이 이상하게 나오는 경우:** LUT가 해당 LOG 프로파일용인지 확인. C-Log3 영상에 C-Log LUT를 적용하면 안 된다.
- **concat 시 에러:** 모든 클립의 해상도, FPS, 코덱이 동일해야 한다. 다르면 `-c:v libx264 -crf 18` 로 재인코딩.
- **한글 텍스트가 깨지는 경우:** fontfile 경로에 CJK 지원 폰트를 명시적으로 지정.

### 토큰/비용 관련
- **영상 분석 토큰 과다:** fps를 낮추거나(0.5fps, 0.2fps), 시간 범위를 지정하여 부분 분석.
- **타입캐스트 API 한도:** 플랜별 월간 다운로드 시간 확인. 베이직 60분, 프로 무제한.

### 품질 관련
- **중간 작업물 화질 저하:** 중간 단계에서 CRF 18 이하 유지. CRF 23 이상으로 올리지 않는다.
- **오디오 싱크 어긋남:** `-async 1` 옵션 추가 또는 `-af aresample=async=1000` 사용.

---

## 저작권 및 라이선스 전략

> 영상에 사용하는 모든 외부 에셋(음원, 효과음, 폰트, 이미지 등)은 저작권이 확보된 것만 사용한다. 프로젝트마다 `LICENSE_LOG.md`를 작성하여 사용한 모든 에셋의 출처·라이선스·다운로드일을 기록한다.

### 배경음악 (BGM)

**안전 우선순위:**

1. **YouTube 오디오 보관함 (가장 안전)**
   - YouTube Studio → 오디오 보관함에서 다운로드
   - Content ID 시스템과 연동되어 신고 가능성이 가장 낮음
   - 일부 트랙은 영상 설명에 출처 표기 필요 (다운로드 시 표시됨)
   - URL: https://studio.youtube.com/ → 오디오 보관함

2. **Pixabay Music (깔끔한 라이선스)**
   - 상업적 사용 무료, 출처 표기 불필요
   - Content ID에 등록되지 않은 오리지널 음원
   - URL: https://pixabay.com/music/

3. **Free Music Archive**
   - CC0(퍼블릭 도메인) 필터 사용 시 완전 자유
   - CC-BY 음원은 출처 표기 필수
   - URL: https://freemusicarchive.org/

4. **유료 구독 서비스 (본격 운영 시)**
   - Epidemic Sound: Content ID 완전 보호, 월 $15~
   - Artlist: 연간 구독, 음원 + 효과음 + 영상 소스
   - Uppbeat: 무료 티어 있음 (월 3곡), URL: https://uppbeat.io/

5. **AI 생성 음악 (주의 필요)**
   - Musicful, Suno, Udio 등으로 직접 생성 가능
   - 단, 일부 AI 음악 생성 서비스는 저작권 침해 소송이 진행 중
   - 반드시 해당 서비스 약관에서 "YouTube 상업적 사용 허용"이 명시적으로 기재된 경우에만 사용
   - 약관이 불명확하면 사용하지 않는 것이 안전

**핵심 주의사항:**
- "무료"라고 표시된 음악이라도 Content ID에 등록되어 있으면 YouTube가 자동 신고할 수 있다
- 영상 설명에 "출처: OOO"라고 써도 Content ID는 이를 인식하지 않는다
- 외부에서 음원 라이선스를 구매했더라도 Content ID가 이를 알 수 없으므로, 이의제기 절차가 필요할 수 있다
- Shorts(60초 미만)에서 저작권 제약 없이 사용 가능한 음악이라도 긴 영상에서는 제약이 적용될 수 있다

### 효과음 (SFX)

| 소스 | 라이선스 | 출처 표기 | URL |
|------|---------|----------|-----|
| Pixabay SFX | 상업적 무료 | 불필요 | https://pixabay.com/sound-effects/ |
| Freesound (CC0 필터) | 퍼블릭 도메인 | 불필요 | https://freesound.org/ |
| Freesound (CC-BY 필터) | 상업적 무료 | 필수 | https://freesound.org/ |
| YouTube 오디오 보관함 | 상업적 무료 | 트랙별 확인 | YouTube Studio |
| Epidemic Sound (유료) | 구독 포함 | 불필요 | https://www.epidemicsound.com/ |

Freesound 사용 시 반드시 라이선스 필터를 CC0(Creative Commons Zero)로 설정하여 검색할 것. CC-BY는 출처 표기가 필요하고, CC-BY-NC는 상업적 사용 불가.

### 폰트

**라이선스 유형 이해:**

- **OFL (SIL Open Font License):** 폰트 자체를 단독 판매하지 않는 한 사용·수정·재배포 자유. 영상 텍스트 삽입에 아무 제약 없음. 가장 안전한 라이선스.
- **공공누리 제1유형:** 출처 표시만 하면 상업적 이용 및 2차 저작물 작성 가능.
- **공공누리 제3유형:** 출처 표시 필요, 상업적 이용 가능하지만 변경 금지.
- **전용 라이선스:** 각 기업/브랜드가 별도 약관으로 배포. 반드시 허용 범위를 개별 확인해야 함.

**영상 제작에 안전한 한글 폰트 (모두 OFL):**

| 폰트 | 제작사 | 특징 |
|------|--------|------|
| Noto Sans KR / Noto Serif KR | Google | 가장 범용적, 다국어 지원 |
| 카카오 큰글씨 / 작은글씨 | 카카오 | 디지털 화면 최적화, 2025년 출시 |
| 나눔고딕 / 나눔명조 | 네이버 | 가장 널리 사용되는 한글 폰트 |
| 나눔스퀘어 / 나눔스퀘어라운드 | 네이버 | 모던한 느낌 |
| 마루부리 | 네이버 | 명조 계열 |
| 프리텐다드 (Pretendard) | 길형진 | 애플 SF 느낌, UI/영상 모두 우수 |
| 배민 한나체 / 주아체 / 도현체 | 우아한형제들 | 개성 있는 디자인 |

**폰트 선택 시 체크리스트:**
1. OFL 라이선스인지 확인 (눈누에서 OFL 필터 적용)
2. 영상 임베드(텍스트 오버레이)가 허용되는지 확인
3. CI/BI(로고) 제작 용도는 별도 확인 필요 (일부 제한)
4. 공식 배포처에서 다운로드 (비공식 재배포 사이트 사용 금지)

**폰트 검색 사이트:**
- 눈누: https://noonnu.cc (OFL 필터 지원)
- Google Fonts: https://fonts.google.com/?subset=korean
- 한국저작권위원회 공유마당: https://gongu.copyright.or.kr (안심글꼴)

**주의:**
- 한글과컴퓨터(한컴오피스) 내장 폰트는 상업적 사용에 제한이 있을 수 있다. 시스템 기본 폰트를 무심코 쓰지 말고, 반드시 별도로 OFL 폰트를 다운받아 사용할 것.
- 일부 기업 배포 폰트는 특정 산업군(도박, 성인물, 게임 등)에서의 사용을 제한하는 경우가 있으므로 약관 확인 필요.

### TTS 나레이션 (타입캐스트)

- 타입캐스트로 생성한 음성의 저작권은 이용 플랜의 약관을 따른다
- 유료 플랜(베이직/프로/비즈니스)에서 생성한 음성은 일반적으로 상업적 영상에 사용 가능
- 생성된 음성을 별도의 음원/보이스팩으로 재판매하는 것은 금지
- 구체적 허용 범위는 타입캐스트 이용약관 최신 버전을 확인: https://typecast.ai/

### LICENSE_LOG.md 템플릿

프로젝트 루트에 아래 형식의 파일을 만들어 사용한 모든 에셋을 기록한다.

```markdown
# 에셋 라이선스 기록

## 프로젝트: [프로젝트명]
## 작성일: [날짜]

### 배경음악
| 파일명 | 곡명 | 출처 | 라이선스 | 출처표기 필요 | 다운로드일 |
|--------|------|------|---------|-------------|-----------|
| main_bgm.mp3 | Summer Vibes | Pixabay | Pixabay License | 불필요 | 2026-04-08 |

### 효과음
| 파일명 | 설명 | 출처 | 라이선스 | 출처표기 필요 | 다운로드일 |
|--------|------|------|---------|-------------|-----------|
| whoosh.wav | 장면전환 | Freesound | CC0 | 불필요 | 2026-04-08 |

### 폰트
| 폰트명 | 제작사 | 라이선스 | 용도 | 다운로드 출처 |
|--------|--------|---------|------|-------------|
| Pretendard | 길형진 | OFL | 타이틀/자막 | https://cactus.tistory.com/306 |
| Noto Sans KR | Google | OFL | 본문 자막 | https://fonts.google.com/ |

### TTS 나레이션
| 서비스 | 플랜 | 캐릭터 | 생성일 | 상업적 사용 |
|--------|------|--------|--------|-----------|
| 타입캐스트 | 프로 | [캐릭터명] | 2026-04-08 | 허용 (약관 확인) |
```

### 저작권 관련 체크리스트 (프로젝트 시작 전)

```
□ BGM: 라이선스 확인 완료, Content ID 안전한 소스인지 확인
□ 효과음: CC0 또는 Pixabay License 확인
□ 폰트: OFL 라이선스 확인, 공식 배포처에서 다운로드
□ TTS: 유료 플랜 확인, 상업적 사용 허용 여부 확인
□ LICENSE_LOG.md 작성 시작
□ 영상 설명(description)에 필요한 출처 표기 문구 준비
```

---

## 장기 과제: CineLink 온디바이스 애플리케이션화

> CineLink 파이프라인을 독립 애플리케이션으로 전환하기 위한 장기 로드맵이다. 로컬 LLM(Gemma 4 등)을 활용하여 클라우드 의존 없이 온디바이스로 영상 편집 AI를 구동하고, SeouLink 브랜드로 콘텐츠를 배포하는 엔드투엔드 시스템을 목표로 한다.

### 왜 온디바이스인가

- 프라이버시: 개인 영상/사진이 외부 서버로 전송되지 않음
- 비용: API 토큰 과금 없이 무제한 사용
- 오프라인: 인터넷 없는 환경(비행기, 오지 여행 중)에서도 소재 분석·정리 가능
- 속도: 네트워크 레이턴시 없이 즉시 응답

### 타겟 모델: Gemma 4 패밀리

Google DeepMind의 Gemma 4 (2026년 4월 출시)는 Apache 2.0 라이선스로 상업적 사용·수정·배포가 완전히 자유롭다.

**모델 라인업:**

| 모델 | 실효 파라미터 | 컨텍스트 | 멀티모달 | 타겟 하드웨어 |
|------|-------------|---------|---------|------------|
| E2B | 2B | 128K | 텍스트+이미지+오디오 | 스마트폰, 라즈베리파이 |
| E4B | 4B | 128K | 텍스트+이미지+오디오 | 스마트폰, 태블릿 |
| 26B (MoE) | 4B 실효 | 256K | 텍스트+이미지+비디오 | 랩탑 GPU (M시리즈 맥) |
| 31B (Dense) | 31B | 256K | 텍스트+이미지+비디오 | 데스크탑 GPU |

**우리 파이프라인과의 매칭:**

- 프레임 분석/장면 이해: Gemma 4 비전으로 대체 가능. 26B/31B는 60초 1fps 비디오를 직접 이해
- 음성 전사: E2B/E4B는 네이티브 오디오 입력으로 음성 인식 지원 (Whisper 대체 가능)
- 나레이션 대본 생성: 31B가 Arena AI 텍스트 리더보드 오픈 모델 세계 3위급 품질
- FFmpeg 명령어 생성: 코딩 벤치마크 우수, 에이전트 도구 호출(function calling) 네이티브 지원
- 다국어: 140개 이상 언어 기본 지원 (한국어/일본어 대본·자막 무리 없음)

### 온디바이스 전환 가능성 평가

**가능 (녹색):**
- 프레임 추출 → 비전 분석 → 장면 태깅/분류
- 음성 전사 (STT)
- 나레이션 대본 작성
- FFmpeg 명령어 자동 생성 (에이전트 패턴)
- 미디어 라이브러리 검색 쿼리 처리
- 다국어 자막 생성

**도전적 (황색):**
- 모바일에서 수백 프레임 순차 분석 — 배터리·발열 이슈, 배치 크기 조절 필요
- 26B MoE 랩탑 실행 — 4bit 양자화 시 M시리즈 맥에서 가능하나 저사양 노트북은 어려움
- 미묘한 색감 판단 — 2B~4B 모델로는 정밀한 색보정 파라미터 결정이 부정확할 수 있음

**어려움 (적색):**
- 고품질 한국어 TTS — Gemma 4는 텍스트→음성 생성 미지원. 타입캐스트 수준의 감정 TTS는 클라우드 API 유지 또는 별도 로컬 TTS 모델 필요
- 실시간 비디오 프리뷰 — LLM의 역할이 아님. 별도 렌더링 엔진/UI 프레임워크 필요
- 정밀 색보정 자동화 — 모니터 캘리브레이션 의존적, 소형 모델로는 한계

### 제안 아키텍처

```
┌───────────────────────────────────────────────┐
│              사용자 인터페이스                  │
│     데스크탑: Electron 또는 Tauri              │
│     모바일: Flutter 또는 React Native          │
│  (폴더 드래그앤드롭 → 분석 → 편집제안 → 출력)   │
└──────────────────┬────────────────────────────┘
                   │
┌──────────────────▼────────────────────────────┐
│            AI 오케스트레이터                    │
│                                                │
│  데스크탑 모드          모바일 모드             │
│  ┌──────────────┐   ┌──────────────┐          │
│  │ Gemma 4 31B  │   │ Gemma 4 E4B  │          │
│  │ 또는 26B MoE │   │ 또는 E2B     │          │
│  │              │   │              │          │
│  │ - 정밀 분석   │   │ - 간이 태깅   │          │
│  │ - 대본 생성   │   │ - 현장 분류   │          │
│  │ - 편집 판단   │   │ - 검색 쿼리   │          │
│  │ - 색보정 결정 │   │ - 메모 기록   │          │
│  └──────────────┘   └──────────────┘          │
│                                                │
│  Ollama / llama.cpp / LM Studio / MLX 기반     │
└──────────────────┬────────────────────────────┘
                   │
┌──────────────────▼────────────────────────────┐
│            미디어 처리 엔진                     │
│                                                │
│  FFmpeg ─── 영상/오디오 편집 실행               │
│  ImageMagick ─── 사진 보정                     │
│  Whisper 또는 Gemma STT ─── 음성 전사          │
│  로컬 TTS (Piper/Edge) ─── 간이 나레이션       │
└──────────────────┬────────────────────────────┘
                   │
┌──────────────────▼────────────────────────────┐
│          미디어 라이브러리 (SQLite)              │
│                                                │
│  클립·인물·대사·장면 인덱스                     │
│  FTS5 전문검색 (대사·태그 검색)                 │
│  크로스 프로젝트 통합 검색                      │
└──────────────────┬────────────────────────────┘
                   │
          (선택) 클라우드 연동
          ├── 타입캐스트 TTS API (고품질 나레이션)
          ├── 클라우드 LLM 폴백 (복잡한 판단)
          └── 클라우드 동기화 (모바일↔데스크탑)
```

**핵심 전략 — 티어드(tiered) 실행:**
- 모바일 (E2B/E4B): 촬영 직후 현장에서 빠른 태깅·분류·메모. 무거운 처리는 안 함.
- 데스크탑 (26B/31B): 정밀 분석, 대본 생성, 편집 판단, 렌더링 실행.
- 클라우드 (선택): 고품질 TTS, 고난도 추론이 필요한 경우에만 API 호출.

### 로드맵

**1단계: 파이프라인 실전 검증 (현재~3개월)**

목표: Claude Code 기반 파이프라인으로 실제 영상 2~3개를 완성하여 자동화 가능 영역과 사람 개입 필수 영역을 검증한다.

작업:
- 이시가키 영상으로 첫 번째 완성작 제작
- 미디어 라이브러리에 데이터 축적 시작
- 파이프라인의 각 단계별 소요 시간·품질·비용 기록
- 어떤 단계가 앱으로 자동화할 가치가 있는지 판단

산출물:
- 완성된 영상 2~3개
- 파이프라인 단계별 평가 리포트
- 미디어 라이브러리 초기 데이터

**2단계: 로컬 LLM 전환 실험 (3~6개월)**

목표: Claude Code가 하던 역할을 Gemma 4 로컬 모델이 대체할 수 있는지 품질을 비교한다.

작업:
- Gemma 4 31B를 Ollama 또는 llama.cpp로 M시리즈 맥에서 실행
- 동일한 클립에 대해 Claude vs Gemma 4의 분석 품질 비교
- 대본 생성 품질 비교
- FFmpeg 명령어 생성 정확도 비교
- 부족한 부분은 프롬프트 엔지니어링 또는 파인튜닝으로 보완

산출물:
- Claude vs Gemma 4 품질 비교 리포트
- 최적 프롬프트 템플릿
- 파인튜닝 필요 여부 판단

**3단계: 데스크탑 앱 프로토타입 (6~12개월)**

목표: GUI가 있는 독립 데스크탑 애플리케이션의 프로토타입을 제작한다.

작업:
- UI 프레임워크 선택 (Electron/Tauri + React)
- Gemma 4 로컬 추론 엔진 통합
- FFmpeg 바인딩 (fluent-ffmpeg 또는 Python subprocess)
- 미디어 라이브러리를 SQLite + FTS5로 전환
- 핵심 워크플로우: 폴더 드롭 → 자동 분석 → 편집 제안 → 원클릭 출력

산출물:
- 동작하는 데스크탑 앱 프로토타입
- 내부 알파 테스트

**4단계: 모바일 확장 및 동기화 (12개월~)**

목표: 모바일에서 촬영 직후 간이 분석을 수행하고, 데스크탑과 라이브러리를 동기화한다.

작업:
- E4B 모바일 실행 (Google AI Edge / Android AICore)
- 촬영 직후 태깅·분류 자동화
- 데스크탑↔모바일 라이브러리 동기화 (로컬 네트워크 또는 클라우드)
- 모바일에서 간단한 편집 지시 → 데스크탑에서 렌더링 큐 실행

산출물:
- 모바일 컴패니언 앱
- 크로스 디바이스 워크플로우

### 기술 선택 시 고려사항

**LLM 추론 엔진:**
- Apple Silicon 맥: MLX가 가장 최적화됨. Ollama도 MLX 백엔드 지원
- NVIDIA GPU: llama.cpp (CUDA), vLLM
- 모바일: Google AI Edge (LiteRT-LM), MediaPipe

**양자화 전략:**
- 31B Dense → 4bit 양자화 시 약 16GB VRAM 필요 (M2 Pro 16GB로 빠듯, M2 Pro 32GB면 여유)
- 26B MoE → 실효 4B이므로 양자화 부담 적음. 8bit로도 M시리즈에서 쾌적
- E4B → 2~3GB RAM이면 충분. 스마트폰에서 실행 가능

**미디어 라이브러리 DB:**
- 프로토타입: JSON 파일 (현재 방식, 간단하지만 검색 느림)
- 프로덕션: SQLite + FTS5 (전문검색 지원, 단일 파일, 크로스 플랫폼)
- 대규모: PostgreSQL + pgvector (임베딩 기반 유사도 검색, 서버 필요)

**UI 프레임워크:**
- Electron: 가장 성숙한 생태계, Chromium 번들로 앱 크기 큼
- Tauri: Rust 기반, 앱 크기 작고 성능 좋음, 생태계는 Electron 대비 작음
- Flutter: 데스크탑+모바일 단일 코드베이스 가능, Dart 학습 필요

### 경쟁 환경 모니터링

이 영역은 빠르게 움직이고 있으므로 아래 프로젝트들을 주시한다:

- **ButterCut** (github.com/barefootford/buttercut): Claude Code 기반 영상 편집, 우리 파이프라인과 유사한 접근
- **Google AI Edge Gallery Agent Skills**: Gemma 4 온디바이스 에이전트 참조 구현
- **Remotion**: React 기반 프로그래매틱 영상 생성, UI 통합 시 참고
- **LosslessCut**: 오픈소스 영상 편집기, FFmpeg 기반 UI 참고
- **OpenCut**: 브라우저 기반 오픈소스 편집기

### 이 장기 과제의 전제 조건

1. **1단계(파이프라인 실전 검증)를 반드시 먼저 완료한다.** 실제로 영상을 몇 개 만들어봐야 어떤 단계가 자동화할 가치가 있고, 어떤 단계는 사람이 개입해야 하는지 알 수 있다.
2. **미디어 라이브러리 데이터가 축적되어야 한다.** 검색·재활용 기능의 가치는 소재가 쌓여야 체감된다.
3. **로컬 LLM 생태계의 발전을 지켜본다.** Gemma 4가 현재 최선이지만, 6개월 후에는 더 나은 모델이 나올 수 있다. 아키텍처를 모델 교체가 쉽도록 추상화해둔다.
