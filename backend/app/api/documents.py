from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db import get_db
from app.models.document import Document
from app.schemas.document import (
    DocumentCreate,
    DocumentUpdate,
    DocumentOut,
    DocumentBrief,
    HeatmapItem,
    StatsOverview,
)

router = APIRouter(prefix='/api', tags=['documents'])


# ─── 创建文档 ───

@router.post('/documents', response_model=DocumentOut, status_code=201)
def create_doc(body: DocumentCreate, db: Session = Depends(get_db)):
    doc = Document(**body.model_dump())
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


# ─── 文档列表（分页） ───

@router.get('/documents', response_model=list[DocumentBrief])
def list_docs(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str = Query(None, description='按标题和标签搜索'),
    db: Session = Depends(get_db),
):
    q = db.query(Document)
    if search:
        like = f'%{search}%'
        q = q.filter(
            Document.title.like(like) | Document.tags.like(like)
        )
    offset = (page - 1) * page_size
    docs = (
        q.order_by(Document.created_at.desc())
        .offset(offset)
        .limit(page_size)
        .all()
    )
    return docs


# ─── 文档详情 ───

@router.get('/documents/{doc_id}', response_model=DocumentOut)
def get_doc(doc_id: int, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail='文档不存在')
    return doc


# ─── 更新文档 ───

@router.put('/documents/{doc_id}', response_model=DocumentOut)
def update_doc(doc_id: int, body: DocumentUpdate, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail='文档不存在')
    update_data = body.model_dump(exclude_unset=True)
    for key, val in update_data.items():
        setattr(doc, key, val)
    db.commit()
    db.refresh(doc)
    return doc


# ─── 删除文档 ───

@router.delete('/documents/{doc_id}', status_code=204)
def delete_doc(doc_id: int, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail='文档不存在')
    db.delete(doc)
    db.commit()


# ─── 批量删除 ───

@router.post('/documents/batch-delete', status_code=204)
def batch_delete(ids: list[int], db: Session = Depends(get_db)):
    db.query(Document).filter(Document.id.in_(ids)).delete(synchronize_session=False)
    db.commit()


# ─── 统计概览 ───

@router.get('/stats/overview', response_model=StatsOverview)
def get_stats(month: str = Query(None), db: Session = Depends(get_db)):
    from datetime import date

    today = date.today()
    month_prefix = month or today.strftime('%Y-%m')

    # 热力图数据：指定月份每天文档数
    rows = (
        db.query(
            func.date(Document.created_at).label('date'),
            func.count(Document.id).label('count'),
        )
        .filter(func.date_format(Document.created_at, '%Y-%m') == month_prefix)
        .group_by(func.date(Document.created_at))
        .all()
    )
    heatmap = [HeatmapItem(date=str(r.date), count=r.count) for r in rows]

    # 总资产数
    total = db.query(func.count(Document.id)).scalar() or 0

    # 本月 AI 转化数
    month_ai = (
        db.query(func.count(Document.id))
        .filter(
            func.date_format(Document.created_at, '%Y-%m') == month_prefix,
            Document.ai_notes.isnot(None),
        )
        .scalar() or 0
    )

    # 连续打卡天数
    streak = 0
    check = today
    while True:
        ds = check.isoformat()
        cnt = (
            db.query(func.count(Document.id))
            .filter(func.date(Document.created_at) == ds)
            .scalar() or 0
        )
        if cnt > 0:
            streak += 1
            check = check.replace(day=check.day - 1) if check.day > 1 else (
                check.replace(month=check.month - 1, day=28) if check.month > 1 else check
            )
        else:
            break

    return StatsOverview(
        streak_days=streak,
        total_assets=total,
        month_ai_count=month_ai,
        ref_count=0,
        heatmap=heatmap,
    )
