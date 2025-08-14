# 发布指南 - MCP Server Bailian Video Synthesis

本文档详细说明如何将 `mcp-server-bailian-video-synthesis` 工具发布到PyPI公共仓库。

## 📋 发布前检查清单

### 1. 代码质量检查
- [ ] 所有测试用例通过
- [ ] 代码符合PEP 8规范
- [ ] 文档字符串完整
- [ ] 类型注解正确
- [ ] 无安全漏洞

### 2. 版本管理
- [ ] 更新版本号（pyproject.toml中的version字段）
- [ ] 更新CHANGELOG.md
- [ ] 确认版本号遵循语义化版本规范（SemVer）

### 3. 文档完整性
- [ ] README.md内容完整且准确
- [ ] API文档更新
- [ ] 使用示例正确
- [ ] 安装说明清晰

### 4. 依赖管理
- [ ] requirements.txt包含所有必需依赖
- [ ] pyproject.toml中的依赖版本正确
- [ ] 无冗余依赖

## 🚀 发布步骤

### 方法一：使用自动化脚本（推荐）

```bash
# 进入项目目录
cd mcp_server_bailian_video_synthesis

# 运行发布脚本
python publish.py

# 或发布到测试PyPI
python publish.py --test-pypi
```

### 方法二：手动发布

#### 1. 安装发布工具

```bash
pip install build twine
```

#### 2. 构建分发包

```bash
# 清理之前的构建
rm -rf dist/ build/ *.egg-info/

# 构建源码包和wheel包
python -m build
```

#### 3. 检查构建结果

```bash
# 检查分发包
twine check dist/*
```

#### 4. 上传到测试PyPI（可选）

```bash
# 上传到测试PyPI进行验证
twine upload --repository testpypi dist/*

# 从测试PyPI安装验证
pip install --index-url https://test.pypi.org/simple/ mcp-server-bailian-video-synthesis
```

#### 5. 上传到正式PyPI

```bash
# 上传到正式PyPI
twine upload dist/*
```

## 🔧 配置PyPI认证

### 方法一：使用API Token（推荐）

1. 登录 [PyPI](https://pypi.org/)
2. 进入 Account Settings → API tokens
3. 创建新的API token
4. 配置认证信息：

```bash
# 创建或编辑 ~/.pypirc
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-your-api-token-here

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-your-test-api-token-here
```

### 方法二：环境变量

```bash
# 设置环境变量
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-your-api-token-here

# Windows
set TWINE_USERNAME=__token__
set TWINE_PASSWORD=pypi-your-api-token-here
```

## 📦 包信息

### 基本信息
- **包名**: `mcp-server-bailian-video-synthesis`
- **描述**: 阿里云百炼通义万相视频合成MCP服务器
- **作者**: AI Assistant
- **许可证**: MIT
- **Python版本要求**: >=3.8

### 分类标签
```python
classifiers=[
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
    "Topic :: Multimedia :: Video",
]
```

## 🧪 发布后验证

### 1. 安装验证

```bash
# 创建新的虚拟环境
python -m venv test_env
source test_env/bin/activate  # Linux/Mac
# 或
test_env\Scripts\activate  # Windows

# 从PyPI安装
pip install mcp-server-bailian-video-synthesis

# 验证安装
python -c "import mcp_server_bailian_video_synthesis; print('安装成功')"
```

### 2. 功能验证

```bash
# 运行基本测试
python -m mcp_server_bailian_video_synthesis --help

# 测试MCP服务器启动
python -m mcp_server_bailian_video_synthesis
```

### 3. 文档验证

- 检查PyPI页面显示是否正确
- 验证README.md渲染效果
- 确认下载链接可用
- 测试安装命令

## 📈 版本发布策略

### 语义化版本控制

- **主版本号（Major）**: 不兼容的API修改
- **次版本号（Minor）**: 向下兼容的功能性新增
- **修订号（Patch）**: 向下兼容的问题修正

### 发布类型

#### 1. Alpha版本（开发版）
```bash
# 版本格式：1.0.0a1, 1.0.0a2
python publish.py --version 1.0.0a1
```

#### 2. Beta版本（测试版）
```bash
# 版本格式：1.0.0b1, 1.0.0b2
python publish.py --version 1.0.0b1
```

#### 3. Release Candidate（候选版）
```bash
# 版本格式：1.0.0rc1, 1.0.0rc2
python publish.py --version 1.0.0rc1
```

#### 4. 正式版本
```bash
# 版本格式：1.0.0
python publish.py --version 1.0.0
```

## 🔄 持续集成/持续部署

### GitHub Actions配置示例

```yaml
# .github/workflows/publish.yml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.8'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    - name: Build package
      run: python -m build
    - name: Publish to PyPI
      uses: pypa/gh-action-pypi-publish@release/v1
      with:
        password: ${{ secrets.PYPI_API_TOKEN }}
```

## 🚨 常见问题与解决方案

### 1. 版本冲突

**问题**: 版本号已存在
```
HTTP Error 400: File already exists
```

**解决方案**:
- 更新版本号
- 检查pyproject.toml中的version字段
- 确保版本号唯一

### 2. 认证失败

**问题**: 上传时认证失败
```
HTTP Error 403: Invalid or non-existent authentication information
```

**解决方案**:
- 检查API token是否正确
- 确认token权限范围
- 重新生成token

### 3. 包大小限制

**问题**: 包文件过大
```
HTTP Error 413: Request Entity Too Large
```

**解决方案**:
- 检查MANIFEST.in文件
- 排除不必要的文件
- 优化包内容

### 4. 依赖解析失败

**问题**: 依赖版本冲突

**解决方案**:
- 检查requirements.txt
- 更新依赖版本
- 测试兼容性

## 📊 发布后监控

### 1. 下载统计

- 监控PyPI下载数据
- 分析用户反馈
- 跟踪问题报告

### 2. 版本采用率

- 观察新版本采用情况
- 收集用户使用数据
- 优化发布策略

### 3. 社区反馈

- 关注GitHub Issues
- 响应用户问题
- 收集改进建议

## 📝 发布记录模板

```markdown
## 版本 X.Y.Z - YYYY-MM-DD

### 新增功能
- 功能描述

### 改进
- 改进描述

### 修复
- 修复描述

### 破坏性变更
- 变更描述

### 依赖更新
- 依赖变更
```

## 🔗 相关资源

- [PyPI官方文档](https://packaging.python.org/)
- [Twine文档](https://twine.readthedocs.io/)
- [语义化版本规范](https://semver.org/)
- [Python打包指南](https://packaging.python.org/tutorials/packaging-projects/)
- [阿里云百炼API文档](https://help.aliyun.com/zh/model-studio/video-generation-api/)

---

**注意**: 发布到PyPI是不可逆的操作，请确保在发布前进行充分测试。建议先发布到测试PyPI进行验证。