# 2. Calling Convention
## Calling Convention?

스터디시간에 사용한 ppt를 업로드했으니, 참고해주시길 바랍니다.  
함수 호출시, 인자들이 어떻게 전달이되고 stack memory는 어떻게 바뀌는지 설명해놨습니다.  

## HackerSchool level 11

```
id: level11
password: what!@#$?
```

```c
#include <stdio.h>
#include <stdlib.h>
 
int main( int argc, char *argv[] )
{
	char str[256];

 	setreuid( 3092, 3092 );
	strcpy( str, argv[1] );
	printf( str );
}
```
level11에 있는 attackme의 코드다. strcpy를 사용하는걸 보니 bof가 터진다.  
우리의 목적은 shell을 따는 것이 목적이므로, 프로그램의 실행흐름을 바꿔서 쉘이 실행되도록 해보자.  
지금 현재 bof로 인해 stack에 들어있는 값을 조작할 수 있는 환경이 주어졌는데, 프로그램의 실행흐름을 바꾸기 위해서는 stack에 저장되어있는 return address를 변조시키면 된다.  
calling convention을 알고있다면 return address가 저장되어있는 곳의 주소값은 ```ebp+4```라는 것을 알 수 있다.  
따라서 buffer, 즉, str의 주소값을 알아낸다면 return address를 조작할 수 있게 된다. 그렇다면 어떻게 공격을 해야할까?  

### Method 1 (Using nop sled technique & shellcode)

shell을 실행시켜주는 code를 shellcode라고 한다.  
buffer에 shellcode를 넣어놓은 후, return address를 buffer의 주소값으로 설정하면 함수 종료시 shellcode가 저장되어있는 주소로 점프를 하면 shellcode가 실행이 되면서 shell이 띄워질 것이다.  
그러나 프로그램을 실행시킬때마다 stack의 시작주소가 바뀌는 ASLR(Adress Space Layout Randomization)이 걸려있기 때문에 buffer의 주소값도 매번 바뀌게 되어 shellcode가 제대로 실행하지 않게 된다.  
따라서 buffer의 주소값이 바뀌더라도 최대한 shellcode 실행 성공률을 높이기 위해 shellcode앞에 nop(no operation; 0x90)을 채워넣어서 정확하게 shellcode 처음부분에 떨어지지 않더라도 nop으로 채워져있는 곳에 떨어지게 된다면 nop을 따라서 쭉 내려오다가 결국 shellcode가 실행이 되게끔 만든다.  

### Method 2 (Using environment variable & shellcode)

shellcode를 stack에 저장하면 stack ASLR때문에 실행하기가 힘들어진다. 따라서 비교적 고정적인 곳에 shellcode를 저장하려고 한다. 바로 환경변수이다.  
환경변수는 프로그램에 종속되어있는 값이 아닌, 운영체제에 종속되어있는 값이기 때문에 모든 프로그램이 환경변수에 대해선 거의 같은 값을 공유하게 된다.  
아래와 같이 환경변수에 shellcode를 등록할 수 있다.
```shell
export shellcode=$(python -c "(shellcode)")
```

그리고 아래와 같이 환경변수의 주소값을 획득하는 프로그램을 만들 수 있다.
```c
// gcc -o shellcode shellcode.c
#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    int p = getenv("shellcode");
    printf("%p\n", p);

    return 0;
}
```

나온 값을 return address에 덮어씌워보자.

### Method 3 (Using Return to Library (RTL) techinique)

첫번째, 두번째 방법 모두 좀 불안정한 방법이다. 첫번째 방법같은경우, stack ASLR때문에 buffer의 주소값이 계속 바뀌고, 두번째 방법같은경우에도, 상황에 따라 살짝씩 달라지기 때문이다. (직접 해보면 알 수 있다. 안먹힐때가 많다.)  
세번째 방법으로 libc 라이브러리에있는 함수를 사용하는 방법이다. 다행히 라이브러리에는 ASLR이 걸려있지 않아서 프로그램을 여러번 실행하더라도 라이브러리가 동일한 메모리 공간에 mapping이 된다. 따라서 libc에있는 system함수를 찾아서 system함수의 주소값을 return address에 넣어주면 system함수가 실행이 될 것이다. 하지만 여기서는 system함수에 "/bin/sh"과 같은 인자를 넣어주어야 한다. 이것은 calling convention을 잘 생각해보면 충분히 전달해줄 수 있다.  
추가적인 힌트를 더 드리자면, "/bin/sh" 문자열은 이미 libc 라이브러리에 존재한다.