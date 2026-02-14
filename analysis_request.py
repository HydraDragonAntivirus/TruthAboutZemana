import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# C# kodundaki (Satir 646) Boundary tanimi (10 tire)
BOUNDARY_VALUE = "----------ZAM-MULTIPARTBOUNDARYSTRING"
# Govde icinde kullanilan ayirici (12 tire) -> ("--" + BOUNDARY_VALUE)
BOUNDARY_SEPARATOR = f"--{BOUNDARY_VALUE}"

URL = "https://zam-cloud.zemana.com/api/scan-post-feedback"

# C# WebClient varsayilan davranislarini taklit eden headerlar
headers = {
    "Content-Type": f"multipart/form-data; boundary={BOUNDARY_VALUE}",
    "Expect": "100-continue",  # .NET WebClient bunu varsayilan olarak gonderir
    "Connection": "Keep-Alive",
    # User-Agent'i bos birakmak veya .NET gibi gostermek daha guvenlidir
    "User-Agent": "ZemanaAntiMalware/1.0" 
}

def build_strict_body(data):
    # String yerine dogrudan BYTES listesi olusturuyoruz
    buffer = []
    
    for key, value in data.items():
        # 1. Boundary ve CRLF
        buffer.append(f"{BOUNDARY_SEPARATOR}\r\n".encode('utf-8'))
        
        # 2. Content-Disposition (C# Satir 652)
        # Dikkat: C# kodunda name="..." kismindan sonra \r\n var.
        buffer.append(f'Content-Disposition: form-data; name="{key}"\r\n'.encode('utf-8'))
        
        # 3. Content-Type (C# Satir 652)
        buffer.append("Content-Type: text/plain; charset=utf-8\r\n".encode('utf-8'))
        
        # 4. Content-Transfer-Encoding (C# Satir 652)
        buffer.append("Content-Transfer-Encoding: 8bit\r\n\r\n".encode('utf-8'))
        
        # 5. Deger (C# Satir 653)
        buffer.append(str(value).encode('utf-8'))
        
        # 6. Deger sonrasi CRLF (C# Satir 654)
        buffer.append(b"\r\n")
        
    # Footer (C# Satir 674)
    # ------------ZAM-MULTIPARTBOUNDARYSTRING--\r\n
    buffer.append(f"{BOUNDARY_SEPARATOR}--\r\n".encode('utf-8'))
    
    # Hepsini tek bir byte dizisine birlestir
    return b"".join(buffer)

payload = {
    "h": "85018be1fd913656bc9ff541f017eacd",
    "isFree": "False",
    "culture": "en-US",
    "partnerId": "2"
}

body_data = build_strict_body(payload)

print(f"[*] Gönderilecek veri uzunluğu: {len(body_data)} bytes")
# print(body_data) # Debug icin byte halini gorebilirsin

try:
    # Veriyi 'data' parametresine BYTES olarak veriyoruz
    response = requests.post(
        URL, 
        data=body_data, 
        headers=headers, 
        verify=False, 
        timeout=30
    )
    
    print(f"[+] Durum Kodu: {response.status_code}")
    print(f"[+] Yanıt Başlıkları: {response.headers}")
    print(f"[+] Yanıt İçeriği: {response.text}")

except Exception as e:
    print(f"[!] Hata oluştu: {e}")