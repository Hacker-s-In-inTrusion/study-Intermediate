# 1. Buffer Overflow
## Buffer Overflow 란?

## BOF를 이용한 공격방법

## Ghidra 설치
CTF 문제풀이를 하려면 바이너리 분석을 해야합니다. 하지만, 항상 기본 gdb에 하는 건 매우 불편하죠. 그래서 바이너리를 분석할 때 매우 유용한 Ghidra라는 프로그램을 이용해서 앞으로의 CTF에도 활용할 겁니다.

### Windows
Ghidra는 Java기반이기에 먼저 Java를 설치해주셔야 합니다. [이 링크](https://jdk.java.net/15/) 에서 다운로드를 받으시면 됩니다.

다운로드를 받으셨다면, 압축을 풀어 원하시는 곳에 압축을 푼 폴더를 이동시킵니다.
```
C:\Program Files\Java\jdk-15.0.2 (예시)
```
이제 Java를 시스템에서 쓰기 위해 몇 가지 환경 변수를 설정해야 됩니다.  
다음과 같이 JAVA_HOME이라는 환경 변수를 새로 만듭니다.
```
변수 이름 : JAVA_HOME
변수 값 : C:\Program Files\Java\jdk-15.0.2 (jdk 폴더 위치)
```
생성하셨다면, Path라는 환경 변수를 찾으시고, 편집을 누르시고, 새로 만들기를 누른 다음 다음을 입력합니다.
```
%JAVA_HOME%\bin
```
다 하셨다면, 이제 Ghidra를 설치할 차례입니다! Main의 README나 [이 링크](https://ghidra-sre.org/)를 통해 압축파일을 받습니다.  
끝나셨다면 압축을 푸시고, ```ghidraRun.bat```을 실행시키시면 됩니다. 그러면 자동으로 Ghidra가 실행됩니다.

Ghidra는 따로 설치과정이 필요하지 않습니다.

### Linux
apt와 같은 저장소 프로그램을 이용하여 openjdk를 설치해줍니다.
```
$ sudo apt install openjdk-15-jdk
```

그 후, ```ghidraRun``` 쉘 스크립트를 눌러 실행하시면 됩니다.

처음 Ghidra를 실행시켰다면 프로젝트를 생성해야됩니다. Ctrl+N으로 새 프로젝트를 생성한 후, __초록색 용__ 이 있는 버튼을 누르시면 분석할 수 있는 화면이 팝업됩니다. 이제 그 화면에다가 분석을 원하는 바이너리를 드래그 & 드롭 하시면 바이너리 분석을 수행한 후 수행한 화면을 보여줍니다.

## BOF Writeup

```c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
void func(int key){
	char overflowme[32];
	printf("overflow me : ");
	gets(overflowme);	// smash me!
	if(key == 0xcafebabe){
		system("/bin/sh");
	}
	else{
		printf("Nah..\n");
	}
}
int main(int argc, char* argv[]){
	func(0xdeadbeef);
	return 0;
}
```

func의 첫번째 인자를 조작하는 문제이다.  
gets 함수는 버퍼의 길이에 상관없이 개행이 읽힐 때까지 읽기 때문에 Buffer Overflow 취약점을 가지고 있다.
따라서 stack상에 overflowme라는 버퍼의 위치와 func함수의 첫번째 인자인 key의 위치를 파악하면 key값을 변조할 수 있다.

overflowme 버퍼는 gets의 함수의 인자로 사용이 되기 때문에 gets가 호출되기 전 인자가 준비되는 과정을 살펴보면 위치를 알 수 있다.  
key의 위치는 x86의 calling convention을 알고 있다면 어셈블리 살펴볼 필요 없이 바로 나오겠지만, calling convention을 잘 모를경우, if 조건문안에 key가 사용되니 해당 부분을 살펴보면 된다.

### Approach

문제의 답을 직접적으로 제공하진 않는다. 그러면 재미없잖아요. 하핳. 하지만 payload의 기본적인 틀은 제공한다.  
```payload_for_this_problem```은 직접 구해보자. payload를 구성할 때 little endian을 조심해야한다.

### In Shell
```sh
(python3 -c "print('payload_for_this_problem')"; cat) | nc pwnable.kr 9000
```
키보드를 이용해서는 전달할 수 없는 바이트값들이 존재하기 때문에 위와 같이 파이썬을 이용하여 전달할 것이다.  
```(;cat) | ``` 다음과 같은 모양을 사용하는 이유는, shell을 딴 다음에도 shell에 입력을 할 수 있어야 하는데 이 역할을 cat이 해준다.  
왜냐하면 nc로 들어가는 값은 파이프로 인해 파이프 앞쪽에 있는 명령어들의 stdout과 묶여있기 때문에 cat을 사용하지 않으면 파이썬 명령어가 끝나는 동시에 파이프가 닫히고 nc가 종료되기 때문에 shell을 따도 shell을 사용할 수 없게되기 때문이다.

### Using pwntools (python)
```py
from pwn import *

# nc서버와 연결 remote(ip, port)
p = remote('pwnable.kr', 9000)

# payload 구성 Hint: p32()함수 요긴하게 사용된다.
# p32함수의 return값은 bytes다. python3에선 string과 바로 concatenate되지 않을 것이다.
payload = 'payload_for_this_problem'

# payload 전달
p.sendline(payload)

# interactive shell환경 제공
p.interactive()
```

pwntools를 사용한 정답은 같이 올려놓은 py파일을 참고하면 된다.