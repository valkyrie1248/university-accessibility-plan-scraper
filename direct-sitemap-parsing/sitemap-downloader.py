#Function to try to download sitemaps for a set of domains.
import requests
import pandas as pd

def wait(adtl_info = ''):
    '''
    Use to force program to pause for user before continuing to execute
    '''
    input(adtl_info + ' Press enter to continue.')

#def domain_list(domain_inputs):
#    return domain_inputs.split()


#def get_maps(domain_list):
#    maps={}
#    for domain in domain_list:
#        maps[f"{domain} map"] = get_map(domain)
#    return maps

def potentials(domains_list):
    for site in domains_list[['WEBADDR', 'DISAURL']]:
        site = site+'/sitemap.xml'
    return domains_list

def check_maps(potentials):
    for url in potentials:
        try:
            print(f"Attempting to download {url}")
            response = requests.get(url)
            if response.txt != None:
                url=url
            if response.txt == None:
                url = response.raise_for_status()
        except Exception as e:
            print('The error is ', e)
            print(url + ' is not a valid sitemap.')
            url =  'Error'
    site_maps = potentials
    return site_maps

# def get_map(domain):
#     try:
#         url = domain+'/sitemap.xml'
#         #print(f"Attempting to download {url}")
#         response = requests.get(url)
#         if response.txt != None:
#             return(url)
#         if response.txt == None:
#             return(response.raise_for_status())
#     except Exception as e:
#         print('The error is ', e)
#         #print(domain+'/sitemap.xml is not a valid sitemap.')
#         return None

#def get_maps(domain_list):
#    maps={}
#    for domain in domain_list['WEBADDR']:
#        maps[f"{domain} map"] = get_map(domain_name, home, dis_serv)
#    return maps

#def get_map(domain_name, home, dis_serv):
#    try:
#        url = home+'/sitemap.xml'
#        #print(f"Attempting to download {url}")
    #     response = requests.get(url)
    #     if response.txt != None:
    #         return(url)
    #     if response.txt == None:
    #         return(response.raise_for_status())
    # except Exception as e:
    #     print('The error is ', e)
    #     #print(domain+'/sitemap.xml is not a valid sitemap.')

def domains(file):
    unis_df = pd.read_csv(file)
#    print(unis_df.head())
    domains = unis_df[['INSTNM', 'WEBADDR', 'DISAURL']]
    return domains
    print(domains_list.head())
    wait()
    
# def get_sitemaps(domains_list):
#     names = domains_list[['INSTNM']]
#     home_maps = domains_list[['WEBADDR' + '/sitemap.xml']]
#     dis_maps = domains_list[['DISAURL' + 'sitemap.xml']]

#domain_inputs = input("Enter some domains with spaces between them: ")
site_maps = check_maps(potentials(domains("/Users/harkmorper/learning-scrapers/university-accessibility-plan-scraper/websites.csv")))
print(site_maps.head())

# domain_list = 
# print(get_maps(domain_list(domain_inputs)))
