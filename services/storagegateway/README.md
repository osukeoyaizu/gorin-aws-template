## 手順

### エンドポイント作成
storagegateway

### ゲートウェイ作成
- ボリュームゲートウェイ
- キャッシュボリューム
- EC2起動
    - m5.xlarge
    - パブリックアドレス付与
    - セキュリティグループで全許可
    - ボリューム追加
        - 80(ルート)
        - 165(キャッシュ)
        - 150(バッファ)
- APアドレス:パブリックIP
- ホストされたVPC


### 接続
https://docs.aws.amazon.com/ja_jp/storagegateway/latest/vgw/ConfiguringiSCSIClientInitiatorRedHatClient.html

```
sudo yum install -y iscsi-initiator-utils
sudo service iscsid start
sudo service iscsid status
```
```
sudo /sbin/iscsiadm --mode discovery --type sendtargets --portal [GATEWAY_IP]:3260
sudo /sbin/iscsiadm --mode node --targetname iqn.1997-05.com.amazon:[ISCSI_TARGET_NAME] --portal [GATEWAY_IP]:3260,1 --login
ls -l /dev/disk/by-path
```

### ファイルシステムを作成し、マウント
#### ファイルシステムを作成（初回のみ）
```
sudo mkfs.xfs /dev/sda
```
#### マウントポイント作成＆マウント
```
sudo mkdir -p /mnt/sgw_volume
sudo mount /dev/sda /mnt/sgw_volume
```
#### 再起動後も自動マウント
- UUID取得
```
sudo blkid /dev/sda
```
- /etc/fstab 編集
```
sudo vi /etc/fstab
```
- 追記
```
UUID=xxxx-xxxx  /mnt/sgw_volume  xfs  defaults,_netdev  0  0
```
- 確認(エラーが出なければ OK)
```
sudo umount /mnt/sgw_volume
sudo mount -a
```

### テストファイル作成
```
cd /mnt/sgw_volume
sudo touch test1.txt test2.txt test3.txt
sudo ls -l
echo "StorageGateway Test 1" | sudo tee test1.txt
echo "StorageGateway Test 2" | sudo tee test2.txt
echo "StorageGateway Test 3" | sudo tee test3.txt
```

### セッション削除
```
# マウント解除
umount /mnt/xxx

# iSCSI セッション確認
iscsiadm -m session

# ログアウト
iscsiadm -m node -T ターゲット名 -p IPアドレス --logout
```