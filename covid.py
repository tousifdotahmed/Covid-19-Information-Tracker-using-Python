import re
import tkinter as tk
from tkinter import messagebox
import bs4
import matplotlib.pyplot as plt
import requests
import datetime
from ttkwidgets.autocomplete import AutocompleteCombobox


def get_html_data(url):
    data = requests.get(url)
    return data


def get_covid_detail():
    url = "https://www.worldometers.info/coronavirus/"
    html_data = get_html_data(url)
    bs = bs4.BeautifulSoup(html_data.text, 'html.parser')
    info_div = bs.find("div", class_="content-inner").findAll("div", id="maincounter-wrap")
    all_detail = ""


    for i in range(3):
        text = info_div[i].find("h1", class_=None).get_text()

        count = info_div[i].find("span", class_=None).get_text()

        all_detail = all_detail + text + " " + count + "\n"


    return ("\nWorld Wide Data\n\n"+all_detail)

countbut=0
data=[]
case=[]
recover=[]
country=[]
name=""
countryplot={}
def get_country_data():
    global name
    name = textfield.get()

    url="https://worldometers.info/coronavirus/country/"+name;
    html_data = get_html_data(url)
    bs = bs4.BeautifulSoup(html_data.text, 'html.parser')

    info_div = bs.find("div", class_="content-inner").findAll("div", id="maincounter-wrap")
    all_detail = ""


    for i in range(3):
        text = info_div[i].find("h1", class_=None).get_text()

        count = info_div[i].find("span", class_=None).get_text()

        if text == 'Coronavirus Cases:':
            modi1=re.sub("[^\d\.]", "", count)
            case.append(int(modi1))


        if text == 'Deaths:':
            modi2=re.sub("[^\d\.]", "", count)
            data.append(int(modi2))

        if text == 'Recovered:':
            modi3=re.sub("[^\d\.]", "", count)
            recover.append(int(modi3))


        all_detail = all_detail + text + " " + count + "\n"

    mainlabel['text']="\n"+name.capitalize()+"\n\n"+all_detail


    return mainlabel['text']


def reload():
    new_data = get_covid_detail()
    mainlabel['text']=new_data
    time3=time()
    timeshow['text']="Update time: "+time3


def time():
    return str(datetime.datetime.now().strftime('%Y/%m/%d %H.%M.%S'))


def plotgraph():
    newdata = dict(zip(country, data))
    #print(newdata)

    countries = list(newdata.keys())
    values = list(newdata.values())

    plt.figure(figsize=(10, 5))


    plt.bar(countries, values, color='maroon',width=0.4)
    time1 = time()
    plt.xlabel("Countires")
    plt.ylabel("Death Records")
    plt.title("Death Records in graph at :"+time1)
    plt.show()
    max_key = max(newdata, key=newdata.get)

    window.option_add('*Dialog.msg.font', 'Roboto 20')
    if (len(values)>1):
        messagebox.showinfo(title="Alert",message=max_key.capitalize() + ' is in a terrible situation')


countries =[
        'us', 'india','brazil','uk', 'russia',
        'turkey ', 'france', 'germany', 'iran', 'argentina',
        'spain','italy', 'colombia', 'indonesia', 'mexico', 'poland',
        'ukraine', 'south-africa', 'netherlands ', 'philippines',
        'malaysia', 'czech-republic', 'peru','thailand','iraq','belgium','canada','romania','chile','japan',
        'bangladesh','viet-nam','israel','pakistan','serbia','sweden','austria','portugal','hungary','switzerland','jordan','greece','kazakhstan',
        'cuba','morocco','georgia','nepal','slovakia','united-arab-emirates','tunisia','bulgaria','lebanon','belarus','croatia','guatemala','ireland',
        'azerbaijan','sri-lanka','costa-rica','bolivia','saudi-arabia','denmark','ecuador','myanmar','south-korea','lithuania','panama','paraguay',
        'slovenia','venezuela','state-of-palestine','kuwait','dominican-republic','uruguay','mongolia','honduras','libya','ethiopia','moldova',
        'egypt','armenia','norway','oman','bosnia-and-herzegovina','bahrain','singapore','latvia','kenya','qatar','estonia','australia','macedonia',
        'nigeria','algeria','zambia','albania','finland','botswana','uzbekistan','kyrgyzstan','zimbabwe','montenegro','afghanistan','mozambique',
        'cyprus','ghana','namibia','uganda','cambodia','el-salvador','cameroon','rwanda','china','luxembourg','maldives','jamaica','laos',
        'trinidad-and-tobago','senegal','angola','reunion','malawi','cote-d-ivoire','democratic-republic-of-the-congo','guadeloupe','fiji','swaziland'
        'suriname','syria','french-guiana','french-polynesia','martinique','madagascar','sudan','malta','mauritania','cabo-verde','guyana','gabon',
        'papua-new-guinea','belize','guinea','barbados','togo','tanzania','haiti','benin','seychelles','somalia','bahamas','mauritius','mayotte','channel-islands',
        'timor-leste','andorra','iceland','congo','mali','curacao','nicaragua','tajikistan','taiwan','aruba','burkina-faso','brunei-darussalam','equatorial-guinea',
        'new-zealand','china-hong-kong-sar','saint-martin']


def removedup(items):
    return list(dict.fromkeys(items))



def excel():
    if len(country)==0:
        messagebox.showinfo(title="Pop UP", message="Please enter at least one country")
        reload()
    else:

        import csv

        country1=removedup(country.copy())

        case1=removedup(case.copy())

        data1=removedup(data.copy())  # as dead

        recover1=removedup(recover.copy())

        csv_file = 'Covid_details_' + str(datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')) + '.csv'


        with open(csv_file, 'w', newline="") as file:
            myFile = csv.writer(file)

            # 3 Writing the column headers
            myFile.writerow(["Countries", "Cases", "Deaths",
                             "Recovered"])
            # 4 Getting the number of rows to add

            # 5 Using for loop to write user input to the file
            for i in range(len(country1)):
                myFile.writerow([country1[i], case1[i], data1[i], recover1[i]])
            messagebox.showinfo(title="Pop UP", message="File Saved")






window = tk.Tk()
window.geometry("800x800")
window.title("Covid19 update information")
f = ("Ancona", 20,"bold")
window.config(background="#CAC5FF")


banner = tk.PhotoImage(file="covid.png")
window.iconphoto(True,banner)




tk.Label(window, text= "Covid-19 Tracker", font= f).pack(pady=5)

time2 = time()
timeshow = tk.Label(window, text= "Update time: "+time2, font= f)
timeshow.pack()

mainlabel = tk.Label(window, text = get_covid_detail(), font=f,bg='#CAC5FF',fg='#f94f74')
mainlabel.pack()

search = tk.Label(window, text = 'Search Here', font=f,bg='#CAC5FF',fg='#f94f74').pack()



textfield = AutocompleteCombobox(window,width=30,font=('Times', 18),completevalues=countries)
textfield.pack(pady=20)




def error():
    try:
        get_country_data()
        global countbut
        countbut = countbut + 1
        #print(countbut)
        global name
        country.append(name)


    except:
        messagebox.showwarning(title="WARNING",message="Wrong Input")
        countbut = countbut
        reload()



gbtn = tk.Button(window, text="Get Data", font=f, relief='solid',padx=2, command=error)
gbtn.pack(padx=6, pady=4)


rbtn = tk.Button(window, text="Reload", font=f, relief='solid', command=reload)
rbtn.pack(padx=6, pady=6)

plotbtn = tk.Button(window, text="Create graph", font=f, relief='solid', command=plotgraph)
plotbtn.pack(padx=0, pady=6)

newbtn = tk.Button(window, text="Save data", font=f, relief='solid', command=excel)
newbtn.pack(padx=6, pady=6)


window.mainloop()

