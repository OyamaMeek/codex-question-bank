# 工具

李林高数上册分节题集按微分、积分、微分方程分区编写解析，主代理处理函数与极限并统一编译。复用 Tectonic、ctex、markdown-it-py、PyMuPDF 和既有 KaTeX；用户授权后核对原题图片及最终 PDF 渲染页，记录于 `.agent/visual/`。

线性代数第七版使用现有 PyMuPDF、macOS Vision OCR 可执行文件及识别缓存，由单一代理处理，不新增依赖。

中值定理阶段三套模拟卷由单一代理选编和解析。复用 ctex、amsmath、应用内 Tectonic 与项目缓存；采用源稿检查、数学复算和 PDF 文字几何验证。使用 PDF 与 Ponytail 技能；不调用子代理、截图或图像检查。

本次分节真题详细解析按章节使用并行代理技能分区校订，主代理统一评级规则、题头、检查和编译。使用已有 Tectonic、PyMuPDF 与 Python 标准库；不进行截图或图像检查。

使用 PyMuPDF 提取 PDF 文字层，使用 macOS Vision 在本机识别扫描页。源 PDF 保留在原目录。

本次张宇往年八套由单一代理逐题检查，使用 PyMuPDF 原页图和文字层、嵌入图示哈希及现有 KaTeX 脚本验证，未调用其他代理。

数学模拟卷补用本机 MLX PaddleOCR 生成候选，再逐题对照源 PDF 修正；候选不能作为完成证据。使用 KaTeX 验证 Markdown 公式渲染。往年合集按独立文件分工校对，选填交付文件统一由一名代理组装。

阶段模拟卷使用 LaTeX 和 ctex 排版，使用桌面应用附带的 Tectonic 编译，使用 PyMuPDF 检查 PDF 题序和文本边界。

自动发布使用 GitHub Actions、Tectonic 0.17.0、Python 标准库和 GitHub CLI，PDF 作为 GitHub Release 附件分发。
