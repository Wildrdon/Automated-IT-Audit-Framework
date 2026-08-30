import win32evtlog
from collections import defaultdict
from datetime import datetime, timedelta
from colorama import init, Fore
from tabulate import tabulate

init(autoreset=True)

SERVER = 'localhost'  # Log toplanacak Sunucu / DC IP'si
LOG_TYPE = 'Security'

print(Fore.CYAN + "[!] Windows Güvenlik Logları Taranıyor (Son 24 Saat)...\n")

hand = win32evtlog.OpenEventLog(SERVER, LOG_TYPE)
flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ

failed_logons = defaultdict(list)
account_changes = []

now = datetime.now()
time_limit = now - timedelta(hours=24)

events_processed = 0

while True:
    events = win32evtlog.ReadEventLog(hand, flags, 0)
    if not events:
        break
    
    for event in events:
        event_time = event.TimeGenerated.replace(tzinfo=None)
        if event_time < time_limit:
            continue
            
        event_id = event.EventID & 0xFFFF
        events_processed += 1
        
        # 1. Başarısız Giriş Denemeleri (Event ID 4625)
        if event_id == 4625:
            user = event.StringInserts[0] if event.StringInserts else "Unknown"
            failed_logons[user].append(event_time)
            
        # 2. Yeni Kullanıcı Oluşturuldu (Event ID 4720)
        elif event_id == 4720:
            created_user = event.StringInserts[0] if event.StringInserts else "Unknown"
            by_who = event.StringInserts[4] if len(event.StringInserts) > 4 else "Unknown"
            account_changes.append([event_time.strftime('%Y-%m-%d %H:%M'), "Yeni Kullanıcı", created_user, by_who])
            
        # 3. Gruba Üye Eklendi (Event ID 4728)
        elif event_id == 4728:
            member = event.StringInserts[0] if event.StringInserts else "Unknown"
            group = event.StringInserts[2] if len(event.StringInserts) > 2 else "Unknown"
            account_changes.append([event_time.strftime('%Y-%m-%d %H:%M'), f"Gruba Eklendi ({group})", member, "N/A"])

# --- RAPORLAMA ---

# Brute-Force Analizi (10 Dk içinde 5+ Başarısız Giriş)
brute_force_alerts = []
for user, timestamps in failed_logons.items():
    timestamps.sort()
    for i in range(len(timestamps)):
        # 10 dakikalık pencere kontrolü
        window_events = [t for t in timestamps if 0 <= (t - timestamps[i]).total_seconds() <= 600]
        if len(window_events) >= 5:
            brute_force_alerts.append([user, len(window_events), "YÜKSEK (Brute-Force İhlali)"])
            break

print(Fore.YELLOW + f"[!] Toplam İşlenen Olay Sayısı: {events_processed}\n")

print(Fore.RED + "[!] ŞÜPHELİ OTURUM AÇMA / BRUTE-FORCE ALARMLARI")
if brute_force_alerts:
    print(tabulate(brute_force_alerts, headers=["Kullanıcı Adı", "10 Dk'daki Deneme", "Tehdit Seviyesi"], tablefmt="grid"))
else:
    print(Fore.GREEN + "[+] Şüpheli Brute-Force aktivitesi tespit edilmedi.\n")

print(Fore.MAGENTA + "\n[!] KRİTİK HESAP VEYA GRUP DEĞİŞİKLİKLERİ")
if account_changes:
    print(tabulate(account_changes, headers=["Tarih/Saat", "Olay Tipi", "Hedef Hesap/Grup", "Yapan Kullanıcı"], tablefmt="grid"))
else:
    print(Fore.GREEN + "[+] Son 24 saatte kritik hesap değişikliği bulunamadı.")
