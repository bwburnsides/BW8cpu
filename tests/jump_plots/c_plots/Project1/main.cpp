#include <stdio.h>

int main(void) {
    for (int mode = 1; mode <= 8; mode++)
    {
        switch (mode)
        {
            case 1:
                printf("[Unsigned] Less\n");
                break;
            case 2:
                printf("[Unsigned] Greater or Equal\n");
                break;
            case 3:
                printf("[Unsigned] Lessthan or Equal\n");
                break;
            case 4:
                printf("[Unsigned] Greater\n");
                break;
            case 5:
                printf("[Signed] Less\n");
                break;
            case 6:
                printf("[Signed] Greater or Equal\n");
                break;
            case 7:
                printf("[Signed] Lessthan or Equal\n");
                break;
            case 8:
                printf("[Signed] Greater\n");
                break;
        }

        for (unsigned int b = 0; b < 256; b += 8)
        {
            for (unsigned int a = 0; a < 256; a += 4)
            {
                bool val;

                switch (mode)
                {
                    case 1:
                        val = ((unsigned char)a < (unsigned char)b);
                        break;
                    case 2:
                        val = ((unsigned char)a >= (unsigned char)b);
                        break;
                    case 3:
                        val = ((unsigned char)a <= (unsigned char)b);
                        break;
                    case 4:
                        val = ((unsigned char)a > (unsigned char)b);
                        break;
                    case 5:
                        val = ((signed char)a < (signed char)b);
                        break;
                    case 6:
                        val = ((signed char)a >= (signed char)b);
                        break;
                    case 7:
                        val = ((signed char)a <= (signed char)b);
                        break;
                    case 8:
                        val = ((signed char)a > (signed char)b);
                        break;
                }

                printf("%c", val ? '#' : '.');
            }
            printf("\n");
        }
    }
}