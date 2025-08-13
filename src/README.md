 # 阿里云百炼-通义万相视频编辑统一模型 MCP 服务器

本项目实现了阿里云百炼通义万相视频编辑统一模型的 MCP (Model Context Protocol) 服务器，支持多种视频编辑功能。

## 功能特性

### 支持的视频编辑功能

1. **多图参考视频生成** (`create_task_image_reference`)
   - 基于参考图像和提示词生成视频
   - 支持主体和背景分离控制
   - 支持多种输出尺寸

2. **视频重绘** (`create_task_video_repainting`)
   - 基于输入视频和提示词重新绘制视频内容
   - 保持原有结构，支持深度、边缘、姿态控制

3. **视频局部编辑** (`create_task_video_edit`)
   - 基于掩码图像对视频特定区域进行编辑
   - 精确控制编辑区域

4. **视频延展** (`create_task_video_extension`)
   - 基于短视频片段延长视频时长
   - 支持1秒扩展到5秒

5. **视频画面扩展** (`create_task_video_expansion`)
   - 扩展视频的画面范围
   - 增加更多视觉内容

6. **任务结果查询** (`get_task_result`)
   - 查询任务执行状态和结果
   - 获取生成的视频URL

## 安装和配置

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 获取阿里云百炼API密钥

1. 访问 [阿里云百炼控制台](https://bailian.console.aliyun.com/)
2. 创建应用并获取API Key
3. 确保账户有足够的余额和权限

### 3. 配置API密钥

有两种方式配置API密钥：

**方式1：环境变量**
```bash
export DASHSCOPE_API_KEY=your_api_key_here
```

**方式2：命令行参数**
```bash
python src/mcp-server-bailian_video-synthesis.py your_api_key_here
```

## 使用方法

### 启动MCP服务器

```bash
# 使用环境变量
export DASHSCOPE_API_KEY=your_api_key
python src/mcp-server-bailian_video-synthesis.py

# 或使用命令行参数
python src/mcp-server-bailian_video-synthesis.py your_api_key
```

### 工具使用示例

#### 1. 多图参考视频生成

```json
{
  "name": "create_task_image_reference",
  "arguments": {
    "prompt": "视频中，一位女孩自晨雾缭绕的古老森林深处款款走出，她步伐轻盈，镜头捕捉她每一个灵动瞬间。",
    "ref_images_url": [
      "http://example.com/image1.jpg",
      "http://example.com/image2.jpg"
    ],
    "obj_or_bg": ["obj", "bg"],
    "size": "1280*720"
  }
}
```

#### 2. 视频重绘

```json
{
  "name": "create_task_video_repainting",
  "arguments": {
    "prompt": "视频展示了一辆黑色的蒸汽朋克风格汽车，绅士驾驶着，车辆装饰着齿轮和铜管。",
    "video_url": "http://example.com/input_video.mp4",
    "control_condition": "depth"
  }
}
```

#### 3. 视频局部编辑

```json
{
  "name": "create_task_video_edit",
  "arguments": {
    "prompt": "一只穿着西装的狮子优雅地品着咖啡",
    "video_url": "http://example.com/input_video.mp4",
    "mask_url": "http://example.com/mask.png"
  }
}
```

#### 4. 视频延展

```json
{
  "name": "create_task_video_extension",
  "arguments": {
    "prompt": "一只戴着墨镜的狗在街道上滑滑板，3D卡通",
    "video_url": "http://example.com/short_video.mp4",
    "target_duration": 5
  }
}
```

#### 5. 视频画面扩展

```json
{
  "name": "create_task_video_expansion",
  "arguments": {
    "prompt": "一位优雅的女士正在激情演奏小提琴，她身后是一支完整的交响乐团",
    "video_url": "http://example.com/input_video.mp4",
    "expansion_ratio": 1.5
  }
}
```

#### 6. 查询任务结果

```json
{
  "name": "get_task_result",
  "arguments": {
    "task_id": "task_id_from_create_response"
  }
}
```

## 响应格式

### 创建任务响应

```json
{
  "output": {
    "task_id": "12345678-1234-1234-1234-123456789012"
  },
  "usage": {
    "input_tokens": 100,
    "output_tokens": 50
  },
  "request_id": "request_id_here"
}
```

### 查询结果响应

```json
{
  "output": {
    "task_id": "12345678-1234-1234-1234-123456789012",
    "task_status": "SUCCEEDED",
    "results": [
      {
        "url": "http://example.com/generated_video.mp4"
      }
    ]
  },
  "usage": {
    "input_tokens": 50,
    "output_tokens": 100
  },
  "request_id": "request_id_here"
}
```

## 任务状态说明

- `PENDING`: 任务排队中
- `RUNNING`: 任务执行中
- `SUCCEEDED`: 任务成功完成
- `FAILED`: 任务执行失败

## 注意事项

1. **处理时间**: 视频编辑任务处理时间较长（约5-10分钟），请耐心等待
2. **文件格式**: 支持常见的视频和图像格式
3. **文件大小**: 请确保输入文件大小在API限制范围内
4. **URL有效期**: 生成的视频URL有效期为24小时
5. **费用**: 按照处理时长计费，详见[官方计费说明](https://help.aliyun.com/zh/model-studio/wanx-vace-api-reference)

## 错误处理

常见错误及解决方案：

- **401 Unauthorized**: 检查API密钥是否正确
- **403 Forbidden**: 检查账户余额和权限
- **400 Bad Request**: 检查请求参数是否符合要求
- **429 Too Many Requests**: 请求频率过高，请稍后重试

## 技术支持

- 官方文档: https://help.aliyun.com/zh/model-studio/wanx-vace-api-reference
- API参考: https://help.aliyun.com/zh/model-studio/video-generation-api/

## 许可证

本项目遵循项目根目录下的LICENSE文件。

## 作者

John Chen