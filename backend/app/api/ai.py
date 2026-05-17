from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.document import Document
from app.schemas.document import AITransformRequest, AITransformResponse, DocumentOut
from app.services.ai_service import ai_transform

router = APIRouter(prefix='/api', tags=['ai'])


@router.post('/ai/transform', response_model=AITransformResponse)
async def transform(body: AITransformRequest):
    """对 Markdown 内容执行 AI 转化，返回笔记 + 思维导图"""
    try:
        result = await ai_transform(body.content)
        return AITransformResponse(**result)
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.post('/ai/transform/{doc_id}', response_model=DocumentOut)
async def transform_and_save(doc_id: int, db: Session = Depends(get_db)):
    """对已保存的文档执行 AI 转化，结果写入数据库"""
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail='文档不存在')

    try:
        result = await ai_transform(doc.content)
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))

    doc.ai_notes = result['notes']
    doc.ai_mindmap = result['mindmap']
    db.commit()
    db.refresh(doc)
    return doc
