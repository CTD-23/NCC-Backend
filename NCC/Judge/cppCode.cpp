#include<bits/stdc++.h>
using namespace std;
#define ll long long
#define fastio ios_base::sync_with_stdio(false);cin.tie(NULL);cout.tie(NULL);
#define endl '\n'
#define test ll t; cin >> t; while(t--)
#define vec(ver, n)  vector<ll> ver(n); for (ll i = 0; i < n; i++) cin >> ver[i];
#define pb push_back
#define all(x) (x).begin(),(x).end()

const int32_t mod=1000000007;

ll hashQuery(ll l, ll r, vector<ll>& prehash){
    ll ans = prehash[r];
    if(l>0) ans = (ans - prehash[l-1] + mod)%mod;
    return ans;
}

ll solve(vector<ll>&ans, vector<ll>&v1, ll n1,ll k,ll ind){
    if(ind < 0 || k == 0) return 0;
    ll take =0, nottake =0;
    nottake = solve(ans, v1, n1, k, ind-1);
    if(ans[ind] <= k) take = v1[ind] + solve(ans, v1, n1, k-ans[ind], ind-1);
    return max(take, nottake);
}

signed main(){
    fastio
    test{
        ll n, k; cin >> n >> k;
        string s; cin >> s;
        vec(v, n);
        ll pow = 31,p =31, mod = 1000000007;
        vector<ll> p_pow(n, 0);
        p_pow[0] = 1;
        vector<ll> prehash(n, 0);
        prehash[0] = s[0] - 'a' + 1;
        for(ll i=1;i<n;i++){
            prehash[i] = (prehash[i-1] + (s[i] - 'a' + 1)*pow)%mod;
            p_pow[i] = pow;
            pow = (pow*p)%mod;
        }


        vector<ll> ans;
        // ll ans =0;
        map<ll,ll> mp;
        for(ll i=0;i<n-1;i++){
            ll pref = prehash[i];
            ll suff = hashQuery(n-1-i, n-1, prehash);
            if((pref *p_pow[n-1-i])%mod == suff){
                // ans = max(ans, i);
                // ans.pb(i+1);
                mp[i] +=1;
                for(ll j=1,k=i+1;k<n-1;j++,k++){
                    ll mid = hashQuery(j,k,prehash);
                    if(((pref*p_pow[j])%mod == mid)){
                        ans.pb(i+1);
                        break;
                    }
                }
            }
        }
        string s1= s;
        reverse(s1.begin(), s1.end());
        if(s1 == s) {ans.pb(n); mp[n-1]-=1;}
        // if(s1 == s) ans = n;

        vector<ll> v1;
        for(auto x: ans) v1.pb(v[x-1]);
        ll n1 = ans .size();
        ll val = solve(ans, v1, n1, k, n1-1);
        cout << val << endl;


        // cout << "ANS : ";
        // for(auto x: ans) cout << x << " ";
        // cout << endl;
        // cout << "v1 : ";
        // for(auto x: v1) cout << x << " ";
        // cout << endl;
    }
    return 0;
}