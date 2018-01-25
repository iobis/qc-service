import pyxylookup as xy

# def outliers(req):
#     if req.method == "POST":

# xy.lookup(points, shoredistance=True, )



# Flow
# Spatial outliers
# - get centroid
# Environmental outliers


"""

API endpoints:
- identify outliers
- calculate qc_stats based on a set of points




Spatial outliers:
- calculate centroid
- get distance to centroid
- detect outliers



* What with high sampling bias??? => Tracking data, ...



Faster shoredistance:
- identify hotspot points:
    - points that are very often the nearest shore point
    - store these in a separate datastructure
"""