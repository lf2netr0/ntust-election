import json
import falcon
import Sql_connect

class post:

    def on_post(self, req, resp):
        """Handles POST requests"""
        sql=Sql_connect.sql()
        data=sql.token_search(req.params)
        result = {"errno": 0, "details": "hello"}
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(data)

