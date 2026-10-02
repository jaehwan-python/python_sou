from flask import Flask, render_template, render_template_string, request, session, redirect, url_for
from datetime import timedelta

app = Flask(__name__)

app.secret_key = "abcd1234"
app.permanent_session_lifetime = timedelta(minutes = 5) # 세션 만료 시간 5분 = 장바구니에 담아두고 5분이내 다른 상품을 안넣으면 초기화된다.

# 현재는 아직 DB를 불러오지 않고 직접 만들어서 사용해보자.
products = [
    {"id" : 1, "name" : "노트북", "price" : 35000000},
    {"id" : 2, "name" : "물티슈", "price" : 3500},
    {"id" : 3, "name" : "종이컴", "price" : 350},
    {"id" : 4, "name" : "볼펜", "price" : 1500}
]


# 라우팅 정보 1
@app.route("/")
def product_list():
    return render_template("products.html", products = products)


# 라우팅 정보 2
@app.route("/cart")
def show_cart(): # cart 목록 보기
    cart = session.get("cart", {})
    total = sum(info["price"] * info["qty"] for info in cart.values()) 
    # 단가 * 수량을 하여 금액을 구하는 것이다.
    return render_template("cart.html", cart=cart, total=total)


# 라우팅 정보 3
@app.route("/add/<int:product_id>")
def add_to_cart(product_id):
    # print("product_id : ", product_id)
    
    # 세션 cart가 없으면 빈 dict 생성
    cart = session.get("cart", {})
    # session이라는 것은 여러 키와 그 키에 대한 값을 가지고 있다. 우리는 그 중 cart라는 키를 사용하고 있다.

    # next(..., None) : 묶음형 자료에서 다음 값 1개를 꺼내는 함수
    # 주문상품이 product에 기억된다.
    product = next((p for p in products if p["id"] == product_id), None)

    # 주문 상품이 상품 목록에 없는 경우
    if product is None:
        return "주문상품을 찾을 수 없습니다", 404
    
    # 주문 상품이 상품 목록에 있는 경우 -> 장바구니에 추가
    item_name = product["name"]

    # 이미 상품이 장바구니에 있는데 또 넣을 경우(동일상품) -> 갯수 누적
    if item_name in cart:
        cart[item_name]["qty"] += 1 
    else:
        cart[item_name] = {"price":product["price"], "qty":1}
        # 장바구니에 최초 상품일 경우는 수량1(qty요소(key) 생성)

    # 실무에서 이러지 않지만 우리는 연습이니까 session에 무엇이 어떻게 들어가는지 확인하기 위해 적어줌
    session["cart"] = cart # 변수cart를 session "cart"키에 값으로 저장
    session.permanent = True # 5분 만료가 적용

    return redirect(url_for("show_cart"))
    # cart에 저장 후 장바구니(cart 목록) 보기로 이동


# 라우팅 정보4
# 장바구니 부분 삭제
# 설명 : a라는 친구가 가지고 있는 세션이 있다. 그 세션은 cart(키) = 해당 값들(value)로 구성되어 있다. 
#       세션 속 cart를 밖으로 빼서 cart라는 변수로 저장해주고 밖으로 빼내준 cart라는 변수에 대해서 상품들을 부분수정시킨다. 
#       그때 부분수정이 되더라도 원래 a세션 속 원본 데이터는 바뀌지 않는다. 그리고 바뀐 세션에서 밖으로 빼내어 수정한 그 데이터는 다시 세션속으로 들어간다.   
@app.route("/remove/<item_name>")
def remove_to_cart(item_name):
    cart = session.get("cart")
    # 세션에서 cart 키를 뺌

    if item_name in cart:
        del cart[item_name]
        # 변수 cart 목록에서 부분삭제 상품명을 지움

    session["cart"] = cart
    # 그리고 부분삭제(수정)된 cart목록을 세션의 cart로 덮어 씌운다.

    return redirect(url_for("show_cart"))
    # 장바구니 목록 보기


# 라우팅 정보5
# 장바구니 비우기
@app.route("/clear")
def clear_cart():
    session.pop("cart", None) 
    # 세션의 여러 개 키 중에서 "cart"라는 키를 추출 = 삭제의 효과를 가진다.
    return redirect(url_for("show_cart"))


if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 5000)