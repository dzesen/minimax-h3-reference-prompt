# MiniMax H3 Reference Prompt

一个面向 Codex 的 MiniMax H3 Ref2VA 提示词技能。它可以把中文、英文或混合语言的视频需求，编译成可直接使用的六段式 H3 full-reference prompt，也支持审查、修订和基于现有媒体的功能性反推。

## 能做什么

- 根据图片、视频、音频及文字需求生成 Ref2VA 六段式提示词。
- 明确分配多份参考素材的职责，减少身份、动作、镜头和声音互相串用。
- 审查已有 H3 Ref2VA prompt 的结构、标签、时码、素材映射和声音分层。
- 对已有 prompt 执行添加、替换、删除、移动和重定时，并重新编译所有依赖字段。
- 从图片、视频或音频重建可复用的 Ref2VA prompt，同时区分观察事实、合理推断和无法恢复的信息。
- 使用确定性校验器检查可静态证明的错误。

这个技能专注于 **Ref2VA full-reference 模式**。纯文字 T2VA、没有任何真实参考素材的请求，不应伪造 `<Picture N>`、`<Video N>` 或 `<Audio N>` 标签。

## 快速使用

在 Codex 中直接写：

```text
使用 $minimax-h3-reference-prompt，把以下需求整理成 MiniMax H3 Ref2VA 提示词。

时长 10 秒，9:16。
Picture 1 只负责女主角的脸、发型和服装。
Video 1 只负责动作节奏和从背后绕到人物左侧的相机路径。
不要新增人物、品牌、字幕或其他可读文字。
……
```

也可以使用自然语言触发，例如：

```text
把这张角色图和这段动作视频整理成 H3 的六段式 reference prompt。
```

```text
检查这份 MiniMax H3 Ref2VA 提示词有没有标签、镜头时间或音频分层问题。
```

```text
根据我上传的视频反推一份可继续生成的 H3 提示词，视频会继续作为参考素材使用。
```

## 是否必须提供图片

不一定必须是图片，但必须至少有一种会在 H3 生成时继续提供的真实参考素材：

- 图片可以提供人物身份、物体设计、环境、风格或具体关键帧。
- 视频可以提供动作、镜头、剪辑、节奏、编辑源或续写起点。
- 音频可以提供声音信号、音色、台词、歌词、节奏或音乐风格。

仅有参考音频而没有图片或视频存在官方可行性风险。技能会提示该风险，不会凭空制造视觉素材。

如果现有视频只用于观察，下一次生成时不会继续附加，则应该输出基于观察的文字重建 brief，再转为 H3 base-mode prompt，而不是留下无法解析的 Ref2VA 标签。

## 推荐输入方式

输入不需要先写成专业格式，但以下信息越明确，结果越稳定：

1. 目标时长和固定画幅要求。
2. 每份参考素材的顺序和职责。
3. 必须保留的人物、服装、产品或环境特征。
4. 每个镜头或动作的大致时间位置。
5. 相机相对谁或什么物体运动。
6. 必须逐字保留的台词、歌词、品牌文案或画面文字。
7. 环境声、动作声、画内音乐和观众专属配乐。
8. 明确禁止新增的角色、物体、品牌、文字或剧情。

多参考素材建议明确写成：

```text
Picture 1：只负责 Subject 1 的脸、发型和服装。
Picture 2：只负责场景灯光与空间布局，不转移其中的人物。
Video 1：只负责 Shot 1 的动作与镜头节奏，不提供身份、服装或品牌。
Audio 1：只参考女声的音色和克制语气，不复制原始信号。
```

当“从后方绕到侧面”等空间描述可能有两种解释时，最好写清它是相对人物、车辆、道具还是场景。

## 输出格式

生成或重编译结果包含以下六个字段，顺序固定：

```text
subject_definitions:

summary:

retention_analysis:

detailed_description:

overall_soundscape:

non_diegetic_music:
```

六段主体使用英文。用户提供的台词、歌词、专名、产品文案和可见文字保持原语言及原标点。

### 标签含义

| 标签 | 用途 |
|---|---|
| `<Subject N>` | 从参考素材中抽象出的可复用人物、物体、环境、服装、效果、风格、动作、姿势或表情 |
| `<Picture N>` | 图片本身承担首帧、末帧、关键帧、编辑帧、storyboard 或构图 anchor |
| `<Video N>` | 整段视频承担编辑源、续写起点、镜头、剪辑、节奏或时间结构 |
| `<Audio N>` | 音频信号被复制，或其音色、台词、歌词、节奏、音乐及声音质感被参考 |

图片只提供人物身份或风格时，通常在 `<Subject N>` 定义中引用该图片，不需要额外建立独立的 `<Picture N>` retention 项。

## 四种工作模式

### 1. 正向生成

提供参考素材及目标需求，技能会先建立内部素材职责和连续性蓝图，再输出六段式 prompt。

```text
使用 $minimax-h3-reference-prompt。
Picture 1 负责角色身份与服装，Video 1 只负责舞蹈动作。
生成 8 秒、9:16 的单人舞台表演，不要复制 Video 1 的人物、场景和品牌。
```

### 2. 审查

只指出高影响问题，不主动重写：

```text
使用 $minimax-h3-reference-prompt，只审查下面的 prompt，不要替我重写。
重点检查标签闭环、retention marker、时码、声音分层和未使用素材。
```

### 3. 修订

技能会从当前有效状态重新编译，不会在旧文本后追加“忽略前文”之类的修补句。

```text
把 Shot 2 整段删除，总时长从 10 秒改为 8 秒。
保留其他身份、服装、画幅和风格要求，并重新计算 Shot 编号、时码、retention 和声音提示。
```

支持的修订类型包括 `ADD`、`REPLACE`、`REMOVE`、`MOVE` 和 `RETIME`。

### 4. 反推重建

将现有媒体继续作为下一次生成的参考素材时，可以重建六段式 prompt：

```text
使用 $minimax-h3-reference-prompt 反推这段视频。
下一次 H3 生成时，这段视频仍会作为 Video 1 使用。
请保留它的镜头、节奏和动作结构，但替换人物身份与场景。
```

反推结果是功能性重建，不是原始 prompt 的恢复。原 wording、seed、sampler、隐藏参数、负面提示、缺失参考素材和创作者真实意图通常无法从成片证明。

## 平台限制

| 项目 | 限制 |
|---|---:|
| 目标视频时长 | 4–15 秒整数 |
| Prompt 长度 | 最多 7,000 个 Unicode 字符 |
| 参考图片 | 最多 9 张 |
| 参考视频 | 最多 3 段 |
| 参考音频 | 最多 3 段 |
| 混合参考文件 | 最多 12 个 |
| 单段参考视频或音频 | 2–15 秒 |
| 参考视频总时长 | 最多 15 秒 |
| 参考音频总时长 | 最多 15 秒 |
| API 请求体 | 最多 64 MB |

Ref2VA 未指定画幅时使用 `adaptive`。只有用户或交付平台明确要求时才锁定固定比例。

API transport role 与 prompt 标签不是同一层。`first_frame` 或 `last_frame` API role 不能和任何 `reference_*` role 混用；Ref2VA 中的 `<Picture N>` keyframe anchor 仍作为 reference image 上传。

超过 15 秒的项目需要缩短，或者拆成多条各自合法的 prompt，并明确上一段末态与下一段初态的衔接。

## 校验器

仓库包含不依赖第三方包的静态校验器：

```text
python scripts/validate_ref2va_prompt.py prompt.txt --duration 10 --picture-count 1 --video-count 0 --audio-count 0
```

已知参考媒体时长时，可以逐个传入：

```text
python scripts/validate_ref2va_prompt.py prompt.txt --duration 12 --picture-count 1 --video-count 1 --video-duration 8 --audio-count 1 --audio-duration 6
```

校验器可以检查：

- 六字段数量、顺序和非空状态。
- 7,000 字符和 4–15 秒限制。
- 标签编号、定义、后续使用和 retention 闭环。
- Visual 与 Audio retention marker family。
- Shot 编号、cut time 和内部时间范围。
- `<d>[Language] ...</d>`、speaker ID、`<scenetrans>`、`<cutoff>`。
- 素材数量、缺失附件、未映射附件和 API role 冲突。
- 已提供的参考媒体时长与请求体大小。

`ERROR` 表示可以静态证明的合同错误，退出码为 1。`WARNING` 表示需要人工判断的风险，只有 warning 时仍返回退出码 0。

校验器不能证明人物身份是否真的保持、动作是否物理可信、台词是否和用户原输入逐字一致、是否存在同义词形式的旧要求残留，或 H3 最终生成结果是否遵循 prompt。`PASS` 只覆盖文本和命令中实际提供的元数据。

运行测试：

```text
python -m unittest discover -s tests -v
```

## 安装与更新

仓库根目录就是技能目录，必须保留以下路径：

```text
minimax-h3-reference-prompt/
├── SKILL.md
├── README.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── format-spec.md
│   ├── reverse-reconstruction.md
│   └── revision-compiler.md
├── scripts/
│   └── validate_ref2va_prompt.py
└── tests/
    └── test_validator.py
```

在 Codex 中可以直接要求安装这个私有 GitHub 仓库中的技能。手动安装时，将完整目录复制到：

```text
$CODEX_HOME/skills/minimax-h3-reference-prompt
```

更新后重新打开任务即可使用新版；显式调用名称保持为：

```text
$minimax-h3-reference-prompt
```

## 常见问题

### 输入必须是中文吗？

不需要。输入可以是中文、英文或混合语言，输出六段结构主体统一为英文。

### Picture 1 一定是首帧吗？

不是。只有当图片本身被定义为具体 frame anchor 时，独立的 `<Picture 1>` 才承担首帧、末帧或关键帧职责。用于人物身份的 Picture 通常只是 `<Subject N>` 的来源。

### 每个 Shot 都必须有相机运动吗？

不需要。锁定机位是有效选择。相机运动应服务于动作、信息或构图变化，而不是为了让 prompt 看起来复杂。

### 350–500 英文词是硬限制吗？

不是。它是 reference-generation `detailed_description` 的通常范围。对白密集、视频编辑或源素材复杂度不同都会产生合理偏离，因此校验器只给 warning。

### 能恢复原始 prompt 吗？

不能保证。反推只能根据可见、可听和可测量证据重建功能相近的生产指令。

### 为什么不自动追加通用 negative prompt？

固定 negative dump 缺少可靠依据，也可能和用户目标冲突。技能优先写清期望终态，只在强模型先验确实会破坏硬要求时加入短而局部的限制。

## 进一步阅读

- [MiniMax H3 提示词与生成技能深度研究](https://github.com/dzesen/minimax-h3-reference-prompt/blob/main/docs/research-2026-08-29.md)
- [MiniMax-H3 官方仓库](https://github.com/MiniMax-AI/MiniMax-H3)
- [官方 Ref2VA 输出格式指南](https://github.com/MiniMax-AI/MiniMax-H3/blob/main/skills/h3-prompt-writing/references/ref-en.txt)
- [官方 H3 video skill](https://github.com/MiniMax-AI/cli/blob/main/skill/h3-video/SKILL.md)
