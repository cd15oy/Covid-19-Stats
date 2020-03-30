import matplotlib.pyplot as plt


#I know, it all looks gross. Don't worry about it. 


provinces = [] 
data = []

csv_columns = None

with open("stats.csv" , 'r') as inF:
    province = None
    for row in inF:
        if csv_columns is None:
            csv_columns = row.strip().split(",")
            continue

        line = row.split(",")
        cur_province = line[0].strip()

        # that is, if this is a new province to add
        if cur_province not in provinces:
            provinces.append(cur_province)

            # if there was a previous province
            if province is not None:
                data.append(province)
            
            province = [[],[],[],[]] 
            province[0].append(csv_columns[1])
            province[1].append(csv_columns[2])
            province[2].append(csv_columns[3])
            province[3].append(csv_columns[4])


        line = [float(x.strip()) for x in row.split(",")[2:]]
        province[0].append(row.split(',')[1].strip())
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

        markdown += '![](' + province.replace(' ','%20') + "-" + stats[plot][0] + ".png " + '"' + province + "-" + stats[plot][0] + '")\n\n'


markdown += "# Source\n"
markdown += "All counts taken from [CTV](https://www.ctvnews.ca/health/coronavirus/tracking-every-case-of-covid-19-in-canada-1.4852102)\n\n"
with open("docs/page.md", 'w') as outF:
    outF.write(markdown)