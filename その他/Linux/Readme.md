## SSH鍵ペアを作成するコマンド
```
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```

## RSA鍵ペアをOpenSSLで作成する場合
```
# 秘密鍵を生成
openssl genrsa -out private.pem 4096

# 公開鍵を生成
openssl rsa -in private.pem -pubout -out public.pem
```

## 暗号化ツールで出力されたHexデータをバイナリに戻す
```
xxd -r -p Output.txt > output.bin
```

## 容量不足(No space left on device)
```
df -h

du -sh /* 2>/dev/null

du -sh /var/* 2>/dev/null

du -sh /var/lib/* 2>/dev/null
```

```
sudo systemctl stop docker
sudo rm -rf /var/lib/docker
sudo systemctl start docker
```


## bind9
### /etc/named.conf
skill53.localドメインの正引きをできるようにする
```
//
// named.conf
//
// Provided by Red Hat bind package to configure the ISC BIND named(8) DNS
// server as a caching only nameserver (as a localhost DNS resolver only).
//
// See /usr/share/doc/bind*/sample/ for example named configuration files.
//

options {
        listen-on port 53 { 127.0.0.1; {DNSサーバーIP}; };
        listen-on-v6 port 53 { ::1; };
        directory       "/var/named";
        dump-file       "/var/named/data/cache_dump.db";
        statistics-file "/var/named/data/named_stats.txt";
        memstatistics-file "/var/named/data/named_mem_stats.txt";
        secroots-file   "/var/named/data/named.secroots";
        recursing-file  "/var/named/data/named.recursing";
        # allow-query     { localhost; };
        allow-query     { any; };

        /* 
         - If you are building an AUTHORITATIVE DNS server, do NOT enable recursion.
         - If you are building a RECURSIVE (caching) DNS server, you need to enable 
           recursion. 
         - If your recursive DNS server has a public IP address, you MUST enable access 
           control to limit queries to your legitimate users. Failing to do so will
           cause your server to become part of large scale DNS amplification 
           attacks. Implementing BCP38 within your network would greatly
           reduce such attack surface 
        */
        recursion yes;

        dnssec-validation yes;

        managed-keys-directory "/var/named/dynamic";
        geoip-directory "/usr/share/GeoIP";

        pid-file "/run/named/named.pid";
        session-keyfile "/run/named/session.key";

        /* https://fedoraproject.org/wiki/Changes/CryptoPolicy */
        include "/etc/crypto-policies/back-ends/bind.config";
};

logging {
        channel default_debug {
                file "data/named.run";
                severity dynamic;
        };
        channel query_log {
                file "/var/log/named/queries.log" versions 10 size 20M;
                severity debug;
                print-time yes;
                print-severity yes;
                print-category yes;
        };
        
        category queries {
                 query_log;
        };
};

zone "." IN {
        type hint;
        file "named.ca";
};

zone "skill53.local" IN {
  type master;
  file "skill53.local.zone";
  allow-update { none; };
};

include "/etc/named.rfc1912.zones";
include "/etc/named.root.key";
```


### /var/named/skill53.local.zone
```
$TTL 86400
@   IN  SOA     ns1.skill53.local. admin.skill53.local. (
        2024010101  ; Serial
        3600        ; Refresh
        1800        ; Retry
        604800      ; Expire
        86400 )     ; Minimum TTL

@                               IN  NS      ns1.skill53.local.
ns1.skill53.local.              IN  A     10.3.136.117  
www.skill53.local.                     IN  A       10.3.2.220
```