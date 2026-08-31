# DingTalk Office Agent

基于 Python、FastAPI、LangChain、OpenAI API 与钉钉 Stream 机器人构建的办公自动化助手。

项目支持在钉钉群内通过自然语言查询公告、本人报销单和本地待办，并支持创建、完成待办；通过钉钉发送者身份映射与请求级上下文隔离，限制用户只能访问自己的个人数据。

## 核心功能

- 公告检索：根据关键词查询本地公告数据。
- 本人报销查询：查询当前员工的报销单及状态。
- 待办管理：查询、新增、完成本人待办事项。
- 钉钉群交互：通过钉钉企业内部应用与 Stream 机器人接收群消息并返回结果。
- 身份隔离：将钉钉 `sender_id` 映射为内部员工身份，待办和报销查询均按当前身份过滤。
- 自动化测试：已覆盖身份上下文、未授权访问、数据隔离与钉钉映射等 9 项 pytest 测试。

## 项目架构

```text
钉钉群消息
    ↓
DingTalk Stream Robot
    ↓
app/dingtalk_bot.py
    ↓
LangChain Agent + OpenAI API
    ↓
公告 / 报销 / 待办 Tools
    ↓
SQLAlchemy + SQLite
```

## 技术栈

- Python 3.13
- FastAPI / Uvicorn
- LangChain / langchain-openai
- OpenAI API
- DingTalk Stream SDK
- SQLAlchemy / SQLite
- pytest
- ContextVar

## 项目结构

```text
.
├── app/
│   ├── agent.py              # Agent、模型与工具注册
│   ├── database.py           # SQLite 数据模型与数据访问函数
│   ├── dingtalk_bot.py       # 钉钉 Stream 机器人入口
│   ├── main.py               # FastAPI 本地调试接口
│   ├── user_context.py       # 请求级员工身份上下文
│   └── tools/
│       ├── announcements.py  # 公告查询工具
│       ├── expenses.py       # 本人报销查询工具
│       └── todos.py          # 本人待办查询、创建、完成工具
├── tests/                    # pytest 自动化测试
├── .env.example              # 环境变量模板
├── .gitignore
├── requirements.txt
└── README.md
```

## 本地启动

### 1. 创建虚拟环境并安装依赖

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
```

随后编辑 `.env`，填写自己的 OpenAI API Key、钉钉应用凭证和身份映射。

> 不要提交 `.env`、数据库文件或真实的钉钉用户标识。

### 3. 启动 FastAPI 本地服务

```bash
uvicorn app.main:app --reload
```

本地接口文档地址：

```text
http://127.0.0.1:8000/docs
```

### 4. 启动钉钉 Stream 机器人

在另一个终端中执行：

```bash
source .venv/bin/activate
python -m app.dingtalk_bot
```

当终端显示 Stream 连接成功后，即可在已添加机器人的钉钉群内 @机器人发送消息。

## 自动化测试

运行全部测试：

```bash
python -m pytest -q
```
测试会自动创建独立临时 SQLite 数据库，不读取或修改本地演示数据库 `office_agent.db`。

当前已覆盖：

- 身份上下文设置、嵌套与清理；
- 无身份访问拦截；
- 待办和报销的数据隔离；
- 钉钉发送者身份映射、未知账号与错误配置拦截。

## 数据与安全边界

- 当前公告、报销和待办数据保存在本地 SQLite，属于演示数据。
- 当前身份映射使用 `.env` 中的本地白名单配置。
- 项目尚未接入真实钉钉待办 API 或真实企业业务数据库。
- API Key、钉钉 Secret、真实用户标识和本地数据库均不应上传至 GitHub。

## 后续计划

- 使用临时 SQLite 数据库完善集成测试。
- 增加请求审计日志、工具调用成功率与响应耗时监控。
- 在取得最小必要权限后接入真实钉钉待办或业务系统 API。
- 将本地白名单身份映射升级为企业统一身份服务。

