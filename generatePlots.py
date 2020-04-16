import matplotlib.pyplot as plt
import os 


#I know, it all looks gross. Don't worry about it. 


provinces = [] 
data = []

csv_columns = "Province,Date,Infected,Recovered,Deceased"

path = "COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/"

files = os.listdir(path) 

files = sorted(files)

dataDict = dict() 
provinces = ["Ontario","Manitoba","New Brunswick","Newfoundland and Labrador","Northwest Territories","Nova Scotia","Prince Edward Island","Quebec","Saskatchewan","Yukon","Alberta","Nunavut","British Columbia"]
for p in provinces:
    dataDict[p] = [["Date", "01-21"],["Infected",0],["Recovered",0],["Deceased",0]]


def floatOrZero(x):
    try:
        return float(x)
    except ValueError:
        return 0 

#iterate through each file to grab the total counts from each day for each province
for fl in files:
    if fl == ".gitignore" or fl == "README.md":
        continue 

    with open(path + fl, 'r') as inF: 
        hasData = dict()
        for prov in provinces:
            hasData[prov] = False

        date = fl.split("-")

        for l in inF:
            line = l.split(",")

            

            #The data source changed the CSV format on 3-21 
            if int(date[0]) <= 3 and int(date[1]) <= 21: 
                prov = line[0].strip()
                
                #If this line is a province
                if prov in provinces:
                    hasData[prov] = True #grab the data 
                    dataDict[prov][0].append(date[0] + "-" + date[1])
                    dataDict[prov][1].append(floatOrZero(line[3]))
                    dataDict[prov][2].append(floatOrZero(line[5]))
                    dataDict[prov][3].append(floatOrZero(line[4]))
               
            else:
              
                prov = line[2].strip()
               
                if prov in provinces:
                    hasData[prov] = True
                    dataDict[prov][0].append(date[0] + "-" + date[1])
                    dataDict[prov][1].append(floatOrZero(line[7]))
                    dataDict[prov][2].append(floatOrZero(line[9]))
                    dataDict[prov][3].append(floatOrZero(line[8]))
                 
        #if this day has no data for any province, repeat yesterdays values 
        for x in provinces:
            if not hasData[x]:
                dataDict[x][0].append(date[0] + "-" + date[1])
                dataDict[x][1].append(dataDict[x][1][-1])
                dataDict[x][2].append(dataDict[x][2][-1])
                dataDict[x][3].append(dataDict[x][3][-1])
             
#move the data to the data list that the rest of the script expects
for p in provinces:
    data.append(dataDict[p])

#Convert the total counts, to daily change 
for p,i in zip(provinces, range(len(provinces))):
    oldValues = [0,0,0,0]
    for col in range(1, len(data[i])):
        for day in range(1, len(data[i][col])):
            val = data[i][col][day]

            data[i][col][day] = max(val - oldValues[col],0)
            oldValues[col] = val 


# with open("stats.csv" , 'r') as inF:
#     province = None
#     for row in inF:
#         if csv_columns is None:
#             csv_columns = row.strip().split(",")
#             continue

#         line = row.split(",")
#         cur_province = line[0].strip()

#         # that is, if this is a new province to add
#         if cur_province not in provinces:
#             provinces.append(cur_province)

#             # if there was a previous province
#             if province is not None:
#                 data.append(province)
            
#             province = [[],[],[],[]] 
#             province[0].append(csv_columns[1])
#             province[1].append(csv_columns[2])
#             province[2].append(csv_columns[3])
#             province[3].append(csv_columns[4])


#         line = [float(x.strip()) for x in row.split(",")[2:]]
#         province[0].append(row.split(',')[1].strip())
#         province[1].append(line[0])
#         province[2].append(line[1])
#         province[3].append(line[2])


markdown = "" 
for province,index in zip(provinces, range(len(provinces))):
    markdown += "# " +province + "\n"

    #Here we calculate the average daily percent change in deaths over the last week 
    total=0
    totalList = []
    for x in data[index][3][1:]:
        total += x 
        totalList.append(total) 
    
    def protDiv(x,y):
        if y == 0:
            return (x+1)/(y+1)
        else:
            return x/y

    estimateLength = 5
    estimatedDailyPercentChange = sum([protDiv(float(x),y) for x,y in zip(totalList[-estimateLength:],totalList[-estimateLength-1:-1])])/estimateLength
    aveDailyDeaths = sum(data[index][3][-estimateLength:])/float(estimateLength)

    #This number will be used to estimate the average daily percent change in infections 2 weeks ago 
    #The estimate is for 2 weeks ago since the average time to death is around 2 weeks 
    #This VERY ROUGH estimate can then be used to plot the expected infections along with the reported infections to better visualize how things are changing
    #This should not be interpreted as a real projection. I am not a professional, I just wanted a rough comparison between the reported numbers today, and how things looked a couple weeks ago
    #I'm using deaths to estimate infections because in theory the deaths should be less influenced by sampling biases, that is assuming the majority of deaths are by covid-19 are correctly attributed to covid-19

    #median time to death taken from https://www.thelancet.com/journals/lancet/article/PIIS0140-6736(20)30566-3/fulltext
    #median 18 with values from 15 to 22 

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
        plt.ylim(0, max(totalList))
        plt.title(province + "-" + stats[plot][0])
        markdown += "## " + province + "-" + stats[plot][0] + "\n"
        xAx = stats[0][1:]
        yAx = stats[plot][1:] 
        
        
        p1 = plt.bar(xAx,totalList)
        p2 = plt.bar(xAx,yAx)

        if plot == 1 and aveDailyDeaths >= 1:
            #Since we have data on a range of time to deaths, I'm plotting a range of expected infections 
            colors = ["red", "yellow", "green"]
            lines = [] 
            timeToDeath = 15
            for i in range(3):
                expectedInfections = [x for x in totalList] 
                for x in range(-timeToDeath, 0, 1):
                    expectedInfections[x] = expectedInfections[x-1]*estimatedDailyPercentChange 
                lines.append(plt.plot(xAx, expectedInfections, color=colors[i]))
                timeToDeath += 3
            plt.legend((p1[0], p2[0], lines[0][0], lines[1][0], lines[2][0]), ('Total', 'Daily', 'Expected-15TTD', 'Expected-18TTD', 'Expected-21TTD', ))
        else:
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
    plt.title(province + "-Trends")
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
markdown += "All counts taken from [John Hopkins CSSE](https://github.com/CSSEGISandData/COVID-19)\n\n"
with open("docs/page.md", 'w') as outF:
    outF.write(markdown)