from services.vector_db import QdrantAddressService

def get_address_by_tlc(tlc: str):
    
    qdrant = QdrantAddressService()
    return qdrant.get_address_by_tlc(tlc)
def get_address_by_plsam(plsam: str):
    
    qdrant = QdrantAddressService()
    return qdrant.get_address_by_plsam(plsam)


def get_plsam_tlc_by_address(address: str, top_k: int = 1):
    
    qdrant = QdrantAddressService()
    return qdrant.get_plsam_tlc_by_address(address, top_k=top_k)
