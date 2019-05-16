def missions_per_year(df):
    '''
    From a dataframe with the 'Year' column,
    Plot a graph showing the number of missions per year
    '''

    missions_per_year = df.Year.value_counts()
    plt.plot(missions_per_year.sort_index())
    plt.show()

def missions_per_week(df):
    '''
    From a dataframe with the 'Year' column,
    Plot a graph showing the number of missions per year
    '''

    missions_per_year = df.Year.value_counts()
    plt.plot(missions_per_year.sort_index())
    plt.show()
