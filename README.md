
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

### 2. 设置后端（Django）
#### 2.1 进入后端目录
```bash
cd backend
```

#### 2.2 创建虚拟环境并安装依赖
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### 2.3 安装依赖（requirements.txt 示例）
创建一个 `requirements.txt` 文件，内容如下：
```text
django==4.2
djangorestframework==3.14
djangorestframework-simplejwt==5.3
django-cors-headers==4.3
```

#### 2.4 数据库迁移
```bash
python manage.py makemigrations
python manage.py migrate
```

#### 2.5 创建超级用户（可选）
```bash
python manage.py createsuperuser
```

#### 2.6 运行后端
```bash
python manage.py runserver
```
默认后端运行在 [http://localhost:8000](http://localhost:8000)。

### 3. 设置前端（Vue.js）
#### 3.1 进入前端目录
```bash
cd frontend
```

#### 3.2 安装依赖
```bash
npm install
```

#### 3.3 运行前端
```bash
npm run dev
```
默认前端运行在 [http://localhost:5173](http://localhost:5173)。

## 使用说明
### 1. 访问前端
- 打开浏览器，访问 [http://localhost:5173](http://localhost:5173)。
- 注册新用户或登录（已有超级用户可登录）。
- 创建文章、评论、点赞和收藏。

### 2. API 文档
API 文档基于 OpenAPI 3.0 规范，位于 `docs/api.yaml`（或直接查看你的 OpenAPI JSON）。主要接口：

#### 用户相关
- `POST /api/register/`：用户注册
- `POST /api/login/`：用户登录
- `GET/PUT /api/user/`：获取/修改用户信息

#### 文章相关
- `GET/POST /api/posts/`：获取文章列表/创建文章
- `GET/PUT/DELETE /api/posts/{id}/`：获取/更新/删除文章

#### 评论相关
- `GET/POST /api/comments/`：获取评论列表/创建评论
- `DELETE /api/comments/{id}/`：删除评论

#### 点赞相关
- `POST /api/like/`：点赞文章
- `DELETE /api/like/{id}/`：取消点赞

#### 收藏相关
- `POST /api/collect/`：收藏文章
- `DELETE /api/collect/{id}/`：取消收藏

### 示例请求
点赞文章：
```bash
curl -X POST http://localhost:8000/api/like/ \
  -H "Authorization: Bearer <你的 JWT Token>" \
  -H "Content-Type: application/json" \
  -d '{"post_id": 1}'
```

响应：
```json
{
    "id": 1,
    "post_id": 1,
    "user_id": 1
}
```

## 项目结构
```text
yunmeng-blog/
├── backend/              # 后端代码
│   ├── blog/             # 应用目录
│   │   ├── migrations/   # 数据库迁移文件
│   │   ├── models.py     # 模型（用户、文章、评论、点赞、收藏）
│   │   ├── serializer/   # 序列化器
│   │   ├── views.py      # 视图（API 逻辑）
│   │   └── urls.py       # 路由
│   ├── manage.py         # Django 管理脚本
│   └── requirements.txt  # 后端依赖
├── frontend/             # 前端代码
│   ├── src/              # Vue.js 源代码
│   │   ├── views/        # 页面组件（文章列表、详情等）
│   │   ├── router/       # 路由配置
│   │   └── assets/       # 静态资源
│   ├── package.json      # 前端依赖
│   └── vite.config.js    # Vite 配置文件
└── docs/                 # 文档
    └── api.yaml          # OpenAPI 文档
```

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
- **作者**：你的名字
- **邮箱**：你的邮箱@example.com
- **GitHub Issues**：欢迎提交问题或建议！

## 待办事项
- 添加文章搜索功能
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
