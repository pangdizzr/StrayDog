# StrayDog - 流浪狗识别服务

基于深度学习的流浪狗重识别（ReID）服务，通过图像特征提取和向量相似度搜索，帮助识别和匹配流浪狗信息。

## 功能特性

- 🐕 **图像识别**: 上传狗的照片，自动提取特征向量
- 🔍 **相似度搜索**: 使用FAISS向量数据库进行快速相似度匹配
- 📊 **智能聚合**: 按宠物ID聚合搜索结果，返回最佳匹配和候选结果
- 🎯 **匹配等级**: 根据相似度分数和命中次数，自动判断匹配等级（高/中/低）
- 🚀 **RESTful API**: 基于FastAPI构建，提供标准的HTTP接口

## 技术栈

- **Web框架**: FastAPI
- **深度学习**: PyTorch, TorchVision
- **特征提取**: ResNet50
- **向量搜索**: FAISS-CPU
- **图像处理**: Pillow
- **数值计算**: NumPy

## 项目结构

```
StrayDog/
├── README.md                 # 项目说明文档
├── data/                     # 数据目录
│   └── dogs.xlsx            # 狗的数据文件
└── dogApi/                   # API服务目录
    ├── app.py               # FastAPI应用主文件
    ├── embedding.py         # 图像特征提取模块
    ├── vector_store.py      # FAISS向量存储模块
    ├── search_logic.py      # 搜索结果聚合逻辑
    ├── requirements.txt     # Python依赖包列表
    ├── dog_index.faiss      # FAISS索引文件
    ├── meta.npy            # 元数据文件
    └── test.py             # 测试文件
```

## 安装步骤

### 1. 环境要求

- Python 3.7+
- pip

### 2. 安装依赖

```bash
cd dogApi
pip3 install -r requirements.txt
```

### 3. 依赖包列表

- `fastapi` - Web框架
- `uvicorn` - ASGI服务器
- `torch` - PyTorch深度学习框架
- `torchvision` - 计算机视觉工具库
- `faiss-cpu` - Facebook AI相似度搜索库（CPU版本）
- `pillow` - 图像处理库
- `requests` - HTTP请求库
- `numpy` - 数值计算库

## 启动服务

### 开发模式（自动重载）

```bash
cd dogApi
python3 -m uvicorn app:app --reload
```

### 生产模式

```bash
cd dogApi
python3 -m uvicorn app:app --host 0.0.0.0 --port 8000
```

服务启动后，访问以下地址：

- **API文档**: http://localhost:8000/docs
- **API根路径**: http://localhost:8000

## API使用说明

### 搜索接口

**接口地址**: `POST /search`

**接口描述**: 上传狗的照片，返回最相似的宠物信息

**请求参数**:
- **请求类型**: `multipart/form-data`
- **参数名**: `image`
- **参数类型**: 文件（支持常见图片格式：jpg, png, jpeg等）

**响应字段说明**:

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `status` | string | 请求状态：`ok`(成功)、`no_match`(未找到匹配)、`invalid_image`(无效图片) |
| `match_level` | string | 匹配等级：`high`(高)、`medium`(中)、`low`(低) |
| `top_match` | object | 最佳匹配结果 |
| `top_match.pet_id` | integer | 宠物ID |
| `top_match.best_score` | float | 最佳相似度分数（0-1之间） |
| `top_match.hits` | integer | 命中次数（该宠物在搜索结果中出现的次数） |
| `top_match.sample_urls` | array | 示例图片URL列表（最多2张） |
| `candidates` | array | 候选匹配结果列表（按相似度降序排列） |

**响应示例**:

```json
{
  "status": "ok",
  "match_level": "high",
  "top_match": {
    "pet_id": 12345,
    "best_score": 0.85,
    "hits": 3,
    "sample_urls": [
      "http://example.com/image1.jpg",
      "http://example.com/image2.jpg"
    ]
  },
  "candidates": [
    {
      "pet_id": 12345,
      "best_score": 0.85,
      "hits": 3,
      "sample_urls": [
        "http://example.com/image1.jpg",
        "http://example.com/image2.jpg"
      ]
    },
    {
      "pet_id": 67890,
      "best_score": 0.75,
      "hits": 2,
      "sample_urls": [
        "http://example.com/image3.jpg"
      ]
    }
  ]
}
```

**匹配等级判断规则**:
- **高匹配** (`high`): 最佳匹配分数 >= 0.80
- **中匹配** (`medium`): 最佳匹配分数 >= 0.72 且命中次数 >= 2
- **低匹配** (`low`): 其他情况

**状态码说明**:
- **`ok`**: 成功找到匹配结果
- **`no_match`**: 未找到匹配的宠物信息
- **`invalid_image`**: 上传的文件不是有效的图片格式

**错误响应示例**:

```json
{
  "status": "invalid_image"
}
```

```json
{
  "status": "no_match"
}
```

### 使用示例

**使用curl命令测试**:

```bash
curl -X POST "http://localhost:8000/search" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "image=@/path/to/dog_image.jpg"
```

**使用Python requests库**:

```python
import requests

url = "http://localhost:8000/search"
files = {"image": open("dog_image.jpg", "rb")}
response = requests.post(url, files=files)
result = response.json()
print(result)
```

**使用JavaScript fetch**:

```javascript
const formData = new FormData();
formData.append('image', fileInput.files[0]);

fetch('http://localhost:8000/search', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => console.log(data));
```

## 工作原理

1. **特征提取**: 使用预训练的ResNet50模型提取图像特征向量（2048维）
2. **向量归一化**: 对特征向量进行L2归一化
3. **相似度搜索**: 在FAISS索引中搜索top-k最相似的向量
4. **结果聚合**: 按宠物ID聚合搜索结果，计算最佳分数和命中次数
5. **等级判断**: 根据分数和命中次数判断匹配等级

## 注意事项

- 确保 `dog_index.faiss` 和 `meta.npy` 文件存在于 `dogApi` 目录下
- 首次运行时会加载模型和索引，可能需要一些时间
- 建议使用GPU版本的PyTorch和FAISS以获得更好的性能（当前使用CPU版本）
- 图像会被自动调整为224x224大小进行特征提取

## 开发说明

- 修改代码后，使用 `--reload` 参数会自动重启服务
- API文档可通过访问 `/docs` 路径查看交互式Swagger UI
- 所有依赖包版本见 `dogApi/requirements.txt`
