# 发布指南

本文档说明如何将 `mcp-server-bailian-video-synthesis` 发布到 PyPI 并通过 uvx 使用。

## 发布到 PyPI

### 1. 准备发布环境

```bash
# 安装发布工具
pip install build twine

# 确保所有依赖都已安装
pip install -r requirements.txt
```

### 2. 构建包

```bash
# 清理之前的构建文件
rm -rf dist/ build/ src/*.egg-info/

# 构建包
python -m build
```

### 3. 检查包

```bash
# 检查包的完整性
twine check dist/*
```

### 4. 上传到 PyPI

#### 测试环境（推荐先测试）

```bash
# 上传到 TestPyPI
twine upload --repository testpypi dist/*

# 从 TestPyPI 安装测试
pip install --index-url https://test.pypi.org/simple/ mcp-server-bailian-video-synthesis
```

#### 正式环境

```bash
# 上传到正式 PyPI
twine upload dist/*
```

### 5. 验证发布

```bash
# 从 PyPI 安装
pip install mcp-server-bailian-video-synthesis

# 验证安装
mcp-server-bailian-video-synthesis --help
```

## 使用 uvx 运行

### 1. 安装 uvx

```bash
# 如果还没有安装 uvx
pip install uvx
```

### 2. 使用 uvx 运行

```bash
# 直接运行（会自动安装包）
uvx mcp-server-bailian-video-synthesis YOUR_API_KEY

# 或者设置环境变量
export DASHSCOPE_API_KEY=your_api_key_here
uvx mcp-server-bailian-video-synthesis
```

### 3. 在 MCP 客户端中使用

在 MCP 客户端配置文件中添加：

```json
{
  "mcpServers": {
    "bailian-video-synthesis": {
      "command": "uvx",
      "args": ["mcp-server-bailian-video-synthesis"],
      "env": {
        "DASHSCOPE_API_KEY": "your_api_key_here",
        "UV_DEFAULT_INDEX": "https://pypi.tuna.tsinghua.edu.cn/simple"
      }
    }
  }
}
```

## 版本管理

### 更新版本

1. 更新 `pyproject.toml` 中的版本号
2. 更新 `src/mcp_server_bailian_video_synthesis/__init__.py` 中的 `__version__`
3. 提交更改并创建 git tag
4. 重新构建和发布

```bash
# 创建版本标签
git tag v1.0.1
git push origin v1.0.1

# 重新构建和发布
python -m build
twine upload dist/*
```

## 注意事项

1. **API 密钥安全**：确保不要在代码中硬编码 API 密钥
2. **版本兼容性**：确保与 MCP 协议的兼容性
3. **依赖管理**：保持依赖版本的稳定性
4. **文档更新**：每次发布前更新 README 和文档
5. **测试验证**：在发布前进行充分测试

## 故障排除

### 常见问题

1. **包名冲突**：如果包名已存在，需要选择不同的名称
2. **权限问题**：确保有 PyPI 账户和上传权限
3. **依赖冲突**：检查依赖版本兼容性
4. **构建失败**：检查 `pyproject.toml` 配置

### 调试命令

```bash
# 检查包结构
tar -tzf dist/*.tar.gz

# 检查wheel内容
unzip -l dist/*.whl

# 本地安装测试
pip install dist/*.whl
```

## 自动化发布

可以使用 GitHub Actions 自动化发布流程：

```yaml
# .github/workflows/publish.yml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    - name: Install dependencies
      run: |
        pip install build twine
    - name: Build package
      run: python -m build
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: twine upload dist/*
```