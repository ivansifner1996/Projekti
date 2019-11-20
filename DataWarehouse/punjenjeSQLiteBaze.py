import sqlite3
import pandas as pd
import numpy
connection = sqlite3.connect("test.db")


## pandas dataframe
dataframe = pd.read_csv('WA_Retail-SalesMarketing_-ProfitCost Dataset.csv')
#dataframe.head(3)

# KREIRANJE TABLICE GODINA
godina = dataframe['Year'].unique().tolist()
frame_godina = pd.DataFrame({'ID':list(range(1,len(godina)+1)),
								'Year':godina})
frame_godina.to_sql(con = connection,name='Godina' , if_exists='replace' , index=False)

order_m = dataframe['Order method type'].unique().tolist()
frame_order = pd.DataFrame({'ID':list(range(1,len(order_m)+1)),
								'Tip_narudzbe':order_m})
frame_order.to_sql(con = connection,name='Order_method' , if_exists='replace' , index=False)

#KREIRANJE TABLICE PARTNER

df = pd.DataFrame({
                    'Partner': dataframe['Partners'],
                    'Sifra': dataframe['Sifra']
})
id_partnera = dataframe['Partners'].unique()
idPoPartneru = list(range(1,len(id_partnera)+1))
frame_partner = df.groupby(['Partner', 'Sifra']).agg('count').reset_index()
frame_partner['ID'] = idPoPartneru
frame_partner = frame_partner[['ID', 'Partner', 'Sifra']]
frame_partner.to_sql(con = connection,name='Partners' , if_exists='replace' , index=False)

#print(idPoDrzavi)

#KREIRANJE TABLICE DRZAVA
df = pd.DataFrame({
                    'Drzava': dataframe['Retailer country'],
                    'Kontinent': dataframe['Continent']
})
id_drzave = dataframe['Retailer country'].unique()
idPoDrzavi = list(range(1,len(id_drzave)+1))
frame_drzava = df.groupby(['Drzava', 'Kontinent']).agg('count').reset_index()
frame_drzava['ID'] = idPoDrzavi
frame_drzava = frame_drzava[['ID', 'Drzava', 'Kontinent']]
frame_drzava.to_sql(con = connection,name='Drzava' , if_exists='replace' , index=False)

#KREIRANJE TABLICE TIP PROIZVODA
df = pd.DataFrame({
                    'Tip_proizvoda': dataframe['Product type'],
                    'Linija': dataframe['Product line']
})

id_tipa = dataframe['Product type'].unique()
idPoTipu = list(range(1,len(id_tipa)+1))
frame_tip = df.groupby(['Tip_proizvoda', 'Linija']).agg('count').reset_index()
frame_tip['ID'] = idPoTipu
frame_tip = frame_tip[['ID', 'Tip_proizvoda', 'Linija']]
frame_tip.to_sql(con = connection,name='Tip' , if_exists='replace' , index=False)

#KREIRANJE TABLICE PROIZVOD
#POTREBAN STRANI KLJUC OD TABLICE TIP PROIZVODA
novi_frame = df['Tip_proizvoda'].tolist()
tip_podaci = pd.read_sql_query("select * from Tip",connection)
id_tipa = tip_podaci['ID'].tolist()
naziv_tipa= tip_podaci['Tip_proizvoda'].tolist()

dictionary_tip = {}
for i in id_tipa:
	dictionary_tip[id_tipa[i-1]] = naziv_tipa[i-1]
lista_id = []
#print(dictionary_tip)

for a in novi_frame:
    for b,c in dictionary_tip.items():
        if a==c:
            lista_id.append(b)

novi_dataframe2 = dataframe['Product'].unique().tolist()
primarykey = list(range(1,len(novi_dataframe2)+1))
df = pd.DataFrame({
                    'Naziv_proizvoda': dataframe['Product'],
                    'Tip_ID': lista_id#,
                    #'ID' : list(range(1,len(product_primary)+1))

})

#print(len(df))
frame_proizvod = df.groupby(['Naziv_proizvoda', 'Tip_ID']).agg('count').reset_index()
frame_proizvod['ID'] = primarykey
frame_proizvod = frame_proizvod[['ID', 'Naziv_proizvoda', 'Tip_ID']]
#frame_proizvod
frame_proizvod.to_sql(con = connection,name='Product' , if_exists='replace' , index=False)

###STRANI KLJUCEVI ZA TABLICU CINJENICA
#DOHVACANJE POTREBNIH PODATAKA POMOCU KOJIH SE DOBIVAJU STRANI KLJUCEVI
df = pd.DataFrame({
                    'Godina' : dataframe['Year'],
                    'Naziv_proizvoda': dataframe['Product'],
                    'Tip_narudzbe': dataframe['Order method type'],
                    'Drzava' : dataframe['Retailer country'],
                    'Partner' : dataframe['Partners']


})

#FK NARUDZBA
novi_frameNarudzba = df['Tip_narudzbe'].tolist()
narudzba = pd.read_sql_query("select * from Order_method",connection)
narudzba_id = narudzba['ID'].tolist()
narudzba_naziv = narudzba['Tip_narudzbe'].tolist()
narudzba_dictionary = {}
for i in narudzba_id:
	narudzba_dictionary[narudzba_id[i-1]] = narudzba_naziv[i-1]
narudzba_fk = []
for a in novi_frameNarudzba:
    for b, c in narudzba_dictionary.items():
        if a==c:
            narudzba_fk.append(b)
#print(len(narudzba_fk))

#FK GODINA
novi_frameGodina = df['Godina'].tolist()
godina = pd.read_sql_query("select * from Godina",connection)
godina_id = godina['ID'].tolist()
godina_naziv = godina['Year'].tolist()
godina_dictionary = {}
for i in godina_id:
	godina_dictionary[godina_id[i-1]] = godina_naziv[i-1]
godina_fk = []
for a in novi_frameGodina:
    for b, c in godina_dictionary.items():
        if a==c:
            godina_fk.append(b)
#print(len(godina_fk))

#FK PARTNERS
novi_framePartner = df['Partner'].tolist()
partner = pd.read_sql_query("select * from Partners",connection)
partner_id = partner['ID'].tolist()
partner_naziv = partner['Partner'].tolist()
partner_dictionary = {}
for i in partner_id:
	partner_dictionary[partner_id[i-1]] = partner_naziv[i-1]
partner_fk = []
for a in novi_framePartner:
    for b, c in partner_dictionary.items():
        if a==c:
            partner_fk.append(b)
#print(len(partner_fk))

#FK DRZAVA
novi_frameDrzava = df['Drzava'].tolist()
drzava = pd.read_sql_query("select * from Drzava",connection)
drzava_id = drzava['ID'].tolist()
drzava_naziv = drzava['Drzava'].tolist()
drzava_dictionary = {}
for i in drzava_id:
	drzava_dictionary[drzava_id[i-1]] = drzava_naziv[i-1]
drzava_fk = []
for a in novi_frameDrzava:
    for b, c in drzava_dictionary.items():
        if a==c:
            drzava_fk.append(b)
#print(len(drzava_fk))

# FK PROIZVOD
novi_frameProizvod = df['Naziv_proizvoda'].tolist()
proizvod = pd.read_sql_query("select * from Product",connection)
proizvod_id = proizvod['ID'].tolist()
proizvod_naziv = proizvod['Naziv_proizvoda'].tolist()
proizvod_dictionary = {}
for i in proizvod_id:
	proizvod_dictionary[proizvod_id[i-1]] = proizvod_naziv[i-1]
proizvod_fk = []
for a in novi_frameProizvod:
    for b, c in proizvod_dictionary.items():
        if a==c:
            proizvod_fk.append(b)
#print(len(proizvod_fk))

#PUNJENJE PODATAKA U TABLICU CINJENICA

print("1   "+str(len(dataframe['Product'])))
print("2   "+str(len(narudzba_fk)))
print("3   "+str(len(proizvod_fk)))
print("4   "+str(len(drzava_fk)))
print("5   "+str(len(partner_fk)))
print("6   "+str(len(godina_fk)))
print("7   "+str(len(dataframe['Revenue'])))
print("8   "+str(len(dataframe['Planned revenue'])))
print("9   "+str(len(dataframe['Quantity'])))
print("10  "+str(len(dataframe['Gross profit'])))


proizvod = dataframe['Product'].tolist()
racun = pd.DataFrame({  'ID'           :list(range(1,len(proizvod)+1)),
						'Order_method_ID':narudzba_fk,
						'Product_ID' : proizvod_fk,
						'Retailer_country_ID':drzava_fk,
						'Partner_ID' : partner_fk,
						'Godina_ID' : godina_fk,
						'Revenue'     :dataframe['Revenue'],
						'Planned_revenue'  :dataframe['Planned revenue'],
						'Quantity'  : dataframe['Quantity'],
						'Gross_profit'   : dataframe['Gross profit']
                     })
racun.to_sql(con = connection, name='Racun' , if_exists='replace' , index=False)

print("Tablice su uspjesno kreirane!")