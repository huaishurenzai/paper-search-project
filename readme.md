# Paper Search Project

一个用于练习 Python、Git、HTTP，并逐步扩展到 RAG / Agent 的论文检索项目。

## 当前功能

- 添加论文
- 查看论文
- 关键词搜索论文
- JSON 文件保存和读取

## HTTP 接口设计草稿

未来计划将论文检索项目改造成 FastAPI 接口：

- GET /papers：获取所有论文
- POST /papers：新增论文
- GET /papers/search?keyword=xxx：搜索论文
- PUT /papers/{id}：修改论文
- DELETE /papers/{id}：删除论文