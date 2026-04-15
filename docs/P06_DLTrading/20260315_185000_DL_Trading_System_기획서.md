# 딥러닝 기반 자동매매 시스템 기획서

> 최종 업데이트: 2026-03-15
> 버전: 1.0
> 상태: 기획 완료 / 개발 착수 준비

---

## 1. 프로젝트 개요

### 1.1 목적

딥러닝 모델을 활용하여 금융 시장의 패턴을 학습하고, 학습된 모델의 매수/매도/홀드 시그널을 거래소 API를 통해 실제 주문으로 자동 실행하는 종합 트레이딩 시스템을 구축한다.

두 가지 시장을 대상으로 **동일한 아키텍처**를 공유하되, 거래소 API 레이어만 교체하는 설계로 구현한다:

- **암호화폐 (우선 개발)**: 업비트(Upbit) API — 24시간 시장으로 모델 검증 사이클이 빠르고 실험 반복에 유리
- **주식 (후속 개발)**: 한국투자증권 KIS Developers API — 국내주식 + 해외 ETF (SOXL, TQQQ, TSLL, IONQ 등)

### 1.2 왜 암호화폐를 먼저 하는가

| 요소 | 암호화폐 | 주식 |
|------|----------|------|
| 시장 운영 시간 | **24/7/365** | 국내 6.5시간, 해외 6.5시간 |
| 데이터 축적 속도 | 하루 1,440개 1분봉 | 하루 ~390개 1분봉 |
| 백테스트 반복 실험 | **데이터 연속적, 갭 없음** | 장 마감 갭, 주말 단절 |
| 모델 학습 사이클 | **빠름** (연속 데이터) | 느림 (단절적 데이터) |
| 모의투자 환경 | 소액 실전으로 대체 가능 | 별도 모의투자 계좌 필요 |
| API 제한 | REST 초당 10회, WebSocket 자유 | 모의 초당 1회, 실전 초당 20회 |
| 수수료 | 0.05% (업비트 원화마켓) | 0.015%~0.5% + 세금 |
| 최소 주문금액 | **~5,000원** | 종목가격 × 1주 |

### 1.3 핵심 원칙

- **손절매 절대 원칙**: 모든 포지션에 손절매 로직을 하드코딩한다. 모델이 뭐라 하든 손절매가 우선한다.
- **모듈화 설계**: 거래소 API 레이어만 교체하면 암호화폐 ↔ 주식 전환이 가능한 구조.
- **점진적 증액**: 검증된 전략만 투자금을 늘린다. 성과 없이 증액하지 않는다.
- **로깅 철저**: 모든 주문, 시그널, 모델 판단을 로그로 남겨 추후 분석에 활용.
- **코드 품질**: Claude Code에서 개발 시 타입 힌트, docstring, 단위 테스트를 갖춘다.

---

## 2. 시스템 아키텍처

### 2.1 전체 파이프라인

```
[Data Collector] → [Feature Engine] → [Model Core] → [Risk Manager] → [Order Executor]
       ↓                  ↓                ↓               ↓                ↓
   거래소 API          pandas/ta-lib     PyTorch/FinRL    손절매/포지션     거래소 API
   yfinance/pykrx                                        사이징            주문 실행
```

### 2.2 모듈 상세

| 모듈 | 역할 | 암호화폐 구현 | 주식 구현 |
|------|------|-------------|----------|
| **Data Collector** | 과거/실시간 데이터 수집 | pyupbit + Upbit WebSocket | yfinance + pykrx + KIS API |
| **Feature Engine** | 피처 생성 및 전처리 | **공통** (동일 코드) | **공통** (동일 코드) |
| **Model Core** | 예측/시그널 생성 | **공통** (동일 코드) | **공통** (동일 코드) |
| **Risk Manager** | 리스크 관리/손절매 | **공통** (파라미터만 다름) | **공통** (파라미터만 다름) |
| **Order Executor** | 거래소 주문 실행 | UpbitExecutor | KISExecutor |

> **핵심 설계**: Feature Engine, Model Core, Risk Manager는 거래소에 무관한 공통 모듈이다. Data Collector와 Order Executor만 거래소별로 구현한다.

### 2.3 디렉토리 구조

```
dl-trading/
├── config/
│   ├── settings.yaml          # 전략 파라미터, 종목 목록, 모드 설정
│   ├── .env                   # API Key/Secret (비공개, .gitignore 등록)
│   └── symbols/
│       ├── crypto.yaml        # 암호화폐 종목 목록 (KRW-BTC, KRW-ETH 등)
│       └── stock.yaml         # 주식 종목 목록 (SOXL, TQQQ, 삼성전자 등)
├── data/
│   ├── raw/                   # 원본 OHLCV
│   ├── processed/             # 피처 적용된 데이터
│   └── models/                # 학습된 모델 저장 (.pt, .pth)
├── src/
│   ├── __init__.py
│   ├── collector/
│   │   ├── __init__.py
│   │   ├── base.py            # BaseCollector (추상 클래스)
│   │   ├── upbit.py           # UpbitCollector (pyupbit 기반)
│   │   ├── kis.py             # KISCollector (KIS API 기반)
│   │   └── yfinance_loader.py # 과거 데이터 벌크 수집
│   ├── features/
│   │   ├── __init__.py
│   │   ├── technical.py       # 기술지표 (RSI, MACD, BB, ATR 등)
│   │   ├── preprocessing.py   # 정규화, 윈도우 슬라이싱
│   │   └── sentiment.py       # (Phase 3) 센티먼트 피처
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py            # BaseModel (추상 클래스)
│   │   ├── rule_based.py      # Phase 1: 규칙 기반 전략
│   │   ├── lstm.py            # Phase 2: LSTM 모델
│   │   ├── transformer.py     # Phase 3: TFT 모델
│   │   ├── rl_agent.py        # Phase 3: 강화학습 에이전트 (FinRL)
│   │   └── ensemble.py        # Phase 3: 앙상블 전략
│   ├── risk/
│   │   ├── __init__.py
│   │   └── manager.py         # 손절매, 포지션 사이징, MDD 관리
│   ├── executor/
│   │   ├── __init__.py
│   │   ├── base.py            # BaseExecutor (추상 클래스)
│   │   ├── upbit.py           # UpbitExecutor
│   │   └── kis.py             # KISExecutor
│   ├── backtest/
│   │   ├── __init__.py
│   │   └── engine.py          # 백테스팅 엔진
│   └── utils/
│       ├── __init__.py
│       ├── logger.py          # 로깅 설정
│       ├── notifier.py        # Telegram/이메일 알림
│       └── scheduler.py       # 스케줄러 (APScheduler)
├── notebooks/                 # 분석/실험용 Jupyter
├── tests/                     # 단위 테스트
├── logs/                      # 매매/모델/시스템 로그
├── main.py                    # 메인 실행 (모드: crypto/stock, 환경: virtual/prod)
└── requirements.txt
```

---

## 3. 거래소 API 상세

### 3.1 암호화폐: 업비트 (Upbit)

#### 사전 준비
1. 업비트 계정 생성 및 실명 인증
2. Open API 관리 페이지에서 API 키 발급 (https://upbit.com → MY → Open API 관리)
3. 권한 설정: 자산조회 + 주문조회 + 주문하기 체크
4. IP 주소 등록 (보안)

#### 라이브러리
- **pyupbit**: 업비트 API Python 래퍼 (커뮤니티 라이브러리, pip install pyupbit)
- 공식 문서: https://docs.upbit.com

#### 주요 API

| 기능 | 메서드 | pyupbit 함수 | 비고 |
|------|--------|-------------|------|
| 현재가 조회 | GET /v1/ticker | `pyupbit.get_current_price()` | |
| 캔들 조회 | GET /v1/candles | `pyupbit.get_ohlcv()` | 분/일/주/월봉 |
| 잔고 조회 | GET /v1/accounts | `upbit.get_balances()` | 인증 필요 |
| 시장가 매수 | POST /v1/orders | `upbit.buy_market_order()` | 금액 지정 |
| 시장가 매도 | POST /v1/orders | `upbit.sell_market_order()` | 수량 지정 |
| 지정가 매수 | POST /v1/orders | `upbit.buy_limit_order()` | |
| 지정가 매도 | POST /v1/orders | `upbit.sell_limit_order()` | |
| 주문 취소 | DELETE /v1/order | `upbit.cancel_order()` | |
| WebSocket | wss://api.upbit.com/websocket/v1 | `pyupbit.WebSocketManager` | 실시간 시세 |

#### API 제한
- REST API: **초당 10회** (주문), 초당 30회 (시세 조회)
- WebSocket: 연결당 초당 5회 요청 (Origin 헤더 있을 시)
- Python 서버사이드에서는 Origin 없으므로 실질적 제한 낮음

#### 수수료
- 원화(KRW) 마켓: **0.05%** (매수/매도 각각)
- 왕복 수수료: 0.1%

#### 대상 종목 (초기)
- KRW-BTC (비트코인)
- KRW-ETH (이더리움)
- 추가 종목은 모델 성능에 따라 확장

### 3.2 주식: 한국투자증권 (KIS Developers)

#### 사전 준비
1. 한국투자증권 계좌 보유 확인
2. KIS Developers 포털 서비스 신청 (apiportal.koreainvestment.com)
3. 모의투자 계좌 발급 (한투 홈페이지 또는 MTS)
4. 모의투자용 App Key / App Secret 발급
5. 실전용 App Key / App Secret 별도 발급

#### 라이브러리
- **python-kis (pykis)**: 커뮤니티 래퍼 (pip install python-kis)
- **공식 샘플 코드**: github.com/koreainvestment/open-trading-api
- 공식 문서: apiportal.koreainvestment.com/apiservice

#### 모의 → 실전 전환 설계

| 항목 | 모의투자 | 실전투자 |
|------|---------|---------|
| Base URL | openapivts.koreainvestment.com:29443 | openapi.koreainvestment.com:9443 |
| App Key/Secret | 모의투자용 | 실전용 |
| 계좌번호 | 모의 계좌 | 실전 계좌 |
| API 호출 제한 | **초당 1회** | **초당 20회** |

> config/settings.yaml에 `mode: virtual | prod` 스위치를 두어 한 줄로 전환.

#### 대상 종목
- **해외 ETF**: SOXL, TQQQ, TSL3, TSLL, IONQ, NNOX, BTC 관련 ETF
- **국내주식**: 향후 모델 성능에 따라 선정

#### 주의사항
- 모의투자 API 호출 제한이 초당 1회로 매우 낮음 → Rate Limiter 필수
- 해외주식: 미국 장 시간(KST 23:30~06:00, 서머타임 22:30~05:00) 대응 스케줄러 필요
- 레버리지 ETF(SOXL, TQQQ 등)는 기초지수 데이터도 함께 수집하여 피처로 활용

---

## 4. 로드맵: 4개 Phase

전체 로드맵은 4개 Phase로 구성된다. 각 Phase는 이전 단계의 성과를 검증한 후에만 진행한다.

### Phase 1: 기반 구축 + 규칙 기반 검증 (1~2개월)

**목표**: 거래소 API 연동을 완료하고, 간단한 규칙 기반 전략으로 전체 파이프라인을 안정적으로 돌린다.

#### 1-1. 프로젝트 셋업 (2~3일)
- [ ] 디렉토리 구조 생성 (섹션 2.3 참조)
- [ ] requirements.txt 작성 및 가상환경 구성
- [ ] config 구조 설계: settings.yaml, .env, symbols/
- [ ] 로깅 모듈 구현 (loguru 기반, 파일 + 콘솔 + 일별 로테이션)
- [ ] .gitignore 설정 (.env, data/, logs/, *.pt 등)

#### 1-2. 거래소 API 연동 — 암호화폐 (1주)
- [ ] pyupbit 설치 및 기본 테스트
- [ ] UpbitCollector 구현: 과거 OHLCV 수집 (일봉/분봉), 실시간 WebSocket 시세
- [ ] UpbitExecutor 구현: 시장가 매수/매도, 지정가 매수/매도, 잔고 조회
- [ ] Rate Limiter 구현 (초당 10회 제한 대응)
- [ ] 실제 소액(1만원)으로 매수/매도 테스트 → 정상 체결 확인

#### 1-3. 거래소 API 연동 — 주식 (1주)
- [ ] KIS Developers 서비스 신청 및 모의투자 계좌 발급
- [ ] KISCollector 구현: 국내/해외 시세 조회, 과거 데이터 수집
- [ ] KISExecutor 구현: 모의투자 주문 (국내 + 해외)
- [ ] Rate Limiter 구현 (모의 초당 1회, 실전 초당 20회 대응)
- [ ] 모의투자 매수/매도 테스트 → 정상 체결 확인

#### 1-4. 데이터 파이프라인 (1주)
- [ ] yfinance로 해외 ETF 과거 데이터 수집 (최소 3년치)
- [ ] pykrx로 국내주식 과거 데이터 수집
- [ ] pyupbit으로 암호화폐 과거 데이터 수집 (최대 200일 일봉, 분봉은 제한적)
- [ ] SQLite DB에 OHLCV 저장 스키마 설계 및 구현
- [ ] 자동 업데이트 스케줄러 (APScheduler: 암호화폐 5분마다, 주식 장 시간)

#### 1-5. Feature Engine (1주)
- [ ] 기술지표 생성 모듈: RSI(14), MACD(12,26,9), 볼린저밴드(20,2), ATR(14)
- [ ] 이동평균: MA5, MA20, MA60, MA120
- [ ] 거래량 변화율, 가격 변화율
- [ ] 정규화: Min-Max 또는 Z-Score (설정 가능)
- [ ] 윈도우 슬라이싱: 학습용 시퀀스 데이터 생성 (윈도우 크기 설정 가능)

#### 1-6. 규칙 기반 전략 운영 (2~3주)
- [ ] rule_based.py 구현:
  - 이동평균 교차: MA5 > MA20 매수, MA5 < MA20 매도
  - RSI 필터: RSI > 70 매도 시그널, RSI < 30 매수 시그널
  - 두 시그널 모두 일치할 때만 실제 주문 실행 (보수적)
- [ ] Risk Manager 구현:
  - 포지션별 손절매: -5% (암호화폐), -5% (주식, 레버리지 -3%)
  - 일일 최대 손실: 총 자본 -3% 도달 시 전체 청산
  - 포지션 최대 비중: 단일 종목 20%, 레버리지 ETF 15%
  - 현금 비중 최소: 총 자본의 20%
- [ ] 암호화폐에서 소액(10만원)으로 규칙 기반 전략 실전 운영 시작
- [ ] 매일 성과 로깅: 수익률, 체결 내역, 포지션 상태

#### Phase 1 완료 기준 (다음 단계 진입 조건)
- [x] 암호화폐 + 주식 API 모의주문 정상 체결 확인
- [x] 데이터 수집 → 피처 생성 → 시그널 → 주문 전체 파이프라인 정상 작동
- [x] 규칙 기반 전략으로 최소 2주 연속 운영 완료 (암호화폐)
- [x] 모든 거래 내역이 로그로 추적 가능

---

### Phase 2: 딥러닝 모델 도입 + 검증 (2~3개월)

**목표**: 규칙 기반을 딥러닝(LSTM)으로 교체하고, 규칙 기반 대비 성능 우위를 검증한다.

#### 2-1. LSTM 모델 개발 (2~3주)

**모델 구조:**
```
Input(window_size × features) → LSTM(128, 2layers) → Dropout(0.3) → Dense(64) → Dense(3, softmax)
```

| 항목 | 상세 |
|------|------|
| 입력 | 과거 N일 OHLCV + 기술지표 (윈도우 크기 20/40/60일 실험) |
| 출력 | 3클래스 분류: 상승(+1%↑) / 보합(±1%) / 하락(-1%↓) + Softmax 신뢰도 |
| 학습 데이터 | 최소 2년치 (70% 학습 / 15% 검증 / 15% 테스트) |
| 손실 함수 | CrossEntropyLoss (class weight 적용으로 불균형 대응) |
| 옵티마이저 | Adam (lr=0.001, weight_decay=1e-5) |
| 신뢰도 필터 | Softmax 최대값 0.6 이상일 때만 시그널 발생 |
| 학습 환경 | PyTorch + Apple Silicon MPS 백엔드 |

**암호화폐 특화 피처:**
- 24시간 거래량 변화율
- 김치프리미엄 (해외 거래소 대비 가격 차이) — 선택사항
- BTC 도미넌스 (BTC가 전체 시장에서 차지하는 비중)

**주식 특화 피처 (레버리지 ETF):**
- 기초지수 데이터 (SOX, QQQ, TSLA) 동시 입력
- VIX (변동성 지수)

#### 2-2. 백테스팅 프레임워크 (1~2주)
- [ ] backtest/engine.py 구현:
  - 과거 데이터로 전략 성과 시뮬레이션
  - 거래 비용 반영: 수수료 + 슬리피지
  - Walk-Forward 방식: 학습 기간을 이동시키며 반복 검증 (과적합 방지)
- [ ] 핵심 지표 자동 계산:
  - 총 수익률, 연환산 수익률
  - Sharpe Ratio (위험 대비 수익)
  - MDD (최대 드로다운)
  - 승률, Profit Factor (총이익/총손실)
  - 평균 보유 기간
- [ ] 벤치마크 비교: Buy & Hold, 규칙 기반 전략

#### 2-3. 암호화폐 실전 검증 (4주+)
- [ ] LSTM 모델을 암호화폐에서 소액(10~50만원) 실전 운영
- [ ] 24시간 자동 운영 (스케줄러: 예측 주기 1시간/4시간/일봉 실험)
- [ ] 일일 성과 보고서 자동 생성
- [ ] 모델 예측 vs 실제 결과 비교 분석
- [ ] 주간 리뷰 후 하이퍼파라미터 조정

#### Phase 2 완료 기준
- [ ] LSTM 백테스팅에서 Buy & Hold 대비 우수한 Sharpe Ratio 달성
- [ ] 암호화폐 실전 4주 운영 결과 양의 수익률 확인
- [ ] MDD가 설정한 한도 이내로 관리됨 확인

---

### Phase 3: 고도화 + 주식 실전 전환 (3~6개월)

**목표**: 모델을 고도화하고, 주식 시장에도 실전 배치한다.

#### 3-1. 모델 고도화

**Temporal Fusion Transformer (TFT)**
- 다중 시계열 처리에 특화된 Transformer 모델
- Variable Selection Network으로 어떤 피처가 예측에 중요한지 해석 가능
- 여러 종목/자산을 동시에 처리하여 상관관계 학습
- 참고: Lim et al. (2021) "Temporal Fusion Transformers for Interpretable Multi-horizon Time Series Forecasting"

**강화학습 에이전트 (FinRL)**
- 환경(Environment): 주식/암호화폐 시장 시뮬레이터 (OpenAI Gym 호환)
- 상태(State): OHLCV + 기술지표 + 포지션 정보 + 잔고
- 행위(Action): 각 종목별 매수/매도 비율 (-1 ~ +1 연속값)
- 보상(Reward): 포트폴리오 수익률 - 거래비용 - 리스크 페널티
- 알고리즘: PPO, A2C, DDPG 각각 학습 후 앙상블
- 참고: Liu et al. (2020) "FinRL: A Deep Reinforcement Learning Library for Automated Stock Trading"

**앙상블 전략**
- LSTM + TFT + RL 각각의 시그널을 가중 투표로 결합
- 가중치: 최근 N일 성과 기반 동적 조정 (성과 좋은 모델에 높은 비중)
- 모든 모델이 일치할 때 강한 시그널, 불일치 시 보수적 포지션

#### 3-2. 센티먼트 분석 추가 (선택사항)
- FinBERT로 금융 뉴스 센티먼트 분석 (Araci, 2019)
- Fear & Greed Index, VIX 등 시장 심리 지표 통합
- 암호화폐: Crypto Fear & Greed Index, BTC 도미넌스
- 센티먼트 시그널을 기존 모델의 추가 피처로 활용

#### 3-3. 주식 실전 전환

**전환 조건 (모두 충족 시):**

| 조건 | 기준 |
|------|------|
| 모의투자 기간 | 최소 3개월 이상 연속 운영 |
| 수익률 | 누적 양수 (Buy & Hold 대비 우수 권장) |
| MDD | -15% 이내 유지 |
| Sharpe Ratio | 1.0 이상 (연환산) |
| 시스템 안정성 | 무장애 2주 이상 연속 운영 |

**전환 절차:**
1. 실전 API 키 발급 → config에서 mode: virtual → prod 전환
2. 초기 투자금 100만원 이하로 설정
3. 모의+실전 2주간 병행 운영, 괴리 모니터링
4. 병행 결과 정상 확인 후 실전 단독 전환

#### Phase 3 완료 기준
- [ ] 앙상블 모델이 단일 모델 대비 안정적 성과
- [ ] 주식 소액 실전 1개월 이상 안정적 운영
- [ ] 암호화폐 + 주식 동시 운영 가능

---

### Phase 4: 확장 + 안정적 운영 (6개월~)

#### 4-1. 투자금 점진적 증액
- 월간 양의 수익 시: 100만 → 300만 → 500만 → 1000만 (각 단계 최소 1개월)
- 손실 발생 시: 증액 중단, 모델 재학습 후 재검증
- 투자금 규모에 따른 슬리피지/시장충격 변화 모니터링

#### 4-2. 모델 지속적 개선
- 월 1회 이상 최신 데이터로 재학습
- 성능 드리프트 감지: 최근 N일 정확도가 임계값 이하 시 알림
- 새 모델/피처는 백테스트 → 소액 실전(암호화폐) → 메인 반영 (A/B 테스트)
- 정기적 하이퍼파라미터 튜닝 (Optuna 등 활용 가능)

#### 4-3. 운영 자동화
- **일일 보고서**: Telegram Bot으로 자동 발송 (수익률, 포지션, 특이사항)
- **이상 감지 알림**: API 오류, 큰 손실, 모델 성능 저하 시 즉시 알림
- **월간 종합 보고서**: 수익률, MDD, Sharpe, 종목별 성과 자동 생성
- **시스템 헬스체크**: 프로세스/DB 상태 모니터링, 자동 재시작

---

## 5. 리스크 관리 전략

### 5.1 포지션 수준

| 항목 | 암호화폐 | 주식 (일반) | 주식 (레버리지 ETF) |
|------|---------|-----------|-------------------|
| 손절매 | -5% | -5% | **-3%** |
| 최대 비중 | 30% | 20% | **15%** |
| Trailing Stop | -3% | -3% | -2% |

### 5.2 포트폴리오 수준

| 항목 | 기본값 | 설명 |
|------|--------|------|
| 일일 최대 손실 | -3% | 하루 총 손실 -3% 도달 시 전체 청산 |
| MDD 한도 | -15% | 초과 시 시스템 정지 및 점검 |
| 최대 동시 포지션 | 5개 (암호화폐) / 5개 (주식) | |
| 현금 비중 최소 | 20% | 항상 총 자본의 20%는 현금 유지 |

### 5.3 레버리지 ETF 특별 규칙
- 손절매 강화: 3x ETF는 -3%로 강화 (일반 -5%)
- 비중 축소: 단일 레버리지 ETF에 15% 이상 투입 금지
- 기초지수 동시 입력: 학습 시 SOX(SOXL), QQQ(TQQQ), TSLA(TSLL) 데이터 함께 제공
- 변동성 드래그 고려: 장기 보유 시 복리 효과에 의한 괴리 발생

### 5.4 비상 시나리오

| 상황 | 대응 | 복구 후 |
|------|------|--------|
| API 연결 오류 | 3회 재시도 → 실패 시 알림, 신규 주문 중단 | 포지션 확인 후 재개 |
| MDD 초과 | 전체 청산, 시스템 정지 | 모델 재학습 + 검증 후 재시작 |
| 모델 성능 저하 | 규칙 기반으로 폴백 | 모델 재학습 후 재검증 |
| 시장 급락/서킷브레이커 | 전체 청산 + 시스템 정지 | 시장 안정 후 수동 재개 |
| 거래소 점검 | 자동 감지 → 대기 | 점검 종료 후 자동 재개 |

---

## 6. 기술 스택

| 영역 | 라이브러리 | 용도 |
|------|-----------|------|
| **암호화폐 API** | pyupbit | 업비트 REST + WebSocket |
| **주식 API** | requests + KIS REST API | KIS 주문/시세 |
| **주식 실시간** | websockets + KIS WebSocket | 실시간 체결가/호가 |
| **해외 데이터** | yfinance | 해외 ETF 과거 OHLCV |
| **국내 데이터** | pykrx | 국내주식 과거 OHLCV |
| **데이터 처리** | pandas, numpy | 데이터 정제/변환 |
| **기술지표** | ta-lib 또는 ta (pure Python) | RSI, MACD, BB, ATR 등 |
| **DB** | SQLite → PostgreSQL | 초기 SQLite, 확장 시 전환 |
| **딥러닝** | PyTorch (MPS 백엔드) | LSTM, Transformer |
| **강화학습** | FinRL (Stable-Baselines3) | PPO/A2C/DDPG 에이전트 |
| **센티먼트** | FinBERT (transformers) | 금융 뉴스 분석 |
| **스케줄러** | APScheduler | 정기 실행, 장 시간 대응 |
| **알림** | python-telegram-bot | 성과 보고, 이상 알림 |
| **로깅** | loguru | 전체 시스템 로깅 |
| **설정** | PyYAML + python-dotenv | 설정 관리 |

### 환경 참고
- Python 3.11+ 권장
- Apple Silicon Mac에서 PyTorch MPS 백엔드 활용 가능 (GPU 학습 가속)
- ta-lib: `brew install ta-lib` 후 `pip install TA-Lib` (또는 pure Python `ta` 라이브러리 대체 가능)
- API 키는 .env 파일에 보관, .gitignore에 반드시 추가

---

## 7. 성과 측정 기준

### 7.1 핵심 KPI

| 지표 | 목표 | 설명 |
|------|------|------|
| 총 수익률 | Buy & Hold 대비 우수 | 단순 보유 대비 초과 수익 |
| Sharpe Ratio | ≥ 1.0 (연환산) | 위험 대비 수익. 1.0+ 양호 |
| MDD | ≤ -15% | 최대 드로다운 관리 |
| 승률 | ≥ 50% | 수익 거래 비율 |
| Profit Factor | ≥ 1.5 | 총이익/총손실 |

### 7.2 벤치마크

| 벤치마크 | 설명 |
|----------|------|
| Buy & Hold | 동일 기간 단순 보유 수익률 |
| 규칙 기반 전략 | Phase 1의 MA/RSI 전략 결과 |
| BTC Hold (암호화폐) | 비트코인 단순 보유 |
| SPY/QQQ (주식) | 시장 벤치마크 지수 |

### 7.3 백테스팅 주의사항 (필수 준수)

> 아래 항목은 López de Prado의 "Advances in Financial Machine Learning"에서 강조하는 핵심 사항이다. 위반 시 백테스팅 결과가 실전과 완전히 다를 수 있다.

- **Look-Ahead Bias 방지**: 미래 데이터가 학습/예측에 절대 누출되지 않도록 철저한 시간 순서 관리. 피처 계산 시에도 미래 데이터 참조 금지.
- **Overfitting 방지**: Walk-Forward 방식으로 학습 기간을 이동시키며 반복 검증. 단일 학습/테스트 분할 금지.
- **거래 비용 반영**: 수수료 + 슬리피지 + 환율(해외) 비용을 백테스팅에 반영. 비용 미반영 시 결과 왜곡.
- **Survivorship Bias**: 상장폐지 종목 포함 데이터로 테스트 (해외 ETF는 해당 없음, 암호화폐는 상장폐지 코인 주의).

---

## 8. 운영 시나리오

### 8.1 암호화폐 일일 운영 사이클

24시간 연속 운영. 모델 예측 주기에 따라 시그널 생성.

| 주기 | 작업 |
|------|------|
| **매 N시간** (설정) | 데이터 업데이트 → 모델 예측 → 시그널 생성 → 리스크 체크 → 주문 실행 |
| **매일 00:00 KST** | 일일 성과 정리, 로그 로테이션, 일일 보고서 발송 |
| **매주 월요일** | 주간 성과 리뷰, 모델 성능 드리프트 체크 |
| **매월 1일** | 월간 종합 보고서, 필요 시 모델 재학습 |

### 8.2 주식 일일 운영 사이클

| 시간 (KST) | 작업 |
|------------|------|
| 08:30 | 국내 장 준비: 데이터 업데이트, 모델 예측, 시그널 생성 |
| 09:00 | 국내 장 시작: 주문 실행 + 실시간 모니터링 |
| 15:30 | 국내 장 마감: 일일 성과 정리/로깅 |
| 22:00 | 해외 장 준비: 해외 데이터 업데이트, 모델 예측 |
| 23:30 | 해외 장 시작: ETF 매매 시그널 실행 (서머타임 22:30) |
| 06:00 | 해외 장 마감: 해외 성과 정리, 종합 일일 보고서 발송 |

---

## 9. 참고 자료

### 9.1 핵심 논문 (Claude Code 개발 시 참조)

아래 논문들은 각 Phase에서 모델 구현 시 참고해야 할 핵심 자료이다.

| 논문 | 저자/연도 | 핵심 내용 | 활용 Phase |
|------|----------|----------|-----------|
| Deep Learning for Financial Applications: A Survey | Ozbayoglu et al., 2020 | 금융 딥러닝 전반 서베이. 전체 지형도 파악에 최적 | 전체 |
| Temporal Fusion Transformers for Interpretable Multi-horizon Time Series Forecasting | Lim et al., 2021 | TFT 모델 원논문. 다중 시계열 + 피처 중요도 해석 가능 | Phase 3 |
| FinRL: A Deep Reinforcement Learning Library for Automated Stock Trading | Liu et al., 2020 | 강화학습 트레이딩 라이브러리. PPO/A2C/DDPG 앙상블 | Phase 3 |
| Deep Reinforcement Learning for Automated Stock Trading: An Ensemble Strategy | Yang et al., 2020 | FinRL 앙상블 전략 상세. 실전 적용 방법론 | Phase 3 |
| FinBERT: Financial Sentiment Analysis with Pre-trained Language Models | Araci, 2019 | 금융 텍스트 특화 BERT. 뉴스 센티먼트 분석 | Phase 3 |
| Attention Is All You Need | Vaswani et al., 2017 | Transformer 원논문. TFT의 기초 | Phase 3 |
| Stock Price Prediction Using LSTM, RNN and CNN-Sliding Window Model | Selvin et al., 2017 | LSTM 기반 주가 예측 기초 | Phase 2 |

### 9.2 핵심 서적

| 서적 | 저자 | 핵심 내용 | 활용 |
|------|------|----------|------|
| Advances in Financial Machine Learning | Marcos López de Prado | **백테스팅 함정 방지, 피처 중요도, 실전 노하우**. 반드시 참조 | 백테스팅 설계 |
| Machine Learning for Trading, 2nd Ed. | Stefan Jansen | 전체 파이프라인 실습서. 코드 제공 | 전체 구현 |
| 파이썬을 이용한 비트코인 자동매매 (개정판) | wikidocs.net/book/1665 | 업비트/빗썸/바이낸스 API 실습, pyupbit 활용법 | Phase 1 (암호화폐) |

### 9.3 개발 참고 링크

| 자료 | URL | 용도 |
|------|-----|------|
| 업비트 개발자 센터 | docs.upbit.com | 업비트 API 공식 문서 |
| pyupbit GitHub | github.com/sharebook-kr/pyupbit | 업비트 Python 래퍼 |
| KIS Developers | apiportal.koreainvestment.com | 한투 API 공식 문서 |
| KIS 공식 GitHub | github.com/koreainvestment/open-trading-api | 한투 샘플 코드 |
| python-kis (pykis) | github.com/Soju06/python-kis | 한투 Python 래퍼 |
| FinRL GitHub | github.com/AI4Finance-Foundation/FinRL | 강화학습 트레이딩 라이브러리 |
| KIS 튜토리얼 (wikidocs) | wikidocs.net/159296 | 한투 API 단계별 가이드 |

### 9.4 Claude Code 개발 지침

Claude Code에서 이 기획서를 참조하여 개발할 때 아래 사항을 준수한다:

1. **디렉토리 구조**: 섹션 2.3의 구조를 따른다.
2. **추상 클래스 패턴**: BaseCollector, BaseModel, BaseExecutor를 먼저 정의하고, 거래소별 구현을 상속으로 처리한다.
3. **타입 힌트**: 모든 함수에 타입 힌트를 적용한다.
4. **docstring**: Google 스타일 docstring을 사용한다.
5. **단위 테스트**: tests/ 디렉토리에 각 모듈별 테스트를 작성한다.
6. **설정 외부화**: 하드코딩 금지. 모든 파라미터는 settings.yaml에서 관리한다.
7. **로깅**: print() 대신 loguru logger를 사용한다.
8. **에러 핸들링**: API 호출 시 반드시 try/except + 재시도 로직을 포함한다.
9. **보안**: API 키는 .env 파일에서만 로드한다. 코드에 하드코딩 절대 금지.

---

## 10. 면책

본 기획서는 딥러닝 기반 자동매매 시스템의 기술적 설계를 위한 문서이며, 투자 조언을 제공하는 것이 아닙니다. 모든 투자 결정 및 손실에 대한 책임은 전적으로 투자자 본인에게 있습니다. 특히 레버리지 ETF와 암호화폐는 높은 변동성으로 인해 원금 손실 위험이 크므로 충분한 이해와 검증 후에 투자하시기 바랍니다.
