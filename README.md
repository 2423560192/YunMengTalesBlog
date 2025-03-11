# 云梦物语 Blog

云梦物语 Blog 是一个基于 Django REST Framework 和 Vue.js 实现的博客平台，提供用户管理、文章管理、评论、点赞和收藏功能，适合初学者学习和开发现代 Web 应用。

## 项目简介

云梦物语 Blog 是一个前后端分离的博客系统：

- **后端**：使用 Django 和 Django REST Framework，采用 JWT 认证，提供 RESTful API。
- **前端**：使用 Vue.js 构建单页应用（SPA），通过 Axios 调用后端 API。
- **功能**：支持用户注册/登录、文章创建/编辑/删除、评论、点赞、收藏等功能。

本项目适合学习 Django REST Framework、Vue.js 和前后端分离开发，代码结构清晰，注释详细，易于扩展。

## 功能特性

### 用户管理

- 用户注册、登录（JWT 认证）
- 获取/修改用户信息

### 文章管理

- 创建、查看、更新、删除文章
- 支持分类和标签
- 分页显示文章列表

### 评论管理

- 创建、查看、删除评论
- 支持嵌套评论（回复功能）

### 点赞功能

- 点赞/取消点赞文章

### 收藏功能

- 收藏/取消收藏文章

### 权限控制

- 需登录才能操作（创建文章、评论、点赞、收藏等）
- 仅作者可编辑/删除自己的文章和评论

## 技术栈

### 后端

- Django 4.2
- Django REST Framework 3.14
- MySQL（开发环境，可切换为 SQLite/PostgreSQL）
- JWT 认证（django-rest-framework-simplejwt）

### 前端

- Vue.js 3
- Vue Router
- Axios
- Vite（构建工具）

### 其他

- OpenAPI 3.0（API 文档）

## 安装与运行

### 前置条件

- Python 3.8+（推荐 3.9）
- Node.js 16+（推荐 18）
- Git

### 1. 克隆项目

```bash
git clone https://github.com/yourusername/yunmeng-blog.git
cd yunmeng-blog
```

**注意**：如果克隆失败，请检查链接的合法性或稍后重试。

### 2. 设置后端（Django）

#### 2.1 进入后端目录

```bash
cd YunmengTalesBlog
```

#### 2.2 创建虚拟环境并安装依赖

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### 2.4 数据库迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

#### 2.6 运行后端

```bash
python manage.py runserver
```

默认后端运行在 [http://localhost:8000](http://localhost:8000/)。

### 3. 设置前端（Vue.js）

前端代码位于：

```plaintext
https://github.com/2423560192/YunMengBlog-Vue
```

**注意**：如果无法访问前端项目链接，请检查链接的合法性或稍后重试。

## 使用说明

### 1. 访问前端

- 打开浏览器，访问 [http://localhost:8080](http://localhost:8080/)。
- 注册新用户或登录。
- 创建文章、评论、点赞和收藏。

## 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork 本项目。
2. 创建新分支（`git checkout -b feature/你的功能`）。
3. 提交更改（`git commit -m "添加新功能"`）。
4. 推送到远程分支（`git push origin feature/你的功能`）。
5. 创建 Pull Request。

### 开发规范

- 代码遵循 PEP 8（Python）和 ESLint（JavaScript）。
- 提交前运行测试（如果有）。
- 提交消息清晰，例如：`feat: 添加文章点赞功能`。

## 许可证

本项目采用 MIT 许可证。你可以自由使用、修改和分发，但请保留版权声明。

## 联系方式

- **作者**：辰星
- **邮箱**：[2480419172@qq.com](mailto:2480419172@qq.com)
- **GitHub Issues**：欢迎提交问题或建议！

## 待办事项

- 添加文章搜索功能  【完成】
- 支持图片上传（文章封面）
- 添加单元测试
- 部署到生产环境（Nginx + Gunicorn）

## 常见问题

### 1. 后端跨域问题

如果前端报跨域错误，请确保后端已安装 `django-cors-headers`，并在 `settings.py` 中配置：

```python
INSTALLED_APPS = [
    ...
    'corsheaders',
]

MIDDLEWARE = [
    ...
    'corsheaders.middleware.CorsMiddleware',
    ...
]

CORS_ALLOW_ALL_ORIGINS = True  # 开发环境，生产环境需限制
```

### 2. JWT 认证问题

登录后获取 JWT Token，请求时在头部添加：

```text
Authorization: Bearer <你的 Token>
```

### 3. 数据库切换

开发环境用 SQLite，生产环境建议切换到 MySQL/PostgreSQL，修改 `settings.py` 中的 `DATABASES` 配置。

希望你喜欢这个项目！如果有任何问题，欢迎提交 Issue 或联系我！🌟