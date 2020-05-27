#include <stdio.h>
int main()
{
    int n, i, j; 
    scanf("%d", &n);
    for(i = 1; i <= n; i++)
	{
        for(j = 1; j <= n - i; j++)
            putchar(' ');
        printf("%d", i);
        for(j = 1; j <= 2 * i - 3; j++)
            putchar(' ');
        if(i != 1)
            printf("%d", i);
        for(j = 1; j <= n - i; j++)
            putchar(' ');
        putchar('\n');
    }
    for(i = 1; i <= n - 1; i++)
	{
        for(j = 1; j <= i; j++)
            putchar(' ');
        printf("%d", n - i);
        for(j = 1; j <= 2 * (n - i) - 3; j++)
            putchar(' ');
        if(i != n - 1)
            printf("%d", n - i);
        for(j = 1; j <= i; j++)
            putchar(' ');
        putchar('\n');
    }
    getchar();
    return 0;
}