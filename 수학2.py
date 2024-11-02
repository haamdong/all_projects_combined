import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
import math

# 함수 f(x) 정의하기 
def f(x):
    return 2**(x)  # f(x) = 2^x

# 간격, 계산 할 범위 설정
n = int(input('직사각형의 개수를 입력하세요 :'))
a = 0.1    # 시작지점의 x좌표
b = 10   # 끝지점의 x좌표
dx = (b - a) / n  # 각각의 직사각형의 밑변의 길이

# 면적 구하기
areas = np.zeros(n)
for i in range(n):
    x = a + i * dx
    areas[i] = f(x) * dx

# 모든 면적의 합 구하기
x_values = np.linspace(a, b, 100)  # 시작부터 끝까지의 100개의 x 값 생성
y_values = f(x_values)  # 각 x 값에 대한 y 값 계산
total_area = np.sum(areas)

# 정적분 한 값 구하기
result, _ = quad(f, a, b)

#구분구적법을 통해 구한 값 - 정적분을 통해 구한 값 (오차값)
error_value = abs(result-total_area)

# 그래프 그리기
x = np.linspace(0, b, 1000)  # 0부터 2파이(360도)까지 1000개의 점으로 x값 생성
y = f(x)  # 각 x 값에 대한 함수 값 계산
plt.plot(x, y, label='f(x)')

# 직사각형 그리기
for i in range(n):
    x = a + i * dx
    plt.bar(x, f(x), width=dx, alpha=0.3, align='edge', edgecolor='black')

# y축이 나타낼 값을 표시하고, 그래프의 제목을 써두고, 그래프를 보여주기
plt.figtext(0.3, 0.01, 
            f'Total Area: {total_area:.17f}',
            ha='center', 
            fontsize=12
)
plt.figtext(0.55, 0.01, 
            f'definite integral: {result:.17f}',
            ha='center', 
            fontsize=12
)
plt.figtext(
    0.8, 0.01,
    f'Error value: {error_value:.17f}',
    ha='center',
    fontsize=12
)


plt.ylabel('f(x)')
plt.title('Visualization of Rectangles Under the Curve f(x)')
plt.legend()
plt.tight_layout() 
plt.show()

