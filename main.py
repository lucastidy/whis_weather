import requests
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

def get_forecast():
    URL = 'https://api.openweathermap.org/data/2.5/forecast?lat=50.058592&lon=-122.957281&appid=f72f0b5a77174610a23ee37cb4d66c4a&units=metric'
    response = requests.get(URL)
    json_data = response.json()

    forecasts = []

    for forecast in json_data.get('list', []):
        time = forecast['dt_txt'].split()[1]

        if time == "12:00:00":
            forecasts.append(forecast)

    return forecasts

def update_weather_timer(root, weather_label, dropdown, selected_value):
    print("update_weather_timer called") 
    forecasts = get_forecast()

    # Populating a drop-down menu with dates
    days = [forecast['dt_txt'].split()[0] for forecast in forecasts]
    dropdown['values'] = days

    # Update weather based on selected day
    selected_day = selected_value  # Use the selected_value directly

    print("Selected Day:", selected_day)  # Debugging: Print the selected day

    if selected_day:
        for forecast in forecasts:
            forecast_date = forecast['dt_txt'].split()[0]
            if selected_day == forecast_date:
                temperature = forecast['main']['temp']
                min_temp = forecast['main']['temp_min']
                max_temp = forecast['main']['temp_max']
                feels_like = forecast['main']['feels_like']
                wind_speed = forecast['wind']['speed']
                wind_gust = forecast['wind']['gust']
                description = forecast['weather'][0]['description']
                
                weather_info = f"Temperature: {temperature}°C\n"
                weather_info += f"Min Temp: {min_temp}°C\n"
                weather_info += f"Max Temp: {max_temp}°C\n"
                weather_info += f"Feels Like: {feels_like}°C\n"
                weather_info += f"Wind Speed: {wind_speed} m/s\n"
                weather_info += f"Wind Gust: {wind_gust} m/s\n"
                weather_info += f"Description: {description}"

                weather_label.config(
                    text=weather_info,
                    font=("Arial", 14),  # Adjust the font
                    fg="#FFFFFF",  # Text color (white)
                    bg="#2E2E2E",  # Background color (dark grey)
                    padx=20, pady=20,  # Padding
                    relief=tk.RAISED,  # Add a raised border
                )               
                print("Label updated")  # Debugging: Print when label is updated
                return
    
    weather_label.config(
                    text="",
                    font=("Arial", 14),  # Adjust the font
                    fg="#FFFFFF",  # Text color (white)
                    bg="#2E2E2E",  # Background color (dark grey)
                    padx=20, pady=20,  # Padding
                    relief=tk.RAISED,  # Add a raised border
                )    

def on_dropdown_select(event, root, weather_label, dropdown):
    selected_value = dropdown.get()  # Get the selected value from the dropdown

    # Update the weather display with the selected value
    update_weather_timer(root, weather_label, dropdown, selected_value)

def main():
    root = tk.Tk()
    root.title("Whistler 5-Day Forecast")
    root.geometry("600x500")  # Updated window size
    root.configure(bg="#2E2E2E")  # Dark grey background

    style = ttk.Style()
    style.theme_use('clam')  # Modern theme
    style.configure('TCombobox', fieldbackground="#333333", background="#333333", foreground="#FFFFFF")
    style.configure('TLabel', background="#2E2E2E", foreground="#FFFFFF")

    frame = tk.Frame(root, bg="#2E2E2E", bd=2, relief=tk.RAISED)  # Add a raised border
    frame.pack(pady=30, padx=20, fill=tk.BOTH, expand=True)

    title_label = tk.Label(frame, text="Whistler Blackcomb 5-Day Forecast", font=("Arial", 20, "bold"), bg="#2E2E2E", fg="#FFFFFF")
    title_label.pack(pady=20)

    day_var = tk.StringVar(frame, "Select a day")

    dropdown = ttk.Combobox(frame, textvariable=day_var, font=("Arial", 14), height=10)
    dropdown.pack(pady=10, padx=10, fill=tk.X)

    weather_label = tk.Label(frame, text="", padx=20, pady=20, font=("Arial", 14, "italic"), fg="#FFFFFF", bg="#2E2E2E", wraplength=500, justify=tk.LEFT)
    weather_label.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

    dropdown.bind("<<ComboboxSelected>>", lambda event: on_dropdown_select(event, root, weather_label, dropdown))

    update_weather_timer(root, weather_label, dropdown, selected_value="")

    root.mainloop()

if __name__ == "__main__":
    main()
