import requests,json,re,csv,os
from bs4 import BeautifulSoup
from threading import Thread


path = input('Enter input file : ')
output_path = input('Enter output file : ')
NUMBER_OF_THREADS = int(input('Enter number of threads : '))

def addToCSV(line):
    with open(output_path, 'a', newline='', encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=',')
        row = [line['phone'],line['network']]
        print(row)
        writer.writerow(row)
        
        
headers = {
    'Accept':'application/json, text/javascript, */*; q=0.01',
    'Origin':'https://www.hlrlookup.com',
    'X-Requested-With':'XMLHttpRequest',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
    'Sec-Fetch-Site':'same-origin',
    'Sec-Fetch-Mode':'cors'
}
def get_info(phone):
    payload={'action':'get_lookup_number','number':phone}
    response = requests.post('https://www.hlrlookup.com/wp-admin/admin-ajax.php',data=payload,headers=headers)
    info = 'Not found'
    try:
        data_json = json.loads(response.content)
        html_page = data_json['html']
        html_page = re.sub(r'\\"','"',html_page)
        html_page = re.sub(r'\\/','',html_page)
        soup = BeautifulSoup(html_page,'html.parser')
        elt = soup.find('div',attrs={'class':'label'},text=re.compile(r'ISSUEING\s*NETWORK'))
        parent = elt.parent
        info = parent.find('a').text
    except:
      print(response.content)  
    addToCSV({'phone':phone,'network':info})
    

phones = []
# READ PHONE NUMBERS
with open(path) as f:
    for line in f.readlines():
        if len(line) > 3:
            phones.append(line.strip())
            
i=0
while True:
    Threads = []
    for k in range(i,i+NUMBER_OF_THREADS):
        i+=1
        if(k >= len(phones)):
            break
        th = Thread(target=get_info,args=[phones[k]])
        th.start()
        Threads.append(th)
        
    for th  in Threads:
        th.join()
    #os.system('cls' if os.name == 'nt' else 'clear')
    if(i >= len(phones)):
        break