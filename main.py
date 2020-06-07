import requests
import json
import threading
import time


API_KEY = "tDGxs1abt_qg"
PROJECT_TOKEN = "tcjWGRLiVNSK"
RUN_TOKEN = "tt8nYc-79C3p"


class Data:
    def __init__(self, api_key, project_token):
        self.api_key = api_key
        self.project_token = project_token
        self.params = {
            "api_key": self.api_key
        }
        self.data = self.get_data()

    def get_data(self):
        response = requests.get(f'https://www.parsehub.com/api/v2/projects/{self.project_token}/last_ready_run/data', params=self.params)
        #response = requests.get(f'https://www.parsehub.com/api/v2/projects/{PROJECT_TOKEN}/last_ready_run/data',params={"api_key":API_KEY})
        data = json.loads(response.text)
        return data

    def get_total_cases(self):
        data = self.data['total']

        for content in data:
            if content['name'] == "Coronavirus Cases:":
                return content['value']

    def get_total_deaths(self):
        data = self.data['total']

        for content in data:
            if content['name'] == "Deaths:":
                return content['value']

        return "0"
            
    def get_total_Recovered(self):
        data = self.data['total']

        for content in data:
            if content['name'] == "Recovered:":
                return content['value']

        return "0"

    def get_country_data(self, country):
        data = self.data['country']

        for content in data:
            if content['name'].lower() == country.lower():
                return content

        return "0"
    def get_last_update(self):
        data = self.data['time']

        return data

    def update_data(self):
        response = requests.post(f'https://www.parsehub.com/api/v2/projects/{self.project_token}/run', params=self.params)
        #response = requests.get(f'https://www.parsehub.com/api/v2/projects/{PROJECT_TOKEN}/run/data',params={"api_key":API_KEY})
        print("Data is being updated. This may take a moment !")
        
        time.sleep(0.1)
        old_data = self.data
        while True:
            new_data = self.get_data()
            if new_data != old_data:
                self.data = new_data
                print("Data updated")
                break
                #time.sleep(5)

        #t = threading.Thread(target=poll)
        #t.start()

data = Data(API_KEY,PROJECT_TOKEN)
#print(data.get_last_update())

while True:
    
    print("----"*10+"\nchoose one option for COVID19 Updates")
    print("\t1.Total Corana cases\n\t2.Total Deaths Cases\n\t3.Total Recovered\n\t4.Want to check through countries\n\t5.update\n\t6.Exit\n"+"----"*10)
    
    x=int(input("Your selected option: "))
    
    if x==1:
        print("\nTotal Coronavirus Cases = ",data.get_total_cases())

    elif x==2:
        print("\nTotal Deaths Cases = ",data.get_total_deaths())

    elif x==3:
        print("\nTotal Recovered = ",data.get_total_Recovered())

    elif x==4:
        y=input("Enter the country name :")
        for i,j in data.get_country_data(y).items():
            print("{} : {}".format(i,j))
    elif x==5:
        data.update_data()
    elif x==6:
        print("Thank you")
        break

