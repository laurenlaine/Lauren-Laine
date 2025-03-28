---
title: "Count of Short Term Hospitals in Texas by Zip Code"
author: "Lauren Laine"
format: html
---

```{python}
#import libraries
import pandas as pd
import altair as alt
import shapely
from shapely import Polygon, Point
import matplotlib.pyplot as plt
```

```{python}
pos2016=pd.read_csv(r"C:\Users\laine\OneDrive\Documents\GitHub\problem-set-4-lauren-and-me\pos2016.csv")
```

```{python}
short_term_hos_2016=pos2016[pos2016['PRVDR_CTGRY_CD']==1]
short_term_hos_2016=short_term_hos_2016[short_term_hos_2016['PRVDR_CTGRY_SBTYP_CD']==1]
```
```{python}
import geopandas as gpd
census_data=gpd.read_file(r"C:\Users\laine\OneDrive\Documents\GitHub\problem-set-4-lauren-and-me\gz_2010_us_860_00_500k.shp")
```

```{python}
census_data.head()
prefixes=('75', '76', '77', '78', '79')
census_data['texas']=census_data['ZCTA5'].map(lambda x: 1 if any(str(x).startswith(prefix) for prefix in prefixes)else 0)
texas_data=census_data[census_data['texas']==1]
```

```{python}
geometry=texas_data[['ZCTA5', 'geometry']]
geometry.dtypes
geometry=geometry.dropna()
geometry['ZCTA5']=pd.to_numeric(geometry['ZCTA5'])
geometry.dtypes
```

```{python}
counts=short_term_hos_2016['ZIP_CD'].value_counts()
counts=counts.reset_index()
counts['ZIP_CD']=counts['ZIP_CD'].map(int)
counts.dtypes
```


```{python}
#merge
merge=geometry.merge(counts, left_on='ZCTA5', right_on='ZIP_CD', how='left')
merge=merge.fillna(0)
merge=gpd.GeoDataFrame(merge, geometry='geometry')
```

```{python}
plot=merge.plot(column='count', legend=True).set_axis_off()
plot
```

