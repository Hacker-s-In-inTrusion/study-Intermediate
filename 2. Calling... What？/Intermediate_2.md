# 들어가며
깃헙 시큐리티 팀에서 CTF를 주최한다 해서 관심이 가 찾아봤는데, 일반적인 CTF는 취약점이 있는 바이너리/코드를 주고 플래그를 찾는 방식인데 비해 이 CTF는 CodeQL 사용법을 주어진 소문항들을 해결하면서 익혀나가는 방식이었다. 그래서 결과물도 특정 FLAG가 아닌 CodeQL 코드이고, 이를 제출하여 평가받는 방식이었다. 이번 문제로 인해 CodeQL을 다뤄볼 수 있어 좋은 기회였다고 생각한다.

## Reference
- [문항 페이지](https://securitylab.github.com/ctf/uboot)  
- [CodeQL 공식 document](https://codeql.github.com/docs/)
- [Github Security Blog - UBoot Vulnerabilities](https://securitylab.github.com/research/uboot-rce-nfs-vulnerability)
- [[Writeup] GitHub Security Lab CTF 1: SEGV hunt](https://null2root.github.io/blog/2021/02/12/GitHub-Security-Lab-CTF-1_SEGV-hunt-writeup.html)
## CodeQL 환경
로컬에 직접 CodeQL 환경을 구축할 수 있고 이 편이 실제 실행때 훨씬 빠를것 같지만, 환경 구축의 귀찮음으로 인해 대회측에서 준비한 CodeQL Web IDE를 사용하였다. 문항 페이지에 LGTM's query console 항목을 클릭하면 웹에서도 쉽게 CodeQL 쿼리를 작성하고 테스트해 볼 수 있다.

## Background
이 문제는 실제 UBoot에 있었던 취약점을 CodeQL을 이용해 자동으로 발견하는것이 목적이다. 구체적으로는 네트워크를 통해 값을 전달받는 ```ntohl, ntohs, ntohll```등을 검증 없이 ``memcpy``의 인자로 넘길 때 발생하는 취약점인데, 이러한 코드 패턴을 자동화하여 분석하는것이 최종 목적이다.

# WriteUp

## Step 0: Finding the definition of memcpy, ntohl, ntohll, and ntohs
```CodeQL
import cpp

from Function f
where f.getName() = "strlen"
select f
```
### Question 0.0: Can you work out what the above query is doing?
### Question 0.1: Modify the query to find the definition of memcpy.
strlen을 memcpy로 바꾸기만 하면 된다.
### Question 0.2: ntohl, ntohll, and ntohs can either be functions or macros (depending on the platform where the code is compiled).
As these snapshots for U-Boot were built on Linux, we know they are going to be macros. Write a query to find the definition of these macros.
```
import cpp
from Macros m
where m.getName() = "ntoh(l|ll|s)"
select m
```
처음에는 정규표현식으로 ntoh[\w]* 같은걸 시도해봤는데 잘 동작하지 않아 이것저것 시험해보다 위와 같은 문법이 동작하였다.

## Step 1: Finding the calls to memcpy, ntohl, ntohll, and ntohs
### Question 1.0: Find all the calls to memcpy.
```
import cpp

from FunctionCall fc
where fc.getTarget().hasQualifiedName("memcpy")
select fc
```
구글링을 통해 발견할 수 있었다.

### Question 1.1: Find all the calls to ntohl, ntohll, and ntohs.
이건 좀 어려웠는데, MacroInvocation과 MacroAccess 클래스의 차이가 잘 이해가 안갔고 어떤 메소드를 통해 그 클래스에서 ntoh* 호출을 찾아야 하는지 막막했었다. 공식 문서를 열심히 뒤져가며 여러가지를 찾아보니 다음과 같은 코드를 통해 해결할 수 있었다.
```
import cpp

from MacroInvocation m
where m.getOutermostMacroAccess().getMacroName().regexpMatch("ntoh(l|ll|s)")
select m
```
### Question 1.2: Find the expressions that resulted in these macro invocations.
```
import cpp

from MacroInvocation m
where m.getOutermostMacroAccess().getMacroName().regexpMatch("ntoh(l|ll|s)")
select m.getExpr()
```

## Step 2: Data flow analysis
```
/**
* @kind path-problem
*/

import cpp
import semmle.code.cpp.dataflow.TaintTracking
import DataFlow::PathGraph
 
class YOUR_CLASS_HERE extends Expr {
  // 2.0 Todo 
}
 
class Config extends TaintTracking::Configuration {
  Config() { this = "NetworkToMemFuncLength" }
 
  override predicate isSource(DataFlow::Node source) {
      // 2.1 Todo
  }
  override predicate isSink(DataFlow::Node sink) {
     // 2.1Todo
}
 
from Config cfg, DataFlow::PathNode source, DataFlow::PathNode sink
where cfg.hasFlowPath(source, sink)
select sink, source, sink, "ntoh flows to memcpy"
```
위와 같은 skeleton code를 주고 채우는것이 Step 2.1, 2.2이다. 다음과 같이 CodeQL 코드를 작성할 수 있다.
```
/**
* @kind path-problem
*/

import cpp
import semmle.code.cpp.dataflow.TaintTracking
import DataFlow::PathGraph
 
class MyClass extends Expr {
    MyClass(){
        this = any(MacroInvocation m | m.getOutermostMacroAccess().getMacroName().regexpMatch("ntoh(l|ll|s)")).getExpr()
    }
}
 
class Config extends TaintTracking::Configuration {
    Config() { this = "NetworkToMemFuncLength" }
 
    override predicate isSource(DataFlow::Node source) {
        source.asExpr() instanceof MyClass
    }
    override predicate isSink(DataFlow::Node sink) {
        exists (FunctionCall fc |
            fc.getTarget().getName().regexpMatch("memcpy") and
            fc.getArgument(2) = sink.asExpr()
        )
    } 
}
 
from Config cfg, DataFlow::PathNode source, DataFlow::PathNode sink
where cfg.hasFlowPath(source, sink)
select sink, source, sink, "ntoh flows to memcpy"
```
