#include<stdio.h>
#include<math.h>
void main()
{
int sign=1;
float i=1,sum=0,temp=1;
while(fabs(temp)>=1e-6)
{
sum+=temp;
sign=-sign;
i+=2;
temp=sign/i;
}
sum*=4;
printf("%f\n",sum);
}