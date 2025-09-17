# 本地开发指南

本指南展示如何在不先发布版本或提交到`main`分支的情况下，在本地迭代`specify` CLI。

> 脚本现在有Bash（`.sh`）和PowerShell（`.ps1`）两个版本。CLI会根据操作系统自动选择，除非您传递`--script sh|ps`。

## 1. 克隆和切换分支

```bash
git clone https://github.com/GoooIce/spec-kit.git
cd spec-kit
# 在功能分支上工作
git checkout -b your-feature-branch
```

## 2. 直接运行CLI（最快反馈）

您可以通过模块入口点执行CLI，无需安装任何内容：

```bash
# 从仓库根目录
python -m src.specify_cli --help
python -m src.specify_cli init demo-project --ai claude --ignore-agent-tools --script sh
```

如果您喜欢调用脚本文件样式（使用shebang）：

```bash
python src/specify_cli/__init__.py init demo-project --script ps
```

## 3. 使用可编辑安装（隔离环境）

使用`uv`创建隔离环境，这样依赖关系的解析就像最终用户获得的一样：

```bash
# 创建并激活虚拟环境（uv自动管理.venv）
uv venv
source .venv/bin/activate  # 或在Windows PowerShell上：.venv\Scripts\Activate.ps1

# 以可编辑模式安装项目
uv pip install -e .

# 现在'specify'入口点可用
specify --help
```

由于可编辑模式，代码编辑后重新运行不需要重新安装。

## 4. 直接从Git调用uvx（当前分支）

`uvx`可以从本地路径（或Git引用）运行以模拟用户流程：

```bash
uvx --from . specify init demo-uvx --ai copilot --ignore-agent-tools --script sh
```

您也可以将uvx指向特定分支而不合并：

```bash
# 首先推送您的工作分支
git push origin your-feature-branch
uvx --from git+https://github.com/GoooIce/spec-kit.git@your-feature-branch specify init demo-branch-test --script ps
```

### 4a. 绝对路径uvx（从任何地方运行）

如果您在另一个目录中，使用绝对路径而不是`.`：

```bash
uvx --from /mnt/c/GitHub/spec-kit specify --help
uvx --from /mnt/c/GitHub/spec-kit specify init demo-anywhere --ai copilot --ignore-agent-tools --script sh
```

为方便起见设置环境变量：
```bash
export SPEC_KIT_SRC=/mnt/c/GitHub/spec-kit
uvx --from "$SPEC_KIT_SRC" specify init demo-env --ai copilot --ignore-agent-tools --script ps
```

（可选）定义shell函数：
```bash
specify-dev() { uvx --from /mnt/c/GitHub/spec-kit specify "$@"; }
# 然后
specify-dev --help
```

## 5. 测试脚本权限逻辑

运行`init`后，检查shell脚本在POSIX系统上是否可执行：

```bash
ls -l scripts | grep .sh
# 期望所有者执行位（例如-rwxr-xr-x）
```
在Windows上，您将使用`.ps1`脚本（不需要chmod）。

## 6. 运行Lint/基本检查（添加您自己的）

目前没有捆绑强制的lint配置，但您可以快速检查可导入性：
```bash
python -c "import specify_cli; print('Import OK')"
```

## 7. 本地构建Wheel（可选）

在发布之前验证打包：

```bash
uv build
ls dist/
```
如果需要，将构建的工件安装到新的一次性环境中。

## 8. 使用临时工作区

在脏目录中测试`init --here`时，创建临时工作区：

```bash
mkdir /tmp/spec-test && cd /tmp/spec-test
python -m src.specify_cli init --here --ai claude --ignore-agent-tools --script sh  # 如果仓库复制到这里
```
或者如果您想要轻量级沙盒，只复制修改的CLI部分。

## 9. 调试网络/TLS跳过

如果您在实验时需要绕过TLS验证：

```bash
specify check --skip-tls
specify init demo --skip-tls --ai gemini --ignore-agent-tools --script ps
```
（仅用于本地实验。）

## 10. 快速编辑循环摘要

| 动作 | 命令 |
|--------|---------|
| 直接运行CLI | `python -m src.specify_cli --help` |
| 可编辑安装 | `uv pip install -e .` 然后 `specify ...` |
| 本地uvx运行（仓库根目录） | `uvx --from . specify ...` |
| 本地uvx运行（绝对路径） | `uvx --from /mnt/c/GitHub/spec-kit specify ...` |
| Git分支uvx | `uvx --from git+URL@branch specify ...` |
| 构建wheel | `uv build` |

## 11. 清理

快速删除构建工件/虚拟环境：
```bash
rm -rf .venv dist build *.egg-info
```

## 12. 常见问题

| 症状 | 修复 |
|---------|-----|
| `ModuleNotFoundError: typer` | 运行 `uv pip install -e .` |
| 脚本不可执行（Linux） | 重新运行init或 `chmod +x scripts/*.sh` |
| Git步骤被跳过 | 您传递了 `--no-git` 或Git未安装 |
| 下载了错误的脚本类型 | 明确传递 `--script sh` 或 `--script ps` |
| 企业网络上的TLS错误 | 尝试 `--skip-tls`（不用于生产） |

## 13. 下一步

- 更新文档并使用您修改的CLI运行快速开始
- 满意后开启PR
- （可选）更改落地到`main`后标记版本
