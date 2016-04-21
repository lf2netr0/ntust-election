import random

class token:

    def  init_prepare_token(self):
        p_token = random.sample(range(0,100000),99999)
        for i in range(0,len(p_token)):
            p_token[i] = "{:0>5}".format(p_token[i])
        return p_token
                

