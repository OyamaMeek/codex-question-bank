# 工具

使用 PyMuPDF 提取 PDF 文字层，使用 macOS Vision 在本机识别扫描页。源 PDF 保留在原目录。

阶段模拟卷使用 LaTeX 和 ctex 排版，使用桌面应用附带的 Tectonic 编译，使用 PyMuPDF 检查 PDF 题序和文本边界。

自动发布使用 GitHub Actions、Tectonic 0.17.0、Python 标准库和 GitHub CLI，PDF 作为 GitHub Release 附件分发。
