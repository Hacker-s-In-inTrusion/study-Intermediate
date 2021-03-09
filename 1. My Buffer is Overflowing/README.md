# 1. Buffer Overflow
## Buffer Overflow 란?

## BOF를 이용한 공격방법

## Ghidra 설치
CTF 문제풀이를 하려면 바이너리 분석을 해야합니다. 하지만, 항상 기본 gdb에 하는 건 매우 불편하죠. 그래서 바이너리를 분석할 때 매우 유용한 Ghidra라는 프로그램을 이용해서 앞으로의 CTF에도 활용할 겁니다.

Ghidra는 Java기반이기에 먼저 Java를 설치해주셔야 합니다. [이 링크](https://jdk.java.net/15/) 에서 다운로드를 받으시면 됩니다.

다운로드를 받으셨다면, 압축을 풀어 원하시는 곳에 압축을 푼 폴더를 이동시킵니다.
```
C:\Program Files\Java\jdk-15.0.2 (예시)
```
이제 Java를 시스템에서 쓰기 위해 몇 가지 환경 변수를 설정해야 됩니다.  
다음과 같이 JAVA_HOME이라는 환경 변수를 새로 만듭니다.
```
변수 이름 : JAVA_HOME
변수 값 : C:\Program Files\Java\jdk-15.0.2
```
생성하셨다면, Path라는 환경 변수를 찾으시고, 편집을 누르시고, 새로 만들기를 누른 다음 다음을 입력합니다.
```
%JAVA_HOME%\bin
```
다 하셨다면, 이제 Ghidra를 설치할 차례입니다! Main의 README나 [이 링크](https://ghidra-sre.org/)를 통해 압축파일을 받습니다.  
끝나셨다면 압축을 푸시고, ```ghidraRun.bat```을 실행시키시면 됩니다. 그러면 자동으로 설치되고 Ghidra가 실행됩니다.

처음 Ghidra를 실행시켰다면 프로젝트를 생성해야됩니다. Ctrl+N으로 새 프로젝트를 생성한 후, __초록색 용__ 이 있는 버튼을 누르시면 분석할 수 있는 화면이 팝업됩니다. 이제 그 화면에다가 분석을 원하는 바이너리를 드래그 & 드롭 하시면 바이너리 분석을 수행한 후 수행한 화면을 보여줍니다.

## BOF Writeup
### Approach

### In Shell

### Using pwntools (python)
