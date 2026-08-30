import json
import logging
import os

logging.basicConfig(
    filename='audit_execution.log',
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s'
)

def main():
    try:
        if not os.path.exists("config.json"):
            raise FileNotFoundError("config.json dosyasi bulunamadi!")

        with open("config.json", "r") as f:
            config = json.load(f)

        ip = config["domain_info"]["server_ip"]
        print(f"[*] Denetim Baslatildi. Hedef IP: {ip}")
        logging.info(f"Config basariyla okundu. Hedef IP: {ip}")

    except json.JSONDecodeError:
        print("[!] HATA: config.json dosyasi bozuk (JSON formati hatali)!")
        logging.error("JSON okuma hatasi: Format bozuk.")
    except Exception as e:
        print(f"[!] HATA: {e}")
        logging.error(f"Beklenmeyen hata: {e}")
    finally:
        print("[*] Islemler tamamlandi. Log dosyasi: audit_execution.log")

if __name__ == "__main__":
    main()
