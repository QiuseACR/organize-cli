# organize-cli

按扩展名把目录里的文件归档到子目录。一条命令收拾下载文件夹。

## 怎么跑

```bash
# 先空转，只看计划，不动文件
py organize.py "%USERPROFILE%\Downloads"

# 确认计划没问题，再真移动
py organize.py "%USERPROFILE%\Downloads" --apply
```

## 效果

```
PLAN 照片.jpg -> 图片/
PLAN 报告.pdf -> 文档/
PLAN 备份.zip -> 压缩包/
PLAN 笔记.txt -> 文档/
PLAN 视频.mp4 -> 音视频/
PLAN 未知.xyz -> 其他/

共 6 个文件，仅计划（加 --apply 执行）
```

## 设计要点

- **默认安全**：不带 `--apply` 只打印，永远先看计划
- **零依赖**：只用标准库 `pathlib` 和 `argparse`
- **认不出的后缀**：统一进 `其他/`，日志一眼能看出规则漏了哪个
- **撞名保护**：目标位置已有同名文件就跳过并提示，不覆盖

## 改规则

编辑 `RULES` 字典即可，键是目录名，值是后缀集合：

```python
RULES = {
    "图片": {".jpg", ".png"},
    "文档": {".pdf", ".txt"},
}
```

## 环境

Python 3.9+，Windows / macOS / Linux 通用。

Windows 上如果把输出交给别的程序捕获（管道、IDE 面板），中文会显示成乱码，因为 Python 按 `cp936` 编码吐出，对方按 UTF-8 解读。加一个环境变量就正常：

```cmd
set PYTHONUTF8=1
py organize.py "%USERPROFILE%\Downloads"
```

在普通 cmd 窗口里直接跑，中文正常显示，这条可以跳过。