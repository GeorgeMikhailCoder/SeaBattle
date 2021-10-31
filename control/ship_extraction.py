def ship_placement_oleg(f):
    field = f
    ship_tuple = []
    for i in range(0, 10):
        for j in range(0, 10):

            if (field[i][j] == 9):
                x, y = i, j

                if (j + 1 < 10) and (field[i][j + 1] == 9):

                    for l in range(0, 5):
                        if (j + l > 9):
                            ship_tuple.append((x, y, 0, l))
                            break

                        if field[i][j + l] == 0:
                            ship_tuple.append((x, y, 0, l))
                            break

                        field[i][j + l] = 0
                    continue


                elif (i + 1 < 10) and (field[i + 1][j] == 9):

                    for l in range(0, 5):
                        if (i + l > 9):
                            ship_tuple.append((x, y, 1, l))
                            break

                        if field[i + l][j] == 0:
                            ship_tuple.append((x, y, 1, l))
                            break

                        field[i + l][j] = 0
                    continue
                
                elif i + 1 > 9 and j + 1 > 9:
                    ship_tuple.append((x, y, 1, 1))
                    continue

                elif i + 1 > 9 and j + 1 < 10 and (field[i][j + 1] == 0):
                    ship_tuple.append((x, y, 1, 1))
                    continue

                elif j + 1 > 9 and (field[i + 1][j] == 0):
                    ship_tuple.append((x, y, 1, 1))
                    continue

                elif (field[i][j + 1] == 0) and (field[i + 1][j] == 0):
                    ship_tuple.append((x, y, 1, 1))
                    continue

        output = sorted(ship_tuple, key=lambda x: x[3], reverse=True)
    return output
