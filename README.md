# SM2-SM4 Secure Encrypt System

这是一个基于 Flask 的国密安全加密系统，集成：

- SM2 非对称加密
- SM4 对称加密
- OpenPGP 文件加密
- Web 前后端交互
- 文件加解密
- 文本加解密

系统采用前后端分离架构，实现了国密算法与 PGP 加密的融合应用，可用于信息安全课程设计、密码学实验、文件安全传输等场景。

---

# 项目功能

## 国密 SM2 + SM4 功能

### 密钥初始化

系统自动：

- 生成 SM2 公私钥对
- 生成随机 SM4 密钥
- 使用 SM2 公钥加密 SM4 密钥
- 服务端持久化保存 SM2 私钥
- 返回唯一 key_id

---

### 文本加密

支持：

- 明文输入
- SM4 对称加密
- Base64 输出密文

---

### 文本解密

支持：

- 密文输入
- SM4 解密恢复原文

---

### 文件加密

支持：

- 任意文件上传
- SM4 文件加密
- 下载 `.enc` 文件

---

### 文件解密

支持：

- `.enc` 文件恢复
- 原文件下载

---

# OpenPGP 文件加密功能

系统支持：

- 上传 PGP 公钥
- 上传待加密文件
- 服务端调用 GPG 进行 OpenPGP 加密
- 返回标准 `.gpg` 文件

兼容：

- GnuPG
- Kleopatra
- OpenPGP 标准工具

---

# 项目架构

```text
前端（HTML + JavaScript）
        │
        ▼
Flask Web API（业务逻辑层）
        │
        ▼
国密算法模块（SM2 / SM4）
        │
        ▼
本地密钥存储（keys/）
```

---

# 项目目录结构

```text
SM2-SM4_Secure_Encrypt_System/
│
├── app.py
├── crypto_core.py
├── requirements.txt
│
├── keys/
│
├── temp_gpg/
│
├── templates/
│   └── index.html
│
└── README.md
```

---

# 环境要求

## Python

推荐：

```text
Python 3.10+
```

---

## 系统支持

- Windows 10 / 11
- Ubuntu 22.04 / 24.04
- Debian
- Kali Linux

---

# 安装方法

## 1. 克隆项目

```bash
git clone https://github.com/W1IS5D0OM/SM2-SM4_Secure_Encrypt_System.git
```

进入项目目录：

```bash
cd SM2-SM4_Secure_Encrypt_System
```

---

## 2. 安装 Python 依赖

```bash
pip install -r requirements.txt
```

---

# 安装 GPG（PGP功能必须）

## Ubuntu / Debian

```bash
sudo apt update
sudo apt install gnupg
```

验证：

```bash
gpg --version
```

---

## Windows

下载安装：

Gpg4win：

https://www.gpg4win.org/

安装完成后验证：

```bash
gpg --version
```

若提示：

```text
gpg 不是内部或外部命令
```

需要手动添加：

```text
C:\Program Files (x86)\GnuPG\bin
```

到系统环境变量 PATH。

---

# 运行项目

```bash
python app.py
```

默认访问：

```text
http://127.0.0.1:5000
```

---

# 使用说明

# 一、SM2 + SM4 功能

## 1. 初始化密钥

点击：

```text
初始化密钥
```

系统自动：

- 生成 SM2 密钥对
- 生成 SM4 密钥
- 自动填充 key_id
- 自动填充加密后的 SM4 密钥

---

## 2. 文本加密

输入：

- key_id
- encrypted_sm4_key
- 明文

点击：

```text
加密
```

返回密文。

---

## 3. 文本解密

输入：

- key_id
- encrypted_sm4_key
- 密文

点击：

```text
解密
```

恢复原文。

---

## 4. 文件加密

上传文件后：

点击：

```text
文件加密
```

下载：

```text
xxx.ext.enc
```

---

## 5. 文件解密

上传：

```text
xxx.ext.enc
```

点击：

```text
文件解密
```

恢复原文件。

---

# 二、PGP 文件加密

## 使用步骤

### 1. 生成 PGP 密钥

```bash
gpg --full-generate-key
```

---

### 2. 导出公钥

```bash
gpg --armor --export your@email.com > public.asc
```

---

### 3. 打开 public.asc

复制：

```text
-----BEGIN PGP PUBLIC KEY BLOCK-----
...
-----END PGP PUBLIC KEY BLOCK-----
```

全部内容。

---

### 4. 网页中粘贴 PGP 公钥

上传待加密文件。

点击：

```text
PGP 文件加密
```

系统返回：

```text
xxx.gpg
```

---

# PGP 解密测试

使用私钥解密：

```bash
gpg -d xxx.gpg > restore.xxx
```

例如：

```bash
gpg -d test.jpg.gpg > restore.jpg
```

若恢复文件正常打开：

说明加密成功。

---

# 安全说明

本项目仅用于：

- 学习研究
- 课程设计
- 国密算法实验
- OpenPGP 功能测试

不建议直接用于生产环境。

当前版本：

- 未实现 HTTPS
- 未实现用户鉴权
- 未实现数据库
- 未实现 HSM
- 未实现正式 SM2 椭圆曲线运算库

---

# 技术栈

- Flask
- Python
- HTML
- JavaScript
- GnuPG
- OpenPGP
- SM2
- SM4

---

# 后续可扩展方向

- PGP 解密
- SM2 数字签名
- SM3 哈希
- 用户登录系统
- Docker 部署
- HTTPS
- 数据库存储
- JWT 鉴权
- 文件完整性校验

---

# License

MIT License

---

# 作者
Wisdom
-本项目制作起因为学院需要凑指标,让下面的同学必须提交一个项目,于是我花费2h时间做完了这样一个垃圾东西出来,将就看看吧
