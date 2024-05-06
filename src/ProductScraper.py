import requests
from bs4 import BeautifulSoup
import mysql.connector
from unidecode import unidecode
from sklearn import tree

# scraping function
def get_links(soup):
    links = []
    soup_links = soup('ul' , {'class' : 'c-listing__items'})
    count = 0
    for link in soup_links[0].find_all('a'):
        count += 1
        if count % 2 == 0:
            continue    
        links.append(link.get('href'))
    return links

def get_model(soup):
    model = soup('span', {'class' : 'o-box__header-desc'})
    model = model[0].get_text()
    return model

def get_brand(soup):
    brand = soup('span', {'class' : 'o-box__header-desc'})
    brand = brand[0].get_text()
    brand = brand.split()
    return brand[0]

def get_price(soup):
    price_soup = soup('div', {'class': 'c-product__seller-price-pure js-price-value' })
    price = price_soup[0].get_text().strip().split()
    price = unidecode(price[0])
    price = price.split(',')
    new_price = ''
    for i in price:
        new_price += i
    return int(new_price)

def find_CPU_series(CPU_soup):
    CPU_soup = CPU_soup.find_all('li')
    CPU_series = CPU_soup[1].get_text()
    CPU_series = CPU_series.strip().split()
    CPU_series = CPU_series[2:]
    output = ''
    for i in CPU_series:
        output = output + i + ' '
    return output.strip()

def find_RAM_size(RAM_soup):
    RAM_soup = RAM_soup.find_all('li')
    RAM_series = RAM_soup[0].get_text()
    RAM_series = RAM_series.strip().split()
    RAM_series = RAM_series[3]
    return int(RAM_series)

def find_internalMemory_type(internalMemory_soup):
    internalMemory_soup = internalMemory_soup.find_all('li')
    internalMemory_type = internalMemory_soup[1]
    internalMemory_type = internalMemory_type('div', {'class': 'c-params__list-value'})
    internalMemory_type = internalMemory_type[0].get_text()
    internalMemory_type = internalMemory_type.strip().split()
    if(len(internalMemory_type) > 1) :
        internalMemory_type = internalMemory_type[0] + ' ' + internalMemory_type[1]
    else :
        internalMemory_type = internalMemory_type[0]
    return internalMemory_type

def find_GPU_series(GPU_soup):
    GPU_soup = GPU_soup.find_all('li')
    GPU_series = GPU_soup[0].get_text()
    GPU_series = GPU_series.strip().split()
    GPU_series = GPU_series[3]
    return GPU_series

def find_screnn_size(screnn_soup):
    screnn_soup = screnn_soup.find_all('li')
    screnn_size = screnn_soup[0].get_text()
    screnn_size = screnn_size.strip().split()
    screnn_size = screnn_size[3]
    return float(screnn_size)

def get_information(soup):
    param_box_soup = soup('div', {'class': 'c-params js-product-tab-content'})
    param_soup = param_box_soup[0].find_all('article')
    param_soup = param_soup[0]

    model_soup = param_soup('div', {'class': 'o-box__header'})
    model_soup = model_soup[0]
    param_section_soup = param_soup.find_all('section')     

    physicalSpecifications_soup = param_section_soup[0]
    CPU_soup = param_section_soup[1]
    RAM_soup = param_section_soup[2]
    internalMemory_soup = param_section_soup[3]
    GPU_soup = param_section_soup[4]
    screnn_soup = param_section_soup[5]
    facilities_soup = param_section_soup[6]
    otherFeatures_soup = param_section_soup[7]
    
    model = get_model(model_soup)
    brand = get_brand(model_soup)
    price = get_price(soup)
    CPU = find_CPU_series(CPU_soup)
    RAM = find_RAM_size(RAM_soup)
    memoryType = find_internalMemory_type(internalMemory_soup)
    GPU = find_GPU_series(GPU_soup)
    screenSize = find_screnn_size(screnn_soup)

    return (model, brand, price, CPU, RAM, memoryType, GPU, screenSize)

# Converting function for Models
def convert_brand_to_number(brand):
    if brand == 'ASUS' :
        return 1
    elif brand == 'Lenovo' :
        return 2
    elif brand == 'HP' :
        return 3
    elif brand == 'Acer' :
        return 4
    elif brand == 'Dell' :
        return 5
    elif brand == 'Apple' :
        return 6
    elif brand == 'Microsoft' :
        return 7
    elif brand == 'MSI' :
        return 8
    else :
        return 9
    
def convert_number_to_brand(number):
    if number == 1 :
        return 'ASUS'
    elif number == 2 :
        return 'Lenovo'
    elif number == 3 :
        return 'HP'
    elif number == 4 :
        return 'Acer'
    elif number == 5 :
        return 'Dell'
    elif number == 6 :
        return 'Apple'
    elif number == 7 :
        return 'Microsoft'
    elif number == 8 :
        return 'MSI'
    else :
        return 'Others'

def convert_CPU_to_number(CPU):
    if CPU == 'Pentium' :
        return 1
    elif CPU == 'Celeron' :
        return 2
    elif CPU == 'Core i3' :
        return 3
    elif CPU == 'Core i5' :
        return 4
    elif CPU == 'Core i7' :
        return 5
    else :
        return 6

def convert_number_to_CPU(number):
    if number == 1 :
        return 'Pentium'
    elif number == 2 :
        return 'Celeron'
    elif number == 3 :
        return 'Core i3'
    elif number == 4 :
        return 'Core i5'
    elif number == 5 :
        return 'Core i7'
    else :
        return 'Others'

def convert_memoryType_to_number(memoryType):
    if memoryType == 'هارد دیسک' :
        return 1
    elif memoryType == 'حافظه‌های هیبریدی' or memoryType == 'SSD' :
        return 2
    else :
        return 3   

def convert_number_to_memoryType(number):
    if number == 1 :
        return 'HDD'
    elif number == 2 :
        return 'SSD'
    else :
        return 'Others' 

def convert_GPU_to_number(GPU):
    if GPU == 'Intel' :
        return 1
    elif GPU == 'NVIDIA' :
        return 2
    elif GPU == 'AMD' :
        return 3
    else :
        return 4   

def convert_number_to_GPU(number):
    if number == 1 :
        return 'Intel'
    elif number == 2 :
        return 'NVIDIA'
    elif number == 3 :
        return 'AMD'
    else :
        return 'Others'  

# database function
def update_db(key, price): # update records when price is has changed.
    cnx = mysql.connector.connect (user='root', password='' ,host='127.0.0.1' ,database='Digikala')

    cursor = cnx.cursor()
    cursor.execute( 'UPDATE dbLaptop SET price = %i  WHERE model = \'%s\'' %(price, key) ) 

    cnx.commit()
    cursor.close()
    cnx.close() 

def create_list_of_new_query(list_of_new_laptops):  # To not add duplicate records.

    cnx = mysql.connector.connect (user='root', password='' ,host='127.0.0.1' ,database='Digikala')

    cursor = cnx.cursor()
    query = 'SELECT * FROM dbLaptop'
    cursor.execute(query)
    counter = 0
    for (model, brand, CPU, RAM, memoryType, GPU, screenSize, price ) in cursor:
        for laptop in list_of_new_laptops :
            if model == laptop[0] and price == laptop[7]:
                list_of_new_laptops.remove(laptop)
            elif model == laptop[0] and price != laptop[7]:
                counter += 1
                update_db(model, laptop[7])
                list_of_new_laptops.remove(laptop)
                # we need to update record that model == i[0] and price != i[7]. beacuse price is updated.
    
    cursor.close()
    cnx.close()
    return (list_of_new_laptops, counter)


def insert_into_db(list_of_new_laptops):  # insert all new records in db.
    cnx = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='Digikala')
    cursor = cnx.cursor()
    counter = 0
    for laptop in list_of_new_laptops :
        counter += 1
        query = 'INSERT INTO dbLaptop VALUES ( \'%s\', %i, %i, %i, %i, %i, %f, %i)' %(laptop[0], laptop[1], laptop[2], laptop[3], laptop[4], laptop[5], laptop[6], laptop[7] )
        cursor.execute(query)
        cnx.commit()
    cursor.close()
    cnx.close()
    return counter

def select_laptop_from_db():
    list_of_laptop = []
    list_of_price = []
    cnx = mysql.connector.connect (user='root', password='' ,host='127.0.0.1' ,database='Digikala')

    cursor = cnx.cursor()
    query = 'SELECT * FROM dbLaptop'
    cursor.execute(query)
    counter = 0
    for (model, brand, CPU, RAM, memoryType, GPU, screenSize, price ) in cursor:
        l = []
        l.append(str(brand))
        l.append(str(CPU))
        l.append(str(RAM))
        l.append(str(memoryType))
        l.append(str(GPU))
        l.append(str(screenSize))
        list_of_laptop.append(l)
        l = []
        l.append(str(price))
        list_of_price.append(l)
    cursor.close()
    cnx.close()     
    return (list_of_laptop, list_of_price)


def fetch():
    pageNumber = 0
    list_of_new_laptops = []
    while True :
    
        pageNumber += 1

        url = 'https://www.digikala.com/search/category-notebook-netbook-ultrabook/?has_selling_stock=1&pageno=' + str(pageNumber)

        headers = {"Accept-Language": "en-US,en;q=0.5",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"}
        try:
            r = requests.get(url, headers = headers)
        except:
            continue
        soup = BeautifulSoup(r.text, 'html.parser')
    
        soup_massage = soup('div', {'class':'c-message-light c-message-light--info c-listing-not-found__message'})    # for stop working (end of pages) the url with pageNumber is not exist.
        if soup_massage != []:
            break

        links = get_links(soup)    # get all laptop links.
        #links = links[-1:]
        print ('Reading information from page %i ... ' %pageNumber)
        print ('%i links(laptop) exist in page %i ' %(len(links),pageNumber))
        for link in links :     # for each laptop:
            laptop_url = 'https://www.digikala.com' + link
            try:
                response = requests.get(laptop_url, headers=headers)

            except:
                
                continue
            laptop_soup = BeautifulSoup(response.text, 'html.parser')
            try:
                laptop = []
                model, brand, price, CPU, RAM, memoryType, GPU, screenSize = get_information(laptop_soup)

                brand = convert_brand_to_number(brand)   # 1 = ASUS  ,  2 = Lenovo  ,  3 = HP  ,  4 = Acer  ,  5 = Dell  ,  6 = Apple  ,  7 = Microsoft  ,  8 = MSI  ,  9 = ohters
                CPU = convert_CPU_to_number(CPU)  # 1 = Pentium  ,  2 = Celeron  ,  3 = Core i3  ,  4 = Core i5  ,  5 = Core i7  ,  6 = others
                memoryType = convert_memoryType_to_number(memoryType) # 1 = hardDisk  ,  2 = hybrid , SSD  ,  3 = others
                GPU = convert_GPU_to_number(GPU)   # 1 = Intel  ,  2 = NVIDIA ,  3 = AMD  ,  4 = others
                laptop.append(model) # string
                laptop.append(brand) # int
                laptop.append(CPU) # int
                laptop.append(RAM) # int
                laptop.append(memoryType) #int
                laptop.append(GPU) # int
                laptop.append(screenSize) # float
                laptop.append(price) # int
                list_of_new_laptops.append(laptop)    # list of laptop that we save in dataBase. 
            except:
                pass
        print ('page %i is finished !  ' %pageNumber)


    print ('Data adding to the database ...')

    # after while we have all information (we need) about all laptop exist in Digikala site in [list_of_new_laptop].
    #print(list_of_new_laptops)
    list_of_new_laptops , number_of_update_records = create_list_of_new_query(list_of_new_laptops)  # To not add duplicate records.

    number_of_insert_records = insert_into_db(list_of_new_laptops)
    
    print('< %i record(s) updated >' %number_of_update_records)
    print('< %i record(s) inserted >' %number_of_insert_records)




while 1:
    n = input('For (fetch digikala) enter 1 and for predict price of laptop enter 2 : ') 
    if int(n) == 1:
        fetch()
    elif int(n) == 2:
        list_of_laptop, list_of_price = select_laptop_from_db()
        X = list_of_laptop
        y = list_of_price

        from sklearn import tree
        clf = tree.DecisionTreeClassifier()
        clf = clf.fit(X, y)
        l = []
        brand = input('''
        1 = ASUS
        2 = Lenovo
        3 = HP
        4 = Acer
        5 = Dell
        6 = Apple
        7 = Microsoft
        8 = MSI
        9 = Others
        select your brand : ''')
        CPU = input('''
        1 = Pentium
        2 = Celeron
        3 = Core i3
        4 = Core i5
        5 = Core i7
        6 = Others
        select your CPU : ''')
        RAM = input('''
        select your RAM : ''')  
        memoryType = input('''
        1 = HDD
        2 = SSD
        3 = Others
        select your memoryType : ''')
        GPU = input('''
        1 = Intel
        2 = NVIDIA
        3 = AMD
        4 = Others
        select your GPU : ''')
        screenSize = input('''
        select your screenSize : ''')
        l.append(brand)
        l.append(CPU)
        l.append(RAM)
        l.append(memoryType)
        l.append(GPU)
        l.append(screenSize)
        new_laptop = []
        new_laptop.append(l)
        print(clf.predict(new_laptop))
    elif int(n) == 0:
        break
    else:
        print('It\'s wrong!! please try again.')
        continue