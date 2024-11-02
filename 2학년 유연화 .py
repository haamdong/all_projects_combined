import time as t
import functions as fs
from typing import TextI0

print("운행을 시작하려합니다")

while True:
  n = 0
  try:
    v = float(input("속력값을 입력하십시오. ( km/h ) ")
  except:
    print("속력값 제대로 입력해라")
    n -= 1
  if not n:
    break
  else:
    pass

print("운행을 시작합니다.")
start = t.time()
print("type \"help\" to check commands")
while True:
  order = ''
  order = str(input("명령어를 입력해주십시오"))

  if order == "quit":
    print("프로그램을 종료합니다.")
    break
  elif order == "help":
    print("\n 현재까지 주행거리 : dist\n
          "장애물 탐지: obs\n"
          "속력 재설정: vel\n"
          "차량 이동: move\n"
          "프로그램 종료: quit\n")

  elif order == "dist":
    end = t.time()
    dis_time = round(end-start, 2)
    dist = float(dis_time)
    print("현재까지의 주행거리는 %fm입니다." % float(dist*v*139/500))

  elif order == "obs":
    print("장애물 탐지중")
    t.sleep(1)
    fs.read(3)

  elif order == "move":
    ord_mov = input("1. 원하는 위치의 거리, 각도 입력\n"
                    "2. 원하는 위치의 좌표 입력\n"
                    "3. 세 개의 제어점 입력\n"
                    "4. 네 개의 제어점 입력\n"
                    "사용할 방법의 번호를 입력해주십시오")
def turn_path(cx, cy, R, theta_start, theta_end, num_points=100):
  theta = np.linspace(theta_start, theta_end, num_points)
  x = cx -R * np.cos(theta)
  y = cy + R * np.sin(theta)
  path = list(zip(x, y))
  retunr path
  
def path_call(): # 회전 반지름과 각도
  cx = 0 
  cy = 0
  R = float(input("목표지점까지의 거리:"))
  theta = float(input("목표지점과의 각도:"))
  theta_start = 0
  theta_end = np.pi*theta/180
  path = fs.turn_path(cx, cy, R, theta_start, theta_end, num_point = 200)
  x, y = zip(*path)
  plt.plot(x,y)
  plt.xlabel("X-axis")
  plt.ylabel("Y-axis")
  plt.title("path")
  plt.show()
  
