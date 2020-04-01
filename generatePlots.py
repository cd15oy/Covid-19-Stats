import matplotlib.pyplot as plt

#I added a new plot to make it easy to compare the number of new cases vs the number of recovered or deceased cases
#Reporting of recovered numbers is a little wonky in most provinces, they tend to report a bunch all at once, instead of reporting a few each day as they happen so right now most of the plots are ugly. 
#also, I was going to have the script grab a csv from https://www.canada.ca/en/public-health/services/diseases/2019-novel-coronavirus-infection.html?topic=tilelink but the csv there doesn't include recovered numbers. Since I'd have to continue grabbing recovered numbers manually anyway I didn't bother grabbing that csv 


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
        plt.yticks(range(0,int(max(totalList) + 0.1*max(totalList)+1), stepSize))
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

    #A separate line plot showing infected, recovered, and deceased by day 
    #I'd like be able to see when the number of cases being resolved outpaces the number of cases still active as well as how those cases are resolved
    fix, ax = plt.subplots()
    plt.ylabel(stats[plot][0])
    xTickVals = ["" for x in range(len(stats[0][1:]))]
    for x in range(len(stats[0][1:])):
        if x % 15 == 0:
            xTickVals[x] = stats[0][1:][x]
    plt.xticks(range(len(stats[0])), xTickVals)
    plt.xlabel("Date")

    maxVal = max(stats[1][1:] + stats[2][1:] + stats[3][1:])
    stepSize = int(0.05*maxVal)
    if stepSize == 0:
        stepSize = 1
    plt.yticks(range(0,int(maxVal + 0.1*maxVal +1), stepSize))
    plt.title(province + "-" + stats[plot][0])
    markdown += "## " + province + "-Trends\n"
    
    xAx = stats[0][1:]
    yAx = stats[1][1:] #get infected

    p1 = plt.plot(xAx,yAx)

    yAx = stats[2][1:] #get recovered 
    p2 = plt.plot(xAx, yAx)

    yAx = stats[3][1:] #get deceased 
    p3 = plt.plot(xAx, yAx)

    plt.legend((p1[0], p2[0], p3[0]), ('Infected', 'Recovered', 'Deceased'))
    plt.savefig("docs/"+province + "-Trends.png")
    plt.close()

    markdown += '![](' + province.replace(' ','%20') + "-Trends.png " + '"' + province + "-Trends" + '")\n\n'

markdown += "# Source\n"
markdown += "All counts taken from [CTV](https://www.ctvnews.ca/health/coronavirus/tracking-every-case-of-covid-19-in-canada-1.4852102)\n\n"
with open("docs/page.md", 'w') as outF:
    outF.write(markdown)