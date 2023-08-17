#include<bits/stdc++.h>

using namespace std;
typedef long long ll;
#define sz(s) (int)(s).size()
#define all(s) s.begin(),s.end()

void Speed() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
}

void solve() {
    int n ; cin >> n;
    int a[n] ;
    for(int i = 0 ; i < n ; i++) cin >> a[i];
    sort(a , a + n);
    vector<int> b , c;
    int i = n - 1;
    while(i >= 0 && a[i] == a[n - 1]) c.push_back(a[i--]);
    while(i >= 0) b.push_back(a[i]);
    if(!sz(b)) return cout << "-1\n" , void();
    cout << sz(b) << ' ' << sz(c) << '\n';
    for(auto it : b) cout << it << ' ' ; cout << '\n';
    for(auto it : c) cout << it << ' ' ;  cout << '\n';
}

int main() {
    Speed();
    int tc = 1;
    cin >> tc;
    while (tc--) {
        solve();
    }
    return 0;
}