#include <bits/stdc++.h>
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
}