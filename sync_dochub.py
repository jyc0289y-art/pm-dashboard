#!/usr/bin/env python3
"""
sync_dochub.py — SL Corporation Portfolio DocHub 동기화 스크립트
실행: python3 sync_dochub.py
"""

import os, sys, json, shutil, re, subprocess
from datetime import datetime
from pathlib import Path

# ── 경로 설정 ──
HOME = Path.home()
CLOUD = HOME / "Library/Mobile Documents/com~apple~CloudDocs/developer"
DASH  = Path(__file__).parent
DOCS  = DASH / "docs"

GLOBAL_CLAUDE = HOME / ".claude/CLAUDE.md"
GLOBAL_INSTR  = HOME / ".claude/instructions"
GLOBAL_MODS   = HOME / ".claude/modules"

# 활성 프로젝트 세션 동기화 대상
SESSION_PROJECTS = {
    "P21_FEP":      CLOUD / "FEP",
    "P18_HighLink": CLOUD / "HighLink",
    "P12_HOBIS":    CLOUD / "hobis_cf252",
    "P10_Hodlum":   CLOUD / "Hodlum",
    "P16_CineLink": CLOUD / "CineLink",
}

# 프로젝트 문서 동기화 대상 (docs/{folder}/ 에 MD 파일 복사)
DOC_PROJECTS = {
    "P06_DLTrading":  CLOUD / "dl_trading",
    "P07_DWVA":       CLOUD / "dwva",
    "P08_ClaudeRemote": CLOUD / "Claude_remote",
    "P10_Hodlum":     CLOUD / "Hodlum",
    "P11_MarketLink": CLOUD / "marklink-sl",
    "P12_HOBIS":      CLOUD / "hobis_cf252",
    "P13_PhotoLink":  CLOUD / "PhotoLink",
    "P15_AOMORI":     CLOUD / "AOMORI",
    "P16_CineLink":   CLOUD / "CineLink",
    "P17_Flight":     CLOUD / "flight",
    "P18_HighLink":   CLOUD / "HighLink",
    "P21_FEP":        CLOUD / "FEP",
    "P22_FlashMOE":   CLOUD / "FlashMOE",
}

# 토큰/비밀 제거 패턴
SECRET_PATTERNS = [
    (r'hf_[A-Za-z0-9]{30,}', '[HF_TOKEN_REDACTED]'),
    (r'sk-[A-Za-z0-9]{30,}', '[OPENAI_KEY_REDACTED]'),
    (r'ghp_[A-Za-z0-9]{30,}', '[GITHUB_TOKEN_REDACTED]'),
]

def log(msg): print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def redact_secrets(text):
    for pattern, replacement in SECRET_PATTERNS:
        text = re.sub(pattern, replacement, text)
    return text

def file_ts(path):
    return datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d %H:%M")

def copy_file(src, dest):
    """파일 복사 + 시크릿 제거. 변경된 경우에만 복사."""
    src, dest = Path(src), Path(dest)
    if not src.exists(): return False
    dest.parent.mkdir(parents=True, exist_ok=True)
    text = src.read_text(encoding='utf-8', errors='replace')
    text = redact_secrets(text)
    if dest.exists() and dest.read_text(encoding='utf-8', errors='replace') == text:
        return False  # 변경 없음
    dest.write_text(text, encoding='utf-8')
    return True

def sync_global():
    """전역지침 + 모듈 동기화"""
    log("전역지침 동기화 중...")
    changed = 0
    if copy_file(GLOBAL_CLAUDE, DOCS / "_global/CLAUDE.md"): changed += 1
    for f in GLOBAL_INSTR.glob("*.md"):
        if copy_file(f, DOCS / "_global/instructions" / f.name): changed += 1
    for f in GLOBAL_MODS.glob("*.md"):
        if copy_file(f, DOCS / "_global/modules" / f.name): changed += 1
    log(f"  전역지침: {changed}개 변경")
    return changed

def sync_sessions():
    """세션 파일 + 프로젝트지침 동기화"""
    log("세션 파일 동기화 중...")
    total = 0
    for folder, proj_dir in SESSION_PROJECTS.items():
        changed = 0
        sess_dir = proj_dir / "memory/sessions"
        dest_dir = DOCS / "_sessions" / folder

        # 프로젝트 CLAUDE.md
        claude_md = proj_dir / ".claude/CLAUDE.md"
        if copy_file(claude_md, dest_dir / "CLAUDE.md"): changed += 1

        # 세션 파일 (registry + 최신 10개)
        if sess_dir.exists():
            sess_files = sorted(sess_dir.glob("*.md"))
            for f in [x for x in sess_files if 'registry' in x.name]:
                if copy_file(f, dest_dir / f.name): changed += 1
            recent = [x for x in sess_files if 'registry' not in x.name][-10:]
            for f in recent:
                if copy_file(f, dest_dir / f.name): changed += 1

        if changed: log(f"  {folder}: {changed}개 변경")
        total += changed
    log(f"  세션 총 {total}개 변경")
    return total

def sync_project_docs():
    """프로젝트 MD 문서 동기화 (타임스탬프 형식 파일명만)"""
    log("프로젝트 문서 동기화 중...")
    total = 0
    ts_pattern = re.compile(r'^\d{8}_\d{6}_')
    for folder, proj_dir in DOC_PROJECTS.items():
        if not proj_dir.exists(): continue
        dest_dir = DOCS / folder
        changed = 0
        for f in proj_dir.rglob("*.md"):
            if not ts_pattern.match(f.name): continue
            # docs/ 내부 파일 제외 (pm-dashboard 자체)
            if str(f).startswith(str(DASH)): continue
            if copy_file(f, dest_dir / f.name): changed += 1
        if changed: log(f"  {folder}: {changed}개 변경")
        total += changed
    log(f"  문서 총 {total}개 변경")
    return total

def build_index():
    """docs/_index.json 재생성"""
    log("_index.json 재생성 중...")

    # 프로젝트 메타
    proj_meta = {
        "P06_DLTrading":  ("P06","DL Trading","DL Trading System 자동매매","archived"),
        "P07_DWVA":       ("P07","DWVA","DWVA 보안 취약점 분석 시뮬레이터","archived"),
        "P08_ClaudeRemote":("P08","Claude Remote","텔레그램 봇 기반 원격 Claude 제어","archived"),
        "P10_Hodlum":     ("P10","Hodlum","Ludlum 3030-2 커스텀 로깅 S/W","active"),
        "P11_MarketLink": ("P11","MarketLink","시장 분석 서비스","archived"),
        "P12_HOBIS":      ("P12","HOBIS Cf-252","Cf-252 선량평가 계산기","active"),
        "P13_PhotoLink":  ("P13","PhotoLink","웹 사진 편집기","archived"),
        "P15_AOMORI":     ("P15","AOMORI","아오모리 현지인 여행 가이드","done"),
        "P16_CineLink":   ("P16","CineLink","AI 영상 제작 파이프라인","active"),
        "P17_Flight":     ("P17","Flight","항공권 종합 서비스","archived"),
        "P18_HighLink":   ("P18","HighLink","고속도로 AI 관제 시스템","active"),
        "P21_FEP":        ("P21","FEP","일상속 경험의 심리학 — 유튜브 채널","active"),
        "P22_FlashMOE":   ("P22","FlashMOE","SL Flash MOE 전략","active"),
    }

    projects = []
    for folder, (pnum, name, desc, status) in proj_meta.items():
        d = DOCS / folder
        docs = []
        if d.exists():
            for f in sorted(d.glob("*.md"), key=lambda x: x.name, reverse=True):
                docs.append({
                    "ts": file_ts(f),
                    "title": f.stem.replace('_',' ').strip(),
                    "file": f"{folder}/{f.name}",
                    "tags": []
                })
        projects.append({"id":folder,"p_num":pnum,"name":name,"desc":desc,"status":status,"docs":docs})

    # 세션 기록
    sess_docs = []
    sess_dir = DOCS / "sessions"
    if sess_dir.exists():
        for f in sorted(sess_dir.glob("*.md"), reverse=True):
            sess_docs.append({"ts":file_ts(f),"title":f.stem,"file":f"sessions/{f.name}","tags":["세션"]})
    projects.append({"id":"sessions","p_num":"SYS","name":"세션 기록","desc":"브리핑 채팅창 작업 세션 기록","status":"active","docs":sess_docs})

    # 전역 지침
    global_files = []
    gm = DOCS / "_global/CLAUDE.md"
    if gm.exists():
        global_files.append({"ts":file_ts(gm),"title":"전역 지침 (CLAUDE.md)","file":"_global/CLAUDE.md","tags":["전역지침"]})
    instr_titles = {
        "session_fork.md":"세션 포크 시스템","worker_rules.md":"Worker LLM 규칙",
        "tool_optimization.md":"도구 최적화","brand_info.md":"SL 브랜드 정보",
        "realtime_data.md":"실시간 데이터 파이프라인","autonomous_dev.md":"자율개발모드 규칙",
        "fork_cleanup_guide.md":"세션 정리 가이드",
    }
    for f in sorted((DOCS/"_global/instructions").glob("*.md")):
        global_files.append({"ts":file_ts(f),"title":instr_titles.get(f.name,f.stem),"file":f"_global/instructions/{f.name}","tags":["지침모듈"]})

    module_files = []
    mod_titles = {
        "_index.md":"MOD 레지스트리","MOD-001_goodnotes.md":"MOD-001 GoodNotes 필기 오버레이",
        "MOD-002_stroke_recognizer.md":"MOD-002 획 인식기","MOD-003_markdown_renderer.md":"MOD-003 마크다운 렌더러",
    }
    for f in sorted((DOCS/"_global/modules").glob("*.md")):
        module_files.append({"ts":file_ts(f),"title":mod_titles.get(f.name,f.stem),"file":f"_global/modules/{f.name}","tags":["MOD"]})

    # 세션 메타
    sess_meta = {
        "P21_FEP":{"p_num":"P21","name":"FEP"},
        "P18_HighLink":{"p_num":"P18","name":"HighLink"},
        "P12_HOBIS":{"p_num":"P12","name":"HOBIS"},
        "P10_Hodlum":{"p_num":"P10","name":"Hodlum"},
        "P16_CineLink":{"p_num":"P16","name":"CineLink"},
    }
    sessions_map = {}
    for folder, meta in sess_meta.items():
        d = DOCS / "_sessions" / folder
        if not d.exists(): continue
        files = []
        for f in sorted(d.glob("*.md"), reverse=True):
            tag = "프로젝트지침" if f.name=="CLAUDE.md" else ("레지스트리" if "registry" in f.name else ("진행" if "progress" in f.name else "세션지침"))
            title = f"{meta['p_num']} {meta['name']} 프로젝트지침 (CLAUDE.md)" if f.name=="CLAUDE.md" else f.stem
            files.append({"ts":file_ts(f),"title":title,"file":f"_sessions/{folder}/{f.name}","tags":[tag]})
        sessions_map[folder] = {**meta, "docs":files}

    data = {
        "last_updated": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "projects": projects,
        "instructions": {"global":global_files,"modules":module_files,"sessions":sessions_map}
    }
    (DOCS/"_index.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    log(f"  _index.json 재생성 완료 ({len(projects)}개 프로젝트)")
    return data

def update_html_data(data):
    """index.html의 DATA 상수 업데이트"""
    log("index.html DATA 업데이트 중...")
    html_path = DASH / "index.html"
    html = html_path.read_text(encoding='utf-8')
    compact = json.dumps(data, ensure_ascii=False, separators=(',',':'))
    # DATA = {...}; 패턴 교체
    new_html = re.sub(
        r'const DATA = \{.*?\};',
        f'const DATA = {compact};',
        html, flags=re.DOTALL
    )
    if new_html == html:
        log("  HTML 변경 없음")
        return False
    html_path.write_text(new_html, encoding='utf-8')
    log("  index.html 업데이트 완료")
    return True

def git_commit_push(changed_count):
    """변경사항 커밋 + 푸시"""
    log("Git 커밋 + 푸시 중...")
    os.chdir(DASH)
    subprocess.run(["git","add","-A"], check=True)
    result = subprocess.run(["git","diff","--cached","--quiet"])
    if result.returncode == 0:
        log("  커밋할 변경사항 없음")
        return
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    msg = f"sync: DocHub 자동 동기화 {ts} ({changed_count}개 파일 변경)"
    subprocess.run(["git","commit","-m",msg], check=True)
    subprocess.run(["git","push","origin","main"], check=True)
    log("  푸시 완료")

def main():
    print("=" * 50)
    print("SL Portfolio DocHub 동기화")
    print(f"시작: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    c1 = sync_global()
    c2 = sync_sessions()
    c3 = sync_project_docs()
    total = c1 + c2 + c3

    data = build_index()
    update_html_data(data)
    git_commit_push(total)

    print("=" * 50)
    print(f"완료: {datetime.now().strftime('%H:%M:%S')} | 변경 {total}개")
    print("https://jyc0289y-art.github.io/pm-dashboard/")
    print("=" * 50)

if __name__ == "__main__":
    main()
