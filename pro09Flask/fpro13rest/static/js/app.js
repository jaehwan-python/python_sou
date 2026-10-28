// 화살표 함수객체 생성 후 $에 함수를 할당하였다.
const $ = (sel) => document.querySelector(sel);
//(sel)이라는 id나 name을 가진 부분을 찾아라.
// 

// 위 화살표 함수와 아래 일반 함수는 같다
// function $(sel){
//     return document.quertSelector(sel);
// }
// querySelector()의 괄호에는 id나 name이 오게되고 해당 

// <$("#sendBtn")>
// ex) $("#sendBtn")을 하게 되면 = $함수를 호출한다.
//                              = return document.querySelector(sendBtn);이 실행된다.
// sendBtn이 sel로 들어가게 된다.
// id가 sendBtn인 녀석은 GET요청이라는 버튼이다.
// submit이 아닌 buttion이기에 눌러도 아무 동작을 하지 않기에 우리가 js파일로 만들어서 동작을 넣어 주었다.


$("#sendBtn").addEventListener("click", async() => { 
    // click이벤트가 발생하면 sendBtn이라는 id를  가진 부분에 돌려주어라
    // ajax의 async를 이용함. sendBtn이라는 div에 click이벤트가 발생하면 비동기 처리를 한다.

    // 1. name값 확인
    const name = $("#name").value.trim();
    // 원래라면 이렇게 쓴다 : const name = document.querySelector("#name").value.trim() 위와 동일. 하지만 위 처럼 쓰면 더 쉽게 쓸 수 있다.
    // index.html에서 내가 작성한 name값을 #name에 저장했기 때문에 js파일에서 사용하기 위해서 $함수를 써줌.
    // console.log("name", name);


    // 2. age값 확인
    const age = $("#age").value.trim();
    // console.log("age", age);
    // = 요약 : HTML에서 id가 #sendBtn인 요소를 찾아서 click이벤트를 등록하고, 사용자가 click을 하게되면
    //          name과 age 입력창의 값을 가져와 각각 js변수에 저장한다.


    // 3. params 값 전송(name값, age값)
    // params : get요청으로 보낼 값을 url의 쿼리스트링 형태로 만들어주기 위한 객체
    const params = new URLSearchParams({name, age});
    // 공백과 한글이 포함된 경우 자동으로 인코딩된다. -> '길동'(한글텍스트) = %EA%B8%B8%EB%8F%99로 만들었다.. 누가? URLSearchParms가.
    // name과 age를 get방식으로 url에 붙여 보내기 좋은 형태로 만들어서 params에 저장한다.
    const url = `/api/friend?${params.toString()}`;
    // console.log(url)
    // /api/friend?name=%EA%B8%B8%EB%8F%99&age=23의 형태로 출력된다.

    $("#result").textContent = "요청중..."
    // id가 result인 index.html의 태그에서 "결과출력"이라는 값을 "요청중..."이라고 바꾼다.
    // 서버에 자료요청 시간이 길어지면 보이는 메세지
    
    try{
        const res = await fetch(url, { 
            // await fetch(url, {}) : 서버에 해당 url로 요청을 보내고, 응답이 도착할 때까지 이 함수의 코드 실행을 기다린다. 
            // fetch는 요청을 보내고, await는 응답을 기다린다.
            method:"GET",
            headers:{"ACCEPT": "application/json"}
            // GET방식으로 요청된 정보를 json값(application/json)으로 되돌려주어서 브라우저가 accept하도록 한다.
            // 넘어간 url값이 get방식으로 요청되면 되돌려 받을 때 json타입으로 받는다라는 뜻
            // /api/friend?name=%EA%B8%B8%EB%8F%99&age=23이 url로 get방식으로 요청을 보내고 응답을 json형식의 데이터로 받는다.
        })
        // ajax의 fetch요청이다...

        const data = await res.json();
        // 응답 본문을 JSON으로 파싱(전달)해서 javascript로 객체화시킨다.
        alert(data); // fetch요청이 잘 넘어가는지 실험

        if(!res.ok || data.ok === false){
            $("#result").innerHTML = `<span class = "error"> 에러 : ${data.error}</span>`;
        }
        // name이나 age값이 입력되지 않으면 name/age is required가 뜬다.
        
        // 요청 성공인 경우 -> index.html에서 넘어온 자료들
        $("#result").innerHTML = `
        <div> 이름 : ${data.name} </div>
        <div> 나이: ${data.age} </div> 
        <div> 이름 : ${data.age_group} </div>
        <div> 나이: ${data.message} </div>
        `;

    }catch(err){
        $("#result").innerHTML = `<span class = "error"> 네트워크 파싱 오류 : ${err}</span>`;
    // 클래스가 .error이면 빨간색이 뜨도록 했다(style.css에서)
    }
})
