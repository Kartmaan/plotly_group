# plotly_intervals
A function that groups values from a Pandas Series according to given intervals 
and represent them graphically in the form of bar chart or pie chart with Plotly. Serval 
parameters can be adjusted :
- The plot title
- x/y axis labels
- The intervals chosen for the grouping of values (example: [[0,5], [5,10], ...]
- If no interval is defined, default intervals will be generated from the values present in the Pandas Series
- Display a last interval grouping all the values greater than the last given interval
- The plot kind (bar chart or pie chart)
- Grid display
- Choice of bar color for bar chart
- The output (static/non-interactive image, interactive figure, plotly Figure object, bytes, intervals dictionnary)

# Exemples
For this example we will use a dataset on exoplanets and recover in the form of Pandas Series the column relating to the distance of planetary systems from us :

```
dist = df['sy_dist']
```

To start we will simply insert the Series into the function without adding any parameters :

```
plot_group(dist)
```

![dist](https://user-images.githubusercontent.com/11463619/201731901-2a962c4e-8157-406c-8779-5dc4704f636f.png)

**Intervals have been defined automatically** by the function **based on the values present in the Series** and their dispersion (see the comments in the function for more information).

Now let's relaunch the function but adding some parameters and, in particular, **custom intervals**.

```
# Custom intervals
inter = [[0,25], [25,50], [75,100], [100,125], [125,150]]

plot_group(dist,
intervals = inter, 
title='Distance of exoplanets from us', 
x_label='Distance [parsec]',
y_label='Number of exoplanets',
bar_color='#b4522b')
```

![dist_inter](https://user-images.githubusercontent.com/11463619/201731894-64b68c28-929c-4196-9eb0-ac64d143b4ad.png)

The `higher_vals` parameter allows to add a last interval grouping all the values of the Series greater than the last interval provided

```
# Custom intervals
inter = [[0,400], [400,800], [800,1200]]

plot_group(dist,
intervals = inter,
higher_vals=True,
title='Distance of exoplanets from us', 
x_label='Distance [parsec]',
y_label='Number of exoplanets',
bar_color='#b4522b')
```

![dist_high](https://user-images.githubusercontent.com/11463619/201738946-b9657aca-c540-46b7-9cbc-b19d87ffb982.png)

The representation can also be done in the form of a pie chart :

``` 
inter = [[0,400], [400,800], [800,1200]]

plot_group(dist,
kind='pie_hole',
intervals = inter,
higher_vals=True, 
title='Distance of exoplanets from us')
```

![dist_pie](https://user-images.githubusercontent.com/11463619/201741980-02ba18a3-616e-48d6-9082-0db64e9b7f16.png)
