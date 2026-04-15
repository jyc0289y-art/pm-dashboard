# MOD-001 — GoodNotes 필기 오버레이

## 메타데이터
- **출처**: P1 (SeouLink 한국어교실)
- **생성 세션**: P1.12wc (2026-03-28)
- **버전**: 1.1.0
- **의존성**: 없음 (vanilla JS, zero dependencies)
- **라이선스**: MIT

## 소스 파일

| 파일 | 경로 (출처 프로젝트 기준) | 크기 | 역할 |
|------|--------------------------|------|------|
| `goodnotes.js` | `web_textbooks/js/goodnotes.js` | ~480줄 | IIFE 모듈 — 필기 엔진 전체 |
| `goodnotes.css` | `web_textbooks/css/goodnotes.css` | ~270줄 | 툴바, FAB, 오버레이, 서브메뉴 스타일 |

**절대 경로 (원본)**:
```
~/Library/Mobile Documents/com~apple~CloudDocs/SeouLink/한국어교실/web_textbooks/js/goodnotes.js
~/Library/Mobile Documents/com~apple~CloudDocs/SeouLink/한국어교실/web_textbooks/css/goodnotes.css
```

## 기능 목록

| 기능 | 상세 |
|------|------|
| 펜 | 압력+속도 감지 → 두께 변화, tapered stroke, round cap |
| 형광펜 | multiply 블렌드, 반투명(0.35), square cap, 플랫 질감 |
| 지우개 | 스트로크 단위 삭제 (터치한 선 전체 제거) |
| Undo/Redo | 스택 기반, Ctrl+Z / Ctrl+Shift+Z |
| 색상 팔레트 | 18색 (6×3), 도구별 독립 색상 기억 |
| 굵기 선택 | 도구별 3단계 (가늘게/보통/굵게) |
| 자동 저장 | localStorage, 페이지별 키 자동 생성 |
| 단축키 | 1=펜, 2=형광펜, 3=지우개, ESC=닫기 |
| FAB | 우측 하단 플로팅 버튼으로 on/off 토글 |
| 스크롤 대응 | Fixed viewport canvas + scroll offset 렌더링 |

## 포크 방법

### 1. 파일 복사
```bash
# 대상 프로젝트의 적절한 위치로 복사
cp {원본}/js/goodnotes.js  {대상}/js/goodnotes.js
cp {원본}/css/goodnotes.css {대상}/css/goodnotes.css
```

### 2. HTML 통합
```html
<head>
  <link rel="stylesheet" href="css/goodnotes.css">
</head>
<body>
  <!-- 페이지 콘텐츠 -->
  <script src="js/goodnotes.js"></script>
  <script>GoodNotes.init();</script>
</body>
```

### 3. 옵션 커스텀 (선택)
```javascript
GoodNotes.init({
  storageKey: 'my_custom_key',   // localStorage 키 (기본: URL 기반 자동 생성)
  autoSave: true,                // 스트로크 완료 시 자동 저장
  fab: true,                     // FAB 버튼 표시
  colors: ['#000', '#E00', ...], // 커스텀 색상 팔레트
  defaultPenColor: '#1A1A1A',
  defaultHighlighterColor: '#FFB74D',
  defaultPenWidth: 3,            // 1.5 | 3 | 5
  defaultHighlighterWidth: 20,   // 12 | 20 | 30
});
```

### 4. CSS 테마 오버라이드 (선택)
```css
:root {
  --gn-toolbar-bg: rgba(30, 30, 30, 0.92);
  --gn-active-color: #4A90D9;
  --gn-toolbar-radius: 16px;
}
```

## Public API

| 메서드 | 설명 |
|--------|------|
| `GoodNotes.init(options?)` | 초기화 (DOM 생성, 이벤트 바인딩, 저장 데이터 로드) |
| `GoodNotes.destroy()` | DOM 제거, 상태 초기화 |
| `GoodNotes.toggle()` | 필기 모드 on/off |
| `GoodNotes.isActive` | 현재 활성 상태 (getter) |
| `GoodNotes.undo()` | 실행 취소 |
| `GoodNotes.redo()` | 다시 실행 |
| `GoodNotes.clearAll()` | 전체 지우기 (undo 가능) |
| `GoodNotes.save()` | 수동 저장 |
| `GoodNotes.load()` | 저장 데이터 로드 |
| `GoodNotes.getStrokes()` | 스트로크 데이터 JSON 반환 |
| `GoodNotes.setStrokes(data)` | 스트로크 데이터 주입 |
| `GoodNotes.exportImage(type?, quality?)` | 캔버스를 이미지 DataURL로 내보내기 |

## 변경 이력

| 버전 | 날짜 | 세션 | 변경 내용 |
|------|------|------|----------|
| 1.0.0 | 2026-03-28 | P1.12wc | 초기 구현 (absolute canvas) |
| 1.1.0 | 2026-03-28 | P1.12wc | fixed viewport canvas로 전환 (max canvas 크기 제한 회피) |

## 포크 이력

| 대상 프로젝트 | 세션 | 날짜 | 버전 | 커스텀 |
|--------------|------|------|------|--------|
| (아직 없음) | — | — | — | — |
