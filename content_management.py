def content():
    TOPIC_DICT = {"Basics":["Login Page","/login_request"]}
    for i in (TOPIC_DICT):
        print(TOPIC_DICT[i])
    return TOPIC_DICT

if __name__ == "__main__":
    content()