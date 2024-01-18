import pickle as pk
import pandas as pd
from urllib.parse import urlparse
from app import myfunction as mf

url_lenght = mf.allFunction.calculate_url_length
url_calc_www = mf.allFunction.calculate_www
url_calc_com = mf.allFunction.calculate_com
url_host_lenght = mf.allFunction.calculate_hostname_length
url_calc_ratio = mf.allFunction.calculate_ratio_digits 

# floadDt = pd.read_excel('phishing_dtNew.xlsx')
# # print(floadDt.head())

# '''Random Forest Classification'''
# dt_x = floadDt.loc[:, ['nb_www','nb_com','length_url','length_hostname','ratio_digits_url','ratio_digits_host']]
# dt_y = floadDt.status

# total_hit_model = 0
# for i in range(5):
#   hit_model = mf.allFunction.clf_rf_class(dt_x, dt_y, 0.1, i)
#   total_hit_model += hit_model[0]
#   print(hit_model)

# rat_model = total_hit_model / 5
# print('Nilai Rataan Model:', rat_model)

# with open('m00_rf_mean_acc87p.pkl','wb') as model:
#   pk.dump(hit_model, model)

# with open('m00_rf_mean_acc87p.pkl', 'rb') as model:
#     load_model = pk.load(model)

url_input = 'https://iplogger.com/teslink'
f1 = [url_calc_www(url_input)]
f2 = [url_calc_com(url_input)]
f3 = [url_lenght(url_input)]
f4 = [url_host_lenght(url_input)]
f5 = [url_calc_ratio(url_input)]
f6 = [url_calc_ratio(urlparse(url_input).netloc)]

lm = load_model[2]
ndt = pd.DataFrame({'Feature 1':f1, 'Feature 2':f2, 'Feature 3':f3,
                        'Feature 4':f4, 'Feature 5':f5, 'Feature 6':f6})

pred_rf = lm.predict(ndt)
print(pred_rf)