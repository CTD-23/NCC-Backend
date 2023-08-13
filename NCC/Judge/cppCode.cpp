#include<bits/stdc++.h>
using namespace std;
void solve(int &amount, vector<int>& coins,int sum,int index,int &ans){
        if (index>=coins.size()){
            if (sum == amount){
                ans++;
            }return ;
        }
        if (sum>= amount){
            if (sum == amount){
                ans ++;
            }
            return ;
        }

        sum += coins[index];
        solve(amount,coins,sum,index,ans);
        sum -=coins[index];
        solve(amount,coins,sum,index+1,ans);

    }
    void change(int amount, vector<int>& coins) {
        int ans=0;
        solve(amount,coins,0,0,ans);
        cout<<ans<<endl;
    }

int main()
{
    // int amount = 500;
    // vector<int>coins = {3,5,7,8,9,10,11};
    int amount = 5;
    vector<int>coins = {1,2,5};
    change(amount,coins);
    
    return 0;
}