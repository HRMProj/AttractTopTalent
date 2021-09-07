import requests
import json
import pprint
import xlsxwriter

designResponse = requests.get("http://api.topcoder.com/v2/develop/statistics/tops/design?pageIndex=1&pageSize=100")
designToppers = []
for key in designResponse.json()["data"]:
    designToppers.append(key["handle"])

codeResponse = requests.get("http://api.topcoder.com/v2/develop/statistics/tops/code?pageIndex=1&pageSize=100")
codeToppers = []
for key in codeResponse.json()["data"]:
    codeToppers.append(key["handle"])

dataSciResponse = requests.get("http://api.topcoder.com/v2/data/srm/statistics/tops?rankType=Competitors&pageIndex=1&pageSize=100")
dataSciToppers = []
for key in dataSciResponse.json()["data"]:
    dataSciToppers.append(key["handle"])

designDictionary = {}
for name in designToppers:
#    print(name)
    designChallenges = requests.get("https://api.topcoder.com/v4/members/"+name+"/challenges/").json()["result"]["content"]
#    print(len(designChallenges))
    for challenge in designChallenges:
        if challenge["subTrack"] == "DESIGN":
            if int(challenge["id"]) in designDictionary.keys():
                designDictionary.get(int(challenge["id"]))[2] += 1
            else:    
                designDictionary[int(challenge["id"])] = [challenge["numRegistrants"],challenge["totalPrize"],1]

#pprint.pprint(designDictionary)

workbook = xlsxwriter.Workbook('hello.xlsx')
worksheet = workbook.add_worksheet()
row = 0
column = 0
for key in designDictionary:
    worksheet.write(row, column, key)
    worksheet.write(row, column+1, designDictionary[key][0])
    worksheet.write(row, column+2, designDictionary[key][1])
    worksheet.write(row, column+3, designDictionary[key][2])
    row+=1


codeDictionary = {}
for name in codeToppers:
#    print(name)
    codeChallenges = requests.get("https://api.topcoder.com/v4/members/"+name+"/challenges/").json()["result"]["content"]
#    print(len(codeChallenges))
    for challenge in codeChallenges:
        if challenge["track"] == "DEVELOP" and challenge["subTrack"] != "DESIGN":
            if int(challenge["id"]) in codeDictionary.keys():
                codeDictionary.get(int(challenge["id"]))[2] += 1
            else:    
                codeDictionary[int(challenge["id"])] = [challenge["numRegistrants"],challenge["totalPrize"],1]

#pprint.pprint(codeDictionary)

worksheet = workbook.add_worksheet()
row = 0
column = 0
for key in codeDictionary:
    worksheet.write(row, column, key)
    worksheet.write(row, column+1, codeDictionary[key][0])
    worksheet.write(row, column+2, codeDictionary[key][1])
    worksheet.write(row, column+3, codeDictionary[key][2])
    row+=1

dataSciDictionary = {}
for name in dataSciToppers:
#    print(name)
    dataSciChallenges = requests.get("https://api.topcoder.com/v4/members/"+name+"/challenges/").json()["result"]["content"]
#    print(len(dataSciChallenges))
    for challenge in dataSciChallenges:
        if challenge["track"] == "DATA_SCIENCE":
            if int(challenge["id"]) in codeDictionary.keys():
                dataSciDictionary.get(int(challenge["id"]))[2] += 1
            else:    
                dataSciDictionary[int(challenge["id"])] = [challenge["numRegistrants"],challenge["totalPrize"],1]

pprint.pprint(dataSciDictionary)

worksheet = workbook.add_worksheet()
row = 0
column = 0
for key in dataSciDictionary:
    worksheet.write(row, column, key)
    worksheet.write(row, column+1, dataSciDictionary[key][0])
    worksheet.write(row, column+2, dataSciDictionary[key][1])
    worksheet.write(row, column+3, dataSciDictionary[key][2])
    row+=1

workbook.close()