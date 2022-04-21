#include <stdio.h>
#include <stdlib.h>

#define esc 27
#define backspace 8
#define MAXLINE 10000

void manote(char filename)
{
    FILE *f;
    char c;
    char text_buffer[MAXLINE];
    int i;

    // Open file
    f = fopen(filename, "r");
    if (f == NULL)
    {
        printf("Error opening file\n");
        exit(1);
    }

    // "zeroing" the buffer
    for(i = 0; i < MAXLINE; i++)
    {
        text_buffer[i] = '\0';
    }

    // reading the file
    for(i = 0; text_buffer[i] != EOF; i++)
    {
        text_buffer[i] = fgetc(f);
    }

    // User input
    i = 0;
    while((c = getch()) != esc && i < MAXLINE)
    {
        clrsrc();
        printf("%s", text_buffer);

        if(c == '\n')
        {
            text_buffer[i] = '\n';
        }
        else if(c == backspace)
        {
            // Handle backspace
            if(i > 0)
            {
                text_buffer[i] = '\0';
                --i;
            }
        }
        else
        {
            text_buffer[i] = c;
            i++;
        }
    }
}

int main()
{
    manote("D:\\mano\\code\\mash\\README.md");
    return 0;
}