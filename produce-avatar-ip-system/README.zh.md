# Produce Avatar IP System Skill

这是可直接安装的 Agent Skill 包。它可以从用户的一句话想法开始，经过独立确认节点，逐步产出：

1. 基础 IP 方向和身份母版；
2. 配色、服装、穿戴设备、道具和组合形象；
3. 透明场景主体、可替换背景和组合预览；
4. 动画样片，以及确认后的批量循环视频；
5. Figma 组件、提示词合同、资产清单和 QA 报告。

入口是 [`SKILL.md`](SKILL.md)。跨 Agent 状态机与 ready 标准见 [`portability-and-readiness.md`](references/portability-and-readiness.md)，真实工具和模型审计见 [`tool-provenance.md`](references/tool-provenance.md)。

该 Skill 按能力而不是单一平台路由。缺少 ImageGen、Figma、Aident、Pillow 或 FFmpeg 时，Agent 必须明确交付到哪一步、哪些内容仍待处理，不得把提示词、海报帧或未更新的 Figma 文件描述成完整成品。

安装：

```bash
npx skills add Edward-J-create/produce-avatar-ip-system \
  --skill produce-avatar-ip-system
```

MIT 许可证。仓库不包含原始人物素材、私有 Figma 文件、密钥或生成资产。
