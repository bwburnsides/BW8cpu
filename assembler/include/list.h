typedef struct _Node
{
    struct _Node *prev;
    struct _Node *next;
    char *string;
} Node;

Node *NewNode(char *string);

typedef struct _LinkedList
{
    Node *first;
    Node *last;
    int length;

} LinkedList;

LinkedList *NewList();
int append(LinkedList *list, char *string);