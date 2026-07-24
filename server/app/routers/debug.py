"""调试页面 - 直接显示流水数据，不依赖前端 JS"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["调试"])


@router.get("/debug/{book_id}", response_class=HTMLResponse)
def debug_book(request: Request, book_id: str):
    """直接显示流水数据"""
    from app.models.database import SessionLocal
    from app.models.models import Flow, Book
    db = SessionLocal()
    book = db.query(Book).filter(Book.book_id == book_id).first()
    flows = db.query(Flow).filter(Flow.book_id == book_id).order_by(Flow.day.desc()).limit(50).all()
    db.close()

    if not book:
        return "<h2>账本不存在</h2>"

    rows = ""
    for f in flows:
        rows += f"<tr><td>{f.day}</td><td>{f.flow_type}</td><td>{f.industry_type}</td><td>¥{f.money:.2f}</td><td>{f.name or ''}</td></tr>"

    total = sum(f.money or 0 for f in flows)

    html = f"""<html><head><meta charset="utf-8">
    <title>Debug - {book.book_name}</title>
    <style>
    body {{ font-family: sans-serif; padding: 20px; background: #0f172a; color: #f1f5f9; }}
    table {{ border-collapse: collapse; width: 100%; }}
    th, td {{ padding: 8px 12px; text-align: left; border-bottom: 1px solid #334155; }}
    .total {{ font-size: 24px; margin: 20px 0; color: #34d399; }}
    </style></head><body>
    <h1>{book.book_name}</h1>
    <div class="total">共 {len(flows)} 条流水，合计 ¥{total:.2f}</div>
    <table><tr><th>日期</th><th>类型</th><th>分类</th><th>金额</th><th>名称</th></tr>
    {rows}</table></body></html>"""
    return html
