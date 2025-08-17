import os
import requests

# Base link
img_link = 'https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/'

# Mapping circuit to country
circuit_to_country = {
    "Melbourne": "Australia",
    "Shanghai": "China",
    "Suzuka": "Japan",
    "Sakhir": "Bahrain",
    "Jeddah": "Saudi_Arabia",
    "Miami": "United_States",
    "Imola": "Italy",
    "Monte Carlo": "Monaco",
    "Barcelona": "Spain",
    "Montreal": "Canada",
    "Spielberg": "Austria",
    "Silverstone": "United_Kingdom",
    "Spa-Francorchamps": "Belgium",
    "Budapest": "Hungary",
    "Zandvoort": "Netherlands",
    "Monza": "Italy",
    "Baku": "Azerbaijan",
    "Marina Bay": "Singapore",
    "Austin": "United_States",
    "Mexico City": "Mexico",
    "Sao Paulo": "Brazil",
    "Las Vegas": "United_States",
    "Lusail": "Qatar",
    "Yas Marina": "United_Arab_Emirates"
}

# Failed: Miami, Silverstone, Baku, Las Vegas, Yas Marina

# Create a directory to save the images
os.makedirs("f1_circuit_maps", exist_ok=True)

# Download each image
for circuit, country in circuit_to_country.items():
    # Replace spaces with %20 for URLs
    country_escaped = country.replace(' ', '%20')
    img_url = f"{img_link}{country_escaped}_Circuit"

    print(f"Downloading {circuit} from {img_url}...")
    response = requests.get(img_url)

    if response.status_code == 200:
        filename = f"f1_circuit_maps/{circuit.replace(' ', '_')}.jpg"
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Saved to {filename}")
    else:
        print(f"Failed to download {circuit} (status code {response.status_code})")

print("All done!")
