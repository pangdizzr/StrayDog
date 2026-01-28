import faiss
import numpy as np

class VectorStore:
    def __init__(self, index_path: str, meta_path: str):
        self.index = faiss.read_index(index_path)
        self.meta = np.load(meta_path, allow_pickle=True)

        assert self.index.ntotal == len(self.meta), \
            "❌ index 向量数 和 meta 数量不一致"

        print(f"✅ VectorStore loaded: {self.index.ntotal} vectors")

    def search(self, vector: np.ndarray, top_k=10):
        scores, idxs = self.index.search(vector.reshape(1, -1), top_k)

        results = []
        for score, idx in zip(scores[0], idxs[0]):
            m = self.meta[idx]
            results.append({
                "score": float(score),
                "pet_id": int(m["pet_id"]),
                "owner_id": int(m.get("owner_id", -1)),
                "url": m["url"]
            })
        return results
