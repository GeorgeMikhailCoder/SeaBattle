import random

def создание_своего_поля() -> list:
  """
  documentation:
    Функция создаёт массив, заполненный нулевыми эллементами, размерами 10х10
    В качестве аргументов ничего не передаётся
    Функция возвращает список со вложенным списком
  """
  a = [[0] * 10 for i0 in range(10)]
  return a

def выбор_расстановки_кораблей() -> int:
  """
  documentation:
    Функция выбирает рандомом способ расстановки кораблей
    В качестве аргументов ничего не передаётся
    Функция возвращает номер расстановки кораблей
  """
  numbers = [11, 12, 13, 14, 15, 16, 21, 22, 23, 24, 25, 26, 31, 32, 33, 34, 35, 36]
  random.shuffle(numbers)
  a = random.choice(numbers)
  #print(a)
  return a

def поворот_расстановки(a: int, b: list) -> list:
  """
  documentation:
    Функция получает значение типа поворота\отражения расстановки кораблей
      В качестве аргументов передаются значения
      :param a: номер операции поворота
      :param b: массив расстановки кораблей
    Функция возвращает массив с переставленными кораблями
  """
  d = создание_своего_поля()
  if a == 1:
      for i in range(0, 10):
          for j in range(0, 10):
              d[j][9-i] = b[i][j]
      return d
  elif a == 2:
    for i in range(0, 10):
        for j in range(0, 10):
            d[9 - i][9 - j] = b[i][j]
    return d
  elif a == 3:
      for i in range(0, 10):
          for j in range(0, 10):
              d[9 - j][i] = b[i][j]
      return d
  elif a == 4:
      return b
  elif a == 5:
      for i in range(0, 10):
          for j in range(0, 10):
              d[i][9 - j] = b[i][j]
      return d
  elif a == 6:
      for i in range(0, 10):
          for j in range(0, 10):
              d[9 - i][j] = b[i][j]
      return d

def создание_одного_однопалубного_корабля(a: list) -> list:
  """
  documentation:
    Функция расставляет однопалубные корабли
      В качестве аргументов передаются значения
      :param a: поле с расставленными многопалубными кораблями и с заставленными 8 граничными клетками
    Функция возвращает массив с + 1 однопалубным кораблём
  """
  n = []
  for i in range(0, 10):
      for j in range(0, 10):
         if a[i][j] == 0:
             n.append([i, j])
  # print(n)
  random.shuffle(n)
  b = random.choice(n)
  # print('b = ', b)
  n2 = b[0]
  n3 = b[1]
  # print('i = ', n3, ' j = ', n2)
  if n2 - 1 < 0:
    n4 = 0
  else:
    n4 = n2 - 1
  if n2 + 1 > 9:
    n5 = 9
  else:
    n5 = n2 + 1
  if n3 - 1 < 0:
    n6 = 0
  else:
    n6 = n3 - 1
  if n3 + 1 > 9:
    n7 = 9
  else:
    n7 = n3 + 1
  for i_n in range(n4, n5+1):
      for j_n in range(n6, n7+1):
          a[i_n][j_n] = 8
  a[n2][n3] = 9
  return a

def расстановка_однопалубных_кораблей(a: list) -> list:
  """
  documentation:
    Функция расставляет однопалубные корабли
      В качестве аргументов передаются значения
      :param a: поле с расставленными многопалубными кораблями и с заставленными 8 граничными клетками
    Функция возвращает массив со всеми кораблями
  """
  for k in range(1,5):
      a = создание_одного_однопалубного_корабля(a)

  #print(a)

  for i in range(0, 10):
    for j in range(0, 10):
      if a[i][j] == 8:
        a[i][j] = 0
  return a

def main () -> list:
    """
    documentation:
      Функция создаёт массив, с расставленными кораблями, размерами 10х10
      В качестве аргументов ничего не передаётся
      Функция возвращает список со вложенным списком где стоит наш карабль - 9, где ничего нет - 0
    """
    поле = создание_своего_поля()
    вариант_расстановки = выбор_расстановки_кораблей()

    if вариант_расстановки > 30:
        for i in range(0, 10):
            поле[0][i] = 9
            поле[9][i] = 9
            поле[1][i] = 8
            поле[8][i] = 8
        поле[0][4] = 8
        поле[0][7] = 8
        поле[9][3] = 8
        поле[9][6] = 8
        конечное_поле = поворот_расстановки(вариант_расстановки - 30, поле)
    elif вариант_расстановки > 20:
        for i in range(0, 10):
            поле[0][i] = 9
            поле[2][i] = 9
            поле[1][i] = 8
            поле[3][i] = 8
        поле[0][4] = 8
        поле[0][7] = 8
        поле[2][3] = 8
        поле[2][7] = 8
        конечное_поле = поворот_расстановки(вариант_расстановки - 20, поле)
    elif вариант_расстановки > 10:
        for i in range(0, 10):
            поле[0][i] = 9
            поле[i][0] = 9
            поле[1][i] = 8
            поле[i][1] = 8
        поле[0][4] = 8
        поле[0][8] = 8
        поле[1][0] = 8
        поле[5][0] = 8
        поле[8][0] = 8
        поле[2][8] = 8
        поле[2][9] = 8
        поле[9][2] = 8
        поле[8][2] = 8
        поле[9][1] = 9
        поле[1][9] = 9
        конечное_поле = поворот_расстановки(вариант_расстановки - 10, поле)

    готовое_поле = расстановка_однопалубных_кораблей(конечное_поле)
    количество_корабельных_клеток = 0
    for i in range(0, 10):
        for j in range(0, 10):
            if готовое_поле[i][j]:
                количество_корабельных_клеток += 1
    if количество_корабельных_клеток < 20:
        print("Ошибка! Ошибка! Жульё! Нехватает кораблей!")
        exit(-1)
    #print("-------------------")
    return готовое_поле