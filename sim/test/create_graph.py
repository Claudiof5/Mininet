import pandas as pd
import matplotlib.pyplot as plt

lista_n_hosts = []
lista_medias = []
lista_min = []
lista_max = []

for i in range(1,6):
    filename = f"result_{2**i}devices_50repeticions.csv"
    df = pd.read_csv(filename)
    media_das_medias = df[df["mean"] > 0]["mean"].mean()
    media_dos_min = df[df["min"] > 0]["min"].mean()
    media_dos_max = df[df["max"] > 0]["max"].mean()
    
    lista_n_hosts.append(2**i)
    lista_medias.append(media_das_medias)
    lista_min.append(media_dos_min)
    lista_max.append(media_dos_max)


plt.plot(lista_n_hosts, lista_medias, marker="o", linestyle="-", color="r", label="Mean Response Time")
plt.plot(lista_n_hosts, lista_min, marker="o", linestyle="-", color="g", label="Min Response Time")
plt.plot(lista_n_hosts, lista_max, marker="o", linestyle="-", color="b", label="Max Response Time")

plt.xlabel("Number of Hosts")
plt.ylabel("Mean Response Time")
plt.title("Progression of Means")
plt.legend()

#plt.ylim(0.3,0.9)
plt.grid(True)
plt.show()
    


