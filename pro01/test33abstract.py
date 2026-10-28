# 직원 급여 계산 예제
# 직원이라는 개념은 있지만 실제 급여 계산은 정규직과 아르바이트가 서로 다르다.


from abc import ABC, abstractmethod # 추상 클래스를 쓸거야.

# 직원들의 공통 규격을 정의하는 추상 클래스

class Employee(ABC): #나는 추상 클래스야
    def __init__(self, name):
        self.name = name # 인스턴스 생성이 아니라 인스턴트 정의이다. 

    @abstractmethod # 이 statesment 하나로 아래에 있는 get_salary는 일반메서드에서 추상메서드가 되었다. 그래서 자식 클래스가 반드시 구현해야
#                     하는 메서드로 오버라이딩이 필수이다. = 오버라이딩이 되어야 수행가능하기 때문
    def get_salary(self):
        pass 

    def show_salary(self): # 모든 직원이 공용하는 일반 메서드
        print('이름 : ', self.name)
        print('급여 : ', self.get_salary(), '원') # 이렇게 하면 자식 클래스에서 값을 받아와서 값입력이 가능하다. # 클래스에 따라 다른 결과가 나온다(다형성)

# 정규직
class FullTimeEmployee(Employee):
    def __init__(self, name, montly_salary):
        super().__init__(name)
        self.montly_salary = montly_salary

    def get_salary(self): # 부모 클래스로 부터 자식클래스의 get_salary를 무조건 써야한다. = 강요당함 = 오버라이딩 한것이다.
        return self.montly_salary

    def showMe(self): # 일반 메서드
        print("나는 정규직이야.")

#아르바이트
class PartTimeEmployee(Employee):
    def __init__(self, name, hours, hourly_pay):
        super().__init__(name)
        self.hours = hours
        self.hourly_pay = hourly_pay

    def get_salary(self):
        return self.hours * self.hourly_pay

emp1 = FullTimeEmployee("홍길동", 3500000)
emp2 = PartTimeEmployee("심청이", 80, 10500)

emp1.show_salary()
emp2.show_salary()

