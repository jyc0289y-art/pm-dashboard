# MOD-003 — Markdown→HTML 렌더러

## 메타데이터
- **출처**: P11 (OfficeLink SL / MarkLink SL)
- **생성 세션**: P11.49wc (2026-03-28)
- **버전**: 1.0.0
- **의존성**: `markdown-it`, `markdown-it-task-lists`, `markdown-it-footnote`, `markdown-it-deflist`, `markdown-it-abbr`, `markdown-it-emoji`, `highlight.js` (core + 24 언어)
- **라이선스**: MIT

## 소스 파일

| 파일 | 경로 (출처 프로젝트 기준) | 크기 | 역할 |
|------|--------------------------|------|------|
| `renderer.js` | `src/preview/renderer.js` | ~261줄 | markdown-it 설정 + 플러그인 + 렌더 함수 |

**절대 경로 (원본)**:
```
~/Library/Mobile Documents/com~apple~CloudDocs/developer/marklink-sl/src/preview/renderer.js
```

## 기능 목록

| 기능 | 상세 |
|------|------|
| Markdown→HTML | markdown-it 기반 변환 (linkify, typographer) |
| 코드 하이라이팅 | highlight.js core + 24개 언어 (JS/TS/Python/Java/C/C++/C#/Go/Rust/Ruby/PHP/Swift/Kotlin/Bash/Shell/SQL/JSON/XML/HTML/CSS/MD/YAML/Dockerfile/Diff/Plaintext) |
| 체크리스트 | `- [ ]` / `- [x]` 태스크 리스트 |
| 각주 | `[^1]` 참조 + `[^1]:` 정의 |
| 정의 목록 | `Term\n: Definition` 문법 |
| 약어 | `*[HTML]: Hyper Text Markup Language` |
| 이모지 | `:smile:` → 이모지 문자 변환 |
| 자동 TOC | `[TOC]` 마커 → 목차 자동 생성 (앵커 연동) |
| Heading ID | 슬러그 기반 ID 자동 부여 + 중복 ID 해소 |
| Mermaid 블록 | ` ```mermaid ` → `<div class="mermaid">` (렌더러는 별도) |
| 테이블 래핑 | 스크롤 가능한 `<div>` 컨테이너 자동 래핑 |
| 이미지 lazy-load | `loading="lazy"` 자동 부여 |
| 이미지 크기 | `![alt|100x50](url)` 또는 `![alt|width=100](url)` 문법 |

## 포크 방법

### 1. 파일 복사
```bash
cp {원본}/src/preview/renderer.js {대상}/src/renderer.js
```

### 2. 의존성 설치
```bash
npm install markdown-it markdown-it-task-lists markdown-it-footnote \
  markdown-it-deflist markdown-it-abbr markdown-it-emoji highlight.js
```

### 3. 사용
```javascript
import { render, getRenderer, generateHeadingId } from './renderer.js';

// 기본 렌더링
const html = render('# Hello\n\nWorld');

// markdown-it 인스턴스 접근 (플러그인 추가 등)
const md = getRenderer();
md.use(myCustomPlugin);

// Heading ID 생성 (TOC 빌드 등)
const id = generateHeadingId('My Heading'); // → 'heading-my-heading'
```

### 4. CSS (highlight.js 테마)
```javascript
// 이미 import 포함됨:
import 'highlight.js/styles/github.css';
// 다크 모드 시 CSS class로 전환하거나 다른 테마 import
```

### 5. Mermaid 연동 (선택)
```javascript
// renderer.js는 mermaid 블록을 <div class="mermaid">로 변환만 함
// 실제 렌더링은 별도 처리:
import mermaid from 'mermaid';
mermaid.init(undefined, '.mermaid');
```

## Public API

| 함수 | 설명 |
|------|------|
| `render(markdownText)` | Markdown 문자열 → HTML 문자열 |
| `getRenderer()` | markdown-it 인스턴스 반환 (플러그인 추가용) |
| `generateHeadingId(text)` | 텍스트 → 슬러그 기반 heading ID |

## 커스터마이징

### 언어 추가
```javascript
import lua from 'highlight.js/lib/languages/lua';
hljs.registerLanguage('lua', lua);
```

### 플러그인 제거 (번들 축소)
불필요한 플러그인 import 및 `md.use()` 호출을 제거하면 됩니다.

### HTML 허용
```javascript
// createRenderer() 내에서:
const md = new MarkdownIt({ html: true, ... });
// ⚠️ XSS 위험 — sanitize.js(MOD 후보)와 함께 사용 권장
```

## 변경 이력

| 버전 | 날짜 | 세션 | 변경 내용 |
|------|------|------|----------|
| 1.0.0 | 2026-03-28 | P11.49wc | 초기 등록 (OfficeLink SL에서 추출) |

## 포크 이력

| 대상 프로젝트 | 세션 | 날짜 | 버전 | 커스텀 |
|--------------|------|------|------|--------|
| (아직 없음) | — | — | — | — |
