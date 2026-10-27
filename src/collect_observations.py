import json
import argparse
import requests
from pathlib import Path
from datetime import datetime


class WeatherCollector:
    def __init__(self, station, network):
        self.station = station
        self.network = network
        self.url = "https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py"
    
    
    def fetch_lastest(self):
        params = {
            "station": self.station,
            "network": self.network,
              
        }
        
        response = requests.get(
            self.url,
            params = params,
            timeout = 30,
        )
        response.raise_for_status()
        return response.text
    
    def fetch_history(self,start_time, end_time):
        #params keep same as the API documentation from IEM 
        
        params = {
            "station": self.station,
            "network": self.network, 
            "sts": start_time+"T00:00:00Z",
            "ets" : end_time+"T00:00:00Z",
            
            
        }
        
        response = requests.get(
            self.url,
            params = params,
            timeout = 30,
        )
        response.raise_for_status()
        return response.text
    
    def save_data(self, csv_text, output_path):
        path = Path(output_path)
        path.parent.mkdir(parents = True, exist_ok = True)
        
        path.write_text(csv_text, encoding= "utf-8")
        
        print(f"Data saved to: {path.resolve()}")
        
        
def main():
    
    parser = argparse.ArgumentParser(
        description="Collect weather data for a station."
    )
    
    parser.add_argument("--station",
    required=True)
    parser.add_argument("--network",
    required=True)
    
    parser.add_argument("--start_time")
    parser.add_argument("--end_time")
    parser.add_argument("--output", default=None)
    
    args = parser.parse_args()
    
    project_folder = Path(__file__).resolve().parent.parent
    if args.output is None:
        args.output  = (
            project_folder / "data" / "raw" / f"{args.station}.csv"
        )
    
    
    collector = WeatherCollector(
        station = args.station,
        network = args.network,
    )
    data = collector.fetch_history(args.start_time, args.end_time)
    
    collector.save_data(data, args.output)
        
    
if __name__ == "__main__":
    main()
        
        