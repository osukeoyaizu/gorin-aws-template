## task1
Nova Microのモデルアクセスを有効化する

### エージェントを編集してアクショングループ追加
名前:任意

Lambda関数:virtual-librarian-books-function

#### アクショングループ関数1
名前:search_books

説明:search_books

パラメータ:search_term

説明(パラメータ):the title, author, or subject of the book to search for


#### アクショングループ関数2
名前:get_similar_books

説明:get_similar_books

パラメータ:title

説明(パラメータ):title


**※保存&準備をする**

## task2
### エージェントを編集してアクショングループ追加
名前:任意

Lambda関数:virtual-librarian-users-function

#### アクショングループ関数1
名前:get_username

説明:get_username

パラメータ1:key

説明(パラメータ1):can be email or phone

パラメータ2:value

説明(パラメータ2):for the actual email address or the phone number


#### アクショングループ関数2
名前:validate_username

説明:validate_username

パラメータ:username

説明(パラメータ):username


**※保存&準備をする**

## task3
### エージェントを編集してアクショングループ追加
名前:任意

Lambda関数:virtual-librarian-reservation-function

#### アクショングループ関数1
名前:reserve_book

説明:reserve_book

パラメータ1:book_id

説明(パラメータ1):book_id 

パラメータ2:username

説明(パラメータ2):username


#### アクショングループ関数2
名前:cancel_reservation

説明:cancel_reservation

パラメータ1:book_id

説明(パラメータ1):book_id 

パラメータ2:username

説明(パラメータ2):username


#### アクショングループ関数3
名前:get_existing_reservation

説明:get_existing_reservation

パラメータ2:username

説明(パラメータ2):username

**※保存&準備をする**
