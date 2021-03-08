#include <stdio.h>

int add(int a, int b)
{
        return a+b;
}

int main(int argc, char** argv)
{
        int a = 0;
        int b = 0;
        int c = 0;

        scanf("%d %d", &a, &b);

        if (a > 10) {
                puts("bigger than 10");

        }
        else {
                puts("less than or equal 10");
        }

        for (int i = 0; i < 10; i++) {
                printf("%d\n", i);
        }

        c = add(a, b);

        printf("%d\n", c);

        return 0;
}