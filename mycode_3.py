'''
Designed by : MGSJZLS (wechat / telegram)
Channel 	: youtube.com/c/������������ʦ
�����ȫ���룺����Ƶ������

��ȡ�ڻ� TICKER ������ ʱ�� �� �� ���� �ɽ���
ʶ�� BUY SELL NEUTRAL �����ظ� (��������;֧�ֵı��)
�Զ�������ָţ��֤ �Զ���ţ����С���۸� ���ɽ����Ѻ�д��
ͨ���µ����룬֧��ʵ�̺�ģ�⣨�ڻ���֧��ʵ�̣�
'''

from futu import *

def get_ticker(code):
	quote_ctx.subscribe(code, [SubType.TICKER])
	ret, data1 = quote_ctx.get_rt_ticker(code, 15)
	if(k==1):last_time2=datetime.datetime.now().strftime('%H:%M:%S')
	kf='%.0f' 
# ָ�����ص�С����λ 0��ʾ������С�� 1��ʾ����һλС��
	for i in data1.index:
		if (time_cmp(time.strptime(data1.loc[i].values[1][11:], "%H:%M:%S"), time.strptime(last_time2, "%H:%M:%S")) > 0) and (k>1):
# ʶ������ĸ BUY SELL NEUTRAL : B S N
			if str(data1.loc[i].values[5])[0]=='B':symbol=' + '
			if str(data1.loc[i].values[5])[0]=='S':symbol=' - '
			if str(data1.loc[i].values[5])[0]=='N':symbol=' = '						
			last_time2=data1.loc[i].values[1][11:]
			print(kf%float(data1.loc[i].values[2]),symbol,data1.loc[i].values[3])
			return(kf%float(data1.loc[i].values[2]),symbol,data1.loc[i].values[3])			
		elif k==1:
			if str(data1.loc[i].values[5])[0]=='B':symbol=' + '
			if str(data1.loc[i].values[5])[0]=='S':symbol=' - '
			if str(data1.loc[i].values[5])[0]=='N':symbol=' = '
			print(kf%float(data1.loc[i].values[2]),symbol,data1.loc[i].values[3])
			return(kf%float(data1.loc[i].values[2]),symbol,data1.loc[i].values[3])
		else:		
			return None

def ftw(min1,max1,min2,max2):# �˺����Զ���ţ����С���۸� ���ճɽ�������Ѻ�д��
	req=Request()
	req.sort_field=SortField.TURNOVER
	req.status=WarrantStatus.NORMAL

	req.cur_price_min=float(min1)
	req.cur_price_max=float(max1)
	print(float(min1),float(max1))

	# req.issuer_list = ['BI','HT','HS','CS','UB','BP','SG','VT'] # less BI HS UB 
	req.conversion_min = 10000
	req.conversion_max = 10000

	f=open(r'ftw.csv','w');f.write('');f.close()	
	csvFile = open('ftw.csv','a+', newline='')
	write_ok = csv.writer(csvFile)
###
	req.type_list=['BULL']
	try:
		ret, ls = quote_ctx.get_warrant("HK.800000", req)
		if ret == RET_OK:
			data, last_page, all_count = ls	
		else:
			print('\n �˼۸����� �޷�������ţ��֤���� \n')
			def_txt('ftw try error')
	except:
		req.cur_price_min=0.040
		req.cur_price_max=0.2
		ret , (data, last_page, all_count) = quote_ctx.get_warrant("HK.800000", req)

	if ret!=-1 and len(data)>0:# lambda x:'%.2f' % x
		data['turnover'] =data.apply(lambda x: int(x['turnover'] / 10000), axis=1)
		for i in data[['stock','recovery_price','cur_price','turnover','type','issuer']].iloc[-8:].values:
			write_ok.writerow(i)	
		# print(data[['stock','recovery_price','cur_price','turnover','type','issuer']])
			
	elif ret!=-1 and len(data)==0:	
		req.cur_price_min=0.040
		req.cur_price_max=0.2
		req.type_list=['BULL']
		ret , (data, last_page, all_count) = quote_ctx.get_warrant("HK.800000", req)
		data['turnover'] =data.apply(lambda x: int(x['turnover'] / 10000), axis=1)
		for i in data[['stock','recovery_price','cur_price','turnover','type','issuer']].iloc[-8:].values:
			write_ok.writerow(i)		
	
	req.cur_price_min=float(min2)
	req.cur_price_max=float(max2)
	print(float(min2),float(max2))
		
	req.type_list=['BEAR']
	
	try:
		ret, ls = quote_ctx.get_warrant("HK.800000", req)
		if ret == RET_OK:
			data, last_page, all_count = ls	
		else:
			print(ls)
	except:
		req.cur_price_min=0.040
		req.cur_price_max=0.2
		ret , (data, last_page, all_count) = quote_ctx.get_warrant("HK.800000", req)
	
	if ret!=-1 and len(data)>0:
		data['turnover'] =data.apply(lambda x: int(x['turnover'] / 10000), axis=1)#issuer #conversion_ratio #name #street_rate #issue_size
		for i in data[['stock','recovery_price','cur_price','turnover','type','issuer']].iloc[-8:].values:
			write_ok.writerow(i)
		# print(data[['stock','recovery_price','cur_price','turnover','type','issuer']])	
			
	elif ret!=-1 and len(data)==0:	
		print(data)
		req.cur_price_min=0.040
		req.cur_price_max=0.250
		req.type_list=['BEAR']
		ret , (data, last_page, all_count) = quote_ctx.get_warrant("HK.800000", req)
		data['turnover'] =data.apply(lambda x: int(x['turnover'] / 10000), axis=1)#issuer #conversion_ratio #name #street_rate #issue_size
		for i in data[['stock','recovery_price','cur_price','turnover','type','issuer']].iloc[-8:].values:
			write_ok.writerow(i)
			
def place_(symbol, price, cash, side, volume ,TRD_ENV):# �˺���Ϊͨ���µ�����,TRD_ENV:'REAL' / 'SIMULATE'
	trd_side = TrdSide.SELL if side == 'sell' else TrdSide.BUY			
	ret,data_err=trd_ctx.place_order(price=0, qty=volume, code=symbol, trd_side=trd_side,  order_type=OrderType.MARKET, trd_env=TRD_ENV)
	return(data_err)
	
if __name__ == '__main__':
	quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
	trd_ctx = OpenHKTradeContext(host='127.0.0.1', port=11111,is_encrypt = False, security_firm=SecurityFirm.FUTUSECURITIES)
	read_file = open(r'pwd.txt', 'r');	 # pwd.txt ������λ����;��������
	print('\n',quote_ctx,'\n',trd_ctx)
	pwd_unlock='';selling=0
	if len(pwd_unlock)>1:
		print('\n',trd_ctx.unlock_trade(pwd_unlock),'\n')
	ftw(0.05�� 0.12�� 0.06�� 0.13) # ���ú��� ���� ţ����С���۸� �����Ѻ�д��