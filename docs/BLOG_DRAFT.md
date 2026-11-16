# EE308FZ 极限编程作业博客共用草稿（双人协作版）

> 说明：本草稿已对齐当前仓库真实代码与结构，供两位成员（`832402220`、`832402216`）同步编写和核对。根据课程要求，双人团队可共用一份 Markdown 草稿准备内容，但**两名同学需分别发布各自的个人博客**，发布前请将 `[待填写]` 替换为最终真实截图、链接、提交统计、贡献比例与各自真实的 PSP 耗时，并删去本提示段落。

| Item | Content |
| --- | --- |
| Course for This Assignment | Software Engineering (FZU–MU) |
| Team Name | `[填写团队名称]` |
| Assignment Requirements | [Extreme Programming](https://bbs.csdn.net/topics/620593436) |
| Objectives of This Assignment | 实现支持联系人收藏、多种联系方式与 Excel 导入导出的通讯录应用，并实践模块划分、Git Fork/PR 协作、版本发布与 PSP 过程管理 |
| Other References | [代码规范](https://github.com/w1457344108-coder/832402220_832402216_EE308FZ_ExtremeProgramming/blob/main/docs/CODE_STYLE.md)、[项目 README](https://github.com/w1457344108-coder/832402220_832402216_EE308FZ_ExtremeProgramming/blob/main/README.md) |

## 目录

- [1. 项目地址与运行说明](#1-项目地址与运行说明)
- [2. 模块划分与团队分工](#2-模块划分与团队分工)
- [3. 功能实现思路](#3-功能实现思路)
- [4. 程序运行截图与完整运行视频](#4-程序运行截图与完整运行视频)
- [5. GitHub 提交历史与版本发布](#5-github-提交历史与版本发布)
- [6. 成员贡献比例评估](#6-成员贡献比例评估)
- [7. 合作过程中遇到的困难与解决办法](#7-合作过程中遇到的困难与解决办法)
- [8. PSP 个人软件过程记录表](#8-psp-个人软件过程记录表)

---

## 1. 项目地址与运行说明

| 材料 | 链接 / 说明 |
| --- | --- |
| GitHub 仓库地址 | https://github.com/w1457344108-coder/832402220_832402216_EE308FZ_ExtremeProgramming |
| 代码规范链接 | https://github.com/w1457344108-coder/832402220_832402216_EE308FZ_ExtremeProgramming/blob/main/docs/CODE_STYLE.md |
| 协作流程说明 | https://github.com/w1457344108-coder/832402220_832402216_EE308FZ_ExtremeProgramming/blob/main/docs/COLLABORATION.md |
| Pull Request 链接 | `[合并队友 PR 后填写真实 PR URL]` |
| Release 版本链接 | `[发布 v1.0.0 后填写真实 Release URL]` |
| 在线访问地址（如完成云部署） | `[完成云部署后填写真实公网 URL；若未部署请据实说明]` |

### 技术栈与本地构建运行方式

- **后端**：Python 3、Flask、SQLite、`openpyxl`
- **前端**：HTML5、CSS3、原生 JavaScript（单页交互界面）
- **测试**：`pytest`

运行步骤：

```bash
git clone https://github.com/w1457344108-coder/832402220_832402216_EE308FZ_ExtremeProgramming.git
cd 832402220_832402216_EE308FZ_ExtremeProgramming
pip install -r requirements.txt
pytest -v
python3 app.py
```

启动后在浏览器访问 `http://127.0.0.1:5000`。

---

## 2. 模块划分与团队分工

项目采用分层模块化结构，将数据库持久化、Excel 导入导出、HTTP 接口路由与前端交互界面分离：

```text
address_book/
├── __init__.py       # Flask 应用工厂、SQLite 初始化与上传大小限制
├── db.py             # contacts / contact_methods 双表结构及 CRUD、收藏状态操作
├── excel_service.py  # Excel 导出、模板生成、表头别名解析与导入校验
└── routes.py         # REST API（/api/contacts、/favorite、/export、/import 等）
templates/index.html  # 主界面与新增/编辑、Excel 导入弹窗
static/css/style.css  # 响应式卡片布局、收藏高亮与表单样式
static/js/app.js      # 动态联系方式表单、收藏切换筛选与文件上传交互
tests/                # API、持久化与 Excel 往返导入导出自动化测试
```

| 成员学号 | 负责模块与工作内容 | 对应文件 / 交付物 |
| --- | --- | --- |
| `832402220` | 仓库搭建、数据库设计、核心后端 API、多种联系方式与 Excel 导入导出、基础前端界面与核心测试 | `address_book/*.py`、`templates/index.html`、`static/*`、`tests/*`、`docs/CODE_STYLE.md` |
| `832402216` | `[根据队友最终 PR 实际改动填写，例如：Fork 仓库评审、边界测试用例补充、界面交互优化 / 示例数据完善 / 协同验证与博客整理]` | `[填写队友 PR 中修改的文件与验证记录]` |

---

## 3. 功能实现思路

### 3.1 页面样式与交互布局

前端采用顶部工具栏 + 视图切换标签栏 + 响应式联系人卡片网格布局（`static/css/style.css`）：

- 顶部提供 `Load Demo`（加载示例数据）、`Template`（下载导入模板）、`Import Excel`、`Export Excel` 与 `+ New Contact` 快捷操作。
- 中部提供 `All Contacts` 与 `★ Bookmarked` 视图切换及实时搜索、排序（按收藏优先、姓名 A–Z、最近更新）。
- 每张操作反馈均通过右下角 Toast 提示呈现。

### 3.2 联系人收藏（Bookmark Contacts）

- 数据库 `contacts` 表设置 `is_favorite` 字段（`0` / `1`）并建立 `(is_favorite, name)` 索引（`address_book/db.py`）。
- 后端提供专用接口 `PATCH /api/contacts/<id>/favorite` 支持一键切换或显式设置收藏状态，同时在 `GET /api/contacts?favorite=1` 中返回收藏联系人列表与统计数（`total_count`、`favorite_count`）。
- 前端每张联系人卡片右上角提供 `★ / ☆` 按钮，收藏后卡片呈现金色边框高亮，并可通过顶部 `★ Bookmarked` 标签页快速筛选访问。

### 3.3 多种联系方式（Multiple Contact Methods）

- 通过 `contacts`（1）对 `contact_methods`（N）的一对多外键关联（`ON DELETE CASCADE`）存储任意数量的联系方式，每条记录包含 `method_type`（`phone`、`email`、`social`、`address`、`other`）、`label`（如 `Mobile`、`Work`、`WeChat`、`Home`）和 `value`。
- 前端弹窗支持通过 `+ Add Method` 动态增删多条联系方式行，保存时由后端统一校验并按 `sort_order` 顺序更新。

### 3.4 Excel 导入与导出（Import and Export）

- **导出（`export_contacts_to_xlsx`）**：使用 `openpyxl` 生成 `.xlsx` 文件，确保**每位联系人占一行、每类信息占一列**，列顺序为：`Name`、`Favorite`、`Company`、`Title`、`Phone Numbers`、`Emails`、`Social Media`、`Addresses`、`Other Contacts`、`Notes`。同一类别的多条联系方式按 `Label: Value; ...` 格式组织；单元格设置 `number_format = "@"` 文本格式，避免 `0591-...`、`0086...` 等带前导零的电话号码在 Excel 中丢失前导零。
- **导入（`import_contacts_from_xlsx`）**：校验 `.xlsx` 文件有效性及首行必须包含 `Name` 列（兼容常见中英文表头别名），解析各列多条联系方式并保留含 `https://` 的完整链接，支持跳过空行或缺失姓名的异常行并返回 `imported_count`、`skipped_count` 与 `errors` 明细。

---

## 4. 程序运行截图与完整运行视频

> 以下位置请插入本地或云端真实运行截图与最终视频链接（建议按：启动页面 → 新建含多种联系方式的联系人 → 收藏与收藏视图筛选 → 导出 Excel 并展示表格 → 修改/导入示例 Excel 并核对结果 的顺序录制）。

- **主界面与联系人列表截图**：`[插入截图]`
- **添加/编辑多种联系方式弹窗截图**：`[插入截图]`
- **收藏联系人与 `★ Bookmarked` 筛选视图截图**：`[插入截图]`
- **导出的 Excel 表格截图与导入结果提示截图**：`[插入截图]`
- **完整程序运行视频**：`[填写 B站 / 网盘 / GitHub 等可公开访问的视频链接]`

---

## 5. GitHub 提交历史与版本发布

> 请在队友完成 Fork、PR 合并并发布 `v1.0.0` Release 后，截取 GitHub Insights / Commits 页面并核对以下统计。

- **仓库总提交次数**：`[合并后核对实际数字，当前基线已有 4 次以上，最终应 ≥ 3]`
- **GitHub 提交历史截图**：`[插入仓库 Commits 历史截图]`

| 贡献者（GitHub 账号 / 学号） | 实际提交次数 | 说明 / PR 链接 |
| --- | --- | --- |
| `w1457344108-coder`（`832402220`） | `[核对后填写]` | 仓库初始化、核心后端、前端 UI、基础测试及 PR 合并 |
| `[填写队友 GitHub ID]`（`832402216`） | `[核对后填写]` | `[填写队友 PR 链接与修改说明]` |

---

## 6. 成员贡献比例评估

> 两位成员贡献比例总计需为 **100%**，请根据最终实际编码、测试、协作与文档工作共同确认后填写。

| 成员 | 贡献比例 | 评估依据 |
| --- | --- | --- |
| `832402220` | `[填写]%` | `[依据实际需求拆解、主架构与前后端编码、测试用例与集成发布说明]` |
| `832402216` | `[填写]%` | `[依据实际 Fork/PR 编码改动、测试验证、运行演示与博客整理说明]` |
| **合计** | **100%** | — |

---

## 7. 合作过程中遇到的困难与解决办法

> 请据实记录两人实际遇到的开发、接口、Excel 格式或 Git 协作问题，不虚构未发生的情况。示例格式如下：

| 遇到的问题 | 发现人 / 场景 | 解决办法 | 验证结果 |
| --- | --- | --- | --- |
| `[例如：Excel 中以 https:// 开头的网址被误解析为 Label: Value]` | `[据实填写或替换为实际遇到的问题]` | 在 `_parse_methods_cell` 中判断冒号右侧不以 `//` 开头时才拆分为标签与值 | 通过 `pytest` 往返导入导出测试验证 |
| `[填写协作过程中实际遇到的 Git / 环境 / 界面问题]` | `[据实填写]` | `[据实填写]` | `[据实填写]` |

---

## 8. PSP 个人软件过程记录表

> 单位：分钟。两位成员请分别根据自己真实耗时填写（提交博客时每人保留对应内容即可，或两人表都保留并注明本人表）。

### 成员 A：`832402220`

| Personal Software Process Stages | 预计耗时（分钟） | 实际耗时（分钟） |
| --- | --- | --- |
| Planning（计划） | `[填写]` | `[填写]` |
| · Estimate（估计这个任务需要多少时间） | `[填写]` | `[填写]` |
| Development（开发） | `[填写]` | `[填写]` |
| · Analysis（需求分析） | `[填写]` | `[填写]` |
| · Design Spec（生成设计文档） | `[填写]` | `[填写]` |
| · Design Review（设计复审） | `[填写]` | `[填写]` |
| · Coding Standard（代码规范） | `[填写]` | `[填写]` |
| · Design（具体设计） | `[填写]` | `[填写]` |
| · Coding（具体编码） | `[填写]` | `[填写]` |
| · Code Review（代码复审） | `[填写]` | `[填写]` |
| · Test（测试与调试） | `[填写]` | `[填写]` |
| Reporting（报告） | `[填写]` | `[填写]` |
| · Test Report（测试报告） | `[填写]` | `[填写]` |
| · Size Measurement（计算工作量） | `[填写]` | `[填写]` |
| · Postmortem & Process Improvement Plan（总结与改进计划） | `[填写]` | `[填写]` |
| **合计** | `[填写]` | `[填写]` |

### 成员 B：`832402216`

| Personal Software Process Stages | 预计耗时（分钟） | 实际耗时（分钟） |
| --- | --- | --- |
| Planning（计划） | `[填写]` | `[填写]` |
| · Estimate（估计这个任务需要多少时间） | `[填写]` | `[填写]` |
| Development（开发） | `[填写]` | `[填写]` |
| · Analysis（需求分析） | `[填写]` | `[填写]` |
| · Design Spec（生成设计文档） | `[填写]` | `[填写]` |
| · Design Review（设计复审） | `[填写]` | `[填写]` |
| · Coding Standard（代码规范） | `[填写]` | `[填写]` |
| · Design（具体设计） | `[填写]` | `[填写]` |
| · Coding（具体编码） | `[填写]` | `[填写]` |
| · Code Review（代码复审） | `[填写]` | `[填写]` |
| · Test（测试与调试） | `[填写]` | `[填写]` |
| Reporting（报告） | `[填写]` | `[填写]` |
| · Test Report（测试报告） | `[填写]` | `[填写]` |
| · Size Measurement（计算工作量） | `[填写]` | `[填写]` |
| · Postmortem & Process Improvement Plan（总结与改进计划） | `[填写]` | `[填写]` |
| **合计** | `[填写]` | `[填写]` |
