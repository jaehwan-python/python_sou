// index.html자료에 동작 추가하기

// element(요소) 얻기
const code = document.querySelector('#code');
const sang = document.querySelector('#sang');
const su = document.querySelector('#su');
const dan = document.querySelector('#dan');

// msg와 tbody
const msg = document.querySelector('#msg')
const tbody = document.querySelector('#tbody')

// 4개의 버튼 
const btnAdd = document.querySelector('#btnAdd')
const btnUpdate = document.querySelector('#btnUpdate')
const btnDelete = document.querySelector('#btnDelete')
const btnReload = document.querySelector('#btnReload')

function setMsg(text){
    msg.textContent = text;
}

// 입력한 폼 초기화 = 입력칸이 지워지는 것이다.
function clearForm(){
    code.value = "";
    sang.value = "";
    su.value = "";
    dan.value = "";
    code.focus();
}

// 1. 전체 자료 읽기[조회] : 처음 시작할 때, 추가할 때 실행이 된다
async function loadAll(){
    const res = await fetch("/api/sangdata",{method:"GET"}); // restful에 의해 get은 전체자료조회에 쓰인다.
    const result_datas = await res.json();
    // console.log(datas);
    // alert(datas);
    tbody.innerHTML = ""
    result_datas.datas.forEach(r => {
        const tr = document.createElement("tr");
        tr.innerHTML = "<td>" + r.code + "</td>"
        + "<td>" + r.sang + "</td>" 
        + "<td>" + r.su + "</td>"
        + "<td>" + r.dan + "</td>"
        tbody.appendChild(tr);
        // tbody의 자식으로 있는 <tr>에게
    })
    // 위에 설정한 setMsg와 clearForm함수가 실행됨.
    clearForm();
    setMsg("조회완료")
}


// 2. 상품추가하기[추가]
async function addData(){
    // alert("add");
    // 입력자료 검사가 끝났다고 가정하고 아래 문장 실행
    const add_data = {
        code : code.value,
        sang : sang.value,
        su : Number(su.value),
        dan : Number(dan.value)
    }
    // alert(add_data)
    // alert(JSON.stringify(add_data))
    // js객체를 json 문자열로 변환해준다
    const res = await fetch("/api/sangdata",{
        method : "POST", 
        // 요청명은 아까와 같이 /api/sangdata이지만 메서드가 get이 아닌 post이다.
        // post방식으로 들어온 정보는 자료 추가용이다!
        headers : {"Content-Type":"application/json"},
        body:JSON.stringify(add_data)
        // js객체를 json문자열로 변환하여 서버로 전송하였다.
    })

    await res.json();
    setMsg("추가 완료");
    clearForm();
    // 자료 추가 완료

    loadAll();
    // 추가 후 전체 자료보기
}

// 3. 상품수정하기[수정]
async function updateData(){
    // alert("add");
    // 입력자료 검사가 끝났다고 가정하고 아래 문장 실행
    const up_data = {
        sang : sang.value,
        su : Number(su.value),
        dan : Number(dan.value) 
        // 상품명, 수량, 단가만 받는다(코드는 받지 않음..코드는 pk이기 때문)
    }

    // js객체를 json 문자열로 변환해준다
    const res = await fetch("/api/sangdata/" + code.value, {
        // code.value가 sangdata/뒤에 붙게 된다.
        method : "PUT", 
        // 자료수정이기 때문에 PUT을 사용한다
        headers : {"Content-Type":"application/json"},
        body:JSON.stringify(up_data)
        // js객체를 json문자열로 변환하여 서버로 전송하였다.
    })

    const imsi = await res.json();
    if (imsi.ok)
        setMsg("수정 완료");
    else
        setMsg("수정 실패");

    clearForm();
    loadAll();
    // 수정 후 전체 자료보기
}

// 4. 상품삭제하기[삭제]
async function deleteData(){
    if (!code.value.trim()){
        alert("삭제할 상품 코드를 입력해욧!")
        code.focus();
        return;
    }

    // 만약 code.value의 값이 있다면...
    const res = await fetch("/api/sangdata/" + code.value, {
        // code.value가 sangdata/뒤에 붙게 된다.
        method : "DELETE"
        // 자료 삭제할 번호만 있으면 된다.
    });

    const imsi = await res.json();
    if (imsi.ok)
        setMsg(imsi.msg);
    else
        setMsg("삭제 실패(오류) : ", + imsi.msg);

    clearForm();
    loadAll(); // 삭제 후 전체자료 보기
}

// :조회"
// 함수 호출
window.onload = loadAll;
// 추가버튼 클릭 시 발생
btnAdd.onclick = addData;
//btnAdd를 누르면 addData가 실행된다
btnUpdate.onclick = updateData;
btnDelete.onclick = deleteData;
btnReload.onload = loadAll; // 현재는 의미가 없는 버튼이다.
// 조회는 눌러도 아무 소용이 없다.