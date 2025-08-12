import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
path = 'fcc-forum-pageviews.csv'
df = pd.read_csv(path)
df['date'] = pd.to_datetime(df['date'])

# Clean data
percentile_2_5 = df['date'].quantile(0.025)
percentile_97_5 = df['date'].quantile(0.975)
df = df[(df["date"]>= percentile_2_5) & (df["date"]<= percentile_97_5)] #Extract data, top and botton of 2.5% 

df['yyyy'] = pd.to_datetime(df['date']).dt.year #Extract year, month (number), month (name)
df['mm'] = pd.to_datetime(df['date']).dt.month
df['month'] = pd.to_datetime(df['date']).dt.month_name()


month_order = ["January", "February", "March", "April", "May", "June", 
                "July", "August", "September", "October", "November", "December"]#Month Order for plots


def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(20, 10))
    ax.plot(df['date'], df['value'])

    ax.set(xlabel='Date', ylabel='Page Views', title='Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.grid()

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()

    df_bar = df_bar.groupby(['yyyy','month'])['value'].mean().reset_index()

    df_bar['month'] = pd.Categorical(df_bar['month'], categories=month_order, ordered=True) #To plot in order the months
    df_bar = df_bar.sort_values(by=['yyyy', 'month'])

    # Draw bar plot
    fig, ax = plt.subplots(figsize=(20, 10))

    sns.barplot(x='yyyy', y='value', hue='month', data=df_bar, ax=ax)

    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.set_title('Average Daily Page Views per Month (2016-2019)')
    ax.legend(title='Months')

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, axes = plt.subplots(1, 2, figsize=(20, 10))
    sns.boxplot(x=df["yyyy"], y=df["value"], ax=axes[0])

    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')
    axes[0].set_title('Year-wise Box Plot (Trend)')

    sns.boxplot(x=df["month"], y=df["value"], order=month_order, ax=axes[1])

    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')
    axes[1].set_title('Month-wise Box Plot (Seasonality)')

    plt.xticks(rotation=45)



    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
