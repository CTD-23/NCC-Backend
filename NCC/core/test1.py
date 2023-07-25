import requests

def make_api_request():
    url = "http://127.0.0.1:8000/home/"
    
    headers = {
        # "Authorization": f"Bearer {bearer_token}",
        "Content-Type": "application/json"
    }
    
    
    try:
        response = requests.post(url, headers=headers)
        response_data = response.json()
        
        if response.status_code == 200:
            return response_data
        else:
            print("API request failed with status code:", response.status_code)
            return None
    except Exception as e:
        print("Error occurred during API request:", str(e))
        return None


for i in range(1):
    response = make_api_request()
    print(response)
