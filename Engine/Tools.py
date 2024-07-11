def split_list(lst, n):
    total = len(lst)

    full_groups = total // n

    remainder = total % n
    result = []

    for i in range(full_groups):
        group = lst[i  *  n : (i + 1)  *  n]
        result.append(group)

    if remainder:
        result.append(lst[-remainder:])

    return result

def SortPolygonsByZ(polygons):
  sorted_polygons = sorted(polygons, key=lambda polygon: sum(polygon[i][2] for i in range(2)), reverse=True)
  return sorted_polygons