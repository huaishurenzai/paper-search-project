# Paper Search API

一个基于 FastAPI 的论文检索 API 项目，用于练习 Python 后端、HTTP、Git、pytest，并为后续 RAG / AI Agent 项目做准备。

## 当前功能

- 论文增删改查
- 按关键词搜索论文
- 搜索结果相关性打分
- 按匹配分数排序
- 返回命中字段 `matched_fields`
- JSON 文件持久化
- 自动生成论文 ID
- Pydantic 请求参数校验
- pytest 接口测试
- PDF 文本提取
- FastAPI 自动接口文档

## 项目结构

```text
paper_search_projects/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── storage.py
│   └── routers/
│       ├── __init__.py
│       └── papers.py
├── data/
│   └── papers.json
├── scripts/
│   ├── add_ids.py
│   └── extract_pdf_text.py
├── tests/
│   ├── conftest.py
│   ├── test_papers_api.py
│   └── test_pdf_extraction.py
├── requirements.txt
├── pytest.ini
└── readme.md