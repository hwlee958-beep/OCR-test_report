"""문서 index.html 생성기. 마크다운 원문을 HTML에 그대로 embed 하여 file:// 에서도 동작."""
import json, pathlib, datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent

DOCS = [
    ("rules",  "PASS/FAIL 판정 규정", "module_1", "module_1/docs/pass-fail-rules.md"),
    ("prd",    "OCR 판정 도구 PRD",   "Module_2", "Module_2/docs/prd/ocr-pass-fail-prd.md"),
    ("task1",  "task-001 스캐폴드·UI", "Module_2", "Module_2/spec/task-001.md"),
    ("task2",  "task-002 추출·판정·보고서", "Module_2", "Module_2/spec/task-002.md"),
]
LINKS = [("PRD 디자인 시안", "Module_2/docs/prd-view.html", "별도 페이지로 열기")]

TEMPLATE = pathlib.Path(__file__).with_name("site_template.html").read_text(encoding="utf-8")


def embed(value) -> str:
    """script 태그 안에 안전하게 넣을 JSON. 엔티티는 script 내부에서 해석되지 않으므로
    HTML escape 대신 JSON 이스케이프(\u003c)로 </script> 조기 종료만 차단한다."""
    return json.dumps(value, ensure_ascii=False).replace("<", "\u003c")


def main() -> None:
    docs = []
    for key, title, group, rel in DOCS:
        path = ROOT / rel
        docs.append({
            "key": key, "title": title, "group": group, "path": rel,
            "text": path.read_text(encoding="utf-8"),
        })
    out = TEMPLATE.replace("__DOCS_JSON__", embed(docs))
    out = out.replace("__LINKS_JSON__", embed(LINKS))
    out = out.replace("__BUILT_AT__", datetime.date.today().isoformat())
    (ROOT / "index.html").write_text(out, encoding="utf-8")
    print(f"index.html generated ({len(docs)} docs)")


if __name__ == "__main__":
    main()
