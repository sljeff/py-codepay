from urllib.parse import urlencode
from hashlib import md5


DEFAULT_API_HOST = "https://api.xiuxiu888.com/creat_order/"


class CodePay:
    CODEPAY_TYPE_ALIPAY = 1
    CODEPAY_TYPE_QQ = 2
    CODEPAY_TYPE_WECHAT = 3

    def __init__(self, codepay_id, codepay_key, api_host=DEFAULT_API_HOST):
        self.codepay_id = codepay_id
        self.codepay_key = codepay_key
        self.api_host = api_host

    def create_order(
        self, codepay_type, price, pay_id, notify_url="", return_url="", param="",
    ):
        data = {
            "id": self.codepay_id,
            "pay_id": pay_id,
            "type": codepay_type,
            "price": price,
            "notify_url": notify_url,
            "return_url": return_url,
            "param": param,
        }
        signs = ""
        urls = ""
        for k in sorted(data.keys()):
            v = data[k]
            if not v or k == "sign":
                continue
            if signs:
                urls += "&"
                signs += "&"
            signs += f"{k}={v}"
            urls += f"{k}={urlencode(v)}"
        sign = md5((signs + self.codepay_key).encode()).hexdigest()
        query = f"{urls}&sign={sign}"
        url = f"{self.api_host}?{query}"
        return url

    def check_callback(self, data):
        if "pay_no" not in data:
            return False
        signs = ""
        for k in sorted(data.keys()):
            v = data[k]
            if v == "" or k == "sign":
                continue
            if signs:
                signs += "&"
            signs += f"{k}={v}"
        sign = md5((signs + self.codepay_key).encode()).hexdigest()
        return sign == data.get("sign")
