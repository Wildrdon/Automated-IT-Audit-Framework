import datetime 
from ldap3 import Server, Connection, ALL, SIMPLE
from colorama import init, Fore
from tabulate import tabulate

init(autoreset=True)

# GİZLİLİK VE GÜVENLİK İÇİN BİLGİLER ANONİMLEŞTİRİLMİŞTİR
LDAP_SERVER = '192.168.X.X'
LDAP_USER = 'audit_admin@yourdomain.local'
LDAP_PASSWORD = 'YOUR_SECURE_PASSWORD'
BASE_DN = 'DC=yourdomain,DC=local'

server = Server(LDAP_SERVER, get_info=ALL)
conn = Connection(server, user=LDAP_USER, password=LDAP_PASSWORD, authentication=SIMPLE)

if not conn.bind():
	print(Fore.RED + f"[-] Bağlantı Hatası: {conn.result}")
	exit()

print(Fore.GREEN + "\n[+] Active Directory Sunucusuna Başarıyla Bağlanıldı!")
print(Fore.CYAN + "=" * 65)

print(Fore.YELLOW + "\n[!] MODÜL 1: Parola Süresi Dolmayan Hesaplar Taranıyor...")
search_filter_pne = '(&(objectCategory=person)(objectClass=user)(userAccountControl:1.2.840.113556.1.4.803:=65536))'
conn.search(BASE_DN, search_filter_pne, attributes=['sAMAccountName'])

pne_results = []
for entry in conn.entries:
	pne_results.append([entry.sAMAccountName.value, "ZAFİYET: Şifre Süresi Dolmuyor"])

print(tabulate(pne_results, headers=["Kullanıcı Adı", "Risk Durumu"], tablefmt="grid"))

print(Fore.YELLOW + "\n[!] Modül 2: Domain Admins Grubu Üyeleri Taranıyor...")
group_dn = f"CN=Domain Admins,CN=Users,{BASE_DN}"
conn.search(BASE_DN, f"(&(objectCategory=user)(memberOf={group_dn}))", attributes=['sAMAccountName'])

admin_results = []
for entry in conn.entries:
	admin_results.append([entry.sAMAccountName.value, "YÜKSEK YETKİ (Domain Admin)"])
print(tabulate(admin_results, headers=["Kullanıcı Adı", "Yetki Seviyesi"], tablefmt="grid"))

print(Fore.YELLOW + "\n[!] MODÜL 3: Pasif Hesaplar Taranıyor...")
conn.search(BASE_DN, '(&(objectCategory=person)(objectClass=user))', attributes=['sAMAccountName', 'lastLogonTimestamp'])

def convert_ad_timestamp(timestamp):
	if isinstance(timestamp, datetime.datetime):
		return timestamp.replace(tzinfo=None)
	return None

passive_results = []
now = datetime.datetime.now()
for entry in conn.entries:
	raw_ts = entry.lastLogonTimestamp.value if 'lastLogonTimestamp' in entry else None
	last_logon = convert_ad_timestamp(raw_ts)

	if last_logon:
		days_inactive = (now - last_logon).days
		if days_inactive > 90:
			passive_results.append([entry.sAMAccountName.value, last_logon.strftime('%Y-%m-%d'), f"{days_inactive} gün"])
	else:
		passive_results.append([entry.sAMAccountName.value, "Hiç Oturum Açılmadı", "N/A"])
print(tabulate(passive_results, headers=["Kullanıcı Adı", "Son Giriş Tarihi", "Pasif Kalınan Süre"], tablefmt="grid"))

conn.unbind()
print(Fore.GREEN + "\n[+] AD Güvenlik ve ITGC Otomatik Taraması Tamamlandı!")
