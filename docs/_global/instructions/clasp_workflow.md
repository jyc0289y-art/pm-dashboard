# Google Apps Script 작업 표준 워크플로 — clasp 기반

> **수립**: 2026-05-13 (P31 HJ Safety Sheet 작업 중 도출)
> **로드 조건**: Google Sheets·Docs·Forms·Slides 의 Apps Script 코드 작성·수정·배포 작업이 발생하는 모든 세션
> **핵심 원칙**: **메뉴 클릭·복사 붙여넣기 자동화 금지. clasp 우선.**

## 왜 clasp인가

P31 작업 초반 4시간 동안 다음 비효율이 누적되어 사용자 작업까지 방해:

| 비효율 | 시간 비용 |
|---|---|
| Apps Script 편집기 열기 → Cmd+A → 1500줄 붙여넣기 → 저장 | 매번 2~3분 |
| Chrome MCP로 메뉴 자동 클릭 | 시스템 차단·클립보드 점유 위험 |
| 단일 함수 실행 시 5~80초 대기 후 확인 클릭 | 사이클당 5분 |
| 코드 수정 → 같은 사이클 반복 | 누적 1시간+ |

**clasp 도입 후**: 디스크 `.gs` 수정 → `clasp push` 한 줄 → 1초. 사용자 시트 새로고침만.

## 첫 작업 시 초기 셋업 (1회, 5분)

```bash
# 1. clasp 전역 설치 (Node.js 필요)
npm install -g @google/clasp

# 2. Google 계정 로그인 (사용자 직접 — OAuth)
clasp login    # 브라우저 자동 열림 → Google 계정 선택 → 허용
```

⚠️ **`clasp login`은 시스템이 OAuth 자격증명 획득으로 분류해 Claude의 자동 실행을 차단.** 사용자에게 직접 터미널 실행을 안내.

⚠️ **Apps Script API 활성화 필요** — 첫 `clasp push` 시 "User has not enabled the Apps Script API" 에러 발생. 사용자가 https://script.google.com/home/usersettings 에서 토글 켜야 함. **로그인한 계정과 다른 계정에서 켜면 작동 안 함** — 정확히 같은 계정 확인 필수.

## 프로젝트 연결 (시트당 1회)

```bash
cd <project-dir>/scripts/clasp_project    # 깨끗한 디렉토리
cat > .clasp.json <<EOF
{
  "scriptId": "<Apps Script 프로젝트 ID — script.google.com/.../projects/<여기>/edit>",
  "rootDir": "<절대 경로>"
}
EOF
clasp pull    # 기존 시트의 모든 .gs/.html을 로컬로 가져옴
```

⚠️ **rootDir에는 push할 파일만 두기.** 다른 .gs 파일이 있으면 같이 push됨. 일반 작업용 디스크는 별도 디렉토리.

## 일상 워크플로

```bash
# 디스크 .gs 파일 수정 후
clasp push           # 변경분만 푸시
# 또는 manifest 변경 시
clasp push -f        # force (덮어쓰기 확인 스킵)
```

푸시 후 **시트 새로고침** (Cmd+R) 한 번이면 새 코드 실행. 사용자 메뉴 클릭 1회씩 불필요.

## 함수 자동 실행 (메뉴 클릭 없이)

`clasp run`은 API executable 배포 + Standard GCP 프로젝트 연결이 필요해서 회사 도메인에서는 자주 막힘 ("Only users in the same domain as the script owner may deploy"). 권장 대안:

### 패턴 1 — onOpen 1회용 자동 실행 (가장 깔끔)

```javascript
function p31_installMenu() {   // 또는 onOpen
  // ... 메뉴 코드 ...

  // 1회용 마이그레이션·정리 작업
  try { p31_runOnOpenTasks(); } catch (e) { Logger.log(e.message); }
}

function p31_runOnOpenTasks() {
  const props = PropertiesService.getDocumentProperties();

  // v1: 작업 키마다 플래그 — 한 번만 실행됨
  if (props.getProperty('p31_cleanup_v1') !== 'DONE') {
    try {
      p31_doSomethingOnce_silent();   // 알림 없는 버전
      props.setProperty('p31_cleanup_v1', 'DONE');
    } catch (e) { Logger.log(e.message); }
  }
}
```

- `clasp push` → 사용자 시트 새로고침 → onOpen 발동 → 자동 실행 → 플래그 저장 → 다음 새로고침엔 실행 안 됨.
- **알림창(SpreadsheetApp.getUi().alert) 사용 금지** — onOpen 컨텍스트에서 UI 호출하면 매번 팝업 떠 사용자 짜증.

### 패턴 2 — 시간 트리거 + 자가 삭제

```javascript
function p31_scheduleOneTimeJob() {
  ScriptApp.newTrigger('p31_doJobAndDelete')
    .timeBased()
    .after(5 * 1000)
    .create();
}

function p31_doJobAndDelete() {
  // 작업
  // 자기 자신 트리거 제거
  ScriptApp.getProjectTriggers().forEach(t => {
    if (t.getHandlerFunction() === 'p31_doJobAndDelete') ScriptApp.deleteTrigger(t);
  });
}
```

## 사용자 기존 코드와 공존

사용자 시트에 이미 Apps Script가 있으면 `clasp pull`로 가져온 뒤 함께 push. **함수 이름·상수에 프로젝트 접두어** 필수 (예: `p31_`, `P31_CONFIG`). 같은 이름의 함수가 여러 파일에 있으면 마지막 정의가 우선되어 기존 메뉴가 사라지는 사고 발생.

## 코드 작성 시 주의

- **블록 주석 안에 `*/` 금지** (TRAP-001) — `M_*/F_*/V_*` 같은 텍스트가 주석 안에 있으면 주석이 거기서 종료되고 뒤가 코드로 해석됨.
- **OAuth scope은 appsscript.json 명시** — clasp run·webapp·executionApi 등을 쓸 거면 미리 명시. 추가 시 사용자 재인증 필요.
- **사용자 도메인 가정 검증** (TRAP-002) — "5년 만료/갱신/임박" 같은 비즈니스 규칙은 분야마다 다름. 코드화 전 사용자 명시 확인.

## 도메인 mismatch 회피 (TRAP-005)

사용자 시트 owner와 Apps Script 실행 계정이 **다른 도메인(@개인 vs @회사)** 인 경우 `HtmlService Modal Dialog → google.script.run` 통신이 `PERMISSION_DENIED: 스토리지에서 읽는 중`으로 차단된다. 함수 본체 진입 전이라 try-catch 못 잡음.

### 진단 기준
- 디버그 step 로그가 전혀 출력 안 됨 → 함수 호출 전 차단 (도메인 격리)
- step 로그 일부 출력 후 에러 → 함수 내부 권한 문제 (시트 보호, 데이터 검증 권한 등)

### 우회 패턴 (다이얼로그·base64 통신 없이)

#### A. Drive 폴더 방식 (가장 깔끔, 권장)
```javascript
function loadCsvFromDrive() {
  const folder = DriveApp.getFoldersByName('내폴더이름').next();
  let latest = null, latestTime = 0;
  const files = folder.getFiles();
  while (files.hasNext()) {
    const f = files.next();
    if (f.getName().indexOf('회사홈페이지_member') >= 0) {
      const t = f.getLastUpdated().getTime();
      if (t > latestTime) { latest = f; latestTime = t; }
    }
  }
  const text = latest.getBlob().getDataAsString('EUC-KR');
  // ... CSV 파싱 + 시트 적용
}
```
사용자는 평소처럼 Drive 폴더에 CSV만 업로드. 메뉴 한 번 클릭으로 자동 처리.

#### B. 시트 셀에 임시 데이터 + 함수 호출
사용자가 데이터를 특정 셀에 붙여넣기 → 함수가 그 셀 읽어서 처리.

#### C. UrlFetchApp (외부 API)
공개된 데이터면 직접 fetch.

### 권장 우선순위
1. **Drive 폴더 방식 우선** — 첫 코드부터 이 방식으로 작성
2. HTML Modal Dialog는 도메인 같을 때만 안전
3. 다이얼로그가 꼭 필요하면 도메인 일치 확인 후 사용

## 사용자 안내 시 주의

- **"파일 끝에 추가" 시** Cmd+End → 마지막 줄 → 새 줄에 붙여넣기 명시. Cmd+A → Cmd+V는 통째 교체일 때만 (TRAP-003).
- clasp push 후 시트 새로고침을 명확히 요청.
- 코드를 채팅에 다시 붙여 넣지 말고 `clasp push` 한 줄 메시지로 끝낼 것.

## 메모리에서 빠르게 참조할 키워드

`clasp`, `Apps Script`, `Google Sheets 자동화`, `구글 시트 코드`, `Spreadsheet onOpen`, `PropertiesService 멱등`, `manifest oauthScopes`.

## GAS 함정 4종 (P10 실증, 2026-08-20 — 상세: P10 `docs/production_lessons.md` TRAP-018)

| # | 함정 | 예방 |
|---|------|------|
| 1 | **HtmlService 는 서빙 시 HTML 주석을 제거** | 주석을 구분자·마커로 쓰지 말 것. 구조가 필요한 텍스트는 `.gs` 에 JS 문자열로 내장 |
| 2 | **onOpen = 단순 트리거** — 권한 필요 호출(시트 쓰기·PropertiesService) 즉시 거부 | onOpen 은 메뉴 생성만. 초기화·마이그레이션은 메뉴 클릭 이후로 (본 문서의 «onOpen 1회용 자동 실행» 패턴은 **승인이 끝난 스크립트 전제** — 신규 스크립트에 쓰면 PERMISSION_DENIED) |
| 3 | **다중 계정 로그인 → 대화상자의 google.script.run 통째 차단** ("스토리지에서 읽는 중 PERMISSION_DENIED") | 화면을 열 때 서버가 데이터를 실어 보내고(첫 화면 서버 호출 0회), 저장·생성은 화면 자체 폴백. 확정 진단 = 시크릿 창 재시험 |
| 4 | **getService().getUrl() 이 엉뚱한 배포를 가리킬 수 있음** + 워크스페이스는 `/a/macros/{도메인}/s/…` 형식만 열림 | 배포 ID 를 빌드 시 코드에 주입해 주소를 직접 조립. `clasp push` 만으로는 웹앱 미갱신 — push+`update-deployment` 를 스크립트로 묶을 것 |
