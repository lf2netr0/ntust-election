# ntust-election-identify

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
creat_project.py(專案ID,投票人檔案名稱)

## 啟動api
api.py為api入口

<br>
'/token' <br>POST為取得授權碼（project_id, student_id or cardID）<br>
         DELETE為更改授權碼使用狀態（token,project_id）<br>
'/elector' <br>GET為根據取得學生資料(project_id, student_id or cardID)<br>
'/verify' <br>GET為驗證該授權碼為可否使用之狀態(token,project_id)<br>


## 驗證授權碼擁有者
test_owner.py(Token,Project_id)
