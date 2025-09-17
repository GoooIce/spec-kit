---
description: 使用计划模板执行实现计划工作流程以生成设计工件。
scripts:
  sh: scripts/bash/setup-plan.sh --json
  ps: scripts/powershell/setup-plan.ps1 -Json
---

根据作为参数提供的实现细节，执行以下操作：

1. 从仓库根目录运行 `{SCRIPT}` 并解析JSON以获取 FEATURE_SPEC、IMPL_PLAN、SPECS_DIR、BRANCH。所有未来的文件路径必须是绝对路径。
2. 阅读并分析功能规范以了解：
   - 功能需求和用户故事
   - 功能性和非功能性需求
   - 成功标准和接受标准
   - 提到的任何技术约束或依赖

3. 阅读 `/memory/constitution.md` 处的宪法以了解宪法要求。

4. 执行实现计划模板：
   - 加载 `/templates/plan-template.md`（已复制到 IMPL_PLAN 路径）
   - 将输入路径设置为 FEATURE_SPEC
   - 运行执行流程（主要）功能步骤1-9
   - 模板是自包含和可执行的
   - 按指定遵循错误处理和门控检查
   - 让模板指导 $SPECS_DIR 中的工件生成：
     * 阶段0生成 research.md
     * 阶段1生成 data-model.md、contracts/、quickstart.md
     * 阶段2生成 tasks.md
   - 将参数中用户提供的详细信息纳入技术上下文：{ARGS}
   - 完成每个阶段时更新进度跟踪

5. 验证执行完成：
   - 检查进度跟踪显示所有阶段完成
   - 确保生成了所有必需的工件
   - 确认执行中没有错误状态

6. 报告结果，包括分支名称、文件路径和生成的工件。

对所有文件操作使用带有仓库根目录的绝对路径以避免路径问题。
