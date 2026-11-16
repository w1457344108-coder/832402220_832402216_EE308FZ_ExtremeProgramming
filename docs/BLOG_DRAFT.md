# EE308FZ 极限编程作业博客共用草稿（双人协作版）

> 说明：本草稿已对齐当前仓库真实代码与结构，供两位成员（`832402220`、`832402216`）同步编写和核对。根据课程要求，双人团队可共用一份 Markdown 草稿准备内容，但**两名同学需分别发布各自的个人博客**，发布前请将 `[待填写]` 替换为最终真实截图、链接、提交统计、贡献比例与各自真实的 PSP 耗时，并删去本提示段落。

| Item | Content |
| --- | --- |
| Course for This Assignment | Software Engineering (FZU–MU) |
| Team Name | `832402220_832402216_EE308FZ_ExtremeProgramming` |
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
| Pull Request 链接 | https://github.com/w1457344108-coder/832402220_832402216_EE308FZ_ExtremeProgramming/pull/1 |
| Release 版本链接 | https://github.com/w1457344108-coder/832402220_832402216_EE308FZ_ExtremeProgramming/releases/tag/v1.0.0 |
| 在线访问地址（阿里云部署） | http://8.163.36.172 |

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
| `832402220`（`w1457344108-coder`） | 仓库搭建、数据库设计、核心后端 API、多种联系方式与 Excel 导入导出（含防重复策略）、多主题与双语前端、阿里云部署及 PR 审查合并 | `address_book/*.py`、`templates/index.html`、`static/*`、`deploy/setup_server.sh`、`tests/*`、`docs/*` |
| `832402216`（`LiuJianhao7`） | Fork 仓库开发、键盘快捷键（`/` 聚焦搜索、`Esc` 关闭弹窗）、双语搜索清空按钮及中文表头/搜索排序边界测试（[PR #1](https://github.com/w1457344108-coder/832402220_832402216_EE308FZ_ExtremeProgramming/pull/1)） | `templates/index.html`、`static/css/style.css`、`static/js/app.js`、`tests/test_contacts_api.py`、`tests/test_excel.py` |

---

## 3. 功能实现思路

### 3.1 页面样式与交互布局

前端采用顶部工具栏 + 视图切换标签栏 + 响应式联系人卡片网格布局（`static/css/style.css`、`static/js/app.js`）：

- 右上角支持**多主题风格切换**（浅色简约 `Light`、深色夜间 `Dark`、海风青蓝 `Ocean Breeze`、暖纸手账 `Warm Paper`，以及一键亮/暗切换）与 **中/英文双语切换**（偏好通过 `localStorage` 持久化）。
- 顶部提供 `Load Demo`（加载示例数据）、`Template`（下载导入模板）、`Import Excel`、`Export Excel`（在收藏视图下自动切换为 `Export Bookmarked`）与 `+ New Contact` 快捷操作。
- 中部提供 `All Contacts` 与 `★ Bookmarked` 视图切换及实时搜索、一键清空搜索、排序（按收藏优先、姓名 A–Z、最近更新），支持 `/` 聚焦搜索与 `Esc` 关闭弹窗快捷键，每条联系方式支持一键复制及电话/邮箱/链接直达。
- 每项操作反馈均通过右下角 Toast 提示呈现。

### 3.2 联系人收藏（Bookmark Contacts）

- 数据库 `contacts` 表设置 `is_favorite` 字段（`0` / `1`）并建立 `(is_favorite, name)` 索引（`address_book/db.py`）。
- 后端提供专用接口 `PATCH /api/contacts/<id>/favorite` 支持一键切换或显式设置收藏状态，同时在 `GET /api/contacts?favorite=1` 中返回收藏联系人列表与统计数（`total_count`、`favorite_count`）。
- 前端每张联系人卡片右上角提供 `★ / ☆` 按钮，收藏后卡片呈现金色边框高亮，并可通过顶部 `★ Bookmarked` 标签页快速筛选访问。

### 3.3 多种联系方式（Multiple Contact Methods）

- 通过 `contacts`（1）对 `contact_methods`（N）的一对多外键关联（`ON DELETE CASCADE`）存储任意数量的联系方式，每条记录包含 `method_type`（`phone`、`email`、`social`、`address`、`other`）、`label`（如 `Mobile`、`Work`、`WeChat`、`Home`）和 `value`。
- 前端弹窗支持通过 `+ Add Method` 动态增删多条联系方式行，保存时由后端统一校验并按 `sort_order` 顺序更新。

### 3.4 Excel 导入与导出（Import and Export）

- **导出（`export_contacts_to_xlsx`）**：使用 `openpyxl` 生成 `.xlsx` 文件，确保**每位联系人占一行、每类信息占一列**，列顺序为：`Name`、`Favorite`、`Company`、`Title`、`Phone Numbers`、`Emails`、`Social Media`、`Addresses`、`Other Contacts`、`Notes`。同一类别的多条联系方式按 `Label: Value; ...` 格式组织；单元格设置 `number_format = "@"` 文本格式，避免 `0591-...`、`0086...` 等带前导零的电话号码在 Excel 中丢失前导零。
- **导入（`import_contacts_from_xlsx`）**：校验 `.xlsx` 文件有效性及首行必须包含 `Name` 列（兼容常见中英文表头别名），支持**同名联系人处理策略**（`skip` 跳过重复、`update` 覆盖更新、`allow` 全部作为新联系人导入），解析各列多条联系方式并保留含 `https://` 的完整链接，跳过空行或缺失姓名的异常行并返回 `imported_count`、`updated_count`、`skipped_count` 与 `errors` 明细。

### 3.5 云服务器部署（Web Deployment，+15 分可选加分项）

项目已部署至**阿里云轻量应用服务器**（公网访问地址：http://8.163.36.172）：

- 通过自动化部署脚本 [deploy/setup_server.sh](https://github.com/w1457344108-coder/832402220_832402216_EE308FZ_ExtremeProgramming/blob/main/deploy/setup_server.sh) 配置独立 Python 虚拟环境与持久化 SQLite 数据库路径。
- 使用 `Gunicorn`（单 Worker + 4 线程，避免 SQLite 多进程锁竞争）配合 `systemd` 服务实现后台常驻与异常自动重启。
- 使用 `Nginx` 将 `80` 端口反向代理至 `127.0.0.1:5000`，并配置 `client_max_body_size 12M` 支持 Excel 文件上传。

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

> 以下统计口径以 `main` 分支最终提交历史为准；发布博客前请截取 GitHub Commits / Insights 页面一并附上。

- **仓库总提交次数**：`15` 次（包含 PR #1 合并提交，远超 ≥ 3 次要求）
- **GitHub 提交历史截图**：`[插入仓库 Commits 历史截图]`

| 贡献者（GitHub 账号 / 学号） | 实际提交次数 | 说明 / PR 链接 |
| --- | --- | --- |
| `w1457344108-coder`（`832402220`） | `13` 次（含 PR 合并提交） | 仓库初始化、核心后端、前端 UI、云部署脚本、基础测试、文档及 PR #1 合并 |
| `LiuJianhao7`（`832402216`） | `2` 次 | [PR #1](https://github.com/w1457344108-coder/832402220_832402216_EE308FZ_ExtremeProgramming/pull/1)：`4bac2df`（快捷键与搜索清空）与 `92d3153`（中文表头与搜索排序测试） |

---

## 6. 成员贡献比例评估

> 两位成员经协商确定贡献比例为 **50% : 50%**（合计 **100%**）。

| 成员 | 贡献比例 | 评估依据 |
| --- | --- | --- |
| `832402220`（`w1457344108-coder`） | `50%` | 负责仓库搭建、SQLite 与核心后端 API、Excel 导入导出、多主题与双语 UI、阿里云部署、PR #1 审查合并及 Release 发布 |
| `832402216`（`LiuJianhao7`） | `50%` | 负责 Fork 协作开发、键盘快捷键与双语搜索清空交互、中文表头与搜索排序边界测试（PR #1）、协同测试与博客整理 |
| **合计** | **100%** | — |

---

## 7. 合作过程中遇到的困难与解决办法

以下均为本次开发与双人 Git 协作过程中真实遇到并验证解决的问题：

| 遇到的问题 | 发现人 / 场景 | 解决办法 | 验证结果 |
| --- | --- | --- | --- |
| 队友准备同步代码时在页面未找到 `Sync fork` 按钮 | `832402220` & `832402216` / GitHub Fork 协作阶段 | 通过 GitHub 接口排查确认仓库已公开但 `forks_count` 为 `0`（尚未创建 Fork），引导队友先从主仓库创建 Fork 并切出分支开发后发起 PR #1 | 成功创建 Fork 并完成 PR #1 合并，保留双方完整提交记录 |
| Excel 导出后电话前导零易丢失，且“其他联系方式”中 `https://` 网址含冒号易被误拆为 `Label: Value` | `832402220` / Excel 导入导出模块设计 | 导出时为单元格设置文本格式 `@` 保留前导零；导入解析函数 `_parse_methods_cell` 判断冒号右侧不以 `//` 开头时才拆分为标签与值 | `pytest -v` 往返导入导出测试验证前导零（如 `0591-12345678`、`0086...`）与 `https://` 网址均完整保留 |
| 新增 `/` 聚焦搜索框快捷键时需避免与输入框输入及中文输入法冲突 | `832402216` / PR #1 前端快捷键实现 | 在 `keydown` 监听中过滤 `event.isComposing`、组合键以及焦点在 `input` / `textarea` / `select` 或弹窗内的场景 | 通过 `24` 项浏览器键盘/主题/语言交互验证，确认正常输入斜杠不受干扰 |
| 阿里云服务器部署后 Nginx 默认限制上传大小为 1MB，低于应用允许的 10MB Excel 上限 | `832402220` / 阿里云生产环境配置 | 在自动化部署脚本 `deploy/setup_server.sh` 生成的 Nginx 配置中显式加入 `client_max_body_size 12M` 并使用 Gunicorn 单进程多线程配合持久化 SQLite | `http://8.163.36.172/api/health` 与页面公网访问均返回 `HTTP 200` |

---

## 8. PSP 个人软件过程记录表

> 单位：分钟。其中 `832402220` 的计划与开发阶段耗时已依据 `2026-11-16` 实际开发会话及 Git 提交时间线整理（报告与录屏/发博收尾项请在完成录屏与博客发布后核对补齐）；`832402216` 请由队友据实填写。

### 成员 A：`832402220`

| Personal Software Process Stages | 预计耗时（分钟） | 实际耗时（分钟） |
| --- | --- | --- |
| **Planning（计划）** | **15** | **15** |
| · Estimate（估计这个任务需要多少时间） | 15 | 15 |
| **Development（开发）** | **130** | **135** |
| · Analysis（需求分析） | 15 | 15 |
| · Design Spec（生成设计文档） | 15 | 15 |
| · Design Review（设计复审） | 10 | 10 |
| · Coding Standard（代码规范） | 10 | 10 |
| · Design（具体设计） | 15 | 15 |
| · Coding（具体编码） | 35 | 40 |
| · Code Review（代码复审） | 15 | 15 |
| · Test（测试与调试） | 15 | 15 |
| **Reporting（报告）** | **40** | **`[待录屏与发博后核对，如 40]`** |
| · Test Report（测试报告） | 15 | 15 |
| · Size Measurement（计算工作量） | 10 | 10 |
| · Postmortem & Process Improvement Plan（总结与改进计划） | 15 | `[待录屏与发博后补充]` |
| **合计** | **185** | **`[待录屏与发博后汇总，当前已完成 175 分钟]`** |

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
