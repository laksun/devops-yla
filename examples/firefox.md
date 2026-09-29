The most robust approach is to force Firefox to use a family-filtering DNS service and lock that setting with a policy file, so it can't be changed from within the browser.

**1. Create a policy file**

Create `C:\Program Files\Mozilla Firefox\distribution\policies.json` (you'll need to create the `distribution` folder) with:

```json
{
  "policies": {
    "DNSOverHTTPS": {
      "Enabled": true,
      "ProviderURL": "https://family.cloudflare-dns.com/dns-query",
      "Locked": true
    },
    "DisablePrivateBrowsing": true,
    "BlockAboutConfig": true,
    "ExtensionSettings": {
      "*": { "installation_mode": "blocked" }
    }
  }
}
```

This forces Cloudflare's family DNS, which blocks adult content and malware. It also disables private windows and `about:config`, and blocks add-on installs so VPN or proxy extensions can't get around the filter. If you'd prefer a filter that also enforces SafeSearch, CleanBrowsing's family filter (`https://doh.cleanbrowsing.org/doh/family-filter/`) is an alternative.

**2. Restart Firefox and verify**

Open `about:policies` to confirm the policies are active. Then check Settings → Privacy & Security → DNS over HTTPS, which should be greyed out.

**3. Lock down Windows itself**

The person being filtered should use a standard (non-admin) Windows account. Otherwise they could just edit or delete the policy file. It's also worth removing other browsers or blocking them, since Microsoft Family Safety's web filtering only applies to Edge.

**If you already filter at the network level** (for example with AdGuard Home or OpenDNS), there's an alternative. Instead of pointing Firefox at a family provider, set `"Enabled": false, "Locked": true` under `DNSOverHTTPS`. This stops Firefox from using its own encrypted DNS, which would otherwise bypass your router or AdGuard filtering.
