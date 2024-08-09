import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.interpolate import CubicSpline
from datetime import datetime, timedelta

# 지표면 기온 데이터를 CubicSpline으로 보간
points = [(0, 11.9), (6.25, 10), (8.25, 12), (11.75, 18), (15.25, 20), (17.75, 18), (23.5, 12), (24, 11.9)]
t_points, T_points = zip(*points)
cs = CubicSpline(t_points, T_points)

# 파라미터 설정
height = 2000  # 대기 높이 (m)
n_layers = 200  # 층의 수
dt = 300  # 시간 간격 (초, 5분)
total_time = 24 * 3600  # 총 시뮬레이션 시간 (초, 24시간)
n_steps = int(total_time / dt)

# 초기 조건 설정 (0시 상태)
z = np.linspace(0, height, n_layers)  # 높이 배열
T = np.zeros(n_layers)  # 초기 온도 분포 (섭씨)

# 시작 시간 설정
start_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

# 지표면 온도 변화 함수 (CubicSpline 사용)
def surface_temperature(t):
    hour = t / 3600
    return cs(hour)

# 시뮬레이션 함수
def simulate_step(T, t):
    # 경계 조건: 지표면 온도
    T[0] = surface_temperature(t)
    
    # 상층 대기 온도 감율 적용
    lapse_rate = 0.0065  # 표준 대기 온도 감율 (°C/m)
    T[1:] = T[0] - lapse_rate * z[1:]
    
    # 간단한 역전층 모델 (야간)
    hour = t / 3600
    if 18 <= hour or hour < 6:
        inversion_height = int(n_layers * 0.1)  # 높이의 10%까지 역전층 형성
        inversion_strength = 3  # 역전층의 강도 (°C)
        inversion_profile = np.linspace(inversion_strength, 0, inversion_height)
        T[:inversion_height] += inversion_profile
    
    return T

# 그래프 초기화
fig, ax = plt.subplots(figsize=(10, 6))
line, = ax.plot(T, z)
ax.set_xlim(0, 30)
ax.set_ylim(0, height)
ax.set_xlabel('Temperature (°C)')
ax.set_ylabel('Height (m)')
ax.set_title('Atmospheric Temperature Profile')

# 현재 시간을 표시할 텍스트 객체
time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, fontsize=12)

# 애니메이션 업데이트 함수
def update(frame):
    global T
    t = frame * dt
    T = simulate_step(T, t)
    line.set_xdata(T)
    
    current_time = start_time + timedelta(seconds=t)
    time_text.set_text(f'Current Time: {current_time.strftime("%H:%M")}')
    
    return line, time_text

# 애니메이션 생성
anim = FuncAnimation(fig, update, frames=n_steps, interval=50, blit=True)
plt.tight_layout()
plt.show()