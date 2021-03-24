import requests
import time

swapi_base_url = "https://swapi.dev/api/"
base_search_url = "?search="

search_fields = {}

#Categories: "people": "http://swapi.dev/api/people/",
#            "planets": "http://swapi.dev/api/planets/",
#            "films": "http://swapi.dev/api/films/",
#            "species": "http://swapi.dev/api/species/",
#            "vehicles": "http://swapi.dev/api/vehicles/",
#            "starships": "http://swapi.dev/api/starships/"

def process_search_term(lookup):
    """
    Removes any whitespace from the search string, and replaces them with the appropriate character to pass as a URL
    :param lookup:
    :return: lookup
    """
    lookup = lookup.replace(" ", "+")
    return lookup

def search_suffix(lookup):
    """
    Combines the search for term with the string needed to run the query in the api
    :param lookup:
    :return: search_suffix
    """
    lookup = process_search_term(lookup)
    search_suffix = base_search_url + lookup
    return search_suffix

def set_search_fields(lookup):
    """

    :param lookup:
    :return:
    """
    lookup = process_search_term(lookup)
    search_sfx = search_suffix(lookup)
    search_url = swapi_base_url + search_sfx
    response = requests.get(search_url)
    global_search_fields = response.json()
    global search_fields
    for key, value in global_search_fields.items():
        search_fields[key] = value

def get_field_id(url):
    """
    Extracts the field and id from a given url
    :param url:
    :return:
    """
    url = url.lstrip(swapi_base_url)
    url.strip('/')
    url = url.split('/')
    field = url[0]
    id = url[1]
    return field, id

def status_check(response):
    if response.ok:
        return True
    else:
        print(response.status_code)
        return False

def global_search(lookup):
    """
    Searches for the given search term across all the categories
    :param lookup:
    :return:
    """
    lookup = process_search_term(lookup)
    results = []
    for key, value in search_fields.items():
        new_results = local_search(lookup, key)
        if bool(new_results):
            for x in range(len(new_results)):
                results.append(new_results[x])
    return results


def local_search(lookup, field):
    """
    Searches for the given search term in a specified category
    :param lookup:
    :return: listed_results
    """
    lookup = process_search_term(lookup)
    global search_fields
    results = []
    listed_results = []
    search_sfx = search_suffix(lookup)
    for i in search_fields.keys():
        if i == field:
            response = requests.get(search_fields[field] + search_sfx)
            response = response.json()
            if response['count'] != 0:
                results = response['results']
                for j in range(len(results)):
                    listed_results.append(results[j])
                if response['count'] > 10:   #Checks if there is more than one page of returned results
                    for j in range(response['count']//10):
                        new_response = requests.get(search_fields[field] + search_sfx + '&page=' + str(j+2))
                        new_response = new_response.json()
                        new_results = new_response['results']
                        #results['results'].append(new_results['results'])
                        for k in range(len(new_results)):
                            listed_results.append(new_results[k])
    return listed_results

def print_results(results):
    """
    Prints the results of a search to a text file
    :param results:
    :return:
    """
    f = open('search_results.txt', 'w')
    for i in range(len(results)):
        cresult = results[i]
        for key, value in cresult.items():
            print(str(key) + ': ' + str(value) + '\n', file=f)
        print('\n', file=f)
    f.close()

def check_film(lookup):
    """

    :param lookup:
    :return:
    """
    lookup = lookup.lower()
    film_rn = {'iv': '1', 'v': '2', 'vi': '3', 'i': '4', 'ii': '5', 'iii': '6'}
    if lookup.isnumeric():
        if int(lookup) in range(1-6):
            return lookup
    else:
        if len(lookup) <= 4:
            for key in film_rn:
                if key == lookup:
                    lookup = film_rn[key]
        else:
            search_film = local_search(lookup, 'films')
            if len(search_film) == 1:
                film_id = get_field_id(search_film[0]['url'])
                lookup = film_id
            elif len(search_film) > 1:
                print('Two many films match given criteria')
                lookup = '#'      
    return lookup


def print_scrawl(lookup):
    """
    Prints the opening scrawl of the given film
    :param lookup:
    :return:
    """
    film_url = 'http://swapi.dev/api/films/'
    if int(lookup):
        found_film = requests.get(film_url + str(lookup))
        found_film = found_film.json()
        crawl = found_film['opening_crawl'].split('\r\n')
        print('\n\n\n\n\n')
        longest = len(max(crawl))
        for i in range(len(crawl)):
            print(crawl[i].center(longest+(longest//2)))
            time.sleep(1)
        for j in range(10):
            print('\n')
            time.sleep(1)


set_search_fields("")
#print(global_search("skywalker"))
#print(global_search("star"))
#print(global_search("spaniel"))

print('Beginning file print')
print_results(global_search("star"))
print('End file print')

print('HERE')
print(check_film('iv'))

#print_scrawl(1)
print_scrawl(check_film('vi'))
