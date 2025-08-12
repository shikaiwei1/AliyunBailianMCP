# 开发环境
1. python3.12
2. 安装依赖：`pip install -r requirements.txt`

# MCP说明总则：
1. 阿里云百炼的API_KEY（DASHSCOPE_API_KEY）,在MCP启动时通过参数传入。
2. 百炼每个模块的不同用法和接口，封装成1个MCP工具。
3. 每个MCP前缀：`mcp-server-bailian_`,后面跟功能的英文名称，如：`mcp-server-bailian_video-synthesis`。（英文名一般以接口名命名）
4. 举例：以`[视频生成](https://help.aliyun.com/zh/model-studio/video-generation-api/)`功能为例，其各个功能核心方法总结为2步骤：，核心为2个步骤：`步骤1：创建任务获取任务ID`，`步骤2：根据任务ID查询结果`。其中步骤1调用接口https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis 步骤2 调用接口https://dashscope.aliyuncs.com/api/v1/tasks/{task_id} 其下面的通义万相各类视频生成功能而视频生成功能有分为`图生视频-基于首尾帧`,`图生视频-基于首帧`,`文生视频`,`通用视频编辑`等。而不同的功能传参又有不同。那么，应当按照如下方式生成：
   1. 生成1个MCP工具，名为`mcp-server-bailian_video-synthesis`
   2. 该工具下，有2类方法；
      1. 一类是`创建任务获取任务ID`，对应`[视频生成](https://help.aliyun.com/zh/model-studio/video-generation-api/)`的`步骤1`，同时根据不同的功能，分别封装成不同的方法。命名规则：`create_task_{功能名}`
      2. 另一类是`根据任务ID查询结果`，对应`[视频生成](https://help.aliyun.com/zh/model-studio/video-generation-api/)`的`步骤2`；由于各个功能通用，则只封装成1个方法。命名：`get_task_result`
5. 每个MCP工具应当有详细的工具说明和参数说明。参数说明应当尽可能还原官方文档的接口参数。并附上官方帮助文档URL
6. MCP工具完成调试后，应当发布到pip仓库，供所有人使用。


# MCP工具开发说明：
1. MCP开发请参照[官方文档](https://github.com/modelcontextprotocol/python-sdk);浏览web页或使用context7查询官方文档。
2. 每个MCP工具都应当有一个对应的python文件，文件名就是MCP工具的名称，如：`mcp-server-bailian_video-synthesis.py`。
3. 每个MCP工具的python文件，应当有一个对应的工具说明，工具说明应当包含工具的名称、工具的前缀、工具的参数说明、工具的返回值说明。这些参数说明应当遵循官方文档。