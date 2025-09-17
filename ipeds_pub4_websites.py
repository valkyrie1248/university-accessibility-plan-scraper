import pandas as pd
#You can just alias a module or function when you import it!

def wait(adtl_info = ''):
    '''
    Use to force program to pause for user before continuing to execute
    '''
    input(adtl_info + ' Press enter to continue.')

unidir_df = pd.read_csv('hd2023.csv', encoding = 'ISO-8859-1') #Default encoding utf-8 didn't work. latin1 did.
#We can set the index column with df=df.set_index('column_name') or including optional arg index_col=column_number

#We can convert cleaned panda data back to a csv or json named fn with df.to_type('fn.type').
#To convert to sql, use df.to_sql('fn', con) where con=sqlite3.connect('database.db')

print(unidir_df.head()) #Shows the first 5 rows by default, but accepts number as argument. Can do .tail() for last rows.
wait()
unidir_df.info() #One of the first things we should call.
wait()
print('\nTotal rows = ' + str(unidir_df.shape[0]) + '\nTotal columns = ' + str(unidir_df.shape[1]) +'\n')
'''
(rows, columns)
No parentheses, because it's an attribute not a method.
Very useful for seeing how many rows/columns are left after filtering or otherwise cleaning data
'''
wait('Time to start cleaning our data! ')
#Time to start cleaning!

unidir_df.drop_duplicates(inplace=True) #What it says on the tin. inplace=True keyword will just modify the object in place.
print('\nAfter removing duplicates:\nTotal rows =  ' + str(unidir_df.shape[0]) + '\nTotal columns = ' + str(unidir_df.shape[1]) +'\n')
wait()

#Define the subset where SECTOR == 1 (1 is the code for public, 4 year).
pub4 = unidir_df[unidir_df['SECTOR'] == 1]
pub4.info()
wait('\nAfter filtering out everything except for public, 4+ year universities, our data looks totally different!\n')
print(pub4.head())

#Okay. Let's snag the college names websites from this list.
websites = pub4[['UNITID', 'INSTNM', 'WEBADDR', 'DISAURL']]
wait('Now we pulled out just the columns with the unique IDs, school names, main website, and disability services website.')
websites.head()
wait('\nYou did it! Once you press enter, it will save the cleaned data as a json file and a csv!\n')

#Now, it's time to rewrite the cleaned data into files for later.
websites.to_json('websites.json')
websites.to_csv('websites.csv')


