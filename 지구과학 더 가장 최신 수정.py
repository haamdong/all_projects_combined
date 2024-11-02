import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
from datetime import datetime, timedelta
from matplotlib.animation import FuncAnimation
plt.rcParams['font.family'] = 'Malgun Gothic'

# 실측치 데이터 포인트
points = [(0, -3), (1, -4), (2, -3), (3, -4), (4,-4),(5,-4), 
          (6, -5), (7,-5), (8, -1), (9, 2), (10, 5), (11, 7),
          (12, 9), (13, 10), (14, 10), (15, 11), (16, 10),
          (17, 9), (18, 6), (19, 4), (21, 1), (23, -1), (24, -3)]

t_points, T_points = zip(*points)
cs = CubicSpline(t_points, T_points, extrapolate=False)

# 고정된 기온 값 설정
min_temp = -5  # 새벽 3시의 최저 기온 (섭씨)
max_temp = 11  # 낮 최고 기온 (섭씨)

# 파라미터 설정
height = 2000  # 대기 높이 (m)
n_layers = 100  # 층의 수
dt = 60  # 시간 간격 (초)
total_time = 24 * 3600
n_steps = int(total_time / dt)

# 초기 조건 설정 (새벽 3시 상태)
T = np.linspace(min_temp, min_temp - 5, n_layers)  # 초기 온도 분포
z = np.linspace(0, height, n_layers)  # 높이 배열

# 시작 시간 설정
start_time = datetime.now().replace(hour=3, minute=0, 
                                    second=0, microsecond=0)

def get_Alpha(t):
    # t는 초 단위 시간
    hour = (t / 3600) % 24  # 시각을 시간 단위로 변환
    
    if hour >= 6 and hour < 18:  # 낮 시간대
        return 0.001 + (hour - 6) / 12 * (0.005 - 0.001)
    elif hour >= 18:  # 저녁 시간대 (해질녘)
        return 0.005 - (hour - 18) / 6 * (0.005 - 0.001)
    else:  # 밤 시간대
        return 0.001

# 지표면 온도 변화 함수
def surface_temperature(t):
    hour = (t / 3600) % 24  # 시간 단위로 변환하여 범위 체크
    if hour < min(t_points) or hour > max(t_points):
        return np.nan  # 보간 범위 밖이면 NaN 반환
    return cs(t / 3600)  # 보간 함수 호출

# 시뮬레이션 함수
def simulate_step(T, t):
    dz = height / (n_layers - 1)
    
    # 시간에 따른 열확산 계수 설정
    heat_transfer_rate = get_Alpha(t)
    
    # 새로운 온도 배열 초기화
    new_T = np.copy(T)
    
    # 각 층의 온도 갱신
    for i in range(1, n_layers - 1):
        delta_T_up = T[i+1] - T[i]# 위층과의 온도차
        delta_T_down = T[i-1] - T[i] # 아래층과의 온도차
        temp_change = heat_transfer_rate * (10*delta_T_up + 30*delta_T_down) * dt / dz**2
        new_T[i] = T[i] + temp_change
    
    # 경계 조건
    new_T[0] = surface_temperature(t)  # 지표면 온도
    new_T[-1] = new_T[-2]  # 상부 경계 조건
    
    return new_T

# 그래프 초기화
fig, ax = plt.subplots(figsize=(10, 6))
line, = ax.plot(T, z)
ax.set_xlim(min_temp - 10, max_temp + 5)
ax.set_ylim(0, height)
ax.set_xlabel('기온 (°C)')
ax.set_ylabel('고도 (m)')
ax.set_title('대기 온도 개요')

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
anim = FuncAnimation(fig, update, frames=n_steps, interval=5, blit=True)

plt.tight_layout()
plt.show()