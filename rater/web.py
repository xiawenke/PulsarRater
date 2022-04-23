import os
import requests
import http.server
import socketserver
import re
import webbrowser
import shutil
from PIL import Image
from .rate import rate

__DIR__ = os.path.abspath('.')

class PrestoCliper:
    def __init__(self, filename, destination = False):
        if(destination == False):
            destination = __DIR__ + "/psr_cache"
            
        if(os.path.isdir(destination) == False):
            os.mkdir(destination)
            
        self.fileExportName = filename.split("/")[-1]
        
        self.best_pulse(filename, destination)
        '''
        self.best_pulse2(filename, destination)
        self.information(filename, destination)
        self.frequency_subband(filename, destination)
        self.dispersion_measurement(filename, destination)
        self.period(filename, destination)
        self.period_derivative(filename, destination)
        '''
        
    def clip(self, left, upper, right, lower, filename = "example.jpg", savename = "example_best_pulse.jpg"):
        img = Image.open(filename)
        cropped = img.crop((img.size[0] * left, img.size[1] * upper, img.size[0] * right, img.size[1] * lower))  # (left, upper, right, lower)
        cropped.save(savename)

    def best_pulse(self, filename, destination):
        self.clip(0, 0, .28, .29, filename, destination + "/" + self.fileExportName + "_best_pulse.jpg")
    # best_pulse("example.jpg")

    def best_pulse2(self, filename, destination):
        self.clip(.0, .26, .40, .99, filename, destination + "/" + self.fileExportName + "_best_pulse2.jpg")
    # best_pulse2("example.jpg")

    def information(self, filename, destination):
        self.clip(.28, .0, .99, .28, filename, destination + "/" + self.fileExportName + "_information.jpg")
    # information("example.jpg")

    def frequency_subband(self, filename, destination):
        self.clip(.385, .278, .70, .76, filename, destination + "/" + self.fileExportName + "_frequency_subband.jpg")
    # frequency_subband("example.jpg")

    def dispersion_measurement(self, filename, destination):
        self.clip(.385, .743, .70, .98, filename, destination + "/" + self.fileExportName + "_dispersion_measurement.jpg")
    # dispersion_measurement("example.jpg")

    def period(self, filename, destination):
        self.clip(.70, .26, .99, .64, filename, destination + "/" + self.fileExportName + "_period.jpg")
    # period("example.jpg")

    def period_derivative(self, filename, destination):
        self.clip(.69, .64, .99, .98, filename, destination + "/" + self.fileExportName + "_period_derivative.jpg")
    # period_derivative("example.jpg")

# PrestoCliper("example.png")

class Plots:
    def __init__(self, url):
        self.tempDir = __DIR__ + "/download_cache"
        self.url = self.format_url(url)
        self.scanID = self.url.split("/")[-2]
        self.webContent = requests.get(self.url).content.decode()
        self.plotList = self.plot_list()
        
        if(os.path.isdir(self.tempDir) == False):
            os.mkdir(self.tempDir)
        
        self.plots()
        
    def format_url(self, url):
        if(url[-1] != "/"):
            url = url + "/"
        
        return url
    
    def plot_list(self):
        plotList = list()
        urls = re.compile(r'<a.+?href=\"(.+?)\".*>').findall(self.webContent)
        for thisUrl in urls:
            if("cand." in thisUrl):
                plotList.append(thisUrl)

        return plotList

    def plots(self):
        for thisPlot in self.plotList:
            open(self.tempDir + "/" + self.scanID + "-" + thisPlot, "wb").write(requests.get(self.url + thisPlot).content)

# Plots("http://venus.fandm.edu/~fcrawfor/export/pks70/S0/S00101_1/")

class PKS70():
    def __init__(self, links = False):
        self.__DIR__ = os.path.abspath('.')
        self.downloadCache = self.__DIR__ + "/download_cache"
        self.plotCache = self.__DIR__ + "/psr_cache"
        self.pulsars = self.__DIR__ + "/detected_pulsars"
        self.urls = []

        if(os.path.isdir(self.downloadCache)):
            shutil.rmtree(self.downloadCache)
            
        if(os.path.isdir(self.plotCache)):
            shutil.rmtree(self.plotCache)

        if(not os.path.isdir(self.pulsars)):
            os.mkdir(self.pulsars)

        if(links == False):
            while True:
                thisInput = input("URL > ")
                if(thisInput == ""):
                    print(len(self.urls), "url(s) added:")
                    for thisUrl in self.urls:
                        print("  ", thisUrl)
                        
                    break
                else:
                    self.urls.append(thisInput)
                    print("#", len(self.urls), thisInput, "added.")
        else:
            self.urls = links
              
        # Download
        for thisUrl in self.urls:
            print("Downloading " + thisUrl + "...")
            Plots(thisUrl)

        # Clip
        plots = list()
        filelist = os.listdir(self.downloadCache)
        for filename in filelist:
            filepath = os.path.join(self.downloadCache, filename)
            if(os.path.isdir(filepath) == False):
                print("Clip: " + filepath)
                PrestoCliper(filepath)
                plots.append({"plot": filepath.split("/")[-1], "path": filepath})

        # Rate
        for thisPlot in plots:
            print("Rating: " + thisPlot["plot"], end="")
            rt = rate()
            thisRt = rt.rate(self.plotCache + "/" + thisPlot["plot"] + "_best_pulse.jpg")
            print("  ", thisRt)

            if(thisRt > 0.90):
                print("  ", thisRt, ":", thisPlot["plot"])
                shutil.copy(thisPlot["path"], self.pulsars + "/" + thisPlot["plot"])
                print("", "🟢 Signal detected in", thisPlot["plot"])