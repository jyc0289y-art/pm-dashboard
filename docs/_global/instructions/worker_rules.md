# Worker(부하 LLM) 활용 규칙

MCP로 연결된 로컬/외부 LLM을 활용해 토큰을 절약한다.
단, 품질과 정확성이 우선이며 할루시네이션 위험이 있는 작업은 위임하지 않는다.

## 사용 가능한 Worker

| Worker | 도구명 | 용도 |
|--------|--------|------|
| Ollama qwen2.5:14b | `ask_worker`, `worker_summarize_text`, `worker_translate` | 요약, 번역 초안, 단순 텍스트 |
| Ollama qwen2.5-coder:7b | `ask_worker` (model 지정) | 코드 포맷, 린트 체크 |
| Gemini CLI | `gemini_ask` | 교재 대화문, 문법 설명 |
| Gemini Vision | `gemini_analyze_image` | 이미지 분석, 프롬프트 역엔지니어링 |

## 위임 기준

**Worker에게 맡겨도 되는 것:**
- 2000자 이상 텍스트 요약 → `worker_summarize_text`
- 번역 초안 (한/영/일) → `worker_translate` → Claude 감수
- 반복적 텍스트 대량 생성 → `ask_worker` 초안 → Claude 검수
- 코드 포맷팅/구문 체크 → `ask_worker` (qwen2.5-coder:7b)
- 교재 대화문/예문 초안 → `gemini_ask` → Claude 검수
- 데이터 추출, 포맷 변환 → `ask_worker`

**Claude가 직접 해야 하는 것 (위임 금지):**
- 설계 결정, 아키텍처 판단, 복잡한 추론
- 최종 결과물 품질 판정 및 검수
- 사용자 의도 해석, 모호한 지시 구체화
- URL/경로/파일명 생성 (할루시네이션 위험)
- 숫자 계산, 날짜 연산
- API 코드 작성 (엔드포인트/파라미터)
- 보안 관련 코드, 인증/결제 로직
- 긴 코드 리팩토링 (전체 맥락 이해 필요)

## 할루시네이션 방지 규칙

1. Worker 위임 시 system 프롬프트에 항상 포함:
   `"모르는 것은 '확실하지 않음'이라고 답하라. 추측하지 마라."`
2. "사실 확인"(요약/추출)은 위임 OK, "사실 생성"(새 내용)은 Claude 검수 필수
3. Worker 결과물은 검증 가능한 형태로 요청 (번역 시 원문 병기, 요약 시 키워드 목록)
4. Worker 결과를 사용자에게 전달 전 Claude가 반드시 한 번 검토

## 토큰 절약 패턴

- **요약 후 투입**: 긴 파일 → `worker_summarize_text` → 요약본만 Claude에 전달
- **초안 → 검수**: 대량 생성 → Worker 초안 → Claude 수정분만 처리
- **번역 체인**: 원문 → `worker_translate` 초역 → Claude 감수

## Worker 사용 리포트

사용자가 "워커 사용량", "토큰 절약 리포트", "워커 리포트" 등을 요청하면:
- 해당 세션에서 Worker에게 위임한 작업 목록 정리
- 각 위임 작업의 예상 토큰 절약량 추정 (입력/출력 텍스트 길이 기반)
- Claude 직접 처리 vs Worker 위임 비율 보고

예상 절약 기준:
- 요약 위임 1건 = 입력 텍스트 글자 수 × 0.5 토큰 절약
- 번역 위임 1건 = 출력 텍스트 글자 수 × 0.8 토큰 절약
- 텍스트 생성 위임 1건 = 출력 텍스트 글자 수 × 0.75 토큰 절약
