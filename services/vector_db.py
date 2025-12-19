import os
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any, Optional

from dotenv import load_dotenv


# Load env vars
load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION")

if not QDRANT_URL or not QDRANT_API_KEY:
    raise ValueError("Please set QDRANT_URL and QDRANT_API_KEY in .env")

client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY, prefer_grpc=False)

# Embedding model
embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
VECTOR_SIZE = 768

class QdrantAddressService:
    def __init__(self):
        self.client = client

    def _iter_hits(self, res):
        if not res:
            return
        for item in res:
            if hasattr(item, "payload") or (isinstance(item, dict) and "payload" in item):
                yield item
            elif isinstance(item, (list, tuple)):
                for sub in item:
                    if hasattr(sub, "payload") or (isinstance(sub, dict) and "payload" in sub):
                        yield sub
            else:
                continue

    def get_address_by_tlc(self, tlc: str) -> Optional[Dict[str, Any]]:
        flt = Filter(must=[FieldCondition(key="tlc", match=MatchValue(value=tlc))])
        res = self.client.scroll(
            collection_name=COLLECTION_NAME,
            scroll_filter=flt,
            limit=1,
            with_payload=True,
            with_vectors=False
        )
        for hit in self._iter_hits(res):
            if hasattr(hit, "payload"):
                return hit.payload
            if isinstance(hit, dict):
                return hit.get("payload")
        return None

    def get_address_by_plsam(self, plsam: str) -> Optional[Dict[str, Any]]:
        flt = Filter(must=[FieldCondition(key="plsam", match=MatchValue(value=plsam))])
        res = self.client.scroll(
            collection_name=COLLECTION_NAME,
            scroll_filter=flt,
            limit=1,
            with_payload=True,
            with_vectors=False
        )
        for hit in self._iter_hits(res):
            if hasattr(hit, "payload"):
                return hit.payload
            if isinstance(hit, dict):
                return hit.get("payload")
        return None
    def get_plsam_tlc_by_address(self, address: str, top_k: int = 1) -> List[Dict[str, Any]]:
        flt = Filter(
            must=[FieldCondition(key="address", match=MatchValue(value=address))]
        )
        res = self.client.scroll(
            collection_name=COLLECTION_NAME,
            scroll_filter=flt,
            limit=top_k,
            with_payload=True,
            with_vectors=False
        )
        out = []
        for hit in self._iter_hits(res):
            if hasattr(hit, "payload"):
                payload = hit.payload
            elif isinstance(hit, dict):
                payload = hit.get("payload", {})
            else:
                continue
            out.append({"plsam": payload.get("plsam"), "tlc": payload.get("tlc")})
            if len(out) >= top_k:
                break
        return out


