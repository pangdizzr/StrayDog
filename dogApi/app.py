import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from PIL import Image
from io import BytesIO

from embedding import image_to_vector
from vector_store import VectorStore
from search_logic import aggregate_by_pet

app = FastAPI(title="Dog ReID Service")

store = VectorStore(
    index_path="dog_index.faiss",
    meta_path="meta.npy"
)

class SearchResponse(BaseModel):
    status: str
    match_level: str = None
    top_match: dict = None
    candidates: list = None

@app.post("/search", response_model=SearchResponse)
async def search_dog(image: UploadFile = File(...)):
    """
    接收上传的狗图片，返回最相似宠物信息
    """
    try:
        img_bytes = await image.read()
        img = Image.open(BytesIO(img_bytes)).convert("RGB")
    except Exception:
        return {"status": "invalid_image"}

    # 生成向量
    vec = image_to_vector(img)

    # FAISS 搜索
    raw = store.search(vec, top_k=10)
    final = aggregate_by_pet(raw)

    if not final:
        return {"status": "no_match"}

    top1 = final[0]

    # 命中等级
    if top1["best_score"] >= 0.80:
        level = "high"
    elif top1["best_score"] >= 0.72 and top1["hits"] >= 2:
        level = "medium"
    else:
        level = "low"

    return {
        "status": "ok",
        "match_level": level,
        "top_match": top1,
        "candidates": final
    }
