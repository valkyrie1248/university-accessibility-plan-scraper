#Function to find sitemaps from a set of domains. (Hope to make it pull out websites related to accessibility soon.p )
import pandas as pd
import asyncio
import aiohttp
import time

# Define a Chrome-like custom User-Agent
headers = {
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9,fr-FR;q=0.8,fr;q=0.7,es-US;q=0.6,es;q=0.5,it-IT;q=0",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:143.0) Gecko/20100101 Firefox/143.0"
    }

cookies = {
        "session_id": "9412d7hdsa16hbda4347dagb",
        "user_preferences": "dark_mode=false"
    }

def wait():
    '''
    Use to force program to pause for user before continuing to execute
    '''
    input('Press enter to continue.')

def raw_domains(file):
    unis_df = pd.read_csv(file)
    raw_domains = unis_df[['INSTNM', 'WEBADDR', 'DISAURL']]
    return raw_domains

def prep_domains(raw_domain):
    prepped_domain = raw_domain.strip("/")
    return prepped_domain

async def validate(session, prepped_domain):
    start = time.perf_counter()
    print(f'Validating and normalizing {prepped_domain} ...')
    if prepped_domain.startswith('http'):
        domain = prepped_domain
        try:
            async with session.get(domain) as response:
                if response.status == 200:
                    print(f'{domain} is a valid website.')
                    stop = time.perf_counter()
                    print('Time taken: ', stop - start)
                    return domain
                else:
                    error = f'{domain} is not a valid website.'
                    print(error)
                    stop = time.perf_counter()
                    print('Time taken: ', stop - start)
                    return error
        except aiohttp.ClientError as e:
            error = f'Validation of {prepped_domain} failed: {e}'
            print(error)
            stop = time.perf_counter()
            print('Time taken: ', stop - start)
            return error
        except asyncio.TimeoutError:
            error = f'Validation of {prepped_domain} timed out.'
            print(error)
            stop = time.perf_counter()
            print('Time taken: ', stop - start)
            return error
    else:
        try:
            domain = 'https://'+prepped_domain
            async with session.get(domain) as response:
                if response.status == 200:
                    print(f'{domain} is a valid website.')
                    stop = time.perf_counter()
                    print('Time taken: ', stop - start)
                    return domain
                else:
                    error = (f'{domain} is not a valid website.')
                    print (error)
                    try:
                        domain = 'http://'+prepped_domain
                        async with session.get(domain) as response:
                            if response.status == 200:
                                print(f'{domain} is a valid website.')
                                stop = time.perf_counter()
                                print('Time taken: ', stop - start)
                                return domain  
                            else:
                                error = f'{domain} is not a valid website'
                                print(error)
                                stop = time.perf_counter()
                                print('Time taken: ', stop - start)
                                return error
                    except aiohttp.ClientError as e:
                        error = f'Validation of {prepped_domain} failed: {e}'
                        print(error)
                        stop = time.perf_counter()
                        print('Time taken: ', stop - start)
                        return error
                    except asyncio.TimeoutError:
                        error = f'Validation of {prepped_domain} timed out.'
                        print(error)
                        stop = time.perf_counter()
                        print('Time taken: ', stop - start)
                        return error
        except aiohttp.ClientError as e:
            error = f'Validation of {prepped_domain} failed: {e}'
            print(error)
            stop = time.perf_counter()
            print('Time taken: ', stop - start)
            return error
        except asyncio.TimeoutError:
            error = f'Validation of {prepped_domain} timed out.'
            print(error)
            stop = time.perf_counter()
            print('Time taken: ', stop - start)
            return error

async def check_potential(session, domain):
    start = time.perf_counter()
    print('Looking for sitemaps.')
    if domain.startswith('http'):
        potential = domain + '/sitemap.xml'
        try:
            print(f'Attempting to fetch {potential} ...')
            async with session.get(potential) as response:
                if response.status == 200:
                    url = potential
                    print(f'sitemap found: {url}')
                    stop = time.perf_counter()
                    print('Time taken: ', stop - start)
                    return url
                else:
                    e = response.raise_for_status()
                    error = 'Sitemap not found'
                    print (f'{potential} is not a valid website. ' + error + f': {e}')
                    return error
        except aiohttp.ClientError as e:
            error = 'Sitemap not found'
            print(error + f': {e}')
            stop = time.perf_counter()
            print('Time taken: ', stop - start)
            return error
        except asyncio.TimeoutError:
            error = 'Sitemap not found'
            print(error + f': {potential} timed out.')
            stop = time.perf_counter()
            print('Time taken: ', stop - start)
            return error
    else:
        return domain


# def check_potential(domain):
#     if domain.startswith("http"):
#         potential = domain + '/sitemap.xml'
#         try:
#             print(f"Attempting to download {potential}")
#             response = requests.get(potential, timeout = 2)
#             if response.status_code == 200:
#                 url = potential
#                 print(f"Sitemap Found: {url}")
#             else:
#                 url = response.raise_for_status()
#                 error = f'{potential} is not a valid website: {url}'
#                 print(error)
#         except requests.RequestException as e:
#                         error = f'An error occurred while accessing sitemap of {potential}: {e}'
#                         print(error)
#                         return error
#         #except Exception as e:
#         #    print('The error is ', e)
#         #    print(potential + ' is not a valid sitemap.')
#         #    url =  'Error'
#         return url
#     else:
#         return domain


# def validate(prepped_domain):
#     '''
#     This should properly format any url you feed into the sitemap finder.
#     '''
#     # prepped_domain = raw_domain.strip("/")
#     # print(f"Validating {prepped_domain}...")
#     if prepped_domain.startswith("http"):
#         domain = prepped_domain
#         try:
#             response = requests.get(domain, timeout = 2)
#             if response.status_code == 200:
#                 return domain
#             else:
#                 error = f'{domain} is not a valid website.'
#                 print(error)
#                 return error
#         except requests.RequestException as e:
#             error = f'An error occurred while validating {domain}: {e}'
#             print(error)
#             return error
#     else:
#         try:
#             domain = "https://"+prepped_domain
#             response = requests.get(domain, timeout = 2)
#             if response.status_code == 200:
#                 return domain
#             else:
#                 print(f'{domain} is not a valid wesbite.')
#                 try:
#                     domain = "http://"+prepped_domain
#                     respone = requests.get(domain, timeout = 2)
#                     if response.status_code == 200:
#                         return domain
#                     else:
#                         error = f'{domain} is not a valid website'
#                         print(error)
#                         return error 
#                 except requests.RequestException as e:
#                     error = f'An error occurred while validating {domain}: {e}'
#                     print(error)
#                     return error 
#         except requests.RequestException as e:
#             error = f'An error occurred while validating {domain}: {e}'
#             print(error)
#             return error             
                    

async def main1():
    '''
    Slick mixing of asyncio with pandas by Henry Ecker over on StackOverFlow.
    Passes each value of first two columns into the async function, which means all will be run concurrently rather than sequentially.
    INFINITELY faster than original approach.
    '''
    timeout = aiohttp.ClientTimeout(total=30)
    async with aiohttp.ClientSession(timeout = timeout, cookies = cookies, headers = headers) as session:
        prepped_domains['WEBADDR'] = await asyncio.gather(*(validate(session, prepped_domain) for prepped_domain in prepped_domains['WEBADDR']))
        prepped_domains['DISAURL'] = await asyncio.gather(*(validate(session, prepped_domain) for prepped_domain in prepped_domains['DISAURL']))
    validated_domains=prepped_domains
    return validated_domains

async def main2():
    timeout = aiohttp.ClientTimeout(total=30)
    async with aiohttp.ClientSession(timeout = timeout, cookies = cookies, headers = headers) as session:
        validated_domains['WEBADDR'] = await asyncio.gather(*(check_potential(session, validated) for validated in validated_domains['WEBADDR']))
        validated_domains['DISAURL'] = await asyncio.gather(*(check_potential(session, validated) for validated in validated_domains['DISAURL']))
    sitemaps = validated_domains
    return sitemaps

    
# def check_potentials(domains):
#     domains['WEBADDR'] = domains['WEBADDR'].apply(validate).apply(check_potential)
#     domains['DISAURL'] = domains['DISAURL'].apply(validate).apply(check_potential)
#     domains['WEBADDR'] = domains['WEBADDR'].apply(check_potential)
#     domains['DISAURL'] = domains['DISAURL'].apply(check_potential)
#     return domains


if __name__ == '__main__':
    file_path = input('Input the full file path for the csv of websites: ')
    program_start = time.perf_counter()
    raw_domains = raw_domains(f'{file_path}')
    print(raw_domains.head(2))
    wait()
    prepped_domains = raw_domains.map(prep_domains)
    print(prepped_domains.head(2))
    wait()
    validated_domains = asyncio.run(main1())
    print(validated_domains.head(10))
    wait()
    site_maps = asyncio.run(main2())
    print(f'Total time taken: {time.perf_counter() - program_start} seconds')
    #print(site_maps.head())
    site_maps.to_json('sitemaps1.json')
    site_maps.to_csv('sitemaps1.csv')