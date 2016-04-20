#ntust-election

##設定檔
根據config_sample.py建立

##啟動api
start_api為api入口

```py
import falcon
import post_token


post=post_token.post()
app=falcon.API()
app.add_route('/token',post)＃新增route，以此類推
```
