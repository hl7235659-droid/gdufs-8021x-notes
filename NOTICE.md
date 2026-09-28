# 来源、署名与"未包含"清单

## 上游与致谢

| 项目 | 与本笔记的关系 | 许可 |
| --- | --- | --- |
| [updateing/minieap](https://github.com/updateing/minieap) | EAP 客户端与 **rjv3 插件**基础；本笔记描述的多数行为以它为参照 | GPL-3.0 |
| [jimlee2048/minieap-gdufs](https://github.com/jimlee2048/minieap-gdufs)（原 `jimlee2002`） | 广外（南校区）适配分支；本笔记的协议事实与它一致，并在其基础上补充了**客户端签名**部分 | GPL-3.0 |
| [hyrathb/mentohust](https://github.com/hyrathb/mentohust) | 锐捷 v3/v4 校验算法的历史来源（minieap 上游 README 声明） | GPL 系 |
| [ysc3839/openwrt-minieap](https://github.com/ysc3839/openwrt-minieap)、[luci-proto-minieap](https://github.com/ysc3839/luci-proto-minieap) | OpenWrt 打包与 LuCI 界面参考 | GPL-3.0 |

本笔记中"客户端签名"（`docs/signature.md`）部分为独立逆向所得，**不包含**厂商二进制、其片段或从其中直接复制的大段数据。

## 未包含（刻意的）

- 锐捷官方客户端任何文件或片段（安装包、`8021x.exe`、`RJIX.dll`、Linux `rjsupplicant` 等）；
- 任何抓包（`.pcap`/`.pcapng`）与其字段 dump；
- 任何账号、口令、验证口令派生值（例如报文里的口令派生属性）、校园 Wi-Fi 身份/密码；
- 任何设备标识：MAC、序列号（`Static:<serial>`）、主机名、SSID、内网地址与网关；
- 服务器提示文本中可定位到具体学校/个人的部分（仅保留诊断必需的通用句子）。

## 版本绑定声明

`docs/signature.md` 与 `docs/tables.md` 中给出的地址、常量、表维度，均属于**某一具体版本的 Windows 官方客户端**（记为 V6.86 代次）。
只要下列任一发生变化，就必须重新分析并重算：

1. 变体表 / 轮常量；
2. 被哈希的 `.text` 镜像长度（本版本为 2,809,856 字节）；
3. 镜像中那处 8 字节块密码变换的输入或输出（见 `docs/signature.md` 第 2 节）。

否则结论不成立，症状通常是服务器回 `0x53`「使用了非管理员指定的客户端!」。
