## MySQL
```
sudo dnf install mariadb105
```

## PostgreSQL
```
sudo dnf install -y postgresql15
```

## Oracle
```
sudo dnf install -y libaio unzip
sudo dnf install -y https://download.oracle.com/otn_software/linux/instantclient/219000/oracle-instantclient-basic-21.9.0.0.0-1.el8.x86_64.rpm
sudo dnf install -y https://download.oracle.com/otn_software/linux/instantclient/219000/oracle-instantclient-sqlplus-21.9.0.0.0-1.el8.x86_64.rpm
sudo sh -c "echo /usr/lib/oracle/21/client64/lib > /etc/ld.so.conf.d/oracle-instantclient.conf"
sudo ldconfig
echo 'export PATH=$PATH:/usr/lib/oracle/21/client64/bin' >> ~/.bashrc
source ~/.bashrc
```

