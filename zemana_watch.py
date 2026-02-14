from mitmproxy import http
import re

def request(flow: http.HTTPFlow) -> None:
    # Sadece zemana.com trafiğine bak
    if "zemana.com" in flow.request.pretty_host:
        
        # PostForm (Dosya Yükleme) tespiti
        if b"----------ZAM-MULTIPARTBOUNDARYSTRING" in flow.request.content:
            print("\n" + "="*50)
            print(f"[!] ZEMANA DOSYA YÜKLEME YAKALANDI!")
            print(f"Target: {flow.request.url}")
            
            content = flow.request.content.decode(errors='ignore')
            
            # Parametreleri ayıkla
            for field in ['md5', 'hardwareid', 'version']:
                match = re.search(f'name="{field}"\\r\\n\\r\\n(.*?)\\r\\n', content)
                if match:
                    print(f" -> {field.upper()}: {match.group(1).strip()}")
            
            print("="*50 + "\n")

        # JSON (Ayarlar/Sonuçlar) tespiti
        elif "application/json" in flow.request.headers.get("Content-Type", ""):
            print(f"[i] Zemana JSON Gönderisi: {flow.request.text[:100]}...")
