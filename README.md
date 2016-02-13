# sharapov-bot
bot for this game:
http://teorver.pp.ua/ukr/games/klumba/


#results (1.26s):
http://teorver.pp.ua/ukr/games/klumba/finish.php

best time with DFS: 1.86s 
best time with linear system: 1.26s


#bot's name: 
'Lamzin bot'

#current solution:
use linear system

'''
python
def solve(rows, value):
  for i in range(24):
      if value & (2**i):
          rows[23 - i] |= 2**24
  for i in range(24):
      for j in range(i, 24):
          if rows[j] & (2**i):
              rows[i], rows[j] = rows[j], rows[i]
              break
      for g in range(24):
          if g != i and rows[g] & (2**i):
              rows[g] ^= rows[i]
  result = 0
  for i in range(24):
      if rows[i] & (2**24):
          result |= 2**i
  return result
'''
