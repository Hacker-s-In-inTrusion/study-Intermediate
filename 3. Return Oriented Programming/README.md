# 3. Return Oriented Programming
## Return Oriented Programming (ROP)
악의적인 사용자가 임의의 코드를 주입하여 실행시키는 것을 막기 위하여 메모리 영역에 쓰기권한과 실행권한을 동시에 주지 않는 NX가 도입되었다.  해커스쿨 level11때처럼 stack에 shellcode를 주입한다고 하더라도 NX가 활성화 되어있으면 stack메모리영역에 실행권한이 없기 때문에 shellcode를 실행하지 못하고 segmentation fault를 발생시킨다.  
이렇게 임의의 코드를 주입해서 실행시키는 것이 불가능해지자 해커들은 기존에 프로그램 내에 (혹은 라이브러리 내에) 실행가능한 영역에 존재하는 코드를 짜맞춰서 자신들이 원하는 방향으로 코드흐름이 바뀌도록 하는 방법을 고안해냈다. ret으로 끝나는 코드 gadget들을 모아서 원하는 프로그램 흐름을 만들어내는 것이다.<br><br>
아래 예시는 ROP를 이용해 1 + 2를 계산하는 것이다. 아래와 같이 주소 0x100, 0x200, 0x300에 필요한 gadget이 있다고 해보자.
```
address     assembly
0x100       mov eax, 1
            ret

0x200       mov edi, 2
            ret

0x300       add eax, edi
```
bof취약점이 존재해 return address를 덮을 수 있다고 할 때, 우리는 return address위치부터 4byte씩 0x100, 0x200, 0x300을 넣으면 위 세 명령어가 차례대로 실행하는 모습을 볼 수 있다.
## pwnable.kr 'Horcruxes'
sum을 알기 위해선 a, b, c, d, e, f, g값을 모두 알아야 한다. 함수 A, B, C, D, E, F, G에서 a, b, c, d, e, f, g값을 알려주니 bof를 이용해 return address를 조작하여 함수 A부터 G까지 호출하여 모든 값을 알아내고 다시 ropme함수를 호출하여 sum값을 입력해주면 된다.  
payload도 같이 첨부해놓았으니 참고해주세요.

### Cautions
gets함수는 개행`\n`이 올 때 까지 받기 때문에 gets에 전달되는 input중간에 개행이 들어가면 거기서 잘리게 된다.  
개행은 ascii값으로 10(0xa)다. ropme함수의 주소값을 살펴보면 0xa가 끼어있기 때문에 ropme함수의 주소값을 입력하려고 들면 중간에 개행으로 인해 잘리게 된다. 따라서 ropme함수 내부는 직접적으로 호출이 불가능하다.<br><br>
sum값은 c언어 내부에서 4byte 고정길이값이다. 따라서 이에 대한 overflow handling을 해줘야한다. 파이썬에는 overflow가 일어나지 않고 내부적으로 handling을 해주기 때문에 overflow가 났을 때의 값을 따로 구해줘서 전달해야한다.