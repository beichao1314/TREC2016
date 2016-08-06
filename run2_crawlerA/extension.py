from py_bing_search import PyBingWebSearch

# s1= 	9uCkTYlAG9x4iPdxAeDuQipYvc2vEn6oUbPKZJnFlVY
# s2=3L8LwEROeBFVSA1FwUVKLfIO+Ue979rarr+Y4mBZwaE
s3 = 'E+ok1GP7qpi6xgtE0yfsbrQFZSElgMBK2ZD1kwf/WXA'
s4 = 'AKvk0/D9XzJuCQA9n/a+TFbqwOFder9xd9Yj/22ivA8'
s5='r8OUqrE+DW/W4qs8ShfN2ljAU8214AkuksvYy7iMPGk'

def search(search_term):
    bing_web = PyBingWebSearch(s5, search_term,
                               web_only=False)  # web_only is optional, but should be true to use your web only quota instead of your all purpose quota
    first_ten_result = bing_web.search(limit=10, format='json')  # 1-50
    # second_fifty_result = bing_web.search(limit=50, format='json')  # 51-100
    return first_ten_result
