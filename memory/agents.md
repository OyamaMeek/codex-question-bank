# 工具

同济线代同步测试卷由 FFmpeg 解码 HEIC，使用本机 RapidOCR（ONNX Runtime）提取文字，对照原图逐题校订，用 KaTeX 检查公式语法。

线性代数前两章模拟卷用 PyMuPDF 读取逐年原卷的文字与公式字形坐标，结合真题 Markdown、配套解析校核。扫描公式用本地 PaddleOCR-VL 提取候选并结合对应解析复核。使用 Tectonic 0.17.0、ctex 和双版式入口编译，用 Python 和 mpmath 复算并检查 PDF 页序与留白。

数学分析期中1115 使用 PyMuPDF 提取文字层和嵌入图片，使用本机 RapidOCR 识别题面，对照原卷逐题核对，并用既有 KaTeX 脚本检查公式。

数学分析期中1115 的 LaTeX 版复用 Tectonic 0.17.0、ctex 和双入口试卷模板。用 PyMuPDF 检查分页和字形坐标，用 mpmath 独立复算关键结果。

电子科技大学 2026 年数学分析试卷使用 CPU 版 RapidOCR 识别截图分区，对照放大的原图校勘公式。使用 Tectonic、ctex 编译两版，使用 PyMuPDF 核对分页与文字位置，使用 mpmath 独立复算关键结果。

李林高数上册分节题集按微分、积分、微分方程分区编写、评级和复核，主代理处理函数与极限并统一排序编译。复用 Tectonic、ctex、markdown-it-py、PyMuPDF 和既有 KaTeX；用户授权后核对原题图片及最终 PDF 渲染页，记录于 `.agent/visual/`。

线性代数第七版使用现有 PyMuPDF、macOS Vision、MLX PaddleOCR和ONNX Runtime；补充官方PP-DocLayoutV3版面模型，按正文和公式分别识别。采用dispatching-parallel-agents技能按章节对照原页校订，主代理统一组装与检查，避免各代理同时修改最终文件。

中值定理阶段三套模拟卷由单一代理选编和解析。复用 ctex、amsmath、应用内 Tectonic 与项目缓存；采用源稿检查、数学复算和 PDF 文字几何验证。使用 PDF 与 Ponytail 技能；不调用子代理、截图或图像检查。

本次分节真题详细解析按章节使用并行代理技能分区校订，主代理统一评级规则、题头、检查和编译。使用已有 Tectonic、PyMuPDF 与 Python 标准库；不进行截图或图像检查。

使用 PyMuPDF 提取 PDF 文字层，使用 macOS Vision 在本机识别扫描页。源 PDF 保留在原目录。

本次张宇往年八套由单一代理逐题检查，使用 PyMuPDF 原页图和文字层、嵌入图示哈希及现有 KaTeX 脚本验证，未调用其他代理。

数学模拟卷补用本机 MLX PaddleOCR 生成候选，再逐题对照源 PDF 修正；候选不能作为完成证据。使用 KaTeX 验证 Markdown 公式渲染。往年合集按独立文件分工校对，选填交付文件统一由一名代理组装。

阶段模拟卷使用 LaTeX 和 ctex 排版，使用桌面应用附带的 Tectonic 编译，使用 PyMuPDF 检查 PDF 题序和文本边界。

自动发布使用 GitHub Actions、Tectonic 0.17.0、Python 标准库和 GitHub CLI，PDF 作为 GitHub Release 附件分发。
