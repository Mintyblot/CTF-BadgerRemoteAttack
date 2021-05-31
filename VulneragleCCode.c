#include <stdio.h>
#include <stdlib.h>

char buf[1024];

int very_safe(){
    puts("cal");
}

int loop() {
  char str[100];
  if(!gets(str)) return 0;
  snprintf(buf, sizeof(buf), str);
  write(1, buf, strlen(buf));
  return 1;
}

void main() {
  while(loop());
  exit(0);
}
