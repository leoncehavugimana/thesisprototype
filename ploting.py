def warn(*args, **kwargs):
    pass

'''
# from LOF import allScores
weeks = mdates.WeekdayLocator()
days = mdates.DayLocator()
hours = mdates.HourLocator()
minutes = mdates.MinuteLocator()

weekFmt = mdates.DateFormatter('%W')
dayFmt = mdates.DateFormatter('%D')
hourFmt = mdates.DateFormatter('%H')
minFmt = mdates.DateFormatter('%T')

# Ploting entire consumption curve
file='data/A'
series=utility.plotFunct(file,'1min')
indices=series.index
values=series.values

series1=utility.plotFunct(file,'15min')
indices1=series1.index
values1=series1.values

series2=utility.plotFunct(file,'30min')
indices2=series2.index
values2=series2.values

series3=utility.plotFunct(file,'H')
indices3=series3.index
values3=series3.values

# plotting consumption curve 
def plotFigFunct(ploter, indices, values):
    ploter.plot(indices,values)
    ploter.set_xlabel('TimeStamp',fontsize=12, color=(1, 0, 0, 0))
    ploter.set_ylabel('ConsumedValue',fontsize=12, color=(0, 1, 0, 0))
    ploter.xaxis.set_major_locator(days)
    ploter.xaxis.set_minor_locator(hours)
    ploter.xaxis.set_major_formatter(dayFmt)

fig,ax=plt.subplots(2,2,figsize=(15,10))
fig.suptitle('Household A')
fig.autofmt_xdate()
fig.tight_layout()

plotFigFunct(ax[0,0],indices, values)
ax[0,0].set_title(' 1 min resolution ', fontsize=12, color=(0, 0, 0,1))

plotFigFunct(ax[0,1],indices1, values1)
ax[0,1].set_title(' 15 min resolution ', fontsize=12, color=(0, 0, 0,1))

plotFigFunct(ax[1,0],indices2, values2)
ax[1,0].set_title(' 30 min resolution ', fontsize=12, color=(0, 0, 0,1))

plotFigFunct(ax[1,1],indices3, values3)
ax[1,1].set_title(' 60 min resolution ', fontsize=12, color=(0, 0, 0,1))

image=fig.savefig('plotedFigure')
plt.show()
'''

'''
# ploting individual day nonconf scores
def pltForEachDayFunct(axes, x_indices, val):
    axes.step(x_indices, val)

fig, axes = plt.subplots(figsize=(12, 12))
axes.set_title('non conf scores')
axes.set_xlabel('Day times')
axes.set_ylabel('NonConf scores')
# axes.xaxis.set_major_locator(hours)
# axes.xaxis.set_minor_locator(minutes)
# axes.xaxis.set_major_formatter(hourFmt)
# axes.grid(which='both')
# axes.set_xlim(left=0,right=np.size(allScores[0]))
# axes.set_ylim(bottom=0, top=5)
# axes.set_axis_off()
ticks = [i for i in range(1, np.size(allScores[0]) + 1)]
axes.set_xticks(ticks, minor=True)
day = 0
days = np.size(allScores, 0)
while day < days:
    series = pd.Series(allScores[day], index=np.arange(1, np.size(allScores[day]) + 1))
    index = series.index
    pltForEachDayFunct(axes, index, series)
    day += 1
fig.autofmt_xdate()
# fig.tight_layout()
fig.savefig('NonConfFig')
plt.show()
'''
