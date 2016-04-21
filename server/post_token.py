import json
import falcon
import Sql_connect

class post:

    def on_post(self, req, resp):
        sql = Sql_connect.sql()
        data = sql.token_search(req.params)
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(data)

