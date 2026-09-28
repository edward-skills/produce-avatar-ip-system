# 视觉预览

[English](preview-gallery.md) | 简体中文

这个预览页展示 Skill 能够产出什么，以及分阶段审批如何避免人物身份、头身比、服饰和场景漂移。图片来自两个独立的真实制作系统，用于证明风格跨度与工作流深度，不代表每次运行都要复制这些人物或画风。

## 系统 A｜柔和动漫科技感数字员工

这套较早的制作系统在更换岗位造型和使用场景时，持续保持四个角色各自可识别。第一张矩阵展示模块化服饰扩展：每一行始终是同一个人，只改变岗位对应的服装结构、颜色重点和配饰。

![四个持续身份与五套服饰系列](images/08-soft-anime-tech-outfit-matrix.jpg)

场景矩阵展示下一阶段：把已确认的人物身份与完整造型组合放入五类业务语境，包括活动发布、店铺运营、增长分析、履约处理和 AI 工作台。场景构图可以变化，但不能在放进场景时悄悄重画人物。

![四个持续身份与五类业务场景](images/09-soft-anime-tech-scene-matrix.jpg)

动画源帧板包含二十张用于短循环视频的场景首帧。真实运行时，必须先选择一个代表性图生视频结果，完成身份、循环与动作质量确认，才可以批量渲染其余视频。

![二十张循环动画源帧](images/10-soft-anime-tech-motion-source-frames.jpg)

## 系统 B｜酷感可爱的新街头收藏玩具

后续质量验证案例探索了更概括、低拟人度、强调潮流穿搭的收藏玩具方向。已确认风格源图组合了可爱的大头身比、简化的五官结构、深海军蓝与电光蓝发色，以及紧凑的新街头轮廓。

![酷感可爱的新街头数字人](images/00-digital-human-ip-neo-street-tech.png)

概念方向板说明了为什么 Skill 会先生成真正有差异的风格方向，而不是一开始就铺满整套服饰。用户先确认一种方向，之后才分别确认并扩展身份结构、性别呈现、服饰、道具、场景和视频。

![三个差异明确的视觉方向](images/01-style-directions.png)

## 不只展示成品，也保留纠偏证据

下面的对照记录了一个常见问题：画面技术质量合格，不等于还是同一个人物。评审板必须比较脸部几何、眼距、头部大小、发型轮廓、头部倾斜和身体结构，而不能只看画面是否精致。

![人物身份漂移与恢复对照](images/02-identity-drift-and-recovery.png)

服饰恢复板把同一原则应用到穿搭：中性基础人物不是最终标志造型，随意替换的通用服装也不能继承人物身份阶段的审批结果。

![标志性穿搭漂移与恢复对照](images/03-signature-look-recovery.png)

## 分阶段审批制作框架

![从想法到可复用 IP 系统的分阶段审批流程](images/04-workflow-gates.svg)

![可复用的项目合同与评审记录](images/05-contract-templates.svg)

![可组合 IP 参数模板的独立维度](images/06-ip-template-stack.svg)

![头身比与身体结构模板](images/07-proportion-and-body-templates.svg)

模板维度刻意保持独立。用户可以分别更换渲染风格、头身比、性别呈现、身体结构、脸型、发型、服饰、穿戴、道具、配色或构图，而不会把某一张示例图变成固定人物模板。稳定 ID 位于 [`ip-template-catalog.json`](../produce-avatar-ip-system/assets/templates/ip-template-catalog.json)，工作流规则位于 [`ip-template-system.md`](../produce-avatar-ip-system/references/ip-template-system.md)。

## 复现结构化评审流程

初始化可以中途续接的制作工作区：

```bash
python produce-avatar-ip-system/scripts/init_avatar_project.py ./my-avatar-project \
  --project-name my-avatar-project \
  --personas 4
```

把选定的参数组合解析成阶段提示词和机器可读回执：

```bash
python produce-avatar-ip-system/scripts/assemble_avatar_prompt.py \
  ./my-avatar-project/brief/ip-template-selection-p01.json \
  --catalog ./my-avatar-project/brief/ip-template-catalog.snapshot.json \
  --stage neutral-base \
  --output ./my-avatar-project/prompts/p01-neutral-base.txt \
  --resolved-output ./my-avatar-project/prompts/p01-neutral-base.resolved.json
```

用候选图片或视频代表帧制作带标签的评审板：

```bash
python produce-avatar-ip-system/scripts/build_review_sheet.py \
  ./my-avatar-project/candidates/identity/*.png \
  --output ./my-avatar-project/review/contact-sheets/identity-review.png \
  --columns 4 \
  --title "人物身份结构评审"
```

只有已确认资产才能进入下一阶段。上面的图片是经过筛选的公开预览；仓库不包含凭证、签名链接、私有 Figma 源文件地址或第三方客户源素材。
