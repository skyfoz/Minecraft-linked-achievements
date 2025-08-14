import json
import os

commonSave = {}

with open("serverside.json", "r") as serverside:
    commonSave = json.load(serverside)

# Répertorie les succès finis
finishedAdv = []
for key, value in commonSave.items():
    if value["done"]:
        finishedAdv.append(key)

# server\world\advancements
# Choppe les Data Version pour chaque joueur
playersDataVersion = {}
playerList = []

os.chdir("server\\world\\advancements")
playerList = os.listdir()

for i in playerList:
    with open(i, "r") as file:
        playerAdv = json.load(file)
        playersDataVersion[i] = {"DataVersion": playerAdv["DataVersion"]}

# Modifie le json serverside
for i in playerList:
    with open(i, "r") as file:
        playerAdv = json.load(file)

        for key, value in playerAdv.items():
            if key != "DataVersion":
                if key not in commonSave.keys():
                    commonSave[key] = value
                elif key not in finishedAdv:

                    for criteria, date in value["criteria"].items():
                        if criteria not in commonSave[key]["criteria"]:
                            commonSave[key]["criteria"][criteria] = date

                commonSave[key]["done"] = value["done"]

os.chdir("..\\..\\..")

with open("serverside.json", "w") as file:
    json.dump(commonSave, file, indent=4)

# Réécrit le serverside pour chaque joueur
os.chdir("server\\world\\advancements")
for i in playerList:
    with open(i, "w") as file:
        playerCommonSave = commonSave
        playerCommonSave["DataVersion"] = playersDataVersion[i]["DataVersion"]
        json.dump(playerCommonSave, file, indent=4)

