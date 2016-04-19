import falcon
import post_token


post=post_token.post()
app=falcon.API()
app.add_route('/token',post)
