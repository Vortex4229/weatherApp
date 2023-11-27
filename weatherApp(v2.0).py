import requests
import tkinter as tk


# for converting 24 hour time to 12 in when_entered() (outside class as it doesn't directly manipulate class items)
def time_convert_12(time):
    hour = int(time[0:2])
    if hour > 11:
        if hour == 12:
            return time + " PM"
        else:
            hour = hour - 12
            return str(hour) + time[2:5] + " PM"
    else:
        if hour == 0:
            hour = 12
            return str(hour) + time[2:5] + " AM"
        else:
            return time + " AM"


class myGUI:

    def __init__(self):
        self.root = tk.Tk()

        # creating window
        self.root.geometry("1000x600")
        self.root.resizable(False, False)
        self.root.title("Weather Application")

        # future variables
        self.city = None
        self.region = None
        self.country = None
        self.location_label = None
        self.temperature_label = None
        self.feels_like_label = None
        self.weather_description_label = None
        self.precipitation_label = None
        self.humidity_label = None
        self.cloudcover_label = None
        self.wind_label = None
        self.local_time_label = None
        self.return_button = None

        # home screen GUI
        self.label1 = tk.Label(self.root, text="Enter a City, Region, and Country:", font=('Arial', 18))
        self.label1.pack(padx=10, pady=10)

        self.label2 = tk.Label(self.root, text="City", font=('Arial', 16))
        self.label2.pack(padx=10, pady=10)

        self.city_textbox = tk.Entry(self.root, font=('Arial', 16))
        self.city_textbox.pack(padx=10)

        self.label3 = tk.Label(self.root, text="Region (State)", font=('Arial', 16))
        self.label3.pack(padx=10, pady=10)

        self.region_textbox = tk.Entry(self.root, font=('Arial', 16))
        self.region_textbox.pack(padx=10)

        self.label4 = tk.Label(self.root, text="Country", font=('Arial', 16))
        self.label4.pack(padx=10, pady=10)

        self.country_textbox = tk.Entry(self.root, font=('Arial', 16))
        self.country_textbox.pack(padx=10)

        self.enter_button = tk.Button(self.root, text="Enter", font=('Arial', 16), command=self.false_enter)
        self.enter_button.pack(padx=10, pady=10)

        self.label5 = tk.Label(self.root, text="OR", font=('Arial', 20))
        self.label5.pack(padx=20, pady=20)

        self.current_check = False

        self.current_button = tk.Button(self.root, text="Get Current Location", font=('Arial', 16),
                                        command=lambda: (self.set_true(), self.when_entered()))
        self.current_button.pack(padx=10, pady=10)

        self.root.mainloop()

    def set_true(self):
        self.current_check = True

    def false_enter(self):
        if self.city_textbox.get() == "" and self.region_textbox.get() == "" and self.country_textbox.get() == "":
            return
        else:
            self.when_entered()

    # result GUI
    def when_entered(self):
        if self.current_check:
            ip = requests.get('http://ip-api.com/json/')
            self.city = str(ip.json()['city']).replace("'", "")
            self.region = str(ip.json()['regionName']).replace("'", "")
            self.country = str(ip.json()['country']).replace("'", "")

        else:
            self.city = self.city_textbox.get()
            self.region = self.region_textbox.get()
            self.country = self.country_textbox.get()

        home_widgets = [self.label1, self.label2, self.city_textbox, self.label3, self.region_textbox, self.label4,
                        self.country_textbox, self.enter_button, self.label5, self.current_button]

        for x in range(10):
            home_widgets[x].destroy()

        query = {'query': self.city + ", " + self.region + ", " + self.country, 'access_key': '1ca7680656f01632db2c543226b44484',
                 'units': 'f'}
        weather = requests.get('http://api.weatherstack.com/current', params=query)

        self.location_label = tk.Label(self.root, text=(self.city + ", " + self.region + ", " + self.country), font=('Arial', 20))
        self.location_label.pack(padx=10)

        temperature = str(weather.json()['current']['temperature'])
        self.temperature_label = tk.Label(self.root, text=(temperature + "°F"), font=('Arial', 30))
        self.temperature_label.pack(padx=10, pady=5)

        feels_like = str(weather.json()['current']['feelslike'])
        self.feels_like_label = tk.Label(self.root, text=("Feels like " + feels_like + "°F"), font=('Arial', 18))
        self.feels_like_label.pack()

        weather_description = str(weather.json()['current']['weather_descriptions'])
        weather_description = weather_description.replace("['", "")
        weather_description = weather_description.replace("']", "")
        self.weather_description_label = tk.Label(self.root, text=weather_description, font=('Arial', 25))
        self.weather_description_label.pack(padx=10, pady=15)

        precipitation = str(weather.json()['current']['precip'])
        self.precipitation_label = tk.Label(self.root, text=(precipitation + "% chance of precipitation"),
                                            font=('Arial', 18))
        self.precipitation_label.pack(pady=5)

        humidity = str(weather.json()['current']['humidity'])
        self.humidity_label = tk.Label(self.root, text=(humidity + "% humidity"), font=('Arial', 18))
        self.humidity_label.pack(pady=5)

        cloudcover = str(weather.json()['current']['cloudcover'])
        self.cloudcover_label = tk.Label(self.root, text=(cloudcover + "% cloud coverage"), font=('Arial', 18))
        self.cloudcover_label.pack(pady=5)

        wind_speed = str(weather.json()['current']['wind_speed'])
        wind_direction = str(weather.json()['current']['wind_dir'])[0:1]
        self.wind_label = tk.Label(self.root, text=("Wind is going " + wind_direction + " at " + wind_speed + "mph"),
                                   font=('Arial', 18))
        self.wind_label.pack(pady=10)

        local_time = time_convert_12(str(weather.json()['location']['localtime'])[11:16])
        self.local_time_label = tk.Label(self.root, text="Observation Time:\n" + local_time, font=('Arial', 18))
        self.local_time_label.place(anchor=tk.N, x=890, y=530)

        self.return_button = tk.Button(self.root, text="Return to Home", font=('Arial', 16), command=self.return_to_home)
        self.return_button.place(anchor=tk.N, x=110, y=530)

    # recreates the home GUI made in __init__
    def return_to_home(self):
        result_widgets = [self.location_label, self.temperature_label, self.feels_like_label,
                          self.weather_description_label,
                          self.precipitation_label, self.humidity_label, self.cloudcover_label, self.wind_label,
                          self.local_time_label, self.return_button]

        for x in range(10):
            result_widgets[x].destroy()

        self.label1 = tk.Label(self.root, text="Enter a City, Region, and Country:", font=('Arial', 18))
        self.label1.pack(padx=10, pady=10)

        self.label2 = tk.Label(self.root, text="City", font=('Arial', 16))
        self.label2.pack(padx=10, pady=10)

        self.city_textbox = tk.Entry(self.root, font=('Arial', 16))
        self.city_textbox.pack(padx=10)

        self.label3 = tk.Label(self.root, text="Region (State)", font=('Arial', 16))
        self.label3.pack(padx=10, pady=10)

        self.region_textbox = tk.Entry(self.root, font=('Arial', 16))
        self.region_textbox.pack(padx=10)

        self.label4 = tk.Label(self.root, text="Country", font=('Arial', 16))
        self.label4.pack(padx=10, pady=10)

        self.country_textbox = tk.Entry(self.root, font=('Arial', 16))
        self.country_textbox.pack(padx=10)

        self.enter_button = tk.Button(self.root, text="Enter", font=('Arial', 16), command=self.false_enter)
        self.enter_button.pack(padx=10, pady=10)

        self.label5 = tk.Label(self.root, text="OR", font=('Arial', 20))
        self.label5.pack(padx=20, pady=20)

        self.current_check = False

        self.current_button = tk.Button(self.root, text="Get Current Location", font=('Arial', 16),
                                        command=lambda: (self.set_true(), self.when_entered()))
        self.current_button.pack(padx=10, pady=10)


myGUI()
