import pandas as pd
df=pd.read_excel(r'C:\Users\Shahadat Shuchon\Documents\New folder\data_Luzrene-gps\11.4.22\luzerne_data_100422.xlsx', sheet_name='Farm_ID')
df1=df[["Nom de l'entité ferme",'ID unique producteur CC+','Advisor','Nom du producteur']]
df4=df[['ID unique producteur CC+','Advisor']]
df4=df4.groupby(['ID unique producteur CC+'])['Advisor'].size().reset_index(name='Number of field')
df_thinned = pd.merge(df4,df1.drop_duplicates(),on='ID unique producteur CC+', how='left')
df_thinned = df_thinned[df_thinned['ID unique producteur CC+'] != 'nan']
df_thinned=df_thinned.rename(columns={'ID unique producteur CC+':'Farm_JIRA',"Nom de l'entité ferme":'Farm_Name','Nom du producteur':'Producer'})
### soil_analysis_count ###
# # Analysis results
soil = pd.read_excel(r'C:\Users\Shahadat Shuchon\Documents\New folder\data_Luzrene-gps\11.4.22\luzerne_data_100422.xlsx', sheet_name='Soil_analysis_100422')
soil = soil[['No ferme','Code QR','pH eau (1:1)*']]
ph = soil.dropna(subset=['pH eau (1:1)*'])
ph = ph.drop_duplicates(subset=['Code QR'])
ph_count=ph.groupby(['No ferme'],dropna=True)['pH eau (1:1)*'].nunique().reset_index()
ph_count=ph_count.rename(columns={"No ferme": "Farm_JIRA","pH eau (1:1)*": "Analysis results"})
m1=pd.merge(df_thinned,ph_count, on="Farm_JIRA", how='left')
# # gps data
gps= pd.read_excel(r'C:\Users\Shahadat Shuchon\Documents\New folder\data_Luzrene-gps\11.4.22\luzerne_data_100422.xlsx', sheet_name='luzerne_GPS_advisor')
gps = gps[['No ferme','Code_QR']]
gps_count=gps.groupby(['No ferme'],dropna=True)['Code_QR'].nunique().reset_index()
gps_count=gps_count.rename(columns={"No ferme": "Farm_JIRA","Code_QR": "GPS data"})
m2=pd.merge(m1,gps_count, on="Farm_JIRA", how='left')
### Stem_count ###
stem = pd.read_excel(r'C:\Users\Shahadat Shuchon\Documents\New folder\data_Luzrene-gps\11.4.22\luzerne_data_100422.xlsx', sheet_name='Stem_count_100422')
stem = stem[['Farm_JIRA','Season']]
# # spring
spring=stem.loc[stem['Season'] == "Spring'21"]
spring=spring.groupby(['Farm_JIRA'])['Season'].size().reset_index(name='Spring')
spring = spring[spring['Farm_JIRA'] != 0]
m3=pd.merge(m2,spring, on="Farm_JIRA", how='left')
# # fall
fall=stem.loc[stem['Season'] == "Fall'21"]
fall=fall.groupby(['Farm_JIRA'])['Season'].size().reset_index(name='Fall')
fall = fall[fall['Farm_JIRA'] != 0]
m4=pd.merge(m3,fall, on="Farm_JIRA", how='left')
### file to download ###
m4.to_excel('Count_11.4.22.xlsx')




