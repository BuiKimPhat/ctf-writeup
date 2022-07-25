#include <stdio.h>
#include <string.h>

int main(){
    char usr[69], pwd[69];
    int res[69];
    int flag[69] = {-700416, -724992, -679936, -704512, -786432, -770048, -491520, -483328, -483328, -671744, -761856, -671744, -692224, -483328, -692224, -671744, -483328, -757760, -671744, -757760, -708608, -483328, -499712, -671744, -757760, -483328, -729088, -696320, -671744, -741376, -761856, -499712, -499712, -778240, -622592, -483328, -495616, -778240, -696320, -749568, -503808, -516096, -671744, -495616, -692224, -479232, -503808, -495616, -483328, -495616, -679936, -794624};
    printf("Username: ");
    scanf("%69s", usr);
    printf("Password: ");
    scanf("%69s", pwd);
    if (!strcmp(usr, "pu55yS14yer69")){
        for (int i=0;i<52;i++){
            res[i] = (int)pwd[i] + 69;
            res[i] *= 6-9*(6*9) >> 6;
            res[i] = res[i] << 9;
        };
        printf("Is this the user password?\n");
        int good = 0;
        for (int i=0;i<52;i++){
            if (res[i] == flag[i]) good++;
        };
        printf("\n");
        if (good == 52) {
            printf("Congrats! You are the chosen one, warrior!\n");
        } else {
            printf("Never give up! You are almost done!\nhttps://www.youtube.com/watch?v=ymgejKxrHHc\n");
        }
    } else {
        printf("Never give up!\nhttps://www.youtube.com/watch?v=dQw4w9WgXcQ\n");
    }
    return 0;
}