// 자료 추가 시 입력자료 오류검사
document.addEventListener("DOMContentLoaded", () => { // DOMContentLoade가 발생하면 화살표함수 발생
    const form = document.getElementById("addForm")

    if (!form) return;

    form.addEventListener("submit", (e) => { // submit이벤트가 발생하면 화살표 함수 발생 // submit 이벤트가 발생할 때 그 이벤트 발생 정보를 e에 저장해둠.
        // alert("ok");
        const sang = document.getElementById("sang").value.trim();
        const su = document.getElementById("su").value.trim();
        const dan = document.getElementById("dan").value.trim();

        // 1. 필수 입력 체크
        if (sang === ""){
            alert("상품명을 입력하세요");
            document.getElementById("sang").focus();
            e.preventDefault(); // 이거 시험 나옴 ㅋㅋ
            return;
        }

        // 2. 숫자 체크 (정규표현식)
        if(!/^\d+$/.test(su)){ // test는 키워드이다. -> 정규표현식.test(검사할 문자열(대상))
            alert("수량은 숫자만 허용");
            document.getElementById("su").focus();
            e.preventDefault(); 
            return;
        }

        if(!/^\d+$/.test(dan)){
            alert("단가는 숫자만 허용");
            document.getElementById("dan").focus();
            e.preventDefault(); 
            return;
        }

        // 3. 
    })
})