import data.oapen as OapenAPI
from tasks.clean import get_endpoints


def test_get_endpoints():
    num = 0
    for endpoint in get_endpoints():
        print(endpoint)
        num += 1
        if num > 10: 
            break
        assert endpoint 


def test_weekly():
    for item in OapenAPI.get_weekly_items(limit=5):
        print(len(item.text))
        assert item.name

#test_get_endpoints()
#test_weekly()
