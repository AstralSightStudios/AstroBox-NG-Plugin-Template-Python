# AstroBox 插件模板（Python）

AstroBox **API Level 4** 的 Python 插件模板。用
[componentize-py](https://github.com/bytecodealliance/componentize-py)
把 Python 代码编译成 WebAssembly Component。

## 为什么 Python 能用

Level 4 的 WIT 接口全部是 `async func`，componentize-py 0.25 起完整支持组件模型的
async（WASIp3），宿主接口在 Python 侧就是普通的 `await`：

```python
arch = await host_os.arch()
```

> JavaScript 暂不可用：ComponentizeJS 尚未实现 `async func`，遇到就会
> `not yet implemented`。详见文档里的语言选择章节。

## 环境准备

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install componentize-py==0.25.1
```

再把 WIT 拉下来（作为 submodule）：

```bash
git submodule update --init --recursive
```

## 构建

```bash
python scripts/build_dist.py            # 构建到 dist/
python scripts/build_dist.py --package  # 顺便打成 .abp
```

## 目录

```
.
├── manifest.json     # 插件清单（api_level 必须是 4）
├── scripts/          # 构建脚本
├── src/app.py        # 插件入口（你主要改这里）
└── wit/              # (submodule) WIT 接口定义
```

## 注意

- **类名必须叫 `Lifecycle` / `Event`**：componentize-py 按 WIT 里的导出接口名在
  入口模块里找实现类，名字对不上就会报「Can't instantiate abstract class」。
- 产物体积约 20 MB（内嵌 CPython），首次加载时宿主会预编译并缓存，之后启动很快。
