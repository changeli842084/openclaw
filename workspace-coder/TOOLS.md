# TOOLS.md - 程序员工具使用笔记

## 编程语言环境

### Python
- **解释器路径**：`/usr/bin/python3`
- **包管理**：使用 `pip` 安装依赖，生成 `requirements.txt`：`pip freeze > requirements.txt`
- **虚拟环境**：建议为每个项目创建虚拟环境 `python3 -m venv venv`，激活后安装依赖。

### Node.js
- **解释器**：`node`
- **包管理**：`npm` 或 `yarn`，生成 `package.json`。
- **依赖安装**：`npm install`。

## 代码编辑与调试

### 文件编辑
- 使用 `exec` 工具配合 `echo` 或 `cat` 创建文件，或使用内置的 `write_file` 技能。
- 对于多行代码，可以使用 Here Document 或逐行写入。

### 调试
- Python：可使用 `pdb` 或在代码中插入 `print()` 调试。
- Node.js：可使用 `console.log()` 或内置调试器。

## 测试工具

### Python 测试
- **pytest**：运行 `pytest tests/`，生成测试报告。
- **unittest**：运行 `python -m unittest discover tests`。

### JavaScript 测试
- **Jest**：运行 `npm test`（需在 `package.json` 中配置）。

## 版本控制（需用户授权）
- **Git 命令**：
  - `git init`
  - `git add .`
  - `git commit -m "message"`
  - `git remote add origin <url>`
  - `git push -u origin main`
- **注意**：使用前必须向 manager 确认用户已授权，并获取远程仓库地址。

## 文件操作
- **创建目录**：`mkdir -p /path/to/dir`
- **复制文件**：`cp -r source destination`
- **移动/重命名**：`mv old new`

## 问题排查
- 检查语法错误：运行解释器检查。
- 查看错误日志：使用 `cat` 或 `tail` 查看日志文件。
- 权限问题：使用 `ls -l` 查看文件权限，必要时向 manager 请求调整。
