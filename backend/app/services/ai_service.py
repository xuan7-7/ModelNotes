import os
import json
import traceback
import httpx
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY', '')
DEEPSEEK_BASE_URL = 'https://api.deepseek.com/v1'

SYSTEM_PROMPT = """你是一个知识整理专家。用户给你一段 Markdown 文档，你需要：
1. 提炼为结构化的知识笔记（Markdown 格式，含分级标题、要点列表、关键概念加粗）
2. 生成一个思维导图的 Markdown 列表结构（纯列表，用于 markmap 渲染）

严格按以下 JSON 格式输出，不要加额外说明：
{
  "notes": "## 知识笔记\\n\\n### 要点一\\n...",
  "mindmap": "- 主题\\n  - 子节点1\\n  - 子节点2\\n    - 孙节点"
}"""


async def ai_transform(content: str) -> dict:
    """调用 DeepSeek API，将 Markdown 转化为结构化笔记 + 思维导图"""

    if not DEEPSEEK_API_KEY:
        return fallback_transform(content)

    try:
        async with httpx.AsyncClient(timeout=60) as client:
            resp = await client.post(
                f'{DEEPSEEK_BASE_URL}/chat/completions',
                headers={
                    'Authorization': f'Bearer {DEEPSEEK_API_KEY}',
                    'Content-Type': 'application/json',
                },
                json={
                    'model': 'deepseek-chat',
                    'messages': [
                        {'role': 'system', 'content': SYSTEM_PROMPT},
                        {'role': 'user', 'content': content},
                    ],
                    'temperature': 0.3,
                    'max_tokens': 4096,
                },
            )
            resp.raise_for_status()
            data = resp.json()
            raw = data['choices'][0]['message']['content']
    except Exception as e:
        traceback.print_exc()
        raise RuntimeError(f'DeepSeek API 调用失败: {e}')

    # 解析 AI 返回的 JSON
    try:
        if '```json' in raw:
            raw = raw.split('```json')[1].split('```')[0]
        elif '```' in raw:
            raw = raw.split('```')[1].split('```')[0]
        result = json.loads(raw.strip())
        return {
            'notes': result.get('notes', ''),
            'mindmap': result.get('mindmap', ''),
        }
    except (json.JSONDecodeError, KeyError) as e:
        print(f'AI 返回 JSON 解析失败，使用 fallback。raw: {raw[:300]}')
        return fallback_transform(content)


def fallback_transform(content: str) -> dict:
    """无 API key 或解析失败时的简单规则转换"""
    lines = [l.strip() for l in content.split('\n') if l.strip()]
    if not lines:
        return {'notes': '', 'mindmap': ''}

    root = lines[0].lstrip('#').strip()
    notes_parts = [f'## {root}\n']
    mindmap_parts = [f'- {root}']

    for line in lines[1:12]:
        clean = line.lstrip('#').strip()
        notes_parts.append(f'- **{clean}**')
        mindmap_parts.append(f'  - {clean}')

    return {
        'notes': '\n'.join(notes_parts),
        'mindmap': '\n'.join(mindmap_parts),
    }
