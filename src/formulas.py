Pnorm = 750
CabinVolume = 200
Vair = Pnorm * CabinVolume
HoleSize = 160
RepairRate = 10
AirLoseQuot = 0.048
time = 0


stat = []
stat.append({"time": time, "pressure": Pnorm, "HoleSize": HoleSize})
while HoleSize > 0:
    time+=1
    Vair -= HoleSize * Vair * AirLoseQuot / 100
    HoleSize -= RepairRate
    stat.append({"time": time, "pressure": round(Vair/CabinVolume), "HoleSize": HoleSize})
for s in stat:
    print(s)