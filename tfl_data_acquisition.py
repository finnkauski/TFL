#%%
import os
os.chdir("/media/finn/lin_data/Projects/TFL/images")

class CamSession():
    global r
    global json
    global pd
    global urllib
    
    import requests as r
    import json
    import pandas as pd
    import urllib
    

    url = "https://api.tfl.gov.uk/Place/Type/JamCam"
        
    
    def __init__(self):
        
        self.raw_json = json.loads(r.get(self.url).text)
        
    def parse(self, cols = ["imageUrl","videoUrl"]):
        
        
        
        self.parsed_json = {
                
                di["commonName"]:
                    
                        {
                           
                            di2["key"]:
                            
                            di2["value"] if di2["key"] not in cols
                            
                            
                            else [di2["value"],di2["modified"]] 
                            
                            
                            for di2 in di["additionalProperties"]
                        
                        }
                            
                            for di in self.raw_json
                
                }
        
        self.parsed_df = pd.DataFrame(self.parsed_json).T
        
        for col in cols :
            
            self.parsed_df[[col,col + "_time"]] =  pd.DataFrame(
                
                self.parsed_df[col].tolist(), index= self.parsed_df.index)
            
    
    def image_download(self, images = []):
        
        print(list(self.parsed_df.imageUrl))
        
    
    



if __name__ == "__main__":
    
    obj = CamSession()#
    obj.parse()
    result = obj.raw_json
    df = obj.parsed_df
    obj.image_download()
    
#%%

import urllib

urllib.request.urlretrieve(img,"1.jpg")

