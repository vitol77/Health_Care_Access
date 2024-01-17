import pandas as pd

#Adapted from https://stackoverflow.com/questions/45652772/pandas-read-csv-is-shifting-columns
abbotsford = pd.read_csv('data/Abbotsford.csv', index_col=False)
campbell_River = pd.read_csv('data/Campbell River.csv', index_col=False)
chiliwack = pd.read_csv('data/Chilliwack.csv', index_col=False)
kamloops = pd.read_csv('data/Kamloops.csv', index_col=False)
kelowna = pd.read_csv('data/Kelowna.csv', index_col=False)
nanaimo = pd.read_csv('data/Nanaimo.csv', index_col=False)
penticton = pd.read_csv('data/Penticton.csv', index_col=False)
vancouver = pd.read_csv('data/Vancouver.csv', index_col=False)
vernon = pd.read_csv('data/Vernon.csv', index_col=False)
victoria = pd.read_csv('data/Victoria.csv', index_col=False)

ab = abbotsford.loc[45:54]
ab.columns = ab.columns.to_flat_index()
ab = ab.drop([' Year',' Community_area',' Provincial_value'],axis=1)
ab['City'] = 'Abbotsford'

cp = campbell_River.loc[45:54]
cp.columns = cp.columns.to_flat_index()
cp = cp.drop([' Year',' Community_area',' Provincial_value'],axis=1)
cp['City'] = 'Campbell River'

ch = chiliwack.loc[45:54]
ch.columns = ch.columns.to_flat_index()
ch = ch.drop([' Year',' Community_area',' Provincial_value'],axis=1)
ch['City'] = 'Chilliwack'

km = kamloops.loc[45:54]
km.columns = km.columns.to_flat_index()
km = km.drop([' Year',' Community_area',' Provincial_value'],axis=1)
km['City'] = 'Kamloops'

kl = kelowna.loc[45:54]
kl.columns = kl.columns.to_flat_index()
kl = kl.drop([' Year',' Community_area',' Provincial_value'],axis=1)
kl['City'] = 'Kelowna'

nn = nanaimo.loc[45:54]
nn.columns = nn.columns.to_flat_index()
nn = nn.drop([' Year',' Community_area',' Provincial_value'],axis=1)
nn['City'] = 'Nanaimo'

pt = penticton.loc[45:54]
pt.columns = pt.columns.to_flat_index()
pt = pt.drop([' Year',' Community_area',' Provincial_value'],axis=1)
pt['City'] = 'Penticton'

vc =vancouver.loc[45:54]
vc.columns = vc.columns.to_flat_index()
vc = vc.drop([' Year',' Community_area',' Provincial_value'],axis=1)
vc['City'] = 'Vancouver'

vn = vernon.loc[45:54]
vn.columns = vn.columns.to_flat_index()
vn = vn.drop([' Year',' Community_area',' Provincial_value'],axis=1)
vn['City'] = 'Vernon'

vi = victoria.loc[45:54]
vi.columns = vi.columns.to_flat_index()
vi = vi.drop([' Year',' Community_area',' Provincial_value'],axis=1)
vi['City'] = 'Victoria'

data = pd.concat([ab,cp,ch,km,kl,nn,pt,vc,vn,vi])
data.rename(columns = {' Community_value':'Value',}, inplace = True)
data.reset_index(inplace=True)
data = data.drop(['index'],axis=1)

data.to_csv('Counts/city_profiles.csv')