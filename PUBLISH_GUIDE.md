# 阿里云百炼MCP工具集 - 发布指南

## 📦 项目概述

本项目包含两个独立的阿里云百炼MCP工具：

1. **mcp-server-bailian-video-synthesis**: 视频合成工具
2. **mcp-server-bailian-image**: 图像生成工具

每个工具都是独立的Python包，可以单独发布到PyPI。

## 🏗️ 项目结构

```
AliyunBailianMCP/
├── mcp_server_bailian_video_synthesis/     # 视频合成工具
│   ├── src/
│   │   └── mcp_server_bailian_video_synthesis/
│   │       ├── __init__.py
│   │       └── server.py
│   ├── test/
│   │   ├── __init__.py
│   │   └── test_video_synthesis.py
│   ├── pyproject.toml
│   ├── requirements.txt
│   ├── README.md
│   ├── PUBLISH.md
│   ├── publish.py
│   └── run_tests.py
├── mcp_server_bailian_image/               # 图像生成工具
│   ├── src/
│   │   └── mcp_server_bailian_image/
│   │       ├── __init__.py
│   │       └── server.py
│   ├── test/
│   │   ├── __init__.py
│   │   └── test_image_generation.py
│   ├── pyproject.toml
│   ├── requirements.txt
│   ├── README.md
│   ├── PUBLISH.md
│   ├── publish.py
│   └── run_tests.py
├── README.md                               # 项目总体说明
├── LICENSE                                 # 许可证
└── PUBLISH_GUIDE.md                        # 本文档
```

## 🚀 快速发布

### 方法一：使用自动化脚本（推荐）

每个工具目录下都有 `publish.py` 脚本，可以自动化整个发布流程：

```bash
# 发布视频合成工具
cd mcp_server_bailian_video_synthesis
python publish.py

# 发布图像生成工具
cd mcp_server_bailian_image
python publish.py
```

### 方法二：手动发布

```bash
# 进入工具目录
cd mcp_server_bailian_video_synthesis  # 或 mcp_server_bailian_image

# 运行测试
python run_tests.py

# 构建包
python -m build

# 检查包
twine check dist/*

# 上传到PyPI
twine upload dist/*
```

## 📋 发布前检查清单

### 通用检查项

- [ ] 所有测试通过
- [ ] 代码符合PEP 8规范
- [ ] 文档更新完整
- [ ] 版本号已更新
- [ ] 依赖项正确配置
- [ ] 许可证文件存在

### 视频合成工具特定检查

- [ ] 所有视频生成功能测试通过
- [ ] API接口参数验证正确
- [ ] 异步任务处理正常
- [ ] 错误处理机制完善

### 图像生成工具特定检查

- [ ] text2imagev2功能测试通过
- [ ] 支持的模型列表最新
- [ ] 图像尺寸参数验证正确
- [ ] DashScope SDK集成正常

## 🔧 版本管理策略

### 语义化版本控制

遵循 [Semantic Versioning](https://semver.org/) 规范：

- **MAJOR.MINOR.PATCH** (例如: 1.2.3)
- **MAJOR**: 不兼容的API更改
- **MINOR**: 向后兼容的功能添加
- **PATCH**: 向后兼容的错误修复

### 版本发布节奏

- **补丁版本**: 每周或按需发布（bug修复）
- **次要版本**: 每月发布（新功能）
- **主要版本**: 每季度或半年发布（重大更改）

## 🧪 测试策略

### 自动化测试

每个工具都包含完整的测试套件：

```bash
# 运行单个工具的测试
cd mcp_server_bailian_video_synthesis
python run_tests.py

# 或使用pytest
pytest test/ -v
```

### 集成测试

```bash
# 运行所有工具的测试
for tool in mcp_server_bailian_*; do
    echo "Testing $tool..."
    cd $tool
    python run_tests.py
    cd ..
done
```

## 📚 文档维护

### 必需文档

每个工具必须包含：

1. **README.md**: 功能介绍、安装指南、使用示例
2. **PUBLISH.md**: 详细的发布说明
3. **API文档**: 工具参数和返回值说明

### 文档更新流程

1. 代码更改后立即更新相关文档
2. 发布前检查所有文档的准确性
3. 确保示例代码可以正常运行

## 🌐 PyPI发布流程

### 1. 准备环境

```bash
# 安装发布工具
pip install build twine

# 配置PyPI凭据（首次）
twine configure
```

### 2. 测试发布（可选）

```bash
# 上传到测试PyPI
python publish.py --test-pypi

# 测试安装
pip install --index-url https://test.pypi.org/simple/ mcp-server-bailian-video-synthesis
```

### 3. 正式发布

```bash
# 上传到正式PyPI
python publish.py

# 验证安装
pip install mcp-server-bailian-video-synthesis
```

## 🔄 持续集成建议

### GitHub Actions配置

建议为每个工具配置以下自动化流程：

1. **自动测试**: 每次提交时运行测试
2. **自动发布**: 创建tag时自动发布到PyPI
3. **代码质量检查**: 使用flake8、black等工具
4. **安全扫描**: 检查依赖项安全漏洞

### 示例工作流

```yaml
name: Test and Publish

on:
  push:
    tags:
      - 'v*'

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.12
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: python run_tests.py
  
  publish:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.12
      - name: Build and publish
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
        run: |
          pip install build twine
          python -m build
          twine upload dist/*
```

## 📞 支持和维护

### 问题反馈

- **GitHub Issues**: 用于bug报告和功能请求
- **文档问题**: 通过PR直接修复
- **安全问题**: 通过私有渠道报告

### 维护计划

- **定期更新**: 跟进阿里云百炼API更新
- **依赖管理**: 定期更新依赖项版本
- **性能优化**: 持续改进工具性能
- **文档维护**: 保持文档的准确性和完整性

## ⚠️ 注意事项

1. **API密钥安全**: 确保示例代码中不包含真实的API密钥
2. **向后兼容**: 尽量保持API的向后兼容性
3. **测试覆盖**: 新功能必须有对应的测试用例
4. **文档同步**: 确保代码更改后及时更新文档
5. **版本标记**: 使用git tag标记每个发布版本

## 🎯 发布目标

- **稳定性**: 确保每个发布版本都经过充分测试
- **易用性**: 提供清晰的文档和示例
- **兼容性**: 保持与不同Python版本的兼容性
- **性能**: 持续优化工具性能
- **社区**: 建立活跃的用户社区

---

**维护团队**: Bailian Team
**最后更新**: 2024-01-XX
**下次审查**: 2024-XX-XX