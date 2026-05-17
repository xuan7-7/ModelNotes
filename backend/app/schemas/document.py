from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


# ─── 请求体 ───

class DocumentCreate(BaseModel):
    title: str = ''
    content: str = ''
    tags: str = ''
    ai_notes: Optional[str] = None
    ai_mindmap: Optional[str] = None


class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[str] = None
    ai_notes: Optional[str] = None
    ai_mindmap: Optional[str] = None


class AITransformRequest(BaseModel):
    content: str = Field(..., description='Markdown 原文')


# ─── 响应体 ───

class DocumentOut(BaseModel):
    id: int
    title: str
    content: str
    tags: str
    ai_notes: Optional[str] = None
    ai_mindmap: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {'from_attributes': True}


class DocumentBrief(BaseModel):
    """列表用，不含全文"""
    id: int
    title: str
    tags: str
    ai_notes: Optional[str] = None
    created_at: datetime

    model_config = {'from_attributes': True}


class AITransformResponse(BaseModel):
    notes: str
    mindmap: str


class HeatmapItem(BaseModel):
    date: str
    count: int


class StatsOverview(BaseModel):
    streak_days: int
    total_assets: int
    month_ai_count: int
    ref_count: int
    heatmap: list[HeatmapItem]
