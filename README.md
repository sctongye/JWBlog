# JW Blog - Django + Vue3 全栈博客系统  
JW Blog - Full Stack Blog System with Django + Vue3

[![Demo](https://img.shields.io/badge/Demo-wangjiayu.com%2Fblog-blue?logo=google-chrome&logoColor=white)](https://wangjiayu.com/blog)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-3.2%2B-success?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Vue](https://img.shields.io/badge/Vue-3.x-brightgreen?logo=vue.js)](https://vuejs.org/)
[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)

---

> 🌏 **在线演示 Demo**：[https://wangjiayu.com/blog](https://wangjiayu.com/blog)

---

## ✨ 项目简介 | Project Introduction

JW Blog 是一个基于 Django REST Framework（后端）和 Vue3（前端）实现的现代化全栈博客系统。  
本项目在 [Dusai 的 django-vue-tutorial](https://github.com/stacklens/django-vue-tutorial) 基础上进行了优化和功能增强，适合学习、二次开发和个人博客部署。

JW Blog is a modern full-stack blog system built with Django REST Framework (backend) and Vue3 (frontend).  
It is an improved and enhanced version based on [Dusai's django-vue-tutorial](https://github.com/stacklens/django-vue-tutorial), suitable for learning, secondary development, and personal blog deployment.

---

## 🚀 主要特性 | Key Features

- 🖥️ 前后端完全分离，接口规范，易于维护和扩展  
  Fully separated frontend and backend, standardized APIs, easy to maintain and extend
- 📱 响应式设计，适配 PC 和移动端  
  Responsive design for both PC and mobile
- 🏷️ 文章分类与标签，支持多标签/多分类筛选  
  Article categories and tags, supports multi-tag/category filtering
- 👁️‍🗨️ 文章访问量统计，首页与单篇文章均有独立计数  
  Article view count, both homepage and individual articles have independent counters
- 🔍 文章搜索与分页，支持关键字检索与高效分页  
  Article search and pagination, supports keyword search and efficient pagination
- 💬 评论系统，支持多级评论（可选）  
  Comment system, supports multi-level comments (optional)
- 👤 用户系统，支持注册、登录、JWT鉴权、用户中心  
  User system, supports registration, login, JWT authentication, and user center
- 📝 富文本编辑与 Markdown 支持  
  Rich text editing and Markdown support
- 🖼️ 图片上传与头像管理  
  Image upload and avatar management
- 🌐 社交媒体集成，支持自定义社交链接与图标  
  Social media integration, supports custom social links and icons
- 🛠️ 后台管理，基于 Django Admin  
  Backend management based on Django Admin
- 🧩 代码结构清晰，注释详细，适合学习和二次开发  
  Clean code structure, detailed comments, suitable for learning and secondary development

---

## 🛠️ 技术栈 | Tech Stack

- **后端 Backend**：Python 3.8+、Django 3.2+、Django REST Framework
- **前端 Frontend**：Vue 3.x、Vue Router、Axios、Element Plus (可选)
- **数据库 Database**：SQLite3（默认，可切换为 MySQL/PostgreSQL）
- **其他 Others**：Font Awesome、Toast UI Editor、JWT

---

## 🗂️ 目录结构 | Project Structure

```text
JWBlog/
├── backend/                # Django 后端 / Django backend
│   ├── apps/               # 业务应用 / Business apps
│   ├── django_main/        # 主项目配置 / Main project config
│   ├── manage.py
│   └── requirements.txt
├── frontend/               # Vue3 前端 / Vue3 frontend
│   ├── src/
│   │   ├── assets/         # 静态资源 / Static assets
│   │   ├── components/     # Vue 组件 / Vue components
│   │   ├── views/          # 页面视图 / Page views
│   │   ├── router/         # 路由配置 / Router config
│   │   ├── composables/    # 组合式API逻辑 / Composables
│   │   └── App.vue
│   ├── public/
│   └── package.json
├── media/                  # 用户上传的图片等 / User uploaded files
└── README.md
```

---

## ⚙️ 运作机制与核心功能说明 | How It Works & Core Features

### 1. 前后端分离架构 / Separated Architecture

- 后端仅负责数据接口（RESTful API），所有页面渲染、交互逻辑均在前端完成。  
  Backend only provides RESTful APIs, all rendering and logic are handled by frontend.
- 前端通过 Axios 调用后端 API，实现数据的获取、展示与交互。  
  Frontend uses Axios to call backend APIs for data fetching, display, and interaction.

### 2. 文章与标签/分类 / Articles, Tags & Categories

- 文章支持多标签（ManyToMany）和单分类（ForeignKey）。  
  Articles support multiple tags (ManyToMany) and single category (ForeignKey).
- 侧边栏仅显示当前所有文章实际使用的标签和分类，自动剔除无效项。  
  Sidebar only shows tags/categories used by existing articles, unused ones are hidden.
- 支持通过点击标签/分类进行文章筛选，筛选条件体现在 URL query 参数中，便于分享和 SEO。  
  Supports filtering articles by clicking tags/categories, filter state is reflected in URL query for sharing and SEO.

### 3. 访问量统计 / View Counter

- 首页和每篇文章均有独立访问计数，后端通过接口自动记录。  
  Homepage and each article have independent view counters, backend records via API.
- 访问量数据通过 API 实时获取，前端展示。  
  View count is fetched via API and displayed on frontend.

### 4. 搜索与分页 / Search & Pagination

- 支持文章标题、正文的模糊搜索。  
  Supports fuzzy search for article title and content.
- 支持分页，前端分页参数与后端 API 对接。  
  Supports pagination, frontend and backend parameters are integrated.

### 5. 用户与权限 / User & Permissions

- 支持注册、登录、JWT 鉴权。  
  Supports registration, login, and JWT authentication.
- 登录后可进入用户中心，支持文章发布、编辑、删除等操作（需权限）。  
  After login, users can access user center, publish/edit/delete articles (with permission).
- 超级用户可通过 Django Admin 进行后台管理。  
  Superusers can manage via Django Admin.

### 6. 评论系统（可选）/ Comment System (Optional)

- 支持多级评论，评论与文章、用户关联。  
  Supports multi-level comments, comments are linked to articles and users.
- 评论接口与文章接口分离，便于维护。  
  Comment API is separated from article API for maintainability.

### 7. 富文本与图片上传 / Rich Text & Image Upload

- 支持 Markdown 编辑与实时预览。  
  Supports Markdown editing and live preview.
- 支持图片上传，图片存储于后端 media 目录。  
  Supports image upload, images are stored in backend media directory.

### 8. 社交媒体集成 / Social Media Integration

- 支持 Instagram、Twitter、YouTube 等社交链接，图标采用 Font Awesome，支持品牌色自定义。  
  Supports Instagram, Twitter, YouTube, etc., icons use Font Awesome with brand colors.

---

## 🏁 快速开始 | Quick Start

### 1. 克隆项目 Clone the Project

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2. 后端部署 Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser  # 创建管理员账号 / Create admin user
python manage.py runserver
```

### 3. 前端部署 Frontend Setup

```bash
cd frontend
npm install
npm run serve
```

### 4. 访问 Access

- 前端页面 Frontend：[http://localhost:8080/](http://localhost:8080/)
- 后端 API Backend：[http://127.0.0.1:8000/api/](http://127.0.0.1:8000/api/)

---

## 🙏 鸣谢与致敬 | Acknowledgement

本项目基于 [Dusai 的 django-vue-tutorial](https://github.com/stacklens/django-vue-tutorial) 改进，感谢原作者的开源精神和详细教程。  
This project is based on [Dusai's django-vue-tutorial](https://github.com/stacklens/django-vue-tutorial). Thanks to the original author for the open source spirit and detailed tutorial.

---

## 📄 许可证 | License

本项目遵循 [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/deed.zh) 协议，欢迎学习和非商业性使用，转载请注明出处。  
This project is licensed under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/). Free for learning and non-commercial use, please indicate the source.

---

## 📬 联系与交流 | Contact

- 博主主页 Homepage：[https://wangjiayu.com](https://wangjiayu.com)
- 博客演示 Demo：[https://wangjiayu.com/blog](https://wangjiayu.com/blog)
- Issues 或 PR 欢迎交流与改进！  
  Issues or PRs are welcome for discussion and improvement!

---

**Enjoy Blogging! 🚀 | 祝你写博愉快！**

---

## 📝 如何上传项目到 GitHub 并忽略隐私/本地文件  
How to Upload Your Project to GitHub and Ignore Private/Local Files

### 1. 创建 .gitignore 文件  
Create a `.gitignore` file in your project root (如果已有可直接编辑)：

```gitignore
# Python
*.pyc
__pycache__/
db.sqlite3
media/
.env
venv/
# VSCode
.vscode/
# Node
node_modules/
dist/
# OS
.DS_Store
Thumbs.db
```
> 你可以根据实际情况添加更多不需要上传的文件夹和文件。  
> Add more files/folders as needed for your project.

### 2. 初始化 Git 仓库  
Initialize Git repository

```bash
git init
git add .
git commit -m "Initial commit"
```

### 3. 创建远程仓库  
Create a new repository on [GitHub](https://github.com/) (e.g. `JWBlog`).

### 4. 关联远程仓库  
Link to remote repository

```bash
git remote add origin https://github.com/your-username/your-repo-name.git
```

### 5. 推送到 GitHub  
Push to GitHub

```bash
git push -u origin main
```
> 如果你用的是 `master` 分支，最后一条命令应为 `git push -u origin master`  
> If you use `master` branch, use `git push -u origin master` instead.

---

**注意事项 Tips**  
- **不要上传包含敏感信息的文件**（如 `.env`、数据库、用户上传的图片等）。  
  Do **not** upload sensitive files (e.g. `.env`, database, user uploads, etc.).
- **.gitignore** 文件能帮你自动忽略这些内容。  
  Use `.gitignore` to automatically ignore these files.
- **首次推送后，后续只需 `git add .`、`git commit -m "msg"`、`git push` 即可。**  
  After the first push, just use `git add .`, `git commit -m "msg"`, and `git push` for future updates.

---

如需进一步帮助，欢迎提 Issue 或联系我！  
For further help, feel free to open an Issue or contact me! 