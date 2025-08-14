# 阿里云百炼MCP工具集

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-orange.svg)](https://github.com/modelcontextprotocol)

阿里云百炼MCP工具集是一套基于Model Context Protocol (MCP)的AI工具，用于集成阿里云百炼AI服务。本项目包含两个独立的MCP工具，支持视频合成和图像生成功能。

## 🚀 快速开始

### 安装

```bash
# 安装视频合成工具
pip install mcp-server-bailian-video-synthesis

# 安装图像生成工具
pip install mcp-server-bailian-image
```

### 配置API密钥

在使用前，需要设置阿里云百炼API密钥：

```bash
# 设置环境变量
export DASHSCOPE_API_KEY="your-api-key-here"

# 或在Windows中
set DASHSCOPE_API_KEY=your-api-key-here
```

获取API密钥：
1. 访问[阿里云百炼控制台](https://bailian.console.aliyun.com/)
2. 创建应用并获取API Key
3. 确保账户有足够的调用额度

## 📦 工具介绍

### 1. 视频合成工具 (mcp-server-bailian-video-synthesis)

基于阿里云百炼通义万相的视频生成功能，支持多种视频创作场景。

**主要功能：**
- 🎬 多图参考视频生成
- 🎨 视频重绘
- ✂️ 局部视频编辑
- 📏 视频延展
- 🖼️ 视频画面扩展

**支持的工具：**
- [通义万相-通用视频编辑API](https://help.aliyun.com/zh/model-studio/wanx-vace-api-reference)
  - `create_task_multi_image_video_generation` - 多图参考视频生成
  - `create_task_video_repaint` - 视频重绘
  - `create_task_partial_video_editing` - 局部视频编辑
  - `create_task_video_extension` - 视频延展
  - `create_task_video_frame_expansion` - 视频画面扩展

- 通义万象-视频通用功能
  - `get_task_result` - 获取任务结果（上述所有异步任务都支持）

### 2. 图像生成工具 (mcp-server-bailian-image)

基于阿里云百炼通义万相V2版API的图像生成功能，支持文生图。

**主要功能：**
- 🖼️ 文生图 (Text-to-Image)
- 🎨 多种AI模型选择
- 📐 自定义图像尺寸
- 🔄 正向和反向提示词

**支持的工具：**
- `text2imagev2` - 文生图功能

**支持的模型：**
- 详见[官方文档](https://help.aliyun.com/zh/model-studio/text-to-image-v2-api-reference)
## 🛠️ 开发环境设置

### 克隆项目

```bash
git clone <repository-url>
cd AliyunBailianMCP
```

### 安装开发依赖

```bash
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt
pip install pytest mcp dashscope httpx
```

### 运行测试

```bash
# 测试视频合成工具
cd mcp_server_bailian_video_synthesis
python run_tests.py

# 测试图像生成工具
cd mcp_server_bailian_image
python run_tests.py

# 运行完整的发布准备检查
cd ..
python check_release_readiness.py
```

## 📁 项目结构

```
AliyunBailianMCP/
├── mcp_server_bailian_video_synthesis/     # 视频合成工具
│   ├── src/mcp_server_bailian_video_synthesis/
│   │   ├── __init__.py
│   │   └── server.py                      # 主服务器代码
│   ├── test/                              # 测试文件
│   ├── pyproject.toml                     # 项目配置
│   ├── requirements.txt                   # 依赖列表
│   ├── README.md                          # 详细说明
│   ├── PUBLISH.md                         # 发布指南
│   ├── CHANGELOG.md                       # 更新日志
│   ├── publish.py                         # 发布脚本
│   └── run_tests.py                       # 测试脚本
├── mcp_server_bailian_image/               # 图像生成工具
│   ├── src/mcp_server_bailian_image/
│   │   ├── __init__.py
│   │   └── server.py                      # 主服务器代码
│   ├── test/                              # 测试文件
│   ├── pyproject.toml                     # 项目配置
│   ├── requirements.txt                   # 依赖列表
│   ├── README.md                          # 详细说明
│   ├── PUBLISH.md                         # 发布指南
│   ├── CHANGELOG.md                       # 更新日志
│   ├── publish.py                         # 发布脚本
│   └── run_tests.py                       # 测试脚本
├── check_release_readiness.py              # 发布准备检查
├── publish_all.py                         # 一键发布脚本
├── PUBLISH_GUIDE.md                       # 总体发布指南
├── RELEASE_SUMMARY.md                     # 发布准备总结
└── README.md                              # 本文档
```

## 🔧 使用方法

### 在Claude Desktop中配置

1. 打开Claude Desktop配置文件：
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Linux: `~/.config/Claude/claude_desktop_config.json`

2. 添加MCP服务器配置：

```json
{
  "mcpServers": {
    "bailian-video": {
      "command": "uvx",
      "args": ["mcp-server-bailian-video-synthesis"],
      "env": {
        "DASHSCOPE_API_KEY": "your-api-key-here"
      }
    },
    "bailian-image": {
      "command": "uvx",
      "args": ["mcp-server-bailian-image"],
      "env": {
        "DASHSCOPE_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

3. 重启Claude Desktop

### 使用示例

#### 图像生成

```
请帮我生成一张图片：一只可爱的小猫在花园里玩耍，阳光明媚，高质量，4K分辨率
```

#### 视频生成

```
请帮我创建一个视频生成任务：基于这张图片生成一个10秒的视频，展示花朵在微风中摇摆的场景
```

## 📚 文档

- [视频合成工具详细文档](mcp_server_bailian_video_synthesis/README.md)
- [图像生成工具详细文档](mcp_server_bailian_image/README.md)
- [发布指南](PUBLISH_GUIDE.md)
- [发布准备总结](RELEASE_SUMMARY.md)

## 🚀 发布到PyPI

### 快速发布（推荐）

```bash
# 发布所有工具到正式PyPI
python publish_all.py

# 发布到测试PyPI
python publish_all.py --test-pypi

# 跳过测试直接发布
python publish_all.py --skip-tests
```

### 单独发布

```bash
# 发布视频合成工具
cd mcp_server_bailian_video_synthesis
python publish.py

# 发布图像生成工具
cd mcp_server_bailian_image
python publish.py
```

## 🧪 测试

项目包含完整的测试套件：

- **视频合成工具**: 11个测试用例
- **图像生成工具**: 14个测试用例
- **测试覆盖**: 服务器初始化、工具注册、API调用、参数验证、错误处理

```bash
# 运行所有测试
python check_release_readiness.py

# 运行单个工具测试
cd mcp_server_bailian_video_synthesis
python run_tests.py
```

## 📋 系统要求

- **Python**: 3.8+
- **操作系统**: Windows, macOS, Linux
- **网络**: 需要访问阿里云API
- **依赖**: 详见各工具的requirements.txt

## 🔐 安全注意事项

1. **API密钥安全**: 不要在代码中硬编码API密钥
2. **环境变量**: 使用环境变量管理敏感信息
3. **网络安全**: 确保网络连接安全
4. **权限控制**: 合理设置API调用权限

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开Pull Request

## 📄 许可证

本项目采用MIT许可证 - 详见 [LICENSE](LICENSE) 文件

## 📞 支持与反馈

- **问题反馈**: [GitHub Issues](https://github.com/your-repo/issues)
- **功能请求**: [GitHub Discussions](https://github.com/your-repo/discussions)
- **邮箱支持**: your-email@example.com

## 🔗 相关链接

- [阿里云百炼官方文档](https://help.aliyun.com/zh/model-studio/)
- [Model Context Protocol](https://github.com/modelcontextprotocol)
- [Claude Desktop](https://claude.ai/desktop)
- [PyPI项目页面](https://pypi.org/)

---

**开发团队**: AI助手  
**最后更新**: 2024年1月  
**版本**: 1.0.0


