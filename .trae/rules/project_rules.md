# WiFi 评分系统 - 项目规则

## 项目概述

这是一个基于 Django REST Framework + Vue 3 的 WiFi 设备评分系统，支持用户注册登录、设备浏览、评价、收藏以及设备提交审核功能。

## 技术栈

### 后端
- Django 6.0
- Django REST Framework
- SQLite（开发环境）
- Token 认证

### 前端
- Vue 3
- Vite
- Vue Router
- Bootstrap 5
- Axios

## 项目结构

```
rating_wifi/
├── wifirating/              # Django 后端
│   ├── api/                # API 应用
│   │   ├── models.py       # 数据模型
│   │   ├── views.py        # 视图函数
│   │   ├── serializers.py  # 序列化器
│   │   ├── urls.py         # URL 配置
│   │   ├── utils.py        # 工具函数
│   │   └── migrations/     # 数据库迁移
│   ├── wifirating/         # 项目配置
│   │   ├── settings.py     # Django 设置
│   │   └── urls.py         # 主 URL 配置
│   └── manage.py           # Django 管理脚本
├── wifi-rating-app/        # Vue 前端
│   ├── src/
│   │   ├── api/           # API 调用
│   │   ├── assets/        # 静态资源
│   │   ├── components/    # Vue 组件
│   │   ├── router/        # 路由配置
│   │   ├── views/         # 页面视图
│   │   ├── App.vue        # 根组件
│   │   └── main.js        # 入口文件
│   └── package.json       # 前端依赖
└── .trae/
    └── rules/
        └── project_rules.md  # 本文件
```

## 开发环境设置

### 后端设置

1. 创建虚拟环境：
```bash
cd wifirating
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. 安装依赖：
```bash
pip install django djangorestframework django-cors-headers
```

3. 运行迁移：
```bash
python manage.py makemigrations
python manage.py migrate
```

4. 创建超级用户（可选）：
```bash
python manage.py createsuperuser
```

5. 启动开发服务器：
```bash
python manage.py runserver
```

### 前端设置

1. 安装依赖：
```bash
cd wifi-rating-app
npm install
```

2. 启动开发服务器：
```bash
npm run dev
```

3. 构建生产版本：
```bash
npm run build
```

## 代码规范

### Python 代码规范

1. **PEP 8 风格**：遵循 PEP 8 代码风格指南
2. **导入顺序**：标准库 → 第三方库 → 本地模块
3. **类命名**：使用 PascalCase（如 `WifiModel`）
4. **函数命名**：使用 snake_case（如 `get_user_profile`）
5. **常量命名**：使用 UPPER_CASE（如 `APPROVAL_PENDING`）

### JavaScript/Vue 代码规范

1. **组件命名**：使用 PascalCase（如 `UserProfile.vue`）
2. **函数命名**：使用 camelCase（如 `getUserProfile`）
3. **常量命名**：使用 UPPER_CASE
4. **组件结构**：template → script → style

## 数据库规范

### 模型设计

1. **表名**：使用 `db_table` Meta 选项指定表名（如 `users`, `wifi_models`）
2. **外键**：使用 `related_name` 参数明确关联关系
3. **索引**：对频繁查询的字段添加索引
4. **软删除**：使用 `on_delete=models.SET_NULL` 保留历史数据

### 迁移管理

1. 每次修改模型后必须创建迁移：
```bash
python manage.py makemigrations
```

2. 应用迁移：
```bash
python manage.py migrate
```

3. 不要手动修改迁移文件

## API 设计规范

### 认证机制

1. 使用 Token 认证
2. 登录/注册接口返回 token 和用户信息
3. 所有需要认证的接口使用 `@permission_classes([IsAuthenticated])` 装饰器
4. 前端通过 `Authorization: Token <token>` 头传递认证信息

### 权限控制

1. 用户只能访问和修改自己的数据（个人资料、收藏、评价、提交记录）
2. 使用 `request.user.id != user_id` 检查权限
3. 返回 403 状态码表示权限不足

### 响应格式

**成功响应**：
```json
{
  "message": "操作成功",
  "data": {...}
}
```

**错误响应**：
```json
{
  "message": "错误描述"
}
```

### 状态码使用

- 200: 成功
- 201: 创建成功
- 400: 请求参数错误
- 401: 未认证
- 403: 权限不足
- 404: 资源不存在
- 500: 服务器错误

## 安全规范

### 环境变量

生产环境必须设置以下环境变量：
- `DJANGO_SECRET_KEY`: Django 密钥
- `DEBUG`: False
- `ALLOWED_HOSTS`: 允许的主机列表
- `CORS_ALLOWED_ORIGINS`: 允许的跨域来源
- `SECURE_SSL_REDIRECT`: True
- `SESSION_COOKIE_SECURE`: True
- `CSRF_COOKIE_SECURE`: True

### 密码安全

1. 使用 Django 的密码验证器
2. 密码最小长度为 6 位
3. 使用 `set_password()` 方法加密存储密码

### CORS 配置

1. 开发环境：允许所有来源（`CORS_ALLOW_ALL_ORIGINS = True`）
2. 生产环境：明确指定允许的来源（`CORS_ALLOWED_ORIGINS`）

### 文件上传

1. 头像文件存储在 `media/avatars/` 目录
2. 限制文件大小和类型
3. 使用 `process_and_save_avatar` 工具函数处理文件

## 测试规范

### 运行测试

```bash
cd wifirating
python manage.py test
```

### 测试覆盖

1. 所有 API 接口必须有测试
2. 测试正常流程和错误情况
3. 测试权限控制

## 部署规范

### 生产环境检查清单

- [ ] 设置 `DEBUG = False`
- [ ] 配置 `ALLOWED_HOSTS`
- [ ] 设置 `SECRET_KEY`
- [ ] 配置 `CORS_ALLOWED_ORIGINS`
- [ ] 启用 HTTPS（`SECURE_SSL_REDIRECT = True`）
- [ ] 配置静态文件服务
- [ ] 配置媒体文件服务
- [ ] 使用生产数据库（PostgreSQL 推荐）
- [ ] 配置日志记录

### 静态文件收集

```bash
python manage.py collectstatic
```

## 常见命令

### Django 后端

```bash
# 启动开发服务器
python manage.py runserver

# 创建迁移
python manage.py makemigrations

# 应用迁移
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser

# 运行测试
python manage.py test

# 打开 Django Shell
python manage.py shell

# 填充测试数据
python manage.py populate_data
```

### Vue 前端

```bash
# 启动开发服务器
npm run dev

# 构建生产版本
npm run build

# 预览生产构建
npm run preview

# 安装依赖
npm install
```

## 注意事项

1. **开发与生产分离**：开发环境使用 SQLite，生产环境使用 PostgreSQL
2. **敏感信息保护**：不要将密钥、密码等敏感信息提交到版本控制
3. **API 版本控制**：当前为 v1，如需重大变更应考虑版本控制
4. **数据备份**：定期备份数据库
5. **日志记录**：生产环境应配置适当的日志级别

## 故障排查

### 常见问题

1. **CORS 错误**：检查 `CORS_ALLOWED_ORIGINS` 配置
2. **401 未授权**：检查 token 是否正确传递
3. **403 权限不足**：检查用户是否有权限访问该资源
4. **数据库迁移失败**：删除 `db.sqlite3` 和 `migrations/` 目录（除 `__init__.py` 外），重新迁移
5. **静态文件 404**：运行 `python manage.py collectstatic`

## 联系方式

如有问题，请联系项目维护者。
