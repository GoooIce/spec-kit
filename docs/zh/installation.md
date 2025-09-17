# 安装指南

## 前提条件

- **Linux/macOS**（或Windows；现已支持PowerShell脚本，无需WSL）
- AI编程代理：[Claude Code](https://www.anthropic.com/claude-code)、[GitHub Copilot](https://code.visualstudio.com/)或[Gemini CLI](https://github.com/google-gemini/gemini-cli)
- [uv](https://docs.astral.sh/uv/) 用于包管理
- [Python 3.11+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)

## 安装

### 初始化新项目

开始的最简单方法是初始化新项目：

```bash
uvx --from git+https://github.com/github/spec-kit.git specify init <项目名称>
```

或在当前目录中初始化：

```bash
uvx --from git+https://github.com/github/spec-kit.git specify init --here
```

### 指定AI代理

您可以在初始化期间主动指定您的AI代理：

```bash
uvx --from git+https://github.com/github/spec-kit.git specify init <项目名称> --ai claude
uvx --from git+https://github.com/github/spec-kit.git specify init <项目名称> --ai gemini
uvx --from git+https://github.com/github/spec-kit.git specify init <项目名称> --ai copilot
```

### 指定脚本类型（Shell vs PowerShell）

所有自动化脚本现在都有Bash（`.sh`）和PowerShell（`.ps1`）两个版本。

自动行为：
- Windows默认：`ps`
- 其他操作系统默认：`sh`
- 交互模式：除非您传递`--script`，否则会提示您选择

强制特定脚本类型：
```bash
uvx --from git+https://github.com/github/spec-kit.git specify init <项目名称> --script sh
uvx --from git+https://github.com/github/spec-kit.git specify init <项目名称> --script ps
```

### 忽略代理工具检查

如果您希望获取模板而不检查正确的工具：

```bash
uvx --from git+https://github.com/github/spec-kit.git specify init <项目名称> --ai claude --ignore-agent-tools
```

## 验证

初始化后，您应该在AI代理中看到以下可用命令：
- `/specify` - 创建规范
- `/plan` - 生成实现计划
- `/tasks` - 分解为可操作任务

`.specify/scripts`目录将包含`.sh`和`.ps1`脚本。

## 故障排除

### Linux上的Git凭据管理器

如果您在Linux上遇到Git身份验证问题，可以安装Git凭据管理器：

```bash
#!/usr/bin/env bash
set -e
echo "正在下载Git凭据管理器v2.6.1..."
wget https://github.com/git-ecosystem/git-credential-manager/releases/download/v2.6.1/gcm-linux_amd64.2.6.1.deb
echo "正在安装Git凭据管理器..."
sudo dpkg -i gcm-linux_amd64.2.6.1.deb
echo "正在配置Git使用GCM..."
git config --global credential.helper manager
echo "正在清理..."
rm gcm-linux_amd64.2.6.1.deb
```
