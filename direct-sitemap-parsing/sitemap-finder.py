#Function to find sitemaps from a set of domains. (Hope to make it pull out websites related to accessibility soon.p )
import requests
import pandas as pd
import asyncio as aio


def wait():
    '''
    Use to force program to pause for user before continuing to execute
    '''
    input('Press enter to continue.')

def domains(file):
    unis_df = pd.read_csv(file)
#    print(unis_df.head())
    domains = unis_df[['INSTNM', 'WEBADDR', 'DISAURL']]
    print(domains.head())
    wait()
    return domains



def validate(raw_domain):
    '''
    This should properly format any url you feed into the sitemap finder.
    '''
    raw_domain = raw_domain.strip("/")
    print(f"Validating {raw_domain}...")
    if raw_domain.startswith("http"):
        domain = raw_domain
        try:
            response = requests.get(domain, timeout = 2)
            if response.status_code == 200:
                return domain
            else:
                error = f'{domain} is not a valid website.'
                print(error)
                return error
        except requests.RequestException as e:
            error = f'An error occurred while validating {domain}: {e}'
            print(error)
            return error
    else:
        try:
            domain = "https://"+raw_domain
            response = requests.get(domain, timeout = 2)
            if response.status_code == 200:
                return domain
            else:
                print(f'{domain} is not a valid wesbite.')
                try:
                    domain = "http://"+raw_domain
                    respone = requests.get(domain, timeout = 2)
                    if response.status_code == 200:
                        return domain
                    else:
                        error = f'{domain} is not a valid website'
                        print(error)
                        return error 
                except requests.RequestException as e:
                    error = f'An error occurred while validating {domain}: {e}'
                    print(error)
                    return error 
        except requests.RequestException as e:
            error = f'An error occurred while validating {domain}: {e}'
            print(error)
            return error             
                    

def check_potential(domain):
    if domain.startswith("http"):
        potential = domain + '/sitemap.xml'
        try:
            print(f"Attempting to download {potential}")
            response = requests.get(potential, timeout = 2)
            if response.status_code == 200:
                url = potential
                print(f"Sitemap Found: {url}")
            else:
                url = response.raise_for_status()
                error = f'{potential} is not a valid website: {url}'
                print(error)
        except requests.RequestException as e:
                        error = f'An error occurred while accessing sitemap of {potential}: {e}'
                        print(error)
                        return error
        #except Exception as e:
        #    print('The error is ', e)
        #    print(potential + ' is not a valid sitemap.')
        #    url =  'Error'
        return url
    else:
        return domain
    
def check_potentials(domains):
    domains['WEBADDR'] = domains['WEBADDR'].apply(validate).apply(check_potential)
    domains['DISAURL'] = domains['DISAURL'].apply(validate).apply(check_potential)
#    domains['WEBADDR'] = domains['WEBADDR'].apply(check_potential)
#    domains['DISAURL'] = domains['DISAURL'].apply(check_potential)
    return domains

#send the successful ones into a new file and errors into a diff file.
    
#site_maps = check_potentials(domains("/Users/harkmorper/learning-scrapers/university-accessibility-plan-scraper/test_websites.csv"))
file_path = input("Input the full file path for the csv of websites: ")
site_maps = check_potentials(domains(f'{file_path}'))
#print(site_maps.head())
site_maps.to_json('sitemaps.json')
site_maps.to_csv('sitemaps.csv')


if __name__ == '__main__':
    start = perf_counter()
    file_path = input("Input the full file path for the csv of websites: ")
    site_maps = check_potentials(domains(f'{file_path}'))
    #print(site_maps.head())
    site_maps.to_json('sitemaps.json')
    site_maps.to_csv('sitemaps.csv')
    stop = perf_counter()
    print('time taken: ', stop - start)