import falcon
from server import post_token


token=post_token.post()
app=falcon.API()
app.add_route('/token',token)
