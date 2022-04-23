#include <stdio.h>
#include <stdlib.h>
#include <conio.h>
#include <string.h>

#define esc 27
#define backspace 8
#define MAXLINE 1024

void manote(char filename[])
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
    fread(text_buffer, sizeof(char), MAXLINE, f);

    // User input
    i = strlen(text_buffer);
    printf("%s", text_buffer);
    while(text_buffer[i] != esc && i < MAXLINE)
    {
        system("cls");
        text_buffer[i] = _getch();

        if(text_buffer[i] == backspace)
        {
            text_buffer[i] = '\0';
            i--;
            continue;
        } else if(text_buffer[i] == '\r')
        {
            text_buffer[i] = '\n';
        }
        i++;
    }

    f = fopen(filename, "w");
    if (f == NULL)
    {
        printf("Error opening file\n");
        exit(1);
    }
    fwrite(text_buffer, sizeof(char), strlen(text_buffer), f);
}

int main()
{
    char path[] = "birdee";
    manote(path);
    return 0;
}