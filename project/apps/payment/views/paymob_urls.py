from accept.payment import URLs

class CustomUrls(URLs):
    def __init__(self):
        super().__init__()
        self.base_url = "https://uae.paymob.com/api/"
