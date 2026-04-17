# LawLink

<div align="center">
  <img src="logo.svg" alt="LawLink Logo" width="120" />
  <h3>全球法律数据资源库</h3>
  <p>一个精选的全球法律研究、数据分析和司法参考资源目录，覆盖 190+ 国家与地区。</p>
</div>

## 🌟 项目简介

**LawLink** 旨在为法律从业者、研究人员和数据分析师提供一个系统化、结构化且极具美感的全球法律数据资源导航平台。

项目采用纯净的前端架构，所有资源数据通过结构化的 JSON 驱动，界面采用“电子档案库（Digital Ledger）”的美学设计，兼顾了专业感与现代排版的优雅。

### 核心特性

- **🌍 广度覆盖**：收录包含联合国（UN）、欧盟（EU）、世界贸易组织（WTO）等跨国组织，以及全球 190+ 主权国家/地区的法律链接。
- **📊 多维视图**：
  - **按地区浏览**：支持按大洲及次区域（如：亚洲 -> 东亚）进行结构化下钻。
  - **按热度排行**：内置基于全球综合实力（GDP Top 20）与司法热度的加权榜单。
- **⚡ 极速检索**：前端本地实时过滤，支持中英文名称、地区、资源类型等全字段搜索。
- **🛠 状态追踪**：内置数据完善度追踪（“已完成” / “进行中”），方便协同共建。

## 🚀 部署与运行

本项目是一个零配置的纯静态网页应用，完全不需要任何构建工具或打包流程。

### 本地预览
只需启动一个本地 HTTP 服务器即可（因为使用了 `fetch` 加载 `data.json`，直接双击 `index.html` 会因跨域安全策略导致加载失败）：

```bash
# 使用 Python 3 启动
python3 -m http.server 8080

# 或者使用 Node.js 的 http-server
npx http-server -p 8080
```
然后在浏览器中访问 `http://localhost:8080` 即可。

### 线上部署 (GitHub Pages)
项目已经配置了 GitHub Actions 自动部署。当你将代码推送到 `main` 分支时，GitHub 将自动把静态文件部署到 GitHub Pages 上。

**启用步骤：**
1. 进入 GitHub 仓库的 **Settings** -> **Pages**。
2. 在 **Build and deployment** 下的 **Source** 选项中，选择 **GitHub Actions**。
3. 推送代码，等待 Action 运行完毕即可获得线上访问地址。

## 📝 如何贡献与补充数据？

项目的视图代码（`index.html`）与数据层（`data.json`）完全分离。

### 方法一：直接修改 JSON（推荐）
如果你想补充某个国家的法律资源，直接打开 `data.json` 文件，搜索对应的国家（例如 `"id": "CN"`），在 `"resources"` 数组中修改或追加内容即可：

```json
{
  "name": "资源名称",
  "url": "https://...",
  "type": "立法法规",
  "desc": "关于该资源的简短描述"
}
```
*注：修改完成后，建议将该国家的 `"status"` 字段改为 `"已完成"`。*

### 方法二：通过脚本重建数据
项目包含一个 `rebuild_data.py` 脚本，它负责从 [REST Countries API](https://restcountries.com/) 抓取全球基础国家数据，并清洗、分组生成初始的 `data.json` 框架。
如果你需要彻底重置数据或修改底层的分类逻辑（如增加新的跨国组织），可以修改并运行此脚本：
```bash
python3 rebuild_data.py
```

## 🎨 技术栈

- **Vue 3**：核心响应式逻辑与数据渲染（通过 CDN 引入）。
- **Tailwind CSS**：原子化样式引擎（通过 CDN 引入）。
- **Phosphor Icons**：图标库。
- **原生 HTML/JS/CSS**：零构建，极致轻量。

## 📄 许可证

MIT License
