#include <stdio.h>

void print_flag(){
    char flag[0x100];
    FILE *fp;
    fp = fopen("flag.txt","r");
    fgets(flag, sizeof(flag), fp);
    puts(flag);
}

int main(){
    setvbuf(stdin, NULL, 2, 0);
    setvbuf(stdout, NULL, 2, 0);
    puts(
"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n"
"Welcome to the basics of binary exploitation!\n"
"For this challenge, you'll learn about buffer overflows!\n"
"\n"
"Here we see our source code takes in an input, and gives you the flag if\n"
"is_admin is true. But is_admin is set to false by default, so there is no\n"
"way to change that right? Well, welcome to binary exploitation! The first\n"
"you will learn in your journey is a buffer overflow.\n"
"\n"
"The first thing you will need to know is how variable are stored. In this\n"
"case, the variable is_admin and name are stored one after another. It looks\n"
"like this\n"
"           +----+--------+\n"
"Variables: |name|is_admin|\n"
"           +----+--------+\n"
"Press enter to continue..."
);
getc(stdin);
puts(
"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n"
"These variables take different sizes, any existing programming knowledge\n"
"tell you an int is 4 bytes, a char is 1 byte and an array takes up\n"
"multiple bytes.\n"
"\n"
"Here, we see is_admin takes up 4 bytes and name takes up 1*0x20=32 bytes\n"
"(1 is the size of char). We will represent it like so\n"
"Variables:\n"
"+--------------------------------+--------+\n"
"|name                            |is_admin|\n"
"+--------------------------------+----+---+\n"
"|????????????????????????????????|0000|\n"
"+--------------------------------+----+\n"
"\n"
"Here, each digit represents one byte, ? is unknown data, and 0000 is the\n"
"current value of is_admin (Note this representation is not completely\n"
"accurate but will suffice for this challenge).\n"
"Press enter to continue..."
);
getc(stdin);
puts(
"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n"
"If I were to enter \"Joshua\" when it asked for input, it will look\n"
"something like this internally"
"Variables:\n"
"+--------------------------------+--------+\n"
"|name                            |is_admin|\n"
"+--------------------------------+----+---+\n"
"|Joshua??????????????????????????|0000|\n"
"+--------------------------------+----+\n"
"\n"
"Here, my input fills up the first 6 characters, leaving the rest unfilled\n"
"Press enter to continue..."
);
getc(stdin);
puts(
"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n"
"Knowing this, if we were to compile this, either by typing `make` or \n"
"`gcc -no-pie -fno-stack-protector babybof.c -o babybof`\n"
"We get a warning,\n"
"+-------------------------------------------------------------------+\n"
"| warning: the `gets' function is dangerous and should not be used. |\n"
"+-------------------------------------------------------------------+\n"
"\n"
"Why is it dangerous? It only takes input! How bad can that be?\n"
"The reason why gets is dangerous is because there is no limit to how much\n"
"you can input. You can send a 1000 character input and gets will happily\n"
"take the input and store it for you.\n"
"Going back to our internal representation of our variables, we see what\n"
"we typed in is placed into name. The size of name allows us to store 32 bytes\n"
"or 32 characters. But what happens if we store more than 32 characters into\n"
"name? Well, there is nothing preventing you from writing into is_admin.\n"
"This is our buffer overflow! We are able to write past (overflow) the space\n"
"`name` (our buffer) is sized for.\n"
"\n"
"Finally, if we write more than 32 characters, say 100 As, we see the following\n"
"Variables:\n"
"+--------------------------------+--------+--+\n"
"|name                            |is_admin|  |\n"
"+--------------------------------+----+---+--+\n"
"|AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA|AAAA|AAA...|\n"
"+--------------------------------+----+------+\n"
"\n"
"We overwrote is_admin WITH As. Since is_admin is not 0 anymore, it passes\n"
"the if statement and we will get our flag!\n"
"\n"
"Are you ready to try it on your own?\n"
"Press enter to continue..."
);
getc(stdin);
    int is_admin=0;
    char name[0x20];
    puts("What is your name?");
    gets(name);
    if(is_admin){
        puts("Hi admin, here is your flag");
        print_flag();
    }else{
        puts("You're not the admin!");
    }
}
