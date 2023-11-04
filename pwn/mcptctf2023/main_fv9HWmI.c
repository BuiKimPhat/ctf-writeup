#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <wchar.h>
#include <stdlib.h>
#include <locale.h>

int main(int argc, char **argv) {
    char cache[MB_CUR_MAX];
    char flag[1024];
    if (argc == 0) {
        fprintf(stderr, "what‽");
        return 3;
    }
    char *flag2 = getenv("FLAG");
    for (int i = 0; i < strlen(flag2) && i < 1023; i++) {
        flag[i] = flag2[i];
    }
    setlocale(LC_ALL, ""); // so fgetwc works
    wchar_t wc = fgetwc(stdin);
    if (wc == WEOF) {
        if (errno != 0) {
            perror("reading stdin");
            return errno;
        }
        return 1;
    }
    int s = wctomb(cache, wc);
    if (s == -1) {
        fprintf(stderr, "wctomb: %s\n", strerror(errno));
        return errno;
    }
    printf("%s\n", cache);
    fflush(stdout); // jail stuffs
    return 0;
}
