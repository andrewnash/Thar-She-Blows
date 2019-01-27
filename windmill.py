from geopy.distance import great_circle
import pandas as pd

# stores all spec data about windmills
# HARD CODED TO READ 12 VALUES ONLY
# access values: [windmilltype +1]['value']
turbineList = []
turbineInfo = []

# imports specification data about turbines from sheet
# stores data in dictionary for algo use
def getSheetData():
    df = pd.read_excel('aec.xlsx', sheet_name='computerReadable')
    values = ['class', 'diameter', 'bLength', 'sweptArea', 'cutInSpeed', 'nominalPowerS', 'cutOutSpeed', 'nominalPower',
              'costPerDepth', 'unitCost', 'maintCost', 'buildTime']
    for column in df:
        if("Type " in column):
            specs = []
            turbineDict = {}

            for i in (number + 1 for number in range(12)):
                specs.append(df[column][i])

            for i in range(len(specs)):
                turbineDict = dict(zip(values, specs))

            turbineList.append(turbineDict)

## returns distance in square meters
def getSquareDistance(coord1, coord2):
    # Modify to get X coords
    xDist1 = (coord1[0], 0)
    xDist2 = (coord2[0], 0)
    # Modify to get Y coords
    yDist1 = (0, coord1[1])
    yDist2 = (0, coord2[1])

    # Get distances and multiply to give square area
    xDistance = great_circle(xDist1, xDist2).m
    yDistance = great_circle(yDist1, yDist2).m
    area = xDistance*yDistance
    return (area, xDistance, yDistance)

def windMillsPerArea(type, area):
    # rotor diameter * 7 = distance needed between each
    # distance needed*distance needed = square area
    rotorDiameter = turbineList[type]['diameter']
    areaPerWindmill = rotorDiameter * 7 * rotorDiameter * 7
    print(areaPerWindmill)
    # int() truncates the decimal
    totalWindmills = int(area/areaPerWindmill)
    return (totalWindmills)

def generateTurbineList(type, xDist, yDist, realNumTowers, coordOne, coordTwo):
    # Fixed granularity of distances between lat and long
    xGran = 1333
    yGran = 555

    # Read data from files
    windData = pd.read_excel('aec.xlsx', sheet_name='wind-data')
    depthData = pd.read_excel('aec.xlsx', sheet_name='depth-data')

    rotorDiameter = turbineList[type]['diameter']
    minimumSpacing = rotorDiameter*7

    tempXDist = 0
    tempYDist = 0

    # Sort the towers out to array
    for i in range(realNumTowers):
        if(tempXDist < xDist):
            tempXDist = tempXDist + minimumSpacing
        else:
            tempXDist = 0
            tempYDist = tempYDist + minimumSpacing

        # number in the array
        xNum = int(tempXDist/xGran)
        yNum = int(tempYDist/yGran)

        itX = 0
        itY = 0
        lats = windData.columns.values[1:]
        longs = windData[list(windData)[0]].tolist()

        # Find iterator for X coord
        for i in range(0, len(lats) - 1):
            if(lats[i] == coordOne[0]):
                itX = i

        # Find iterator for Y coord
        for j in range(1, len(longs) - 1):
            if(longs[j] == coordOne[1]):
                itY = j

        # Hardcoded fix for off by one error
        itY = itY + 1

        turbineInfo.append([lats[itX+xNum], longs[itY+yNum], windData.iloc[itX+xNum][itY+yNum],depthData.iloc[itX+xNum][itY+yNum]])

## Returns total farm energy in kW
def getNomPower(numberWindmills, type):
    nomPower = turbineList[type]['nominalPower']
    return(numberWindmills*nomPower)

## Returns yearly maint cost in mil/year
def getBuildCost(numberWindmills, type):
    unitCost = turbineList[type]['unitCost']
    return(numberWindmills*unitCost)

## Returns yearly maint cost in mil/year
def getBaseMaintCost(numberWindmills, type):
    maintCost = turbineList[type]['maintCost']
    return(numberWindmills*maintCost)

## Returns time to build project in years
def getProjectTime(type):
    return(turbineList[type]['buildTime'])

## Generates Report
##  coordOne and coordTwo (lat, long)
## radioBoxes is a dict containing bools for radioboxes on form
def generateReport(coordOne, coordTwo, radioBoxes, farmType):

    getSheetData()
    farmType = farmType
    area, xDist, yDist = getSquareDistance(coordOne, coordTwo)
    numWindmills = windMillsPerArea(farmType, area)
    generateTurbineList(farmType, xDist, yDist, numWindmills, coordOne, coordTwo)
    power = getNomPower(numWindmills, farmType)
    buildCost = getBuildCost(numWindmills, farmType)
    baseMaintCost = getBaseMaintCost(numWindmills, farmType)
    buildTime = getProjectTime(farmType)

    # Temp variables to hold new params
    buildCostExtras = 0
    maintCostSavings = 0
    extraPowerMade = 0

    # The following ifs calculate the added benefits of options
    if(radioBoxes['heli']):
        maintCostSavings = maintCostSavings - (6*10000)/1000000
        maintCostSavings = maintCostSavings + (6*baseMaintCost*0.005)


    if(radioBoxes['vessel']):
        maintCostSavings = maintCostSavings + (baseMaintCost*0.06)
        buildCostExtras = buildCostExtras + 100000000/1000000

    if(radioBoxes['diags']):
        maintCostSavings = -1* (baseMaintCost + 250000)/1000000
        extraPowerMade = power * 0.01

    if(radioBoxes['log']):
        baseMaintCost = baseMaintCost + (250000/1000000)
        extraPowerMade = power * 0.01

    # Calculate extra cost due to depth
    for i in range(0, numWindmills):
        buildCost = buildCost + (turbineInfo[i][3]*turbineList[farmType]['costPerDepth']/1000000)

    powerAfterWind = 0
    # Calculate lost power due to wind
    for i in range(0, numWindmills):
        # P = π/2 * r² * v³ * ρ * η
        # ^ Formula for power... speed is exponential three
        nomPower = turbineList[farmType]['nominalPower']
        nomPowerS = turbineList[farmType]['nominalPowerS']
        avgSpeed = turbineInfo[i][2]

        powerRatio = (avgSpeed * avgSpeed * avgSpeed)/(nomPowerS * nomPowerS * nomPowerS)

        powerAfterWind = powerAfterWind + powerRatio*nomPower

    power = power + extraPowerMade
    baseMaintCost = baseMaintCost - maintCostSavings
    buildCost = buildCost + buildCostExtras

    powerAfterFiveYears = power
    if(radioBoxes['upgrade']):
        powerAfterFiveYears = powerAfterFiveYears + powerAfterFiveYears*0.05

    print("Area (m^2):", area)
    print("Number of mills: ", numWindmills)
    print("Nom Power: (MW)", power/1000)
    print("Power after wind: (MW)", powerAfterWind/1000)
    print("Nom Power after Five years: (MW)", powerAfterFiveYears/1000)
    print("Maint Cost ($M/Yr): ", baseMaintCost)
    print("Base Build Cost ($M):", buildCost)
    print("Project Time:", buildTime)

    return({'area': area, 'millNum': numWindmills, 'nomPower': power, 'powerAfterWind': powerAfterWind, 'nomPower5': powerAfterFiveYears,
    'maintCost': baseMaintCost, 'buildCost': buildCost, 'projTime': buildTime, 'towerList': turbineInfo})
