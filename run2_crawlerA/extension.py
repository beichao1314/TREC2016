from py_bing_search import PyBingWebSearch

# s1= 	9uCkTYlAG9x4iPdxAeDuQipYvc2vEn6oUbPKZJnFlVY
# s2=3L8LwEROeBFVSA1FwUVKLfIO+Ue979rarr+Y4mBZwaE
s3 = 'E+ok1GP7qpi6xgtE0yfsbrQFZSElgMBK2ZD1kwf/WXA'
s4 = 'AKvk0/D9XzJuCQA9n/a+TFbqwOFder9xd9Yj/22ivA8'
s5='r8OUqrE+DW/W4qs8ShfN2ljAU8214AkuksvYy7iMPGk'

def search(search_term):
    bing_web = PyBingWebSearch(s5, search_term,web_only=False)  
    first_ten_result = bing_web.search(limit=10, format='json')  
    return first_ten_result
