import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.dates as mdates
from datetime import datetime, timedelta

# 사용자 입력
min_temp = float(input("새벽 3시의 최저 기온을 입력하세요 (섭씨): "))
max_temp = float(input("낮 최고 기온을 입력하세요 (섭씨): "))

# 파라미터 설정
height = 1000  # 대기 높이 (m)
n_layers = 100  # 층의 수
dt = 300  # 시간 간격 (초, 5분)
total_time = 12 * 3600  # 총 시뮬레이션 시간 (초, 12시간)
n_steps = int(total_time / dt)

# 초기 조건 설정 (새벽 3시 상태)
T = np.linspace(min_temp, min_temp - 5, n_layers)  # 초기 온도 분포 (섭씨)
z = np.linspace(0, height, n_layers)  # 높이 배열

# 열 확산 계수 (m^2/s)
K = 0.1

# 시작 시간 설정
start_time = datetime.now().replace(hour=3, minute=0, second=0, microsecond=0)

# 지표면 온도 변화 함수
def surface_temperature(t):
    hour = (t / 3600 + 3) % 24  # 3시부터 시작
    if 3 <= hour < 15:  # 3시부터 15시까지 온도 상승
        return min_temp + (max_temp - min_temp) * np.sin(np.pi * (hour - 3) / 12)
    else:
        return max_temp - (max_temp - min_temp) * np.sin(np.pi * (hour - 15) / 12)

# 시뮬레이션 함수
def simulate_step(T, t):
    dz = height / (n_layers - 1)
    
    # 열 확산
    dTdt = K * np.diff(T, 2) / dz**2
    T[1:-1] += dTdt * dt
    
    # 경계 조건
    T[0] = surface_temperature(t)  # 지표면 온도
    T[-1] = T[-2]  # 상부 경계 조건
    
    return T

# 그래프 초기화
fig, ax = plt.subplots(figsize=(10, 6))
line, = ax.plot(T, z)
ax.set_xlim(min_temp - 10, max_temp + 5)
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