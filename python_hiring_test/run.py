"""Main script for generating output.csv."""

import csv
def main():
   import pandas as pd

   #read in data
   data = pd.read_csv('./data/raw/pitchdata.csv')

   #create pitcher team table   
   pteam= data.groupby(['PitcherTeamId','HitterSide'], as_index=False).sum()
   pteam =pteam.drop(pteam[pteam.PA <25].index)
   pteam['Subject'] = 'PitcherTeamId'
   pteam['Split'] = pteam.HitterSide.apply(lambda x:"vs LHH" if x=='L' else 'vs RHH')
   pteam.columns =['SubjectId' if x =='PitcherTeamId' else x for x in pteam.columns]

                

   #create hitting team table
   hteam= data.groupby(['HitterTeamId','PitcherSide'], as_index=False).sum()
   hteam =hteam.drop(hteam[hteam.PA <25].index)
   hteam['Subject'] = 'HitterTeamId'
   hteam['Split'] = hteam.PitcherSide.apply(lambda x:"vs LHP" if x=='L' else 'vs RHP')
   hteam.columns =['SubjectId' if x =='HitterTeamId' else x for x in hteam.columns]

   #create pitcher table
   pitcher = data.groupby(['PitcherId','HitterSide'], as_index=False).sum()
   pitcher =pitcher.drop(pitcher[pitcher.PA <25].index)
   pitcher['Subject'] = 'PitcherId'
   pitcher['Split'] = pitcher.HitterSide.apply(lambda x:"vs LHH" if x=='L' else 'vs RHH')
   pitcher.columns =['SubjectId' if x =='PitcherId' else x for x in pitcher.columns]

   #create hitter table
   hitter= data.groupby(['HitterId','PitcherSide'], as_index=False).sum()
   hitter =hitter.drop(hitter[hitter.PA <25].index)
   hitter['Subject'] = 'HitterId'
   hitter['Split'] = hitter.PitcherSide.apply(lambda x:"vs LHP" if x=='L' else 'vs RHP')
   hitter.columns =['SubjectId' if x =='HitterId' else x for x in hitter.columns]

   #combine tables for calculations
   features = ['SubjectId','Split','Subject','PA','AB','H','TB','BB','SF','HBP']
   calc_data=pd.concat([pteam[features],hteam[features],pitcher[features],hitter[features]])

   #perform calculations
   calc_data['AVG'] = (calc_data.H/calc_data.AB).round(3)
   calc_data['OBP'] = ((calc_data.H + calc_data.BB + calc_data.HBP)/(calc_data.AB + calc_data.BB + calc_data.HBP + calc_data.SF)).round(3)
   calc_data['SLG'] = (calc_data.TB/calc_data.AB).round(3)
   calc_data['OPS'] = (calc_data.OBP + calc_data.SLG).round(3)

   #present appropriate information
   calc_data= pd.melt(calc_data, id_vars = ['SubjectId','Split','Subject'], value_vars = ['AVG','OBP','SLG','OPS'], var_name = 'Stat',value_name = 'Value')
   #export data
   calc_data.to_csv('./data/processed/output.csv')
if __name__ == '__main__':
    main()
