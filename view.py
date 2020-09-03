import tkinter
from tkinter import Tk, Label, Button, Entry, IntVar, END, W, E, ttk
from tkinter.filedialog import askopenfilename
import PrepareData
from tkinter import messagebox as mb
import clustering
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import chart_studio.plotly as py
import pandas as pd
import plotly.express as px
import matplotlib.image as mpimg

class view:
    def __init__(self, master):
        self.master = master
        master.title("K Means Clustering")
        master.minsize(600, 400)
        self.addressFile = ""
        self.browseLabel = Label(master, text='Data path:')
        self.browseLabel.grid(row=1,column=0)
        self.browseBox = Entry(master,width=50)
        self.browseBox.focus_set()
        self.browseBox.grid(row=1,column=1)
        self.browswe_button = Button(master, command=self.browse, text="Browse")
        self.browswe_button.grid(row=1,column=2);
        self.clustersLabel = Label(master, text='Number of clusters k')
        self.clustersLabel.grid(row=2,column=0)
        self.ClustersBox = Entry(master)
        self.ClustersBox.focus_set()
        self.ClustersBox.grid(row=2,column=1)
        self.runsLabel = Label(master, text='Number of runs')
        self.runsLabel.grid(row=3,column=0)
        self.runsBox = Entry(master)
        self.runsBox.focus_set()
        self.runsBox.grid(row=3,column=1)
        self.preProcessor = Button(master, command=self.clean, text="Pre-process")
        self.preProcessor.grid()
        self.cluster = Button(master, command=self.cluster, text="Cluster")
        self.cluster.grid()


    # open the browser window
    def browse(self):
        filename = askopenfilename()
        self.addressFile = filename
        self.browseBox.insert(0,filename)

    # send the clean data to the clustering model and then display the results
    def cluster(self):
        if(self.wrongInput is True):
            mb.showerror("K Means Clustering", "wrong input")
        else:
            try:
                model = clustering.clustering.kmeans(self,self.df,self.ClustersBox.get(),self.runsBox.get())
                fig = plt.figure(figsize=(4, 4))
                plt.scatter(model['Social support'],model['Generosity'],c=model['clusters'], cmap='jet')
                plt.title('Generosity as a function of social support')
                plt.xlabel('social support')
                plt.ylabel('generosity')
                canvas = FigureCanvasTkAgg(fig, master=root)
                canvas.draw()
                canvas.get_tk_widget().grid(row=6, column=1, ipadx=20, ipady=20)

                newDF = self.addCodeCountries(model)
                fig = px.choropleth(newDF, locations="CODE",
                                    color="clusters",
                                    hover_name="COUNTRY",
                                    color_continuous_scale=px.colors.sequential.Plasma)

                py.sign_in('chenshor', 'vK4Ro730ZZHKIVCzFSBH')
                py.image.save_as(fig, filename='country.png')
                self.showImage()
                MsgBox = mb.askokcancel("K Means Clustering", "clustering completed successfully!")
            except ValueError:
                self.wrongInput = True

    # display the countries map
    def showImage(self):
        img = mpimg.imread('country.png')
        imgplot = plt.figure(figsize=(4, 4))
        plt.imshow(img)
        plt.title('choropleth graph')
        canvas2 = FigureCanvasTkAgg(imgplot, master=root)
        canvas2.draw()
        canvas2.get_tk_widget().grid(row=6, column=6, ipadx=20, ipady=20)

    # adds to the data the countries code for the map
    def addCodeCountries(self,model):
        df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_world_gdp_with_codes.csv')
        countries = pd.DataFrame(model)
        allCountries = pd.DataFrame(df)
        countries.rename(columns={'country':'COUNTRY'}, inplace=True)
        merged = countries.merge(allCountries,on=['COUNTRY'],how='left')
        return merged

    # cleans the data
    def clean(self):
        try:
            x = int(self.ClustersBox.get())
            y = int(self.runsBox.get())
            self.df=(PrepareData.PrepareData.cleanData(self,self.addressFile,x,y))
            if self.df is not None:
                self.wrongInput=False
                MsgBox = mb.askokcancel("K Means Clustering", "Preprocessing completed successfully!")
                if MsgBox == 'yes':
                    root.destroy()
                    self.wrongInput=False
            else:
                mb.showerror("K Means Clustering", "wrong input")
                self.wrongInput = True
        except ValueError:
            mb.showerror("K Means Clustering", "wrong input")
            self.wrongInput = True




root = Tk()
my_gui = view(root)
root.mainloop()
