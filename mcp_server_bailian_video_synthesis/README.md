# MCP Server Bailian Video Synthesis

阿里云百炼-通义万相视频编辑统一模型MCP服务器

## 功能特性

- **多图参考视频生成**: 基于多张参考图片生成视频
- **视频重绘**: 对现有视频进行重新绘制
- **局部编辑**: 对视频的特定区域进行编辑
- **视频延展**: 延长视频时长
- **视频画面扩展**: 扩展视频画面范围
- **异步任务处理**: 支持创建任务和查询结果的异步操作
- **易于集成**: 标准MCP协议，可与Claude Desktop等工具无缝集成

## 安装

### 从PyPI安装

```bash
pip install mcp-server-bailian-video-synthesis
```

### 从源码安装

```bash
git clone <repository-url>
cd mcp_server_bailian_video_synthesis
pip install -e .
```

## 配置

### 获取API密钥

1. 访问[阿里云百炼控制台](https://bailian.console.aliyun.com/)
2. 创建应用并获取API Key
3. 设置环境变量或在启动时传入API Key

### 环境变量设置

```bash
export DASHSCOPE_API_KEY="your-api-key-here"
```

## 使用方法

### 启动MCP服务器

```bash
# 使用uvx启动（推荐）
uvx mcp-server-bailian-video-synthesis

# 或者直接传入API Key
uvx mcp-server-bailian-video-synthesis --api-key your-api-key-here
```

### Claude Desktop配置

在Claude Desktop的配置文件中添加：

```json
{
  "mcpServers": {
    "bailian-video-synthesis": {
      "command": "uvx",
      "args": ["mcp-server-bailian-video-synthesis"],
      "env": {
        "DASHSCOPE_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

## 支持的工具

### 创建任务工具

- `create_task_image_reference`: 多图参考视频生成
- `create_task_video_repainting`: 视频重绘
- `create_task_video_edit`: 局部编辑
- `create_task_video_extension`: 视频延展
- `create_task_video_expansion`: 视频画面扩展

### 查询结果工具

- `get_task_result`: 根据任务ID查询处理结果

## 错误处理

服务器会自动处理以下错误情况：
- API密钥无效或缺失
- 网络连接问题
- 参数验证错误
- 任务处理失败

## 开发

### 安装开发依赖

```bash
pip install -e ".[dev]"
```

### 运行测试

```bash
pytest
```

### 代码格式化

```bash
black .
isort .
```

## 许可证

MIT License

## 相关链接

- [阿里云百炼官方文档](https://help.aliyun.com/zh/model-studio/)
- [视频生成API文档](https://help.aliyun.com/zh/model-studio/video-generation-api/)
- [MCP协议规范](https://github.com/modelcontextprotocol/specification)