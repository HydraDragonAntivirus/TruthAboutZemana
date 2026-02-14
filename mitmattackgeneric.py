import logging
from mitmproxy import http

def request(flow: http.HTTPFlow) -> None:
    # 1. Her gelen isteği terminale bas (bağlantıyı test etmek için)
    # logging.info yerine print kullanarak tamponu (buffer) zorlayalım
    print(f"\n[AKIS] {flow.request.pretty_host} -> {flow.request.path}")

    # 2. Zemana kontrolünü daha esnek yapalım (case-insensitive)
    if "zemana" in flow.request.pretty_host.lower():
        print("!!!" + " ZEMANA YAKALANDI ".center(40, "=") + "!!!")
        
        # Multipart içeriği kontrol et
        if b"BOUNDARYSTRING" in flow.request.content:
            print("[+] Dosya yükleme (Multipart) içeriği bulundu!")
            # Ham verinin ilk 200 karakterini bas
            print(flow.request.content[:200].decode(errors='ignore'))