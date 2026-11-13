# 李林高数上册分节题集检查

2026-11-13。用户已明确授权查看原题图并检查 PDF 排版。涉及文件：`output/李林高数上册分节题集.tex`、同名 PDF 及 `output/lilin-figures/`。最终 PDF 页面为 800×600 bp，以下渲染图均为 1200×900 像素，非空。

## 最终 PDF

| 页面 | 图片 | 观察结果 |
| --- | --- | --- |
| 目录，第1页 | [目录](lilin-ipad-contents.png) | 四章19节目录、题数与说明均在同页，页脚完整。 |
| 第26题，第52页 | [极限题](lilin-ipad-question.png) | 分数上下排列，lim 条件位于下方；题下留白，未出现解析。 |
| 第26题解析，第53页起 | [解析](lilin-ipad-solution.png) | 解析独立分页，公式、文字和页眉页脚均在页面内。 |
| 第202题 | [图题](lilin-ipad-graph-question.png) | 原导函数曲线可辨认，选项与图示完整，下方留有手写区域。 |
| 第202题解析 | [图题解析](lilin-ipad-graph-solution.png) | 逐个检查导数变号及零点接合点，与题页分开。 |
| 多小问积分解析 | [积分解析](lilin-ipad-long-solution.png) | 检查公式与文字边界，无重叠或截断；完整解析由源稿及逐页检查确认。 |
| 第212题 | [留白最少题页](lilin-ipad-dense-question.png) | 曲线和选项可辨认，题下仍留约150bp空白。 |

全部页面另用文字和图形坐标检查题解对应、800×600bp尺寸、内容边界及书签；编译日志检查缺字、警告和溢出。渲染抽查不代表 iPad 实机测试，也不代替数学推导复核。

## 原题疑点

以下图片来自讲义原 PDF，均为 842×596 像素，非空。对应文件为生成后的 LaTeX 题面及解析。

- [原第77页](lilin-condition-source-77.png)：分段函数右支分母为四分之一乘以 x²；据此恢复题面，连续参数为 −1。
- [原第164页](lilin-condition-source-164.png)：右端确为三阶导数；恢复第三撇，并给出三次 Rolle 定理证明。
- [原第469页](lilin-condition-source-469.png)：方程为三阶线性方程；恢复各项正确阶数。

其余条件疑点见 [微分方程原页记录](lilin-condition-ode-review.md)，积分公式与几何图形见 [积分原页记录](lilin-integrals-source-review.md)。
