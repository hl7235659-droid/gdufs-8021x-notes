# reference/ —— 参考实现

## 这里有什么

| 文件 | 内容 | 需要外部数据吗 |
| --- | --- | --- |
| `variant_dispatch.py` | 变体分派（挑战 → 变体号 0..4）+ 对 `vectors/vectors.json` 的自测 + `--show-pitfall` 演示"负数取模"陷阱 | 不需要，纯标准库 |
| `README.md` | 本文件：为什么不提供完整摘要实现 | — |

跑法：

```sh
python reference/variant_dispatch.py
python reference/variant_dispatch.py --show-pitfall
```

## 为什么不提供"完整摘要实现"

摘要（属性 `0x4d`/`0x60` 的 128 个 hex 字符）的输入包含：

1. **客户端自身的 `.text` 镜像**（本代次 2,809,856 字节）；
2. 该镜像上一处 **8 字节块密码变换**的结果；
3. 若干**从客户端二进制里提取的表**（`MIXT`、打包/解包系数、Whirlpool 的表与轮常量、三个摘要常量）。

这三类都是**厂商二进制派生的数据**：本笔记选择只公开"算法结构 + 常量位置 + 提取与验证方法"，
不随仓库分发这些数据（理由见 `../docs/limits.md` §3、`../docs/tables.md`）。

因此读者要自己完成的部分是：**定位 → 提取 → 自校验**。算法结构见 `../docs/signature.md`，
提取思路见 `../docs/tables.md` §3，验证用 `../vectors/vectors.json`（先跑分派，再比摘要）。

## 一个完整实现大致会有的形状

```
dispatch(challenge)            -> variant            # 本仓库已给
blob_load()                    -> bytes             # 从你自己那份客户端取 .text 镜像
image_transform(blob)          -> bytes             # 那处 8 字节块密码变换（按同样方式取值）
primitive_p1/p2/p3/p4(...)     -> bytes             # 四个被改写的分组原语
slice_transform_493a30(...)    -> bytes             # 位切片变换（需要提取的表）
assemble(variant, challenge, blob) -> 128 hex chars # 各变体的拼装与输出切分
```

建议把"表"放在独立文件里并标注其来源版本；一旦客户端升级（见 `../docs/signature.md` §7），
换表比改算法更常见。
