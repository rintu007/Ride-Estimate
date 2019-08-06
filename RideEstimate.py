import requests
from uber_rides.session import Session
from uber_rides.client import UberRidesClient
import time
from tkinter import *

class InvalidInputException(Exception):
    pass

def getPrice(lat1, long1, lat2, long2): #, serviceType):
    if (lat1 != 0): #serviceType.lower() == 'uber':
        session = Session(server_token = "YOUR SERVER TOKEN")
        client = UberRidesClient(session)
        response = client.get_price_estimates( start_latitude = lat1, start_longitude = long1, end_latitude = lat2, end_longitude = long2, seat_count = 2 )
        time.sleep(1)
        estimate = response.json.get('prices')
        time.sleep(1)
        print ('Uber Price:',estimate) #[0]['estimate'])
        return estimate[0]['estimate']
    # elif serviceType.lower() == 'ola':
    #     link = 'https://devapi.olacabs.com/v1/products?pickup_lat={}&pickup_lng={}&drop_lat={}&drop_lng={}&service_type=p2p&category=mini'.format(lat1, long1, lat2, long2)
    #     response1 = requests.get(link)
    #     json = response1.json['ride_estimate'][0]
    #     time.sleep(1)
    #     min = json['amount_min']
    #     max = json['amount_max']
    #     estimate = '{}-{}'.format(min,max)
    #     print('Ola Price:',estimate)
    #     return estimate
    else:
        raise InvalidInputException

root = Tk(className='Ride Estimate')
root.config(background = '#000000')

def onClick():
    try:
        add1 = entryPick.get()
        add2 = entryDrop.get()
        # service = entryService.get()
        print(add1)
        print(add2)
        l1 = LatLong(add1)
        d1 = l1.getLatLong()
        lati1 = d1['lat']
        longi1 = d1['lng']
        address1 = d1['address']
        print(lati1,longi1)

        l2 = LatLong(add2)
        d2 = l2.getLatLong()
        lati2 = d2['lat']
        longi2 = d2['lng']
        address2 = d2['address']
        print(lati2,longi2)

        fare = getPrice(lati1,longi1,lati2,longi2) #,service)
        print(
            'You will be charged around Rs. {} for travelling from {} to {} using {}.'.format(fare, address1,address2)) #,
                                                                                              #service))

        x = 'Approximate Fare = Rs.{}/- \nFrom: {} \nTo: {} \nBy: {}'.format(fare, address1,address2)#,
                                                                                              #service)
        lblOutput['text'] = x
    except Exception as e:
        print(e)

class LatLong:
    def __init__(self, add):
        self.address = add

    def getLatLong(self):
        try:
            url = 'http://maps.googleapis.com/maps/api/geocode/json'
            params = {
                'address' : self.address,
                'sensor' : 'false',
                'region' : 'india'
            }
            response = requests.get(url, params = params)
            time.sleep(1)
            data = response.json()
            result = data['results'][0]
            geodata = dict()
            time.sleep(1)
            geodata['lat'] = result['geometry']['location']['lat']
            geodata['lng'] = result['geometry']['location']['lng']
            geodata['address'] = result['formatted_address']
            return geodata
        except Exception as e:
            print (e)

lblTitle = Label(root, text = 'Fare Estimate', font = ('Century Gothic',32), background="#000000", foreground = '#377ce5' )
lblTitle.pack()
lblTitle = Label(root, text = 'OLA-UBER fares at one stop.', font = ('Century Gothic',8), background="#000000", foreground = '#ffffff' )
lblTitle.pack()

empty0 = Label(root, background="#000000", height=2, width=2)
empty0.pack()
lblPick = Label(root, text = 'Enter Your Pickup Location',  font = ('Century Gothic',16), background="#000000", foreground = 'white')
lblPick.pack()

empty1 = Label(root, background="#000000", height=2, width=2)
empty1.pack()

entryPick = Entry(root)
entryPick.configure({"background": "white", "foreground":"black", "width":"70", "border":"3px"})
entryPick.pack()
#entryPick.grid(row = 3, column = 2)
empty2 = Label(root, background="#000000", height=2, width=2)
empty2.pack()

lblDrop = Label(root, text = 'Enter Your Drop Location', font = ('Century Gothic',16), background="#000000", foreground = 'white')
lblDrop.pack()
#lblDrop.grid(row = 5, column = 0)
empty3 = Label(root, background="#000000", height=2, width=2)
empty3.pack()

entryDrop = Entry(root)
entryDrop.configure({"background": "white", "foreground":"black", "width":"70", "border":"3px"})
entryDrop.pack()
#entryDrop.grid(row = 5, column = 2)
empty4 = Label(root, background="#000000", height=2, width=2)
empty4.pack()

# lblCar = Label(root, text = 'Enter cab service (Ola/Uber)', font = ('Century Gothic',16), background="#000000", foreground = 'white')
# lblCar.pack()

# empty5 = Label(root, background="#000000", height=2, width=2)
# empty5.pack()

# entryService = Entry(root)
# entryService.configure({"background": "white", "foreground":"black", "width":"70", "border":"3px"})
# entryService.pack()
#entryCar.grid(row = 7, column = 2)
empty6 = Label(root, background="#000000", height=2, width=2)
empty6.pack()

btn = Button(root, text = 'Estimate Fares', command = onClick, font = ('Century Gothic',14), background = '#000000', foreground = '#377ce5')
btn.pack()

#empty7 = Label(root, background="#000000", height=2, width=2)
#empty7.pack()

lblOutput = Label(root, height=100, width=1000, wraplength=1000, font = ('Century Gothic',16), background = '#000000', foreground = '#377ce5')
lblOutput.pack()

root.mainloop()