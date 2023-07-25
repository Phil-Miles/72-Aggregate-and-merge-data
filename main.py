import pandas as pd
import matplotlib.pyplot as plt

colors_data = pd.read_csv('data/colors.csv')
themes_data = pd.read_csv('data/themes.csv')
sets_data = pd.read_csv('data/sets.csv')

# [1] how many colors are there?
# .nunique() returns the number of unique values
# >>> print(colors_data['name'].nunique())
# 135

# [1.1] how many transparent/opaque colors?

# [I] using .eq() and .sum()
# >>> print(colors_data['is_trans'].eq('f').sum())
# >>> print(colors_data['is_trans'].eq('t').sum())
# 107
# 28

# [II] using .groupby() and .count()
# >>> print(colors_data.groupby('is_trans').count())
#            id  name  rgb
# is_trans
# f         107   107  107
# t          28    28   28

# [III] using .value_counts()
# >>> print(colors_data.is_trans.value_counts())
# f    107
# t     28
# Name: is_trans, dtype: int64

# [2] how many Lego sets were released during the 1st year?
first_year = sets_data['year'].min()
# [I] to get entire rows:
# >>> print(sets_data[sets_data['year']==first_year])
# [II] to get the number of entries:
# >>> print(sets_data.year.eq(first_year).sum())
# 5

# [3] top 5 lego sets with the most parts
# [I] in two steps
# >>> sets_sorted = sets_data.sort_values(by='num_parts', ascending=False)
# >>> print(sets_sorted.head())
# [II] in a single step
# >>> print(sets_data.sort_values('num_parts', ascending=False).head())
#         set_num                           name  year  theme_id  num_parts
# 15004  BIGBOX-1  The Ultimate Battle for Chima  2015       571       9987
# 11183   75192-1          UCS Millennium Falcon  2017       171       7541
# 10551   71043-1                Hogwarts Castle  2018       246       6020
# 295     10256-1                      Taj Mahal  2017       673       5923
# 221     10189-1                      Taj Mahal  2008       673       5922

# [4] plot the number of sets by year
sets_by_year = sets_data.groupby('year').count()
# >>> plt.plot(sets_by_year.index[:-2], sets_by_year.set_num[:-2])
# >>> plt.show()
# [4.1] plot number of themes by year
themes_by_year = sets_data.groupby('year').agg({'theme_id': pd.Series.nunique})
themes_by_year.rename(columns={'theme_id': 'nr_themes'}, inplace=True)
# >>> plt.plot(themes_by_year.index[:-2], themes_by_year.nr_themes[:-2])
# >>> plt.show()

# [5] put sets_by_year and themes_by_year in one chart
# # get a hold of x-axis and create another one
# >>> ax1 = plt.gca()
# >>> ax2 = ax1.twinx()
# # add styling
# >>> ax1.plot(sets_by_year.index[:-2], sets_by_year.set_num[:-2], color='g')
# >>> ax2.plot(themes_by_year.index[:-2], themes_by_year.nr_themes[:-2], 'b')
# # labeling
# >>> ax1.set_xlabel('Year')
# >>> ax1.set_ylabel('Number of Sets', color='green')
# >>> ax2.set_ylabel('Number of Themes', color='blue')

# [6] parts_per_set series by year
# # we group the data by year and then average the number of parts by that year
parts_per_set = sets_data.groupby('year').agg({'num_parts': pd.Series.mean})
# >>> print(parts_per_set.head())
#       num_parts
# year
# 1949  99.600000
# 1950   1.000000
# 1953  13.500000
# 1954  12.357143
# 1955  36.607143

# [6.1] visualize this trend using the scatter plot
# >>> plt.scatter(parts_per_set.index[:-2], parts_per_set.num_parts[:-2])
# >>> plt.show()

# [7] search for and list out sets corresponding to Star Wars theme
# >>> print(themes_data[themes_data.name == 'Star Wars'])
#       id       name  parent_id
# 17    18  Star Wars        1.0
# 150  158  Star Wars        NaN
# 174  209  Star Wars      207.0
# 211  261  Star Wars      258.0

# [7.1] list out the corresponding products (sets)
# >>> print(sets_data[sets_data.theme_id == 18])
# >>> print(sets_data[sets_data.theme_id == 209])
# etc.

# .merge()
# combines two separate dataframes into one
# works on columns with the same name in both dataframes
set_theme_count = sets_data["theme_id"].value_counts()
set_theme_count = pd.DataFrame({'id': set_theme_count.index,
                                'set_count': set_theme_count.values})
# the keys in the provided dictionary ^ become column names
# to use the .merge() we need to provide two data frames and a column name on which to merge
# we chose 'id' for this, as both dataframes have this column
merged_df = pd.merge(set_theme_count, themes_data, on='id')
# >>> print(merged_df[:3])
#     id  set_count       name  parent_id
# 0  158        753  Star Wars        NaN
# 1  501        656       Gear        NaN
# 2  494        398    Friends        NaN

# [8] plot the themes and their number of sets on a bar chart
# >>> plt.bar(merged_df.name[:10], merged_df.set_count[:10])
# >>> plt.show()

# [8.1] format the text on x-axis to make it more readable
plt.figure(figsize=(14, 8))
plt.xticks(fontsize=14, rotation=45)
plt.yticks(fontsize=14)
plt.ylabel('Nr of Sets', fontsize=14)
plt.xlabel('Theme Name', fontsize=14)

plt.bar(merged_df.name[:10], merged_df.set_count[:10])
plt.show()