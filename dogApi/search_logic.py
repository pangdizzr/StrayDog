from collections import defaultdict

def aggregate_by_pet(results):
    bucket = defaultdict(list)

    for r in results:
        bucket[r["pet_id"]].append(r)

    final = []
    for pet_id, items in bucket.items():
        scores = [x["score"] for x in items]
        final.append({
            "pet_id": pet_id,
            "best_score": max(scores),
            "hits": len(scores),
            "sample_urls": [x["url"] for x in items[:2]]
        })

    final.sort(key=lambda x: x["best_score"], reverse=True)
    return final
