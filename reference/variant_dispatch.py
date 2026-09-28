#!/usr/bin/env python3
"""变体分派参考实现 + 向量自测（纯标准库，可离线运行）。

本文件只实现"从挑战得到变体号"这一步——它是自包含的，不需要任何厂商数据。
完整摘要（128 hex）的复现还需要客户端 `.text` 镜像与其中那处 8 字节块密码变换结果，
见 docs/signature.md §2 与 docs/tables.md。

用法:
    python reference/variant_dispatch.py                # 跑 vectors/vectors.json 的分派自测
    python reference/variant_dispatch.py --show-pitfall # 展示"负数取模"这个经典坑
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

VECTORS = pathlib.Path(__file__).resolve().parent.parent / "vectors" / "vectors.json"


def _s8(b: int) -> int:
    """按有符号 8 位解释一个字节（0x80..0xFF -> -128..-1）。"""
    return b - 256 if b >= 0x80 else b


def variant_of(challenge: bytes) -> int:
    """返回该 EAP-MD5 挑战对应的变体号（0..4）。

    契约：a = (uint32)(int8)c[1] + (uint32)(int8)c[4]（32 位回绕），然后 a % 5。
    """
    if len(challenge) != 16:
        raise ValueError(f"challenge 必须是 16 字节，收到 {len(challenge)}")
    a = (_s8(challenge[1]) + _s8(challenge[4])) & 0xFFFFFFFF
    return a % 5


def variant_of_naive_wrong(challenge: bytes) -> int:
    """**错误示范**：直接对负数取模（Python 语义与 C 的无符号除法不同）。

    保留它是为了说明为什么"看起来一样"的公式会算错——真实案例见 --show-pitfall。
    """
    return (_s8(challenge[1]) + _s8(challenge[4])) % 5


def run_self_test() -> int:
    data = json.loads(VECTORS.read_text(encoding="utf-8"))
    failures = 0
    print(f"{'向量':38} {'期望':>4} {'实得':>4}  判定   类别")
    print("-" * 72)
    for v in data["vectors"]:
        ch = bytes.fromhex(v["challenge_hex"])
        got = variant_of(ch)
        ok = got == v["expected_variant"]
        failures += 0 if ok else 1
        print(
            f"{v['name']:38} {v['expected_variant']:>4} {got:>4}  "
            f"{'OK  ' if ok else 'FAIL'}   {v['class']}"
        )
    print("-" * 72)
    if failures:
        print(f"分派自测失败 {failures} 项")
        return 1
    print("分派自测全部通过（注意：这只验证变体号，不验证摘要）")
    print("提示：摘要比对需要自备同代客户端镜像，见 docs/tables.md")
    return 0


def show_pitfall() -> int:
    # 这条挑战来自 vectors.json 的 official V6.86 · variant 2：正确的变体号是 2，
    # 而"负数取模"的写法会算成 1。
    ch = bytes.fromhex("e715920da1f2412acc8911ddbae532c9")
    right, wrong = variant_of(ch), variant_of_naive_wrong(ch)
    print(f"challenge        : {ch.hex()}")
    print(f"in16[1]          : 0x{ch[1]:02x} -> {_s8(ch[1])}")
    print(f"in16[4]          : 0x{ch[4]:02x} -> {_s8(ch[4])}")
    print(f"正确（无符号回绕）: {right}")
    print(f"错误（负数取模）  : {wrong}")
    return 0 if right != wrong else 2


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--show-pitfall", action="store_true", help="展示负数取模陷阱")
    args = ap.parse_args()
    return show_pitfall() if args.show_pitfall else run_self_test()


if __name__ == "__main__":
    sys.exit(main())
