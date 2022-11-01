#! /home/diego/miniconda3/envs/fdd2/bin/python

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import timedelta

purchase_carts = pd.read_csv('purchase_carts.csv', header=None)
col_names= ['cart_id', 'user_id','book_id', 'purchase_date', 'percentile']
purchase_carts = purchase_carts.rename(columns=lambda x: col_names[x])

ids = purchase_carts['user_id'].max()
scale_parameters = []

mean_p_user = []

for id in range(1,ids+1):
	print(id)
	mean_p = purchase_carts.loc[purchase_carts['user_id'] == id, 'percentile'].mean()
	mean_p_user.append(mean_p)
	scale_parameters.append(mean_p*10**(1+mean_p))

delta = []

for i in range(ids):
	delta.append(np.random.exponential(scale=scale_parameters[i], size=(1))[0])

# Sumar a la fecha delta
# Por cada id, sumarle delta a sus fechas
# Agregar una fila con cart_id = 2 y purchase_date = purchase_date(1) + delta

days_between_purchases = []

for id in range(1, ids+1):
	purchase_carts_2 = purchase_carts.loc[purchase_carts['user_id'] == id]
	purchase_carts_2.reset_index(inplace = True, drop = True)
	date = purchase_carts_2.loc[0]['purchase_date']
	purchase_carts_2['cart_id'] = 2
	purchase_carts_2['purchase_date'] = pd.to_datetime(purchase_carts_2['purchase_date'])
	purchase_carts_2['purchase_date'] = purchase_carts_2['purchase_date'] + pd.Timedelta(weeks = delta[id-1])

	date_2 = purchase_carts_2.loc[0]['purchase_date']
	days_between_purchases.append(date_2 -pd.to_datetime(date))
	frames = [purchase_carts, purchase_carts_2]
	purchase_carts = pd.concat(frames, ignore_index=True)

print(mean_p_user)
for i in range(len(days_between_purchases)):
	days_between_purchases[i] = days_between_purchases[i] / timedelta(days=1)
print(days_between_purchases)

result = {"mean percentile":mean_p_user, "days between purchases":days_between_purchases}

plt.scatter(mean_p_user, days_between_purchases)
plt.show()
