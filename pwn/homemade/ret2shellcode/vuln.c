#include <stdio.h>

char mybuf[69];

int main(){
    char buf[69];
    gets(buf);
    strcpy(mybuf, buf);
    return 0;
}