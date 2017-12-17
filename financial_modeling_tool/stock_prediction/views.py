from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.http import HttpResponse
# from nasdaq_stock_quote import Share
import requests
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


from nsetools import Nse

import numpy as np
import matplotlib.pyplot as plt
import quandl

# Create your views here.

def register(request):
	if request.method == 'POST':
		name = request.POST['name']
		email = request.POST['email']
		password1 = request.POST['password1']
		password2 = request.POST['password2']


		
		if password1 != password2:
			return HttpResponse("Enter Password Correctly")
			
		user = User.objects.create(username=email,first_name=name,email=email)
		user.set_password(password1)
		
		
		user.save()
		user = authenticate(username = email, password = password1)
		if user:
			auth_login(request, user)
			return redirect('/main/')
		
	else:

		return render(request,"register.html")




def login(request):
	if request.method == 'POST':
		email = request.POST['email']
		password = request.POST['password']
		user = authenticate(username = email, password = password)
		if user:
			auth_login(request, user)
			return redirect('/main/')
		else:
			return render(request, 'login.html',{'context' : 'Wrong username or password'})

	else:	
		return render(request, 'login.html')
	


def logout(request):
	if request.user.is_authenticated():
		auth_logout(request)
	else:
		return HttpResponse("invalid")
	return render(request,'login.html')
	


def main(request):
	nse = Nse()

	top_gainers = nse.get_top_gainers()
	top_losers = nse.get_top_losers()
	r = requests.get('https://www.quandl.com/api/v3/datasets/NSE/NIFTY_50.json?api_key=oqf4vFLPo8MrPBGXVjki')
	nifty = r.json()

	nifty_price = []
	nifty_date = []

	count = 0
	for i in nifty['dataset']['data']:

		nifty_date.append(i[0])	
		nifty_price.append(i[1])

		if count == 30:
			break
		else:
			count = count + 1

	print(nifty_date)

	w_symbol = []
	l_symbol = []
	w_price = []
	l_price = []
	w_hprice = []
	l_hprice = []
	w_lprice = []
	l_lprice = []
	w_oprice = []
	l_oprice = []

	count = 0
	for i in top_gainers:
		w_symbol.append(i['symbol'])
		w_price.append(i['ltp'])
		w_hprice.append(i['highPrice'])
		w_lprice.append(i['lowPrice'])
		w_oprice.append(i['openPrice'])

		if count == 2:
			break
		else:
			count = count + 1


	count = 0
	for i in top_losers:
		l_symbol.append(i['symbol'])
		l_price.append(i['ltp'])
		l_hprice.append(i['highPrice'])
		l_lprice.append(i['lowPrice'])
		l_oprice.append(i['openPrice'])

		if count == 2:
			break
		else:
			count = count + 1

	
	loop1 = zip(w_symbol,w_price,w_hprice,w_lprice,w_oprice)
	loop2 = zip(l_symbol,l_price,l_hprice,l_lprice,l_oprice)

	nifty_date = json.dumps(nifty_date)

	return render(request,'mainpage.html',{'loop1':loop1,'loop2':loop2,
	 'nifty_price' : nifty_price, 'nifty_date' : nifty_date})


def classes(request):
	nse = Nse()
	a = ['ABB','DMART','BHEL','TITAN','TATAPOWER','INDIGO','IDEA','MRF','PNB','GODREJCP','LICHSGFIN','JSWSTEEL']
	price = []
	hprice = []
	lprice = []
	oprice = []
	for i in a:
		 q = nse.get_quote(i)
		 price.append(q['averagePrice'])
		 hprice.append(q['dayHigh'])
		 lprice.append(q['dayLow'])
		 oprice.append(q['closePrice'])
	loop = zip(a,price,hprice,lprice,oprice)



	return render(request,'classes.html',{'loop' : loop})


def compare(request):
	return render(request,'compare.html')



def add_stock(request):
	a = json.loads(request.body.decode('utf-8'))
	print (a)

	r = requests.get('https://www.quandl.com/api/v3/datasets/NSE/'+a['stock']+'.json?api_key=oqf4vFLPo8MrPBGXVjki')
	nifty = r.json()

	data = nifty



	nifty_price = []
	nifty_date = []

	count = 0
	for i in nifty['dataset']['data']:

		nifty_date.append(i[0])	
		nifty_price.append(i[1])

		if count == 60:
			break
		else:
			count = count + 1

	pnifty_price = []
	pnifty_date = []

	for i in range(0,29):
		pnifty_date.append(i)
		pnifty_price.append(i)



	abb_array = [1355.8834848465374, 1354.5892688674323, 1353.7087382541565, 1352.9763558146951, 1352.3422224580943, 1351.7539502329214, 1351.2018370264116, 1350.6787580182136, 1350.1820561538075, 1349.7100113844156, 1349.2612594225318, 1348.8345942337073, 1348.4288959033336, 1348.0431109040169, 1347.6762426915313, 1347.327346990468, 1346.9955284249875, 1346.679937695855, 1346.3797690333365, 1346.0942578324789, 1345.8226784374144, 1345.564342057871, 1345.3185948071753, 1345.0848158532385, 1344.8624156750741, 1344.6508344180816, 1344.4495403418657, 1344.2580283548161, 1344.0758186300861, 1343.9024552979886]
	dmart_array = [1121.2839809848156, 1124.4547241900875, 1126.1274456508345, 1127.1064015776828, 1127.6515523500875, 1127.9535724474053, 1128.1227670509727, 1128.217696584536, 1128.270853804346, 1128.3006160855575, 1128.3172815044923, 1128.3266126147798, 1128.3318370142686, 1128.3347621075745, 1128.3363998223876, 1128.3373167478499, 1128.3378301161219, 1128.3381175405227, 1128.3382784634045, 1128.3383685607091, 1128.3384190042643, 1128.3384472465298, 1128.3384630587673, 1128.3384719116989, 1128.3384768682649, 1128.3384796433397, 1128.3384811970441, 1128.3384820669298, 1128.3384825539601, 1128.338482826638]
	bhel_array = [89.788076317834239, 89.595715529478611, 89.486279374403409, 89.411292156188566, 89.347722080867982, 89.288510155991091, 89.231123548654111, 89.174692637172399, 89.118912214211605, 89.06367386541018, 89.008937242131282, 88.954685618415382, 88.900910475395932, 88.847606161886631, 88.794768043982188, 88.7423918637528, 88.690473516835965, 88.639008975170853, 88.587994260022398, 88.537425432431746, 88.487298589706171, 88.437609864003349, 88.388355421643297, 88.339531462674017, 88.291134220526928, 88.243159961705175, 88.19560498548509, 88.148465623623906, 88.101738240071384, 88.055419230684464]
	titan_array = [823.00892353391112, 826.45145499959199, 829.98756693332507, 833.50099113789224, 836.94663099371849, 840.32586157301466, 843.63925800214349, 846.88800123082763, 850.07254219995275, 853.19331063020638, 856.25073046140039, 859.24527100694331, 862.17743936031593, 865.04777935719255, 867.85686852819435, 870.60531612392947, 873.29376109230054, 875.92287014198132, 878.49333581515702, 881.00587458929772, 883.4612250088702, 885.86014585263831, 888.20341434001125, 890.4918243798287, 892.72618486448664, 894.90731801198217, 897.03605775810752, 899.11324820069808, 901.13974209751598, 903.11639941905378]
	tata_power_array = [90.36239487291175, 90.210484646009732, 90.060323511648775, 89.909804614688014, 89.759994486783171, 89.610745882651671, 89.462083554679268, 89.313999614396366, 89.166491767550156, 89.019556759507708, 88.873191532807013, 88.727393024522996, 88.582158201497762, 88.437484053853638, 88.293367595819873, 88.149805865281479, 88.006795923556325, 87.864334855136065, 87.722419767437529, 87.581047790556113, 87.440216077022683, 87.299921801563613, 87.160162160864061, 87.020934373334427, 86.882235678879681, 86.744063338671893, 86.606414634925642, 86.469286870676399, 86.332677369561807, 86.196583475605735]
	indigo_array = [1159.1023370642317, 1162.2490092006969, 1165.0947205131913, 1167.102045231574, 1168.2969936286336, 1168.9510230054289, 1169.280232450071, 1169.4307149462193, 1169.4912690206352, 1169.5106067531033, 1169.513306825708, 1169.5106541694113, 1169.5072206218338, 1169.5044870214799, 1169.5026786019819, 1169.5016108480838, 1169.5010345247806, 1169.5007489624381, 1169.5006206246451, 1169.5005703368963, 1169.5005552091029, 1169.5005539094777, 1169.5005568060333, 1169.5005600966915, 1169.5005626178822, 1169.5005642513133, 1169.500565201241, 1169.5005657071295, 1169.5005659542653, 1169.5005660633526]
	idea_array = [94.857853672966087, 94.722002389183785, 94.603779607068503, 94.498128524867866, 94.401012896049053, 94.311921928247102, 94.230202828005361, 94.155212545997244, 94.086373086051381, 94.023160394336031, 93.965098045985854, 93.911752479376133, 93.862728771251597, 93.81766686705754, 93.776238227256357, 93.738142837769402, 93.703106538546635, 93.670878631401735, 93.641229733720053, 93.613949849213384, 93.588846630768415, 93.565743813722378, 93.544479800697218, 93.524906381511926, 93.506887573739562, 93.490298571233268, 93.475024789461258, 93.460960997799461, 93.448010530066298, 93.436084565569871]
	mrf_array = [67574.173724957829, 67823.843647533431, 67898.501810789196, 67924.118713450545, 67933.288775434747, 67936.756932513803, 67938.091538662266, 67938.601200421617, 67938.797178113848, 67938.872472957955, 67938.901369936022, 67938.912473916265, 67938.916738462518, 67938.918376309477, 67938.919005448377, 67938.919247085592, 67938.919339896689, 67938.919375545098, 67938.919389237228, 67938.919394496275, 67938.919396516241, 67938.919397292091, 67938.919397590085, 67938.919397704536, 67938.919397748512, 67938.919397765392, 67938.919397771882, 67938.919397774371, 67938.919397775331, 67938.919397775695]
	godrej_array = [999.91493661196262, 993.0093345318196, 987.47494730573555, 983.01871272953713, 979.41583633246785, 976.49400844753359, 974.11943960917347, 972.1863404699269, 970.61046339798008, 969.32435651011031, 968.27377969175245, 967.41496121716045, 966.71247407041687, 966.13757637200172, 965.66690405435565, 965.2814340249173, 964.96565715368058, 964.70691546429418, 964.49486880121594, 964.32106425073005, 964.1785875566502, 964.0617802689145, 963.96600979384789, 963.88748215851126, 963.82308935736705, 963.7702847610343, 963.72698133908273, 963.6914684591793, 963.66234383154176, 963.63845781449936]
	lic_array = [549.41603893093998, 550.76644088256876, 552.1351547644482, 553.42622023655883, 554.61309850498401, 555.69395523124524, 556.67557517938189, 557.56587654447833, 558.3727543783898, 559.10363556072218, 559.76538271743948, 560.36429941021697, 560.90615956763122, 561.39624221891154, 561.83936692202531, 562.23992827740892, 562.60192897070419, 562.92901111324613, 563.22448577152647, 563.49136064247057, 563.73236587467579, 563.94997806670779, 564.14644249611115, 564.32379364892529, 564.48387413055082, 564.62835204581074, 564.75873693987774, 564.87639439307225, 564.98255936197017, 565.07834835728033]
	jsw_array = [241.73929726697261, 239.25095248796839, 236.87246473055626, 234.57181243263975, 232.34570862096655, 230.19256166935716, 228.10959220706425, 226.09432857608641, 224.14437318708423, 222.25743607349293, 220.43132237763416, 218.66392810263639, 216.95323494315139, 215.2973057080886, 213.69428003967863, 212.14237044331497, 210.63985859376527, 209.18509189483819, 207.77648027051708, 206.41249316796632, 205.09165675469066, 203.81255129383973, 202.57380868317864, 201.37411014461071, 200.21218405236425, 199.08680388905353, 197.99678631981112, 196.94098937557578, 195.91831073741918, 194.92768611451311]
	pnb = [168.54855630021598, 168.02027994513173, 167.71008715306192, 167.40371650578686, 167.10259057025939, 166.80423163491696, 166.5086562394074, 166.21579656506498, 165.92561506028744, 165.6380734865923, 165.35313470224486, 165.07076226561099, 164.7909204438007, 164.51357419059661, 164.2386891299777, 163.96623153970893, 163.69616833548022, 163.42846705550687, 163.16309584558229, 162.90002344456644, 162.63921917029563, 162.38065290589867, 162.12429508650564, 161.87011668633693, 161.61808920615829, 161.36818466109122, 161.12037556876555, 160.87463493780402, 160.63093625662719, 160.38925348256817]

	sequence_len = 30
	n_hidden_layers = 10
	learning_rate = 0.1
	n_epochs = 20
	f1 = 'relu'
	f2 = 'tanh'
	no_of_pred = 30


	time_steps = []
	data_book = []


	temp=(data['dataset']['data'])
	# print(temp)
	c=0
	for i in temp:
	    time_steps.append(c)
	    data_book=[i[1]]+data_book
	    c=c+1
	# print (data_book)


	mini = min(data_book)
	maxi = max(data_book)
	for i in range(len(data_book)):
	    data_book[i] = (data_book[i] - mini) / (maxi - mini)
	features = []
	labels = []

	for i in range(len(data_book) - sequence_len):
	    features.append(data_book[i:i + sequence_len])
	    labels.append(data_book[i+1:i + sequence_len + 1])


	n_input_layers = 1
	n_output_layers = 1


	activation_f = {
	    'identity': lambda f_x: f_x,
	    'sigmoid': lambda f_x: 1.0 / (1.0 + np.exp(-f_x)),
	    'tanh': lambda f_x: np.tanh(f_x),
	    'arctan': lambda f_x: np.arctan(f_x),
	    'relu': lambda f_x: f_x * (f_x > 0),
	    'softplus': lambda f_x: np.log(1 + np.exp(f_x)),
	    'sinusoid': lambda f_x: np.sin(f_x),
	    'gaussian': lambda f_x: np.exp(-f_x * f_x)
	}
	activation_f_prime = {
	    'identity': lambda f_dx: 1,
	    'sigmoid': lambda f_dx: f_dx * (1.0 - f_dx),
	    'tanh': lambda f_dx: 1.0 - f_dx**2,
	    'arctan': lambda f_dx: 1.0 / (1.0 + np.tan(f_dx)**2),
	    'relu': lambda f_dx: 1.0 * (f_dx > 0),
	    'softplus': lambda f_dx: 1.0 - np.exp(-f_dx),
	    'sinusoid': lambda f_dx: np.cos(np.arcsin(f_dx)),
	    'gaussian': lambda f_dx: -2 * f_dx * np.sqrt(-np.log(f_dx))
	}


	act_f1 = activation_f[f1]
	act_f2 = activation_f[f2]

	act_f1_prime = activation_f_prime[f1]
	act_f2_prime = activation_f_prime[f2]


	V = np.random.normal(scale=0.1, size=(n_input_layers, n_hidden_layers))
	W = np.random.normal(scale=0.1, size=(n_hidden_layers, n_output_layers))
	R = np.random.normal(scale=0.1, size=(n_hidden_layers, n_hidden_layers))


	# print("############## TRAIN ##############")

	# Training-set
	X = features
	Y = labels

	# Epoch-training
	for e in range(n_epochs):

	    E = 0

	    for i in range(len(X)):

	        err = 0

	        V_update = np.zeros_like(V)
	        W_update = np.zeros_like(W)
	        R_update = np.zeros_like(R)

	        h_layers = [np.zeros((1, n_hidden_layers))]

	        dels = []

	        # Forward Pass
	        for j in range(sequence_len):

	            # Forward Prop
	            x = np.array(X[i][j])
	            y = np.array(Y[i][j])

	            h_inter = np.dot(x, V) + np.dot(h_layers[-1], R)
	            h_final = act_f1(h_inter)
	            o_inter = np.dot(h_final, W)
	            o_final = act_f2(o_inter)

	            # Store hidden layer
	            h_layers.append(h_final)

	            err += (0.5 * np.square(y - o_final))[0][0]

	            # Backward Prop
	            del_h_o = -np.multiply(y - o_final, act_f2_prime(o_final))

	            # Store delta
	            dels.append(del_h_o)

	            change_h_o = np.dot(h_final.T, del_h_o)
	            W_update += change_h_o

	        next_del = np.zeros(n_hidden_layers)

	        # Backward Propagation through time
	        for j in range(sequence_len):
	            x = np.array(X[i][-j - 1])

	            del_h = (np.dot(next_del, R.T) + np.dot(dels[-j - 1], W.T)
	                     ) * act_f1_prime(h_layers[-j - 1])

	            change_h_h = np.dot(h_layers[-j - 2].T, del_h)
	            change_i_h = np.dot(x.T, del_h)

	            R_update += change_h_h
	            V_update += change_i_h

	            next_del = del_h

	        E += err / sequence_len

	        # Adjust Weights
	        V -= V_update * learning_rate
	        W -= W_update * learning_rate
	        R -= R_update * learning_rate

	    print("Epoch: %d Error: %f" % (e, E / len(X)))


	# print("############## TEST ##############")

	# Test-set
	inp = features
	test_result = []

	# Start Test
	for i in range(len(inp)):

	    c = []

	    h_layer = np.zeros((1, n_hidden_layers))

	    for j in range(sequence_len):
	        x = np.array(inp[i][j])

	        # Forward prop
	        h_inter = np.dot(x, V) + np.dot(h_layer, R)
	        h_final = act_f1(h_inter)
	        o_inter = np.dot(h_final, W)
	        o_final = act_f2(o_inter)

	        h_layer = h_final

	        c.append(o_final)

	    test_result.append(c[-1][0][0])

	# ax1 = plt.subplot(211)
	# plt.plot(time_steps, data_book)
	# plt.ylim(0.0, 1.0)
	# ax1.set_title("True")
	# ax2 = plt.subplot(212, sharex=ax1)
	# plt.plot(time_steps[-len(test_result):], test_result)
	# plt.ylim(0.0, 1.0)
	# ax2.set_title("Predicted")
	# plt.show()

	# print (test_result)

	print("############## PREDICT ##############")

	# Predict inp
	inp = list(features[-1])
	last_date = time_steps[-1]
	to_be_passed=[]
	abb_array = []
	# Start prediction
	for i in range(no_of_pred):

	    c = []

	    h_layer = np.zeros((1, n_hidden_layers))

	    for j in range(sequence_len):
	        x = np.array(inp[j])

	        # Forward prop
	        h_inter = np.dot(x, V) + np.dot(h_layer, R)
	        h_final = act_f1(h_inter)
	        o_inter = np.dot(h_final, W)
	        o_final = act_f2(o_inter)

	        h_layer = h_final

	        c.append(o_final)

	    inp.append(c[-1][0][0])
	    del inp[0]
	    last_date = last_date + 1
	    predict_op = c[-1][0][0] * (maxi - mini) + mini
	    to_be_passed.append(predict_op)
	    
	    print("Day %d - Percentage Booking = %f" % (last_date, predict_op))

	print (to_be_passed)

	json_data = {
		'nifty_price' : nifty_price,
		'nifty_date' : nifty_date,
		'pnifty_price' : pnifty_price,
		'pnifty_date' : pnifty_date
	}


	return JsonResponse({'data':json_data})


def news(request):
	description=[]
	title=[]
	url=[]
	urltoimg=[]
	news = requests.get('https://newsapi.org/v1/articles?source=cnbc&sortBy=top&apiKey=e469736fcf9c4b22bf6c50657ea1e9a8')
	news = news.json()
	articles = news['articles']
	# print articles

	return render(request,"news.html",{'articles' : articles})


def detail(request,p):
	
	r = requests.get('https://www.quandl.com/api/v3/datasets/NSE/'+p+'.json?api_key=oqf4vFLPo8MrPBGXVjki')
	nifty = r.json()


	nifty_price = []
	nifty_date = []

	count = 0
	# print nifty
	for i in nifty['dataset']['data']:

		nifty_date.append(i[0])	
		nifty_price.append(i[1])

		if count == 30:
			break
		else:
			count = count + 1

	nifty_date = json.dumps(nifty_date)
	# print nifty_date
	# print nifty_price

	return render(request,"detail.html",{'nifty_date' : nifty_date , 'nifty_price' : nifty_price, 'p' : p})



	




@csrf_exempt
def respond_chat(request):
	if request.method == 'POST':
		a = json.loads((request.body.decode("utf-8")))
		print (a)

		b = (a["result"]["parameters"]["date"])
		sym = (a["result"]["parameters"]["Stock_Names"])

		print (b,sym)



		r = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+sym+'&apikey=M6MXYK4KU4IGKTNX')
		r = r.json()
		print (r)

		ans = r['Time Series (Daily)'][b]['4. close']

		print (ans)

		finalstring = "The price of " + sym + " is " + ans
		print(finalstring)
		return JsonResponse({	
		      "speech": finalstring,
		      "messages": [
		        {
		          "type": 0,
		          "speech": finalstring
		        }]})



# abb = [1355.8834848465374, 1354.5892688674323, 1353.7087382541565, 1352.9763558146951, 1352.3422224580943, 1351.7539502329214, 1351.2018370264116, 1350.6787580182136, 1350.1820561538075, 1349.7100113844156, 1349.2612594225318, 1348.8345942337073, 1348.4288959033336, 1348.0431109040169, 1347.6762426915313, 1347.327346990468, 1346.9955284249875, 1346.679937695855, 1346.3797690333365, 1346.0942578324789, 1345.8226784374144, 1345.564342057871, 1345.3185948071753, 1345.0848158532385, 1344.8624156750741, 1344.6508344180816, 1344.4495403418657, 1344.2580283548161, 1344.0758186300861, 1343.9024552979886]