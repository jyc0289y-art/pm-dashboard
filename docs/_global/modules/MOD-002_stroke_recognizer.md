# MOD-002 — StrokeRecognizer

## 메타데이터
- 이름: StrokeRecognizer
- 버전: 1.0.0
- 출처: P14 (3DLink)
- 생성일: 2026-03-28
- 언어: Swift
- 의존성: `simd` (Apple 표준)

## 설명
Apple Pencil / 터치 프리핸드 스트로크를 깨끗한 기하 도형으로 변환하는 인식기.
Ramer-Douglas-Peucker 간소화 + 도형 분류 기반.

## 기능
| 도형 | 인식 방식 |
|------|----------|
| Line | 시작/끝점 추출 + 수평/수직 5° 스냅 |
| Circle | centroid + 평균 반지름 |
| Arc | 3점(시작/중간/끝) 원 피팅 → 시작/끝 각도 |
| Rectangle | 스트로크 바운딩 박스 |

## 소스 파일
| 파일 | 설명 |
|------|------|
| `Sources/App/StrokeRecognizer.swift` | 메인 인식기 (163줄) |

## 포크 방법
1. `StrokeRecognizer.swift` 복사
2. 프로젝트에 맞는 입출력 타입 정의:
   - 입력: `[SIMD2<Double>]` 포인트 배열 + 도구 선택 enum
   - 출력: 인식된 도형 엔티티 (geometry enum)
3. 3DLink 의존 타입(`SketchTool`, `SketchEntity`, `SketchGeometry`)을 프로젝트 타입으로 교체하거나 제네릭화

## API
```swift
struct StrokeRecognizer {
    /// points: 스크린/캔버스 좌표 시퀀스, tool: 현재 선택된 도형 도구
    static func recognize(points: [SIMD2<Double>], tool: SketchTool) -> SketchEntity?
}
```

## 확장 포인트
- 도형 추가: `recognize()` switch + private 인식 메서드 추가
- 스냅 각도 조정: `recognizeLine` 내 5° 상수 변경
- 최소 크기 임계값: circle 0.5mm, rectangle 1.0mm — 프로젝트별 조정

## 변경 이력
| 버전 | 날짜 | 변경 |
|------|------|------|
| 1.0.0 | 2026-03-28 | 초기 등록 (P14.6wc) |

## 포크 이력
| 프로젝트 | 버전 | 날짜 | 비고 |
|----------|------|------|------|
| (원본) P14 3DLink | 1.0.0 | 2026-03-28 | 원본 |
