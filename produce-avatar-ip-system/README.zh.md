# Produce Avatar IP System Skill

这是可直接安装的 Agent Skill 包。它可以从用户的一句话想法开始，经过独立确认节点，逐步产出：

1. 基础 IP 方向和身份母版；
2. 配色、服装、穿戴设备、道具和组合形象；
3. 透明场景主体、可替换背景和组合预览；
4. 动画样片，以及确认后的批量循环视频；
5. Figma 组件、提示词合同、资产清单和 QA 报告。

入口是 [`SKILL.md`](SKILL.md)。跨 Agent 状态机与 ready 标准见 [`portability-and-readiness.md`](references/portability-and-readiness.md)，真实工具和模型审计见 [`tool-provenance.md`](references/tool-provenance.md)。

1.2 版补全了真正的 IP 参数模版，而不是固化一张示例人物图。渲染风格、头身比、性别呈现、身体结构、脸型、发型、服饰、穿戴、道具、配色和构图都有可独立组合的 ID；性别呈现与胸廓/肩宽/躯干结构分开选择。阶段解析器会生成可复现的 prompt，并在基础人物阶段强制回到正视、零歪头、完整头顶、简单 T 恤、无道具和无最终造型。1.1 版的代表角色双验证和审批门仍然保留。

可以直接初始化一个可续接的项目：

```bash
python scripts/init_avatar_project.py ./my-avatar-project \
  --project-name my-avatar-project \
  --personas 4
```

随后可以从生成的参数选择文件组装阶段 prompt：

```bash
python scripts/assemble_avatar_prompt.py \
  ./my-avatar-project/brief/ip-template-selection-p01.json \
  --catalog ./my-avatar-project/brief/ip-template-catalog.snapshot.json \
  --stage neutral-base
```

该 Skill 按能力而不是单一平台路由。缺少 ImageGen、Figma、Aident、Pillow 或 FFmpeg 时，Agent 必须明确交付到哪一步、哪些内容仍待处理，不得把提示词、海报帧或未更新的 Figma 文件描述成完整成品。

安装：

```bash
npx skills add Edward-J-create/produce-avatar-ip-system \
  --skill produce-avatar-ip-system
```

该包已通过公开 `skills` CLI 对 Codex、Claude Code、Cursor 和 OpenCode 做安装冒烟测试。所有宿主共用同一份 `SKILL.md`、相对路径引用、模板和脚本；可选的 `agents/openai.yaml` 只增强 OpenAI 宿主的发现与界面展示，不是其他 Agent 的运行依赖。

MIT 许可证。仓库不包含原始人物素材、私有 Figma 文件、密钥或生成资产。
