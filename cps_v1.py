import requests
import time
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET

# API connection details
hostname = '172.16.200.50'
api_key = 'LUFRPT1sWkdlMGxzOUF6L2R0SXFraEk0QjNac2pxQm89Qy8zTVhBOW9ZR0xLN1pwYjNiVzdIVFA2OTJTa2JhamltRTE5eG1UZzBlRzEvTG8zSVdjOEd5TEZVWHdPYWsrRA=='  # You can generate this key from the firewall's web interface

# Function to fetch CPS data via API
def fetch_cps_data():
    url = f'https://{hostname}/api/'
    params = {
        'type': 'op',
        'cmd': '<show><session><info></info></session></show>',
        'key': api_key
    }
    
    response = requests.get(url, params=params, verify=False)
    if response.status_code == 200:
        return parse_cps_response(response.text)
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return None

# Function to parse the CPS value from the API response
def parse_cps_response(response_text):
    root = ET.fromstring(response_text)
    cps_value = root.find('.//cps').text  # Adjust the XPath based on the actual response format
    return int(cps_value)

# Function to update CPS graph in real-time
def update_graph():
    while True:
        cps_value = fetch_cps_data()
        if cps_value is not None:
            cps_data.append(cps_value)
            plt.clf()  # Clear the current plot
            plt.plot(cps_data, label='CPS')
            plt.xlabel('Time (seconds)')
            plt.ylabel('CPS')
            plt.title('Connections Per Second (CPS) Over Time')
            plt.legend()
            plt.grid(True)
            plt.pause(1)  # Pause for 1 second before fetching the next data point

# Main function
if __name__ == '__main__':
    cps_data = []
    plt.ion()  # Turn on interactive mode
    
    try:
        update_graph()
    except KeyboardInterrupt:
        print("Data collection interrupted.")
