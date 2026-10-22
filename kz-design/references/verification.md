---
name: verification
description: "kz-design 交付前验证清单。"
version: 1.0.2
---

# 验证清单

> **版本**: v1.0.2
> **用途**: 在交付视觉产物前完成最小浏览器、截图、交互和导出检查

## 最小验证

- HTML 文件能在目标方式打开：file URL、local dev server 或用户指定环境。
- 页面非空白，首屏没有明显错位、遮挡、缺字体、缺图或控制台 error。
- 文字不溢出容器，不压住按钮、图表、设备框、字幕或后续内容。
- 关键图像加载成功，且不是低分辨率拉伸。
- 交互元素有 hover/active/focus 或清楚状态反馈。

## Playwright 建议

可用以下方式做截图或点击验证，按项目实际路径调整：

```bash
npx playwright screenshot file:///absolute/path/to/demo.html /absolute/path/to/screenshot.png --viewport-size=1440,1000
```

交互原型至少覆盖：

- 进入详情或下一步
- tab / segmented control 切换
- modal / drawer / tooltip / annotation 打开关闭
- 主 CTA 是否能触发预期状态

## 固定画布验证

幻灯片、海报、动画 stage、设备框等固定格式产物需要额外检查：

- 画布比例正确，没有滚动条污染。
- 全部内容都在安全区内。
- 截图或导出后文字仍可读。
- 宽屏和窄屏预览都没有关键元素重叠。
- 固定画布需要缩放容器时，缩放只影响外层 stage，不让内部元素因视口变化重新排版。
- 幻灯片背景优先落在根画布上，不额外嵌套满屏背景层制造遮挡和 z-index 风险。

## 导出保真验证

PDF、PPTX、图片包、打印型报告等静态导出物不能只看浏览器截图，还要检查实际导出结果：

- 导出文件能打开，页数、比例、分页和安全区符合预期。
- 文字保持清晰；PDF/文档型产物优先保留文字可选择能力，不用整页截图替代文本。
- 链接、二维码、脚注、图表来源和图片说明没有在导出后丢失。
- 图片数量和关键图表与源页面一致，没有空白、低清拉伸或被裁切。
- 静态导出不要依赖 hover、transition、auto animation 或运行时图表才能理解。
- 图表用于 PDF/PPTX 时优先预渲染或确认目标导出链路能稳定保留，并记录图表保留情况；不把动态 canvas 当成唯一信息载体。

## 动画 / 视频验证

- 首帧不黑屏，末帧有明确收束。
- 录制模式下不显示调试按钮、进度条或浏览器 chrome。
- Canvas 或 Three.js 场景非空、在视口内、确实有运动或交互。
- 若用户要求音频，最终文件必须有 audio stream。
- GIF 需要检查 palette、循环和文件大小。

## 交付说明

最终回复只保留高信号信息：

- 产物路径或可访问 URL
- 已完成的验证动作
- 当前仍是 placeholder 的素材或假设
- 用户下一步最该检查的 1-3 件事

## 验证记录模板

每个设计产物默认写入 `${DESIGN_OUTPUT_DIR}/validation-notes.md`：

```markdown
# Validation Notes

## Artifact
- Main file:
- Output directory:
- Export files:

## Checks Run
- Command:
- Screenshot:
- Interaction path:
- Console errors:

## Known Gaps
- Placeholder assets:
- Unverified assumptions:
- User review needed:
```

## 版本历史

- **v1.0.2** (2026-05-31) - 新增固定画布与静态导出保真验证，覆盖分页、文字可选择、链接和图表保留。
- **v1.0.1** (2026-05-30) - 新增 `validation-notes.md` 记录模板，补齐交付验证证据格式。
- **v1.0.0** (2026-05-30) - 初始版本：定义 kz-design 的最小验证闭环。
