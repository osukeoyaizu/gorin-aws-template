## install手順(amazonlinux2023)
https://qiita.com/tamorieeeen/items/13c7f8ea7c38a0146325

## javaインストール
```
dnf list --available "java-*corretto*"
sudo dnf -y install java-17-amazon-corretto-devel
```

## mavenインストール
```
dnf search maven
sudo dnf -y install maven
```

## Hello.java
```
public class Hello {
    public static void main(String[] args) {
        System.out.println("Hello, Amazon Linux 2023!");
    }
}
```

## ファイルコンパイル
```
sudo javac Hello.java
```

## コンパイルしたクラスを実行
```
sudo java Hello
```

## manifestファイル作成
```
Main-Class: Hello

```

## jarファイル作成
```
sudo jar cfe Hello.jar <クラス名> Hello.class
```

## jarファイル作成(manifstファイルあり)
```
jar cfm HelloWorld.jar manifest.txt HelloWorld.class
```

## jarファイル実行
```
sudo java -jar Hello.jar
```

## mavenを使用したjarファイル作成
```
cd <pom.xmlと同じ階層>
mvn package
```