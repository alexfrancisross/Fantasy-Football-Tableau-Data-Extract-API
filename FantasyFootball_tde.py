from datetime import datetime
import sys, requests, os
from dataextract import *

# Define the table's schema for fixture_history
def makeTableDefinition():
    tableDef = TableDefinition()
    tableDef.setDefaultCollation(Collation.EN_GB)
    tableDef.addColumn('Name',         Type.CHAR_STRING)
    tableDef.addColumn('Team',         Type.CHAR_STRING)
    tableDef.addColumn('Position',        Type.CHAR_STRING)
    tableDef.addColumn('Photo',           Type.CHAR_STRING)
    tableDef.addColumn('Selected By %',        Type.DOUBLE)
    tableDef.addColumn('News',           Type.CHAR_STRING)
    tableDef.addColumn('Now Cost', Type.INTEGER)
    tableDef.addColumn('Code', Type.INTEGER)
    tableDef.addColumn('Current Fixture', Type.CHAR_STRING)
    tableDef.addColumn('Next Fixture', Type.CHAR_STRING)
    tableDef.addColumn('Status', Type.CHAR_STRING)
    tableDef.addColumn('Chance of Playing This Round', Type.CHAR_STRING)
    tableDef.addColumn('Chance of Playing Next Round', Type.CHAR_STRING)
    tableDef.addColumn('Value Form',        Type.DOUBLE)
    tableDef.addColumn('Value Season',        Type.DOUBLE)
    tableDef.addColumn('In Dream Team', Type.BOOLEAN)
    tableDef.addColumn('Form',        Type.DOUBLE)
    tableDef.addColumn('Date',       Type.CHAR_STRING)
    tableDef.addColumn('Round',         Type.INTEGER)
    tableDef.addColumn('Opponent',        Type.CHAR_STRING)
    tableDef.addColumn('Minutes Played',           Type.INTEGER)
    tableDef.addColumn('Goals Scored',        Type.INTEGER)
    tableDef.addColumn('Assists',           Type.INTEGER)
    tableDef.addColumn('Clean Sheets', Type.INTEGER)
    tableDef.addColumn('Goals Conceded',       Type.INTEGER)
    tableDef.addColumn('Own Goals',         Type.INTEGER)
    tableDef.addColumn('Penalties Saved',        Type.INTEGER)
    tableDef.addColumn('Penalties Missed',           Type.INTEGER)
    tableDef.addColumn('Yellow Cards',        Type.INTEGER)
    tableDef.addColumn('Red Cards',           Type.INTEGER)
    tableDef.addColumn('Saves', Type.INTEGER)
    tableDef.addColumn('Bonus',       Type.INTEGER)
    tableDef.addColumn('EA Sports PPI',         Type.INTEGER)
    tableDef.addColumn('Bonus Points System',        Type.INTEGER)
    tableDef.addColumn('Net Transfers',           Type.INTEGER)
    tableDef.addColumn('Value',        Type.INTEGER)
    tableDef.addColumn('Points',           Type.INTEGER)
    return tableDef

# Define the table's schema for season_history
def makeTableDefinition2():
    tableDef2 = TableDefinition()
    tableDef2.setDefaultCollation(Collation.EN_GB)
    tableDef2.addColumn('Name',         Type.CHAR_STRING)
    tableDef2.addColumn('Team',         Type.CHAR_STRING)
    tableDef2.addColumn('Position',        Type.CHAR_STRING)
    tableDef2.addColumn('Photo',           Type.CHAR_STRING)
    tableDef2.addColumn('Selected By %',        Type.DOUBLE)
    tableDef2.addColumn('News',           Type.CHAR_STRING)
    tableDef2.addColumn('Now Cost', Type.INTEGER)
    tableDef2.addColumn('Season',       Type.CHAR_STRING)
    tableDef2.addColumn('Minutes Played',           Type.INTEGER)
    tableDef2.addColumn('Goals Scored',        Type.INTEGER)
    tableDef2.addColumn('Assists',           Type.INTEGER)
    tableDef2.addColumn('Clean Sheets', Type.INTEGER)
    tableDef2.addColumn('Goals Conceded',       Type.INTEGER)
    tableDef2.addColumn('Own Goals',         Type.INTEGER)
    tableDef2.addColumn('Penalties Saved',        Type.INTEGER)
    tableDef2.addColumn('Penalties Missed',           Type.INTEGER)
    tableDef2.addColumn('Yellow Cards',        Type.INTEGER)
    tableDef2.addColumn('Red Cards',           Type.INTEGER)
    tableDef2.addColumn('Saves', Type.INTEGER)
    tableDef2.addColumn('Bonus',       Type.INTEGER)
    tableDef2.addColumn('EA Sports PPI',         Type.INTEGER)
    tableDef2.addColumn('Bonus Points System',        Type.INTEGER)
    tableDef2.addColumn('Value',        Type.INTEGER)
    tableDef2.addColumn('Points',           Type.INTEGER)
    return tableDef2

def makeTableDefinitionFixtures():
    tableDefFixtures = TableDefinition()
    tableDefFixtures.setDefaultCollation(Collation.EN_GB)
    tableDefFixtures.addColumn('Name',         Type.CHAR_STRING)
    tableDefFixtures.addColumn('Team',         Type.CHAR_STRING)
    tableDefFixtures.addColumn('Position',        Type.CHAR_STRING)
    tableDefFixtures.addColumn('Photo',           Type.CHAR_STRING)
    tableDefFixtures.addColumn('Selected By %',        Type.DOUBLE)
    tableDefFixtures.addColumn('News',           Type.CHAR_STRING)
    tableDefFixtures.addColumn('Now Cost', Type.INTEGER)
    tableDefFixtures.addColumn('Match Date and Time',       Type.CHAR_STRING)
    tableDefFixtures.addColumn('Gameweek',           Type.CHAR_STRING)
    tableDefFixtures.addColumn('Opponent',        Type.CHAR_STRING)

    return tableDefFixtures

# Print a Table's schema to stderr.
def printTableDefinition(tableDef):
    for i in range(tableDef.getColumnCount()):
        type = tableDef.getColumnType(i)
        name = tableDef.getColumnName(i)
        print >> sys.stderr, "Column {0}: {1} ({2:#06x})".format(i, name, type)

# Insert data into fixture_history.tde
def insertFixtureHistoryData(table):
    tableDef = table.getTableDefinition()

    #for each player (~700 in total)
    for i in range(700):
        playerurl = "http://fantasy.premierleague.com/web/api/elements/%s/"
        r = requests.get(playerurl % i)
        row = Row(tableDef)

        # skip non-existent players
        if r.status_code != 200: continue

        #print player name being written
        print str(i) + " writing to fixture_history.tde: " + r.json()["first_name"] + " " + r.json()["second_name"]

        #build string to hold play and fixture info for each match this season
        row.setCharString(0, r.json()["first_name"].encode('utf-8') + " " + r.json()["second_name"].encode('utf-8'))
        row.setCharString(1, r.json()["team_name"].encode('utf-8'))
        row.setCharString(2, r.json()["type_name"].encode('utf-8'))
        row.setCharString(3, r.json()["photo"].encode('utf-8'))
        row.setDouble(4, float(r.json()["selected_by"]))
        row.setCharString(5, r.json()["news"].encode('utf-8'))
        row.setInteger(6, r.json()["now_cost"]*100000)
        row.setInteger(7, r.json()["code"])
        row.setCharString(8, r.json()["current_fixture"].encode('utf-8'))
        row.setCharString(9, r.json()["next_fixture"].encode('utf-8'))
        row.setCharString(10, r.json()["status"].encode('utf-8'))
        row.setCharString(11, str(r.json()["chance_of_playing_this_round"]).encode('utf-8'))
        row.setCharString(12, str(r.json()["chance_of_playing_next_round"]).encode('utf-8'))
        row.setDouble(13, float(r.json()["value_form"]))
        row.setDouble(14, float(r.json()["value_season"]))
        row.setBoolean(15, r.json()["in_dreamteam"])
        row.setDouble(16, float(r.json()["form"]))

        data = r.json()["fixture_history"]["all"]

        #for each match write row to fixture_history.tde
        for x in range (0, len(data)):
            row.setCharString(17, data[x][0].encode('utf-8')) #Date
            row.setInteger(18, data[x][1]) #Round
            row.setCharString(19, data[x][2].encode('utf-8')) #Opponent
            row.setInteger(20, data[x][3]) #Minutes Played
            row.setInteger(21, data[x][4]) #Goals Scored
            row.setInteger(22, data[x][5]) #Assists
            row.setInteger(23, data[x][6]) #Clean Sheets
            row.setInteger(24, data[x][7]) #Goals Conceded
            row.setInteger(25, data[x][8]) #Own Goals
            row.setInteger(26, data[x][9]) #Penalties Saved
            row.setInteger(27, data[x][10]) #Penalties Missed
            row.setInteger(28, data[x][11]) #Yellow Cards
            row.setInteger(29, data[x][12]) #Red Cards
            row.setInteger(30, data[x][13]) #Saves
            row.setInteger(31, data[x][14]) #Bonus
            row.setInteger(32, data[x][15]) #EA Sports PPI
            row.setInteger(33, data[x][16]) #Bonus Points System
            row.setInteger(34, data[x][17]) #Net Transfers
            row.setInteger(35, data[x][18]*100000) #Value
            row.setInteger(36, data[x][19]) #Points
            table.insert(row)

# Insert data into fixtures.tde
def insertFixturesData(table):
    tableDef = table.getTableDefinition()

    #for each player (~700 in total)
    for i in range(700):
        playerurl = "http://fantasy.premierleague.com/web/api/elements/%s/"
        r = requests.get(playerurl % i)
        row = Row(tableDef)

        # skip non-existent players
        if r.status_code != 200: continue

        #print player name being written
        print str(i) + " writing to fixtures.tde: " + r.json()["first_name"] + " " + r.json()["second_name"]

        #build string to hold play and fixture info for each match this season
        row.setCharString(0, r.json()["first_name"].encode('utf-8') + " " + r.json()["second_name"].encode('utf-8'))
        row.setCharString(1, r.json()["team_name"].encode('utf-8'))
        row.setCharString(2, r.json()["type_name"].encode('utf-8'))
        row.setCharString(3, r.json()["photo"].encode('utf-8'))
        row.setDouble(4, float(r.json()["selected_by"]))
        row.setCharString(5, r.json()["news"].encode('utf-8'))
        row.setInteger(6, r.json()["now_cost"]*100000)

        data = r.json()["fixtures"]["all"]

        #for each match write row to fixture_history.tde
        for x in range (0, len(data)):
            row.setCharString(7, data[x][0].encode('utf-8')) #Date and Time
            row.setCharString(8, data[x][1].encode('utf-8')) #GameWeek
            row.setCharString(9, data[x][2].encode('utf-8')) #Opponent
            table.insert(row)


# Insert data into season_history.tde
def insertseasonData(table):
    tableDef = table.getTableDefinition()

    #for each player (~700 in total)
    for i in range(700):
        playerurl = "http://fantasy.premierleague.com/web/api/elements/%s/"
        r = requests.get(playerurl % i)
        row = Row(tableDef)

        # skip non-existent players
        if r.status_code != 200: continue

        #print player name being written
        print str(i) + " writing to season_history.tde: " + r.json()["first_name"] + " " + r.json()["second_name"]

        #build string to hold play and fixture info for each match this season
        row.setCharString(0, r.json()["first_name"].encode('utf-8') + " " + r.json()["second_name"].encode('utf-8'))
        row.setCharString(1, r.json()["team_name"].encode('utf-8'))
        row.setCharString(2, r.json()["type_name"].encode('utf-8'))
        row.setCharString(3, r.json()["photo"].encode('utf-8'))
        row.setDouble(4, float(r.json()["selected_by"]))
        row.setCharString(5, r.json()["news"].encode('utf-8'))
        row.setInteger(6, r.json()["now_cost"]*100000)

        #build string to hold play and fixture info for season history
        data = r.json()["season_history"]
        #for each match write row to season_history.tde
        for x in range (0, len(data)):
            row.setCharString(7, data[x][0].encode('utf-8')) #Season
            row.setInteger(8, data[x][1]) #Minutes Played
            row.setInteger(9, data[x][2]) #Goals Scored
            row.setInteger(10, data[x][3]) #Assists
            row.setInteger(11, data[x][4]) #Clean Sheets
            row.setInteger(12, data[x][5]) #Goals Conceded
            row.setInteger(13, data[x][6]) #Own Goals
            row.setInteger(14, data[x][7]) #Penalties Saved
            row.setInteger(15, data[x][8]) #Penalties Missed
            row.setInteger(16, data[x][9]) #Yellow Cards
            row.setInteger(17, data[x][10]) #Red Cards
            row.setInteger(18, data[x][11]) #Saves
            row.setInteger(19, data[x][12]) #Bonus
            row.setInteger(20, data[x][13]) #EA Sports PPI
            row.setInteger(21, data[x][14]) #Bonus Points System
            row.setInteger(22, data[x][15]*100000) #Value
            row.setInteger(23, data[x][16]) #Points
            table.insert(row)

#write fixture_history.tde
try:
    os.remove('fixture_history.tde')
except OSError:
    pass

try:
    with Extract('fixture_history.tde') as extract:

        table = None
        if not extract.hasTable('Extract'):
            # Table does not exist; create it
            tableDef = makeTableDefinition()
            table = extract.addTable('Extract', tableDef)
        else:
            # Open an existing table to add more rows
            table = extract.openTable('Extract')

        tableDef = table.getTableDefinition()
        #printTableDefinition(tableDef)

        insertFixtureHistoryData(table)

except TableauException, e:
    print 'Something bad happened:', e

#write fixtures.tde
try:
    os.remove('fixtures.tde')
except OSError:
    pass

try:
    with Extract('fixtures.tde') as extract:

        table = None
        if not extract.hasTable('Extract'):
            # Table does not exist; create it
            tableDef = makeTableDefinitionFixtures()
            table = extract.addTable('Extract', tableDef)
        else:
            # Open an existing table to add more rows
            table = extract.openTable('Extract')

        tableDef = table.getTableDefinition()
        #printTableDefinition(tableDef)

        insertFixturesData(table)

except TableauException, e:
    print 'Something bad happened:', e

#write season_history.tde
try:
    os.remove('season_history.tde')
except OSError:
    pass

try:
    with Extract('season_history.tde') as extract:

        table = None
        if not extract.hasTable('Extract'):
            # Table does not exist; create it
            tableDef = makeTableDefinition2()
            table = extract.addTable('Extract', tableDef)
        else:
            # Open an existing table to add more rows
            table = extract.openTable('Extract')

        tableDef = table.getTableDefinition()
        #printTableDefinition(tableDef)

        insertseasonData(table)

except TableauException, e:
    print 'Something bad happened:', e


