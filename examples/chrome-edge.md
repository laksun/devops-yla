Chrome ve Edge'de aynı ayarları yapmak için PowerShell'i **Yönetici olarak** açıp aşağıdaki komutları çalıştırın.

**Chrome**

```powershell
$c = "HKLM:\SOFTWARE\Policies\Google\Chrome"
New-Item -Path $c -Force | Out-Null
# Aile filtreli DNS (DoH) - kilitli
Set-ItemProperty -Path $c -Name DnsOverHttpsMode -Value "secure"
Set-ItemProperty -Path $c -Name DnsOverHttpsTemplates -Value "https://family.cloudflare-dns.com/dns-query"
# Gizli pencereyi kapat
Set-ItemProperty -Path $c -Name IncognitoModeAvailability -Value 1 -Type DWord
# Tüm eklenti kurulumlarını engelle
New-Item -Path "$c\ExtensionInstallBlocklist" -Force | Out-Null
Set-ItemProperty -Path "$c\ExtensionInstallBlocklist" -Name "1" -Value "*"
# Ek: Google ve YouTube güvenli arama
Set-ItemProperty -Path $c -Name ForceGoogleSafeSearch -Value 1 -Type DWord
Set-ItemProperty -Path $c -Name ForceYouTubeRestrict -Value 2 -Type DWord
```

**Edge**

```powershell
$e = "HKLM:\SOFTWARE\Policies\Microsoft\Edge"
New-Item -Path $e -Force | Out-Null
# Aile filtreli DNS (DoH) - kilitli
Set-ItemProperty -Path $e -Name DnsOverHttpsMode -Value "secure"
Set-ItemProperty -Path $e -Name DnsOverHttpsTemplates -Value "https://family.cloudflare-dns.com/dns-query"
# InPrivate pencereyi kapat
Set-ItemProperty -Path $e -Name InPrivateModeAvailability -Value 1 -Type DWord
# Tüm eklenti kurulumlarını engelle
New-Item -Path "$e\ExtensionInstallBlocklist" -Force | Out-Null
Set-ItemProperty -Path "$e\ExtensionInstallBlocklist" -Name "1" -Value "*"
# Ek: Bing, Google ve YouTube güvenli arama
Set-ItemProperty -Path $e -Name ForceBingSafeSearch -Value 2 -Type DWord
Set-ItemProperty -Path $e -Name ForceGoogleSafeSearch -Value 1 -Type DWord
Set-ItemProperty -Path $e -Name ForceYouTubeRestrict -Value 2 -Type DWord
```

**Doğrulama**

Tarayıcıları tamamen kapatıp yeniden açın. Ardından Chrome'da `chrome://policy`, Edge'de `edge://policy` sayfasını açıp **Politikaları yeniden yükle** butonuna basın. Tarayıcıda "Kuruluşunuz tarafından yönetiliyor" yazısı görünmesi normaldir.

**Birkaç not**

- `ForceYouTubeRestrict` değerinde 2 katı kısıtlama, 1 orta düzey kısıtlama anlamına gelir.
- Ağ düzeyinde AdGuard Home veya OpenDNS kullanıyorsanız ve tarayıcının bu filtreyi atlamasını istemiyorsanız, `DnsOverHttpsMode` değerini `"off"` yapıp `DnsOverHttpsTemplates` satırını silin.
- Firefox'taki `about:config` engelinin birebir karşılığı yok. Ancak ayarlar zaten kayıt defterinden yönetildiği için tarayıcı içinden değiştirilemez. Kullanıcının standart (yönetici olmayan) hesap kullanması yine şart.
