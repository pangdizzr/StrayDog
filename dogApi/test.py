import faiss
import numpy as np

index = faiss.read_index("dog_index.faiss")
meta = np.load("meta.npy", allow_pickle=True)

print("index size:", index.ntotal)
print("meta size:", len(meta))
print("first meta:", meta[0])
