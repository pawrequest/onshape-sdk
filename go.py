from onshape_sdk import OnshapeClient

if __name__ == '__main__':
    client = OnshapeClient()
    res = client.test_auth()
    print(res)