import matplotlib.pyplot as plt
import random as r
def orientation(p, q, r):
    # 세 점 p, q, r이 시계 방향인지 반시계 방향인지를 판별하는 함수
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        return 0  # 일직선 상에 위치한 경우
    elif val > 0:
        return 1  # 반시계 방향인 경우
    else:
        return 2  # 시계 방향인 경우

def convex_hull(points):
    n = len(points)
    if n < 3:
        return None

    hull = []

    # 가장 왼쪽 하단에 위치한 점을 찾는다.
    leftmost = 0
    for i in range(1, n):
        if points[i][0] < points[leftmost][0]:
            leftmost = i
        elif points[i][0] == points[leftmost][0] and points[i][1] < points[leftmost][1]:
            leftmost = i

    p = leftmost
    q = None

    while True:
        hull.append(points[p])
        q = (p + 1) % n

        for i in range(n):
            if orientation(points[p], points[i], points[q]) == 2:
                q = i

        p = q

        if p == leftmost:
            break

    return hull

def plot_points(points, hull):
    x = [point[0] for point in points]
    y = [point[1] for point in points]

    # 처음 점과 마지막 점을 연결하여 폐곡선을 만듭니다.
    hull.append(hull[0])  
    hull_x = [point[0] for point in hull]
    hull_y = [point[1] for point in hull]

    plt.scatter(x, y, color='blue', label='Points')
    plt.plot(hull_x, hull_y, color='red', 
             label='Convex Hull', linestyle='-', 
             linewidth=2, markersize=0.1, 
             marker='o'
             )  
    
    plt.title('Convex Hull')
    plt.legend()
    plt.grid(True)
    plt.show()
points = [(r.randint(-1000, 69000), 
           r.randint(-9999, 9991)) for _ in range(10)
          ]
ch = convex_hull(points)

plot_points(points, ch)


