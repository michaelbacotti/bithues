---
name: dns-diagnostic
description: Use when troubleshooting DNS issues, domain resolution problems, or website availability. Follow the diagnostic flowchart to avoid circular troubleshooting and misdiagnosis.
---

# dns-diagnostic

## When to Use

- "website not loading"
- "DNS not working"
- "www subdomain broken"
- Cloudflare/GoDaddy/Namecheap DNS changes not taking effect
- GitHub Pages "DNS check unsuccessful"

## Diagnostic Order (never skip)

### Step 1: Check Locally
```bash
dig <domain> +short
dig <domain> CNAME +short
dig <domain> A +short
host <domain> 2>&1
```
This tells you what YOUR machine sees.

### Step 2: Check From Multiple Public Resolvers
```bash
nslookup <domain> 8.8.8.8    # Google DNS
nslookup <domain> 1.1.1.1    # Cloudflare DNS
```
If public resolvers show correct values → problem is local cache.
If public resolvers also show wrong values → problem is authoritative DNS.

### Step 3: Check the Authoritative NS
```bash
dig ns <domain> +short
```
This shows who controls the domain's delegation.

### Step 4: Check Zone vs Registry

**Common mistake:** Confusing DNS records in a zone (Cloudflare/GoDaddy DNS panel) with domain registry delegation (who the registrar says is authoritative for subdomains).

**Key distinction:**
- **Zone records** = what Cloudflare/GoDaddy manages for the domain
- **Registry delegation** = what the domain registrar tells the root servers about who handles subdomains
- **CNAME override** = a CNAME record should take precedence, but NS delegation at the registry level can override it

### Step 5: Check for NS Delegation on Subdomains

If `www.example.com` resolves to wrong IP:
```bash
dig ns www.example.com +short
```
If this returns nameservers (ns1.something.com) instead of nothing → there's a **registry-level NS delegation** for `www` that overrides the zone CNAME.

**This was the www.bithues.com problem (2026-04-06):**
- Cloudflare zone had correct CNAME for www → GitHub Pages ✅
- But registry had NS records for `www` → Afternic nameservers → wrong IP
- The NS records at registry level override zone CNAMEs

### Step 6: Check for Email Routing A Records

Cloudflare Email Routing automatically adds A records for `www` pointing to mail server IPs (76.223.54.146, 13.248.169.48). These override CNAMEs.

If email routing is enabled and www stopped working:
1. Check if there are A records for `www` in the Cloudflare zone
2. Delete them
3. Keep the CNAME

## GitHub Pages Specific

GitHub Pages requires:
1. **Apex domain** → GitHub Pages IPs (185.199.108-111.153) OR CNAME to `*.github.io`
2. **www subdomain** → CNAME to `{username}.github.io` AND added as custom domain in GitHub Pages settings
3. **Custom domain configured in GitHub** → Settings → Pages → Custom domain (separate from DNS!)

**Common issue:** DNS is correct but GitHub Pages settings don't have www configured. Fix: go to GitHub repo → Settings → Pages → add www subdomain.

## DNS Troubleshooting Flowchart

```
Problem: www.example.com not working
│
├─ dig +short www.example.com
│   └─ Returns correct IP/CNAME?
│       ├─ YES → GitHub Pages settings missing www as custom domain
│       └─ NO → Continue
│
├─ dig ns www.example.com
│   └─ Returns nameservers (not empty)?
│       ├─ YES → Registry-level NS delegation for www — check registrar
│       └─ NO → Continue
│
├─ Check Cloudflare zone for www records
│   ├─ A record present? → DELETE it
│   ├─ CNAME present? → OK
│   └─ Proxy = ON (orange)? → Set to DNS only (grey)
│
└─ Wait 5 min → retry
```

## Quick Commands Reference

```bash
# Full resolution path
dig <domain> +trace

# Check specific record type
dig <domain> A +short
dig <domain> CNAME +short
dig <domain> MX +short
dig <domain> NS +short

# Check from public resolvers
nslookup <domain> 8.8.8.8
nslookup <domain> 1.1.1.1

# SSL check
echo | openssl s_client -connect <domain>:443 2>/dev/null | openssl x509 -noout -dates

# HTTP check
curl -sI "https://<domain>/" | head -5
```
