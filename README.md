# 智扫通 · 扫地机器人智能客服系统

基于 **RAG + ReAct** 架构的专业扫地机器人智能客服系统，支持多轮对话、知识检索、天气适配与个性化使用报告生成。

## ✨ 功能特点

### 🤖 智能客服核心
- **RAG向量知识库**：内置2000+条专业问答，覆盖故障排查、使用技巧、维护保养、选购指南
- **ReAct自主工具调用**：自动判断需求并调用对应工具，无需人工干预
- **多轮对话**：支持上下文理解，连续追问式解答
- **流式输出**：实时生成回复，提升用户体验

### 🛠️ 内置工具集
- **天气查询**：自动获取用户所在城市天气，判断是否适合扫地
- **用户身份识别**：自动获取用户ID、所在城市、当前月份
- **个性化报告**：生成指定月份的机器人使用情况报告与保养建议
- **知识库管理**：支持上传文档、重建向量索引，动态扩展知识库

### 📊 报告生成
- 自动获取用户使用记录
- 分析清洁效率、耗材状态、使用对比
- 提供针对性的保养建议
- 支持Markdown格式报告导出

### 📚 知识库管理
- 支持TXT、PDF格式文档上传
- 自动文档分片与向量索引
- MD5去重，仅索引新增或变更文件
- 可视化索引状态与文档列表

## 🚀 技术栈

| 模块 | 技术选型 |
|------|----------|
| 前端界面 | Streamlit 1.30+ |
| 大模型 | 通义千问(Qwen) |
| 向量数据库 | Chroma |
| 框架 | LangChain 0.2+ |
| 嵌入模型 | DashScopeEmbeddings |
| 日志 | Python logging |
| 配置 | YAML |

<img width="1861" height="858" alt="image" src="https://github.com/user-attachments/assets/a5e358c7-e1a3-46ba-b79f-77c3b342a565" />

## 📦 快速开始

### 1. 环境准备
- Python 3.10+
- 通义千问API密钥（https://dashscope.aliyun.com）

### 2. 安装依赖
```bash
git clone https://github.com/你的用户名/sweeper-robot-agent.git
cd sweeper-robot-agent
pip install -r requirements.txt
```

### 3. 配置API密钥
在 `config/rag.yml` 中添加你的通义千问API密钥：
```yaml
chat_model_name: qwen-turbo
embedding_model_name: text-embedding-v2
api_key: 你的API密钥
```

### 4. 初始化知识库
```bash
# 首次运行会自动加载data目录下的文档
# 或在知识库管理页面点击"重建/增量索引"
```

### 5. 启动应用
```bash
streamlit run app.py
```

### 6. 访问应用
打开浏览器访问：http://localhost:8501

## 📁 项目结构

```
sweeper-robot-agent/
├── app.py                  # 应用入口
├── requirements.txt        # 依赖清单
├── .gitignore              # Git忽略文件
├── README.md               # 项目说明
├── agent/                  # ReAct智能体核心
│   ├── react_agent.py      # 智能体实现
│   └── tools/              # 工具集
│       ├── agent_tools.py  # 工具定义
│       └── middleware.py   # 中间件
├── config/                 # 配置文件
│   ├── rag.yml             # RAG配置
│   ├── chroma.yml          # 向量库配置
│   ├── agent.yml           # 智能体配置
│   └── prompts.yml         # 提示词配置
├── data/                   # 知识库文档
├── prompts/                # 系统提示词
│   ├── main_prompt.txt     # 客服主提示词
│   ├── rag_summarize.txt   # RAG总结提示词
│   └── report_prompt.txt   # 报告生成提示词
├── rag/                    # RAG检索模块
│   ├── rag_service.py      # 总结服务
│   └── vector_store.py     # 向量库服务
├── ui/                     # Streamlit界面
│   ├── chat_page.py        # 聊天页面
│   ├── knowledge_page.py   # 知识库管理页面
│   ├── session.py          # 会话管理
│   └── styles.py           # 样式定义
└── utils/                  # 工具函数
    ├── config_handler.py   # 配置加载
    ├── file_handler.py     # 文件处理
    ├── logger_handler.py   # 日志处理
    ├── path_tool.py        # 路径工具
    ├── prompt_loader.py    # 提示词加载
    └── user_context.py     # 用户上下文
```

## 🎮 使用说明

### 智能客服
1. 在聊天输入框输入你的问题
2. 系统会自动判断需求并调用相应工具
3. 支持的问题类型：
   - 故障排查："机器人迷路了怎么办？"
   - 使用技巧："如何提高拖地效果？"
   - 选购建议："小户型适合哪些扫地机器人？"
   - 天气查询："今天适合扫地吗？"
   - 使用报告："给我生成我的使用报告"

### 快捷提问
侧边栏提供常用快捷提问按钮，一键触发：
- 小户型适合哪些扫地机器人？
- 机器人迷路了怎么办？
- 帮我查一下我所在城市的天气，是否适合今天扫地
- 给我生成我的使用报告

### 用户身份模拟
侧边栏可以模拟不同用户身份：
- 用户ID：1001-1010
- 所在城市：深圳、合肥、杭州、北京、上海、广州
- 报告月份：2025-01至2025-12

### 知识库管理
1. 切换到"知识库管理"页面
2. 上传TXT或PDF格式的知识文档
3. 点击"保存上传文件"
4. 点击"重建/增量索引"将文档加入向量库
5. 查看索引状态与文档列表

### 报告导出
生成使用报告后，侧边栏会出现"下载Markdown报告"按钮，点击即可导出。

## 📝 内置知识库内容

- 扫地/扫拖一体机器人故障检测与修复200条
- 扫地机器人常见问题及解答100条
- 扫拖一体机器人常见问题及解答100条
- 扫地机器人+扫拖一体机器人维护保养200条
- 扫地/扫拖一体机器人选购指南200条

## 🔧 配置说明

### 向量库配置 (config/chroma.yml)
```yaml
collection_name: sweeper_robot_knowledge
persist_directory: ./chroma_db
data_path: ./data
chunk_size: 1000
chunk_overlap: 200
separators: ["\n\n", "\n", "。", "！", "？", " ", ""]
k: 3
allow_knowledge_file_type: [".txt", ".pdf"]
md5_hex_store: ./chroma_db/md5.txt
```

### 智能体配置 (config/agent.yml)
```yaml
external_data_path: ./data/external_data.csv
```

## 🤝 贡献指南

1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

## 📄 许可证

本项目采用 MIT 许可证，详情请见 [LICENSE](LICENSE) 文件。

## 📞 联系我们

如有问题或建议，欢迎提交 Issue 或 Pull Request。

---

**智扫通 · 让扫地机器人使用更简单**
