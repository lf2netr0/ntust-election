# ntust-election-identify

透過Http傳輸學號或CardID至伺服器確認身份後<br>
取得投票用token，此token透過兩組金鑰加密後<br>
儲存至DB table，以達到匿名投票目的<br>

## 設定檔
根據config_sample.py建立
```py
config = {
    'public_keys': [#加密金鑰名稱
        'public_1.pem',
        'public_2.pem'
    ],
    'database': {
        'address': '',
        'dbname': '',
        'username': '',
        'password': '',
    },
    ＃Mailgun Setting
    'school_mail': '@mail.ntust.edu.tw',
    'url': 'Base url',
    'key': 'api_key',
    'text': 'text file name'
}
```
## 建立資料表
install.py

## 匯入專案投票人資料
command:
    ```python creat_project.py 專案ID 投票人檔案名稱 ```


## 啟動API
Http server 啟動 api.py

# Route

### token 
Method:POST 為取得授權碼（project_id, student_id or cardID）<br>
Method:DELETE 為更改授權碼使用狀態（token,project_id）<br>
### elector 
Method:GET 為根據取得學生資料(project_id, student_id or cardID)<br>
### verify 
Method:GET 為驗證該授權碼為可否使用之狀態(token,project_id)<br>


## 驗證授權碼擁有者
command:
    ```python test_owner.py Token Project_id```

## 匯出投票專案
command:
    ```python elector_export.py Project_id```
