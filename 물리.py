import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.integrate import solve_ivp

m = 1.0  # 무게추의 질량 (kg)
k = 10.0  # 용수철 상수 (N/m)
c = 0.5  # 감쇠 계수 (kg/s)
x0 = 1  # 초기 변위 (m)
v0 = 0.0  # 초기 속도 (m/s)

def spring_motion(t, y):
    x, v = y
    dxdt = v
    dvdt = -k/m * x - c/m * v  # 감쇠 항 추가
    return [dxdt, dvdt]

# 초기 조건
y0 = [x0, v0]

# 시간 범위
t_span = (0, 100)
t_eval = np.linspace(0, 100, 3000)

# 미분방정식 풀이
sol = solve_ivp(spring_motion, t_span, y0, t_eval=t_eval)

# 결과
t = sol.t
x = sol.y[0]
v = sol.y[1]

# 운동 에너지 계산
kinetic_energy = 0.5 * m * v**2

# 애니메이션 설정
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))

# 용수철 그래프 (수평 방향)
line, = ax1.plot([], [], 'b-', lw=2)
mass, = ax1.plot([], [], 'ro', markersize=10)

ax1.set_xlim(-1.5 * x0, 1.5 * x0)
ax1.set_ylim(-0.2, 0.2)  # 수평 방향으로 이동하므로 y축 범위 축소
ax1.set_xlabel('Position (m)')
ax1.set_ylabel('Height (m)')
ax1.set_title('Mass-Spring System (Damped)')

# 운동 에너지 그래프
line_energy, = ax2.plot([], [], 'g-', lw=2)
ax2.set_xlim(0, 15)
ax2.set_ylim(0, 1.2 * kinetic_energy[12])
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Kinetic Energy (J)')
ax2.set_title('Kinetic Energy')

# 초기화 함수
def init():
    line.set_data([], [])
    mass.set_data([], [])
    line_energy.set_data([], [])
    return line, mass, line_energy

# 애니메이션 업데이트 함수
def update(frame):
    # 수평 방향으로 이동하도록 설정
    line.set_data([0, x[frame]], [0, 0])
    mass.set_data(x[frame], 0)
    line_energy.set_data(t[:frame], kinetic_energy[:frame])
    return line, mass, line_energy

# 애니메이션 생성
ani = animation.FuncAnimation(fig, update, frames=len(t), init_func=init, blit=True, interval=6)

plt.tight_layout()
plt.show()
