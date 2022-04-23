#include <stdio.h>
#include <stdlib.h>
#include <conio.h>
#include <string.h>

#pragma warning(disable : 4996)

#define esc 27
#define backspace 8
#define CTRL_Q 17
#define MAXLINE 1024

void manote(char filename[])
{
    FILE *f; 
    char c = 0;
    char text_buffer[MAXLINE];
    int i;

    // Open file
    f = fopen(filename, "w+");
    if (f == NULL)
    {
        printf("Error opening file\n");
        exit(1);
    }

    // "zeroing" the buffer
    for (i = 0; i < MAXLINE; i++)
    {
        text_buffer[i] = '\0';
    }

    // reading the file
    fread(text_buffer, sizeof(char), MAXLINE, f);

    // User input
    // Enter isn't working properly
    i = strlen(text_buffer);
    while (i < MAXLINE)
    {
        system("cls");
        printf("%s", text_buffer);
        text_buffer[i] = _getch();

        if (text_buffer[i] == backspace && i > 0)
        {
            text_buffer[i] = '\0';
            text_buffer[i-1] = '\0';
            i--;
            continue;
        }
        else if (text_buffer[i] == '\r')
        {
            text_buffer[i] == '\n';
        }
        else if (text_buffer[i] == esc || text_buffer[i] == CTRL_Q)
        {
            break;
        }
        else {
            i++;
        }
    }

    if (text_buffer[i] == esc)
    {
        text_buffer[i] = '\0';
        fwrite(text_buffer, sizeof(char), strlen(text_buffer), f);
        printf("\nWrote to file\n");
    }
    else if (text_buffer[i] == CTRL_Q)
    {
        printf("\nExited without saving");
    }
    else
    {
        printf("\nThere was an error saving the file\n\
            Enter either esc to save or CTRL+Q to quit without saving");
    }
}

int main()
{
    char path[] = "D:\\mano\\code\\manote\\birdee";
    manote(path);
    return 0;
}