import requests

def make_api_request(question, input_data, is_submitted, language, code, bearer_token):
    url = "http://20.198.81.8/api/submit/"
    
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Content-Type": "application/json"
    }
    
    data = {
        "question": question,
        "input": input_data,
        "isSubmitted": is_submitted,
        "language": language,
        "code": code
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response_data = response.json()
        
        if response.status_code == 200:
            return response_data
        else:
            print("API request failed with status code:", response.status_code)
            return None
    except Exception as e:
        print("Error occurred during API request:", str(e))
        return None

# Example usage:
bearer_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjkxNTI2ODI0LCJpYXQiOjE2OTE1MTYwMjQsImp0aSI6IjY4MTFkMzU0Y2ViZTQ4ZmM5MzhjNjMxOGY4YTY1MzMzIiwidXNlcl9pZCI6Nn0.7dL8nML5l2cSehW33nHPEEAshORR4BwhxrM-SZx06PE"
question = "7f185"
input_data = 7
is_submitted = False
language = "cpp"
code = '''#include <bits/stdc++.h>
using namespace std;
bool check(vector<long long> arr, int s, int l) {
    if (s > l) {
        return true;
    }
    if (arr[s] != arr[l]) return false;
    return check(arr, ++s, --l);
}
bool checkPalindrome(long long N) {
    vector<long long> binaryNum;
    long long i = 0;
    while (N > 0) {
        binaryNum.push_back(N % 2);
        N = N / 2;
        i++;
    }
    return check(binaryNum, 0, binaryNum.size() - 1);
}
int main() {
    int n;
    cin >> n;
    bool s = checkPalindrome(n);
    cout << s << endl;
    return 0;
}'''

for i in range(120):
    response = make_api_request(question, input_data, is_submitted, language, code, bearer_token)
    print(response)
