def koch_snowflake(level):
    points_x = [0,1,1/2,0]
    points_y = [0,0,(math.sqrt(3)/2),0]
    for i in range(1,level+1):
        x = []
        L = abs((points_x[0] - points_x[1]))
        l = math.sqrt(((L / 3) * (L / 3) - ((L / 6) * (L / 6))))
        for n in range(len(points_x)-1):
            p = [points_x[n],points_y[n]]
            x.append(p)
            p = [points_x[n]+(points_x[(n + 1)%(len(points_x))]-points_x[n])/3,points_y[n]+(points_y[(n + 1)%(len(points_x))]-points_y[n])/3]
            x.append(p)
            p = [points_x[n]+(points_x[(n + 1)%(len(points_x))]-points_x[n])/2 + (points_y[(n + 1)%(len(points_x))]-points_y[n]) * (l/L) ,points_y[n]+(points_y[(n + 1)%(len(points_x))]-points_y[n])/2 - (points_x[(n + 1)%(len(points_x))]-points_x[n])* (l/L)]
            x.append(p)
            p = [points_x[n] + (2*(points_x[(n + 1)%(len(points_x))] - (points_x[n])) / 3), points_y[n] + 2*(points_y[(n + 1)%(len(points_y))] - points_y[n]) / 3]
            x.append(p)
            p = [points_x[(n + 1)%(len(points_x))],points_y[(n + 1)%(len(points_x))]]
            x.append(p)

        points_x = []
        points_y = []
        for m in range(len(x)):
            points_x.append(x[m][0])
            points_y.append(x[m][1])
    return points_x, points_y
