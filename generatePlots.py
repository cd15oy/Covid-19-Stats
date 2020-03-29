import matplotlib.pyplot as plt


#I know, it all looks gross. Don't worry about it. 


provinces = [] 
data = []

with open("stats.csv" , 'r') as inF:
    province = None
    for row in inF:
        line = row.split(",")
        if len(line) == 1:
            provinces.append(row.strip())
            if province is not None:
                data.append(province)
            province = [[],[],[],[]] 
            line = next(inF).split(',') 
            province[0].append("Date")
            province[1].append(line[0].strip())
            province[2].append(line[1].strip())
            province[3].append(line[2].strip())
        else:
            line = [float(x.strip()) for x in row.split(",")[1:]]
            province[0].append(row.split(',')[0].strip())
            province[1].append(line[0])
            province[2].append(line[1])
            province[3].append(line[2])


markdown = "" 
for province,index in zip(provinces, range(len(provinces)-1)):
    markdown += "# " +province + "\n"
    for plot in range(1,4):
        stats = data[index]
        total=0
        totalList = []
        for x in stats[plot][1:]:
            total += x 
            totalList.append(total) 

        fix, ax = plt.subplots()
        plt.ylabel(stats[plot][0])
        xTickVals = ["" for x in range(len(stats[0][1:]))]
        for x in range(len(stats[0][1:])):
            if x % 15 == 0:
                xTickVals[x] = stats[0][1:][x]
        plt.xticks(range(len(stats[0])), xTickVals)
        plt.xlabel("Date")
        stepSize = int(0.05*max(totalList))
        if stepSize == 0:
            stepSize = 1
        plt.yticks(range(0,int(max(totalList) + 0.1*max(totalList)), stepSize))
        plt.title(province + "-" + stats[plot][0])
        markdown += "## " + province + "-" + stats[plot][0] + "\n"
        xAx = stats[0][1:]
        yAx = stats[plot][1:] 
        
        
        p1 = plt.bar(xAx,totalList)
        p2 = plt.bar(xAx,yAx)
        plt.legend((p1[0], p2[0]), ('Total', 'Daily'))
        plt.savefig("docs/"+province + "-" + stats[plot][0] + ".png")
        plt.close()

        markdown += '![alt text](' + province.replace(' ','%20') + "-" + stats[plot][0] + ".png " + '"' + province + "-" + stats[plot][0] + '")\n'

with open("docs/page.md", 'w') as outF:
    outF.write(markdown)