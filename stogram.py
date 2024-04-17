import pandas as pd
import glob
import os

class Stogram():
    """Class for computing user-days from Instagram content donwloaded using the application Stogram
    from 4KDownload company 
    """
    def __init__(self,path,folder):
        """Initialize the class and defines the attributes photo-users*0

        Args:
            path (_type_): _description_
            folder (_type_): _description_
        """
        os.chdir(path)
        self.folder=folder
        self.path=path
        self.pu=self.photo_users()
        self.vu=self.video_users()

    def photo_users(self):

        
        files=glob.glob("./*.jpg")
        Dates=lambda x: x.replace(".","_").replace(" ","_").replace("/.","_").replace("/","_").split("_")[2]
        Ids= lambda x: x.replace(".","_").replace(" ","_").replace("/.","_").replace("/","_").split("_")[-3]
        Owners= lambda x: x.replace(".","_").replace(" ","_").replace("/.","_").replace("/","_").split("_")[-2]

        dates=list(map(Dates,files))
        ids=list(map(Ids,files))
        owners=list(map(Owners,files))
        dataframe=pd.DataFrame({"id":ids,"date":dates,"owner":owners})
        dataframe["SITE_NAME"]=self.folder
        dataframe["photo-count"]=1.0
        dataframe.date=pd.to_datetime(dataframe.date)
        return dataframe
        
    def print_photo_information(self):
        print("Time range from %s to %s" %(self.pu.date.min(),self.pu.date.max()))
        print("Total number of photos=",len(self.pu))
        print("Total number of unique photo owners=",len(self.pu.owner.unique()))

    def video_users(self):
        files=glob.glob("./*.mp4")
        Dates=lambda x: x.replace(".","_").replace(" ","_").replace("/.","_").replace("/","_").split("_")[2]
        Ids= lambda x: x.replace(".","_").replace(" ","_").replace("/.","_").replace("/","_").split("_")[-3]
        Owners= lambda x: x.replace(".","_").replace(" ","_").replace("/.","_").replace("/","_").split("_")[-2]

        dates=list(map(Dates,files))
        ids=list(map(Ids,files))
        owners=list(map(Owners,files))
        dataframe=pd.DataFrame({"id":ids,"date":dates,"owner":owners})
        dataframe["SITE_NAME"]=self.folder
        dataframe["video-count"]=1.0
        dataframe.date=pd.to_datetime(dataframe.date)
        return dataframe

    def print_video_information(self):
        print("Time range from %s to %s" %(self.vu.date.min(),self.vu.date.max()))
        print("Total number of videos=",len(self.vu))
        print("Total number of unique video owners=",len(self.vu.owner.unique()))
    
    def photo_user_days(self,period="D"):
        pu=self.pu
        pu.date=pu.date.dt.to_period("D")
        pud=pu.groupby(by=["date","owner","SITE_NAME"],as_index=False).mean(numeric_only=True)
        pud.date=pd.PeriodIndex(pud.date).asfreq(period)
        pud=pud.groupby(by=["date","SITE_NAME"],as_index=False).sum(numeric_only=True)
        pud.rename(columns={"photo-count":"IUD"},inplace=True)
        return pud
    
    def video_user_days(self,period="D"):
        vu=self.vu
        vu.date=vu.date.dt.to_period("D")
        vud=vu.groupby(by=["date","owner","SITE_NAME"],as_index=False).mean(numeric_only=True)
        vud.date=pd.PeriodIndex(vud.date).asfreq(period)
        vud=vud.groupby(by=["date","SITE_NAME"],as_index=False).sum(numeric_only=True)
        vud.rename(columns={"video-count":"IUD"},inplace=True)
        return vud
        



if __name__=="__main__":

    path="/home/usuario/Imágenes/4K Stogram/Islas Atlánticas de Galicia"
    
    con=Stogram(path,"Islas Atlánticas de Galicia")
    con.print_photo_information()
    con.print_video_information()
    
    pud=con.photo_user_days(period="M")
    print(pud)

    vud=con.video_user_days(period="M")
    print(vud)

    df=pd.concat([pud,vud])
    df=df.groupby(by=["date","SITE_NAME"],as_index=False).sum(numeric_only=True)
    print(df)
    
