from urllib.request import urlopen
from bs4 import BeautifulSoup
import plotly.plotly as py
import plotly.graph_objs as go


annotations = []

class Team(object):
    
    def __init__(self, name, year, timeSeriesYear):
        self.name = name
        self.year = year
        self.url = "http://www.baseball-reference.com/teams/" + self.name + "/" + self.year + "-schedule-scores.shtml" 
        self.currentGame = 1
        self.currentStreak = 0
        self.winCounts = []
        self.gameLog = []
        self.gameDates = []
        self.timeSeriesYear = timeSeriesYear

    def ReadInSeason(self):
        
        page = urlopen(self.url)       
        soup = BeautifulSoup(page.read(), "lxml")   
        
        top = soup.find('table', {'id': 'team_schedule'}).tbody        
        for thisRow in top.findAll('tr'): 
            
            endCheck = thisRow.find('td', attrs={'data-stat': 'preview'})
            if endCheck:
                break
            
            cell = thisRow.find('td', attrs={'data-stat': 'win_loss_result'})
            if cell: 
                
                outcome = cell.string[0]
                increment = 1 if outcome == "W" else 0
                
                if outcome == "W" and self.currentStreak >= 0:
                    self.currentStreak += 1
                elif outcome == "L" and self.currentStreak <= 0:
                    self.currentStreak -= 1
                else:
                    if abs(self.currentStreak) > 6:
                        self.AddAnnotation(outcome)
                        
                    if outcome == "W":
                        self.currentStreak = 1
                    elif outcome == "L":
                        self.currentStreak = -1
                
                if self.currentGame == 1:
                    self.winCounts.append(increment)
                    txt = "Game 1: Win Number " + str(increment)
                else:
                    winNumber = self.winCounts[ self.currentGame - 2 ]
                    newWinNumber = winNumber + increment
                    self.winCounts.append(newWinNumber)  
                    txt = "Game " + str(self.currentGame) + ": Win Number " + str(newWinNumber)
                
                self.gameLog.append(txt)
                cell = thisRow.find('td', attrs={'data-stat': 'date_game'})
                gameDate = cell['csk']  #'2018-05-22'             
                newDate = self.timeSeriesYear + gameDate[4:10]
                self.gameDates.append(newDate)  
                
                self.currentGame += 1
        
    def CreateTrace(self):
        trace = go.Scatter(
                name = "The " + self.year + " " + self.name,
                x = list(range(1, self.currentGame)),
                y = self.winCounts,                
                text = self.gameLog,
                mode = 'lines+markers'
        )
        return trace
    
    def AddAnnotation(self, outcome):
        streakType = " game " + ("L" if outcome == "W" else "W") + " streak"
        a = dict(
                x = self.currentGame-1,
                y = self.winCounts[self.currentGame-2],
                xref='x',
                yref='y',
                text = str(abs(self.currentStreak)) + streakType,
                showarrow=True,
                arrowhead=10,
                ax=0,
                ay=-40
                )   
        annotations.append(a)


#GET FIRST TEAM STATS
teamA = Team("NYM", "2015", "2015") 
teamA.ReadInSeason()
t1 = teamA.CreateTrace()

#GET SECOND TEAM STATS
teamB = Team("NYM", "2018", "2015")
teamB.ReadInSeason()
t2 = teamB.CreateTrace()

#PLOT EVERYTHING
data = [t1,t2]
layout = dict(title = "Comparing teams' wins over the course of the season.", 
              xaxis = dict(title = "Games Played"),
              yaxis = dict(title = "Wins Accrued"),
              annotations = annotations
)
fig = dict(data=data, layout=layout)
py.plot(fig, filename='2015 vs 2018 mets', sharing='public')


