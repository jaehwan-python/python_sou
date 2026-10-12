// index.html의 script가 이곳을 참조한다. 
// 그래서 index.html의 사용하는 tag를 여기서 불러온다는 것을 표기해준다.
// btnJikwon, btnOne, btnBuser, btnBuserPart, thead, tbody, jikwonno, buserno, msg



// <RESTFul>
// 상품 CRUD라면 보통 이렇게 restful이 구성
// GET      /api/sangdata     전체 상품 조회 
// GET      /api/sangdata/1   1번 상품 조회
// POST     /api/sangdata     상품 추가
// PUT      /api/sangdata/1   1번 상품 수정
// DELETE   /api/sangdata/1   1번 상품 삭제   


const btnJikwon = document.querySelector("#btnJikwon")
const btnOne = document.querySelector("#btnOne")
const btnBuser = document.querySelector("#btnBuser")
const btnBuserPart = document.querySelector("#btnBuserPart")

const thead = document.querySelector("#thead")
const tbody = document.querySelector("#tbody")

const jikwonno = document.querySelector("#jikwonno")
const buserno = document.querySelector("#buserno")

const msg = document.querySelector("#msg")


// <실행할 함수>
// 실행함수1. setMsg -> 조회결과에 출력할 메시지
function setMsg(text){
    msg.textContent = text;
}

// 실행함수2. clearTable -> table 비워주기
function clearTable(){
    thead.innerHTML = "";
    tbody.innerHTML = "";
}

// 실행함수3. makeTable -> table 채우기
function makeTable(rows){ // rows는 클라이언트가 준 자료
    clearTable(); 
    // 먼저 table을 비워라. -> 새로운 조회결과를 다시 표에 넣기 위해서이다.

    if(!rows || rows.length === 0){ // rows가 없거나 rows의 길이가 0이라면...
        setMsg("자료가 없음")
        return;
    } 
    // rows가 없다면 makeTable함수 실행을 끝내라 아니면 아래로 이동

    // ** pytorch를 메인으로 하고 tensorflow를 서브로 학습예정이다. pytorch는 class기반이기에 class 정리 중요


// <key : value불러오기>
    // 1. key값
    let header = "<tr>"; 
    // 표의 가로 한 줄을 만듦
    Object.keys(rows[0]).forEach(key => { // forEach : 하나씩 꺼낸다
    // rows에서 받은 배열 객체의 [0]번째 행만 꺼내서 그 행에서 key값(컬럼이름)만 뽑는다.
    // 뽑은 keys값들에 대해서 forEach를 실행한다. = 그 keys값들에서 다시 하나씩 뺀다.
    // key = "jikwonno"
    // key = "jikwonname"
    // key = "jikwonjik" -> 이렇게 rows에서 [0]번째 행을 꺼내서 key값들만 모으고 그 key값들을 forEach함.
    // Object -> javascript의 그 기능을 이용하여 key/value값을 꺼낸다
        header += "<th>" + key + "</th>"
        // 꺼낸 key값들을 <th>태그로 감싸서 header뒤에 붙인다. 
        // 첫번째 반복 : <tr> <th>jikwonno</th>
        // 두번째 반복 : <tr> <th>jikwonno</th> <th>jikwonname</th>
        // 세번째 반복 : <tr> <th>jikwonno</th> <th>jikwonname</th> <th>jikwonjik</th>
    });
    header += "</tr>" // 뽑은 모든 key에 대하여 <th>태그를 씌운 뒤 위에서 한 <tr>을 닫아준다 = </tr>
    thead.innerHTML = header; 
    // 지금까지 문자열로 만들어둔 header를 실제 html의 <thead>안에 집어넣는다.
    // 위 내용을 thead에 출력
    
    // 2. value값
    rows.forEach(r => {
        let tr = "<tr>"
        Object.values(r).forEach(v => { // forEach : 하나씩 꺼낸다
            tr += "<td>" + v + "</td>"
        });
        tr += "</tr>"
        tbody.innerHTML += tr; 
        // 위 내용을 tbody에 추력
    })
}
// rows로 받은 배열객체(key:value)의 값을 표로 만들었다.


// <실제 자료 조사> -> RESTFul이용하여 crud사용 -> get / post / put / delete 
// 1. 전체 직원 조회
async function loadJikwon(){
// 직원전체 데이터를 서버에 요청해서 받아온 뒤 그 데이터를 표로 만드는 함수
    const res = await fetch("/acorn/jikwon"); // axios방식이 아니기 때문에 직접 json타입으로 바꾸어주어야 한다.
    const mydata = await res.json(); // ajax의 fetch then방식이기 때문에 json 객체 형태로 만듦
    // json객체로 바꾸는 이유 : 그래야 forEach문을 쓸 수 있다.
    // 이렇게 mydata에는 jikwon자료가 있다.
    makeTable(mydata.data); // mydata가 출력된다.
    setMsg("전체 직원 조회 완료");
}

// 2. 직원 1명 조회
async function loadOne(){
    const no = jikwonno.value; // trim() : 앞뒤 여백을 자를 수 있다.
    const res = await fetch("/acorn/jikwon/" + no,{method:"GET"}); 
    // axios방식이 아니기 때문에 직접 json타입으로 바꾸어주어야 한다.
    // 여기서 restful이 발생하여 jikwon뒤에 /가 있어야한다. = jikwonno.value를 들고서버로 간다.
    // 내가 jikwonno에 대해서 직접 입력한 값이 /acorn/jikwon/ 뒤에 들어간다.
    // method:GET은 restful의 4가지 방식 중 하나이다.
    const mydataOne = await res.json(); 
    makeTable([mydataOne.data]); // mydataOne가 출력된다.

    setMsg("직원 1명 조회 완료");
}

// 3. 전체 부서 조회
async function loadBuser(){
// 부서전체 데이터를 서버에 요청해서 받아온 뒤 그 데이터를 표로 만드는 함수
    const res = await fetch("/api/buser"); // axios방식이 아니기 때문에 직접 json타입으로 바꾸어주어야 한다.
    const mydatabu = await res.json(); // ajax의 fetch then방식이기 때문에 json 객체 형태로 만듦
    // json객체로 바꾸는 이유 : 그래야 forEach문을 쓸 수 있다.
    // 이렇게 mydata에는 jikwon자료가 있다.
    makeTable(mydatabu.data); 
    setMsg("전체 부서 조회 완료");
}

// 4. 특정 부서의 직원 조회
async function loadBuserOne(){
    const no = buserno.value; // trim() : 앞뒤 여백을 자를 수 있다.
    const res = await fetch("/api/buser/" + no,{method:"GET"}); 
    // axios방식이 아니기 때문에 직접 json타입으로 바꾸어주어야 한다.
    // 여기서 restful이 발생하여 jikwon뒤에 /가 있어야한다. = jikwonno.value를 들고서버로 간다.
    // 내가 jikwonno에 대해서 직접 입력한 값이 /acorn/jikwon/ 뒤에 들어간다.
    // method:GET은 restful의 4가지 방식 중 하나이다.
    const mydataOnebu = await res.json(); 
    makeTable(mydataOnebu.data); 

    setMsg("특정 부서의 직원 조회 완료");
}


btnJikwon.onclick = loadJikwon; // 함수의 결과를 넘기는 것이 아니라 함수를 넘기는 것이다.
btnOne.onclick = loadOne; // btnOne을 클릭하면 loadOne이 출력된다.(loadOne도 뒤에 괄호가 있으면 안된다.)
btnBuser.onclick = loadBuser;
btnBuserPart.onclick = loadBuserOne;