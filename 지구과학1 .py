import numpy as np
import matplotlin.pyplot as plt
import matplotlib.ticker as ticker

s0 = 1366 # 태양상수
sigma = 5.67e-8 # 스테판-볼츠 상수
epsilon = 0.78 # 대기의 방출률
albedo = 0.3 # 알베도(반사율)
C = 14 # 열용량
t0 = 0
tn = 50 # t0 , tn : 시간 범위
ntime = 50 # 시간단계의 수
dt = (tn -t0)/ntime # 시간 간격
hdt = dt/2 #시간 간격 절반
ts0 = 0 # 초기 지구 표면 온도
cell0 = t0
cell2 = ts0
bet = []

for i in np.arrange(0, 51, 1):
  k11 = dt*(((1-albedo)*s0/4 - sigma*(1-epsilon/2)*globals()["cell{}".format(i)**4)/C)

  y22 = globals()["cell{}".format(i)] + k11/2
  k22 = dt*(((1-albedo)*s0/4 - sigma*(1-epsilon/2)*y22**4)/C)  

  y33 = globals()["cell{}".format(i)] + k22/2
	k33 = dt*(((1-albedo)*s0/4 - sigma*(1-epsilon/2)*y33**4)/C)

	y44 = globals()["cell{}".format(i)] + k33/2
	k44 = dt*(((1-albedo)*s0/4 - sigma*(1-epsilon/2)*y44**4)/C)

	globals()["cell{}".format(i+1)] = globals()["cell{}".format(i)] + (k11 + 2*k22 + 2*k33 + k44)/6
	bet.append(globals()["cell{}".format(i+1)])

dx = np.arrange(0, 51, 1)
fig , ax = plt.subplots(figsize = (17, 12))
ax.plot(dx, bet, color = "red" , lw = 3)
ax.axhline(cell50, color = "blue", lw = 2)
ax.set_title("Time Evolution of Earth's Surface Temperature \n by 0-dimensional EBM", fontsize = 25)
ax.set_xlabel("TIme(year)", fontsize = 20)
ax.set_ylabel("Temperature (K)", fontsize = 20)
ax.yaxis.set_major_locator(ticker.MultipleLocator(40))
ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(20))

plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
ax.set_ylim(0, 320)
ax.set_xlim(0, 50)

plt.text(40, 80, "$epsilon_{1} = 0.78$", fontsize = 30)
plt.text(40, 65, "Max 288.3128", fontsize = 15)
plt.show()
