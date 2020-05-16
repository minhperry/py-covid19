import requests as r
import sys as s

# Search by country code and returns a Country object
def searchByCountryCode(cc):
    u = "https://api.covid19api.com/summary"
    rq = r.get(url=u)
    if (rq.status_code != 200):
        print("Request to API failed! Try again later.")
        exit()
    data = rq.json()
    countries = data['Countries']
    for ct in countries:
        if ct['CountryCode'] == cc.upper() and ct != None:
            return ct

def listCountry():
    u = "https://api.covid19api.com/countries"
    rq = r.get(url=u)
    if (rq.status_code != 200):
        print("Request to API failed! Try again later.")
        exit()
    data = rq.json()
    print("Available countries:")
    for ct in data:
        print('    ',ct['Slug'])

def listCountryStartsWith(ch):
    ch.lower()
    u = "https://api.covid19api.com/countries"
    rq = r.get(url=u)
    if (rq.status_code != 200):
        print("Request to API failed! Try again later.")
        exit()
    data = rq.json()
    print(f"Available countries that start with {ch.upper()}:")
    for ct in data:
        if ct['Slug'].startswith(ch):
            print('    ',ct['Slug'])

def searchCountryCode(ctr):
    ctr = ctr.lower()
    u = "https://api.covid19api.com/countries"
    rq = r.get(url=u)
    if (rq.status_code != 200):
        print("Request to API failed! Try again later.")
        exit()
    data = rq.json()
    for ct in data:
        if ct['Slug'] == ctr:
            return f"Country code for {ctr.capitalize()} is {ct['ISO2'].upper()}."
    return "Country not found! Please try again."

# Display informations about 
def display(country):
    ctr = country['Country']
    conf = country['NewConfirmed']
    tconf = country['TotalConfirmed']
    death = country['NewDeaths']
    tdeath = country['TotalDeaths']
    recv = country['NewRecovered']
    trecv = country['TotalRecovered']
    print(f"""
For {ctr}:
    > New cases: {conf}
    > Total cases: {tconf}
    > New deaths: {death}
    > Total deaths: {tdeath}
    > New recovered: {recv}
    > Total recovered: {trecv}

    /!\ Remaining cases: {tconf - tdeath - trecv}
    """)

# CLI help
def help():
    print(f"""
Usage: py corona.py [opt] [arg]

Parameter opt:
    -h          Display this help message

    -st         Display stat for a country
        >> arg must be a country code

    -sr         Search for a country code
        >> arg must not contain spaces
        >> spaces should be written as -

        -all
            >> List all available countries

            !
                >> List all

            .X
                >> Country starts with letter 'X'
    """)

arg = s.argv

if len(arg) == 1:
    print("No parameters given. Run \"py corona.py -h\" to get help.")
    exit()

if arg[1] == '-h':
    help()
elif arg[1] == '-st':
    display(searchByCountryCode(arg[2]))
elif arg[1] == '-sr':
    if arg[2] == '-all':
        if arg[3] == '!':
            listCountry()
        else:
            listCountryStartsWith(arg[3][1])
    else:
        print(searchCountryCode(arg[2]))