# season-compare-tool

using urllib, beautifulsoup, plotly
https://plot.ly/~brianlondregan36

1. initialize baseball "team" objects you want to compare 
2. hit baseballreference.com page and obtain the team's schedule for the year given

https://www.baseball-reference.com/teams/NYM/2018-schedule-scores.shtml

3. use soup to parse through the markup and grab the W or L from the W/L column
4. also bringing in the date of the game in case you want to use that for chart's x axis (not pictured)
5. list built for the team where each item is a game (x axis) and its value is the number of wins at that time (y axis) 
6. as you go through data, if a win or loss streak is building, create annotation to display this event on chart
7. plot teams and their data on a line chart

![example chart output](https://github.com/brianlondregan36/season-compare-tool/blob/master/2015%20vs%202018%20mets.png?raw=true)

TO DO list
*make simple front-end to choose team and year 
*compute area under the line to get a statstic explaining that teams' course of the season 
