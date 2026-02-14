import requests
import hashlib
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class ZemanaAIRequest:
    def __init__(self):
        # Çalıştığı kesin olan ana sunucu
        self.base_url = "https://zam-ai.zemana.com/api/client/settings"
        self.user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:5.0) Gecko/20100101 Firefox/5.0"

    def get_md5(self, file_path):
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def kill_request(self, file_path):
        file_hash = self.get_md5(file_path)
        
        # Senin daha önce 200 OK aldığın URL yapısını hash sorgusu için modifiye ediyoruz
        # Format: base_url / {HASH} / {PartnerID} / {ProductID} / {Version}
        # Bazı API'lerde settings yerine 'check' veya 'scan' gelir ama önce settings yolunu deneyelim
        
        target_url = f"{self.base_url}/{file_hash}/2/2/3002028/"
        
        print(f"[*] Hedef Tahtası: {target_url}")
        
        headers = {
            "User-Agent": self.user_agent,
            "Accept": "application/json"
        }

        try:
            # Burası kritik: verify=False SSL hatasını ezer
            response = requests.get(target_url, headers=headers, verify=False, timeout=15)
            
            if response.status_code == 200:
                return f"[+] BİNGO! Sunucu Yanıtı: {response.text}"
            else:
                # Eğer hala 404 verirse, 'settings' kısmını 'scan' olarak değiştirmeyi deneyeceğiz
                return f"[-] Sunucu yine 404 verdi. Yol yanlış ama sunucu ayakta. Kod: {response.status_code}"
        except Exception as e:
            return f"[!] Bağlantı koptu: {e}"

# --- ATEŞLE ---
client = ZemanaAIRequest()
print(client.kill_request("test_dosyasi.exe"))
