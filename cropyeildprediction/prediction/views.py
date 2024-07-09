from cv2 import Algorithm
from django.http import HttpResponse
from django.shortcuts import render
import joblib
from datetime import timedelta,date

CROP_NAME= {"Rice":0,"Wheat":1,"Mung Bean":2,"Tea":3,"Millet":4,"Maize":5,"Lentil":6,"Jute":7,"Coffee":8,"Cotton":9,"Ground Nut":10,"Peas":11,"Rubber":12,"Sugarcane":13,"Tobacco":14,"Kidney Beans":15,"Moth Beans":16,"Coconut":17,"Black Gram":18,"Adzuki Beans":19,"Pigeon Peas":20,"Chickpea":21,"Banana":22,"Grapes":23,"Apple":24,"Mango":25,"Muskmelon":26,"Orange":27,"Papaya":28,"Pomegranate":29,"Watermelon":30}

yeild = {
    "crop": {
        0: "Rice",
        1: "Wheat",
        2: "Mung Bean",
        3: "Tea",
        4: "Millet",
        5: "Maize",
        6: "Lentil",
        7: "Jute",
        8: "Coffee",
        9: "Cotton",
        10: "Ground Nut",
        11: "Peas",
        12: "Rubber",
        13: "Sugarcane",
        14: "Tobacco",
        15: "Kidney Beans",
        16: "Moth Beans",
        17: "Coconut",
        18: "Black Gram",
        19: "Adzuki Beans",
        20: "Pigeon Peas",
        21: "Chickpea",
        22: "Banana",
        23: "Grapes",
        24: "Apple",
        25: "Mango",
        26: "Muskmelon",
        27: "Orange",
        28: "Papaya",
        29: "Pomegranate",
        30: "Watermelon",
    },
    "production": {
        0: 2700,
        1: 3411,
        2: 468,
        3: 680,
        4: 2500,
        5: 3000,
        6: 840,
        7: 2850,
        8: 950,
        9: 759,
        10: 1336,
        11: 3500,
        12: 1450,
        13: 90718,
        14: 450000,
        15: 1200,
        16: 133,
        17: 8937,
        18: 533,
        19: 533,
        20: 27000,
        21: 806,
        22: 35000,
        23: 60000,
        24: 20000,
        25: 16000,
        26: 15000,
        27: 8373,
        28: 38000,
        29: 10976,
        30: 25401,
    },
    "quantity": {
        0: "kg",
        1: "kg",
        2: "kg",
        3: "kg",
        4: "kg",
        5: "kg",
        6: "kg",
        7: "kg",
        8: "kg",
        9: "kg",
        10: "kg",
        11: "kg",
        12: "kg",
        13: "kg",
        14: "leafs",
        15: "kg",
        16: "kg",
        17: "nuts",
        18: "kg",
        19: "kg",
        20: "kg",
        21: "kg",
        22: "kg",
        23: "kg",
        24: "kg",
        25: "kg",
        26: "kg",
        27: "kg",
        28: "kg",
        29: "kg",
        30: "kg",
    },
}



datacrop = {
    "CROPNAME": {
        0: "Rice",
        1: "Wheat",
        2: "Mung Bean",
        3: "Tea",
        4: "Millet",
        5: "Maize",
        6: "Lentil",
        7: "Jute",
        8: "Coffee",
        9: "Cotton",
        10: "Ground Nut",
        11: "Peas",
        12: "Rubber",
        13: "Sugarcane",
        14: "Tobacco",
        15: "Kidney Beans",
        16: "Moth Beans",
        17: "Coconut",
        18: "Black Gram",
        19: "Adzuki Beans",
        20: "Pigeon Peas",
        21: "Chickpea",
        22: "Banana",
        23: "Grapes",
        24: "Apple",
        25: "Mango",
        26: "Muskmelon",
        27: "Orange",
        28: "Papaya",
        29: "Pomegranate",
        30: "Watermelon",
    },
    "mintime": {
        0: 90,
        1: 210,
        2: 90,
        3: 1095,
        4: 65,
        5: 110,
        6: 80,
        7: 110,
        8: 1095,
        9: 150,
        10: 40,
        11: 21,
        12: 3560,
        13: 350,
        14: 90,
        15: 25,
        16: 75,
        17: 1910,
        18: 70,
        19: 90,
        20: 90,
        21: 90,
        22: 270,
        23: 40,
        24: 130,
        25: 150,
        26: 80,
        27: 210,
        28: 240,
        29: 120,
        30: 122,
    },
    "maxtime": {
        0: 110,
        1: 240,
        2: 120,
        3: 1456,
        4: 75,
        5: 120,
        6: 110,
        7: 120,
        8: 1456,
        9: 180,
        10: 100,
        11: 30,
        12: 7120,
        13: 365,
        14: 100,
        15: 30,
        16: 90,
        17: 2000,
        18: 85,
        19: 120,
        20: 120,
        21: 120,
        22: 365,
        23: 45,
        24: 150,
        25: 180,
        26: 90,
        27: 240,
        28: 270,
        29: 130,
        30: 135,
    },
    "PESTICIDES": {
        0: "Lambda-cyhalothrin, malathion and zeta-cypermethrin",
        1: "Organochlorines, organophosphates, and synthetic pyrethroids.",
        2: "Carbaryl, sold under the brand name Sevin, is available in powder and liquid form. Powder is used to dust bean plants and is quite effective for control of beetles and most string bean insect pests. The liquid form is diluted with water and sprayed on foliage.",
        3: "Acetamaprid, chlorpyrifos, thiacloprid, imidaclopride, dicofol, methomyl, endosulfan sulfate and carbendazim were among the pesticides found in brewed cups of tea from Lipton, Twinings, Tetley and Uncle Lee's Legends of China found in Canada.",
        4: "No traditional millet farmer uses any of these. No millet crop attracts pests. Since most of the traditional millets are grown ecologically, they do not produce weeds.",
        5: "Methyl demeton 25 EC 500 ml/ha. Carbofuran 3%CG 33.3 kg/ha. Dimethoate 30 1155 ml/ha. Methyl demeton 25% EC 1000 ml/ha.",
        6: "Aphis craccivora Koch (Hemiptera: Aphididae) · Pea aphid: Acyrthosiphon pisum Haris (Hemiptera: Aphididae) · Leaf weevil: Sitona spp.",
        7: "Among the pesticides evaluated against the jute pests under field conditions,endosulfan 35 EC at 350 g a.i./ha was found to be the most effective insecticide for controlling semilooper, Bihar hairy caterpillar and myllocerus weevil. Endosulfan and fenpropathrin provided good control of yellow mite as well.",
        8: "Endosulfan (brand name Thiodan) — used against coffee cherry borer. ... Here is an article on growing coffee without endosulfan. Chlorpyrifos (brand name Dursban). A broad spectrum organophosphate used against coffee cherry borer and coffee leaf miner.",
        9: "Use Neem based insecticides like 5% Neem seed kernel extract (NSKE) and commercial Neem based formulations @ 500-600 ml/ha, starting from 45 days age of the crop or when ETL is reached.",
        10: "Monocrotophos 0.04 %, DDVP 0.05 %, Fenitrothion 0.05 %, Endosulfan 0.07 %, Carbaryl 0.2 %, Quinalphos 0.05 %.",
        11: "Using herbicides is the effective method of controlling weeds in peas cultivation.Propazine, atrazine, simazine 0.60 kg/acre gave good results in controlling the weeds peas plantation. Prometryne at 400 to 450 grams/acre was most beneficial in improving vegetative growth of the plants and yield of pods.",
        12: "Fungicides such as carbendazim (Bavistin) and mancozeb (Indofil/ Dithane M-45), used against Corynespora disease and tridemorph (Calyxim) and propiconazole (tilt), used against root diseases, could be used as per the recommendations of agricultural officers.",
        13: "Application of azospirillum gives atmospheric nitrogen to the sugarcane crop. By applying phosphobacteria crop can get undissolved phosphorous from soil without any loss. Apply azospirillum 5 kg/ha, phosphobacteria 5 kg/ha and FYM 500 kg /ha mix it and apply on 30 days after planting along the furrow and irrigated it.",
        14: "Among the pesticides that are commonly used on tobacco are the highly toxic aldicarb and chlorpyrifos. Methyl bromide, an ozone-depleting chemical slated for world-wide elimination, is often used to fumigate the soil prior to planting tobacco seedlings.",
        15: "Carbaryl, sold under the brand name Sevin, is available in powder and liquid form. Powder is used to dust bean plants and is quite effective for control of beetles and most string bean insect pests. The liquid form is diluted with water and sprayed on foliage.",
        16: "Carbaryl, sold under the brand name Sevin, is available in powder and liquid form. Powder is used to dust bean plants and is quite effective for control of beetles and most string bean insect pests. The liquid form is diluted with water and sprayed on foliage.",
        17: "Spray any one of the following :Malathion 50EC 2 ml/lit (or)Dimethoate 30 EC 1 ml/lit (or)Methyl demeton 25 EC 1 ml/lit (or)Phosphamidon 40 SL 1.25 ml/lit (or)Monocrotophos 36 WSC 1 ml/lit (or)Methomyl 25 EC 1 ml/lit",
        18: "Dimethoate 30% EC 500ml/ha.Methyl demeton 25 500ml/ha.Imidacloprid 17.8 SL 100-125 ml/ha.Thiamethoxam 25% WG 100 g/ha.",
        19: "Carbaryl, sold under the brand name Sevin, is available in powder and liquid form. Powder is used to dust bean plants and is quite effective for control of beetles and most string bean insect pests. The liquid form is diluted with water and sprayed on foliage.",
        20: "Using herbicides is the effective method of controlling weeds in peas cultivation.Propazine, atrazine, and simazine @ 0.60 kg/acre gave good results in controlling the weeds peas plantation. Prometryne at 400 to 450 grams/acre was most beneficial in improving vegetative growth of the plants and yield of pods.",
        21: "Using herbicides is the effective method of controlling weeds in peas cultivation.Propazine, atrazine, and simazine @ 0.60 kg/acre gave good results in controlling the weeds peas plantation. Prometryne at 400 to 450 grams/acre was most beneficial in improving vegetative growth of the plants and yield of pods.",
        22: "Cut the banana plant after harvest at the ground level and treat it with carbaryl (1g/liter) or chlorpyriphos (2.5 ml/lit) at the cut surface. Application of Furadan 3G @ 20 gms or Phorate 10G @ 12 gms or Neem cake @ 1/2 Kg. per pit at planting.",
        23: "There are a wide range of grape pesticides, however, including carbaryl, esfenvalerate, spinosad, permethrin, malathion and pyrethrin, SFGate pointed out. Any plant that grows on a grapevine, other than grapes, is a weed, Purdue explained.",
        24: "Horticultural oil is a well known insecticide for application during a tree's dormant period to prevent unintended harm to beneficial insects such as bees and ladybugs. ",
        25: "Cydim super; 36 g cypermethrin   400 g dimethoate per liter",
        26: "Apply Azospirillum and Phosphobacteria @ 2 kg/ha and Pseudomonas @ 2.5 kg/ha along with FYM 50 kg and neem cake 100 kg before last ploughing. Fertigation: Apply a dose of 200:100:100 kg NPK/ha throughout the cropping period through split application.",
        27: "Glyphosate is an EPA-approved herbicide used on food and non-food crops, including oranges, to help control weeds and grasses and increase yield and quality of crops. It is one of the most widely used tools in agriculture as it helps to also reduce soil erosion and enhance harvesting efficiency.",
        28: "No selective herbicides are registered for papaya crop and non-selective herbicides may be sprayed but must not come in contact with the papaya plans in any way.",
        29: "Spraying of insecticides like Dichlorvos (0.02%) or Malathion (0. 2%) with fish oil rosin soap was found to control the insect population. Application of Phorate 10G (20 g/plant) is effective in controlling the pest population in the soil.",
        30: "Dimethoate and metalaxyl were found to be the most common pesticides detected in watermelon samples from both local markets and supermarkets.",
    },
    "minwater": {
        0: 450,
        1: 450,
        2: 300,
        3: 330,
        4: 450,
        5: 500,
        6: 1168,
        7: 500,
        8: 1168,
        9: 700,
        10: 500,
        11: 350,
        12: 1168,
        13: 1800,
        14: 61,
        15: 300,
        16: 300,
        17: 2000,
        18: 650,
        19: 300,
        20: 350,
        21: 350,
        22: 1800,
        23: 742,
        24: 720,
        25: 750,
        26: 520,
        27: 1365,
        28: 2000,
        29: 952,
        30: 3640,
    },
    "maxwater": {
        0: 700,
        1: 650,
        2: 500,
        3: 350,
        4: 650,
        5: 800,
        6: 1200,
        7: 600,
        8: 1200,
        9: 1300,
        10: 700,
        11: 500,
        12: 1200,
        13: 2200,
        14: 152,
        15: 500,
        16: 500,
        17: 2200,
        18: 680,
        19: 500,
        20: 500,
        21: 500,
        22: 2000,
        23: 1342,
        24: 750,
        25: 780,
        26: 540,
        27: 1385,
        28: 2500,
        29: 980,
        30: 3720,
    },
    "SEASON": {
        0: "Winter",
        1: "Winter",
        2: "Summer",
        3: "Rainy",
        4: "Summer",
        5: "Winter",
        6: "Winter",
        7: "Summer",
        8: "Rainy",
        9: "Summer",
        10: "Summer",
        11: "Winter",
        12: "Summer",
        13: "Summer",
        14: "Winter",
        15: "Summer",
        16: "Summer",
        17: "Both Summer-Winter",
        18: "Summer",
        19: "Summer",
        20: "Winter",
        21: "Winter",
        22: "Rainy",
        23: "Summer",
        24: "Rainy",
        25: "Summer",
        26: "Summer",
        27: "Winter",
        28: "Rainy",
        29: "Rainy",
        30: "Summer",
    },
    "CARE_TAKE": {
        0: "More",
        1: "More",
        2: "More",
        3: "Medium",
        4: "More",
        5: "More",
        6: "More",
        7: "Medium",
        8: "Medium",
        9: "Medium",
        10: "Medium",
        11: "More",
        12: "Less",
        13: "Less",
        14: "Medium",
        15: "More",
        16: "More",
        17: "Less",
        18: "More",
        19: "More",
        20: "More",
        21: "More",
        22: "Medium",
        23: "Medium",
        24: "More",
        25: "Medium",
        26: "Medium",
        27: "More",
        28: "Medium",
        29: "More",
        30: "More",
    },
    "REGION": {
        0: "East-South",
        1: "North",
        2: "North-South",
        3: "South-West",
        4: "North-South",
        5: "North-South",
        6: "North",
        7: "East",
        8: "West",
        9: "North-South",
        10: "North-South",
        11: "North-West",
        12: "South ",
        13: "North-South",
        14: "South",
        15: "North-West",
        16: "North",
        17: "North-South",
        18: "North-South",
        19: "North-West",
        20: "North",
        21: "North-South",
        22: "North-South",
        23: "North-South",
        24: "North",
        25: "North-South",
        26: "North-South",
        27: "East",
        28: "South-East",
        29: "South-West",
        30: "North-South",
    },
}

types = {
28: 'Rice',
30:'Wheat',
11:'Mung Bean',
16:'Tea',
23:'Millet',
21:'Maize',
9:'Lentil',
7:'Jute',
4:'Coffee',
5:'Cotton',
6:'Ground Nut',
12:'Peas',
14:'Rubber',
15:'Sugarcane',
17:'Tobacco',
8:'Kidney Beans',
10:'Moth Beans',
3:'Coconut',
1:'Black gram',
0:'Adzuki Beans',
13:'Pigeon Peas',
2:'Chickpea',
19:'Banana',
20:'Grapes',
18:'Apple',
22:'Mango',
24:'Muskmelon',
25:'Orange',
26:'Papaya',
27:'Pomegranate',
29:'Watermelon'
}

def index(request):
    return render(request,'index.html')

def stages(request):
    return render(request,'stages.html')

def contact(request):
    return render(request,'contact.html')

def result1(request):
    if request.method=="POST":
        yeildpredict=request.POST['yeildpredict']
        measure=request.POST['measure']
        Area=request.POST['Area']
        cropto = request.POST['cropto']
    yeildpredicted = 0
    yeildpredict = int(yeildpredict)
    out = False
    if measure == '1':
        time = datacrop["maxtime"][yeildpredict]
        yeildpredicted = yeild["production"][yeildpredict]
        amount = yeild["quantity"][yeildpredict]
        result = int(Area)*int(yeildpredicted)
        out = True
        days=int(time)
        step1 = (date.today() + timedelta(days=int(days*0))).strftime('%d/%m/%Y')
        step2 = (date.today() + timedelta(days=int(days*0.1))).strftime('%d/%m/%Y')
        step3 = (date.today() + timedelta(days=int(days*0.15))).strftime('%d/%m/%Y')
        step4 = (date.today() + timedelta(days=int(days*0.35))).strftime('%d/%m/%Y')
        step5 = (date.today() + timedelta(days=int(days*0.6))).strftime('%d/%m/%Y')
        step6 = (date.today() + timedelta(days=int(days*0.9))).strftime('%d/%m/%Y')
        step7 = (date.today() + timedelta(days=int(days*0.95))).strftime('%d/%m/%Y')
        complete = (date.today() + timedelta(days=int(days*1))).strftime('%d/%m/%Y')


    
    return render(request,'result1.html',{'out':out,'result':result,'cropto':cropto,'Area':Area,'amount':amount,'time':time,'step1':step1,'step2':step2,'step3':step3,'step4':step4,'step5':step5,'step6':step6,'step7':step7,'complete':complete})


def home(request):
    return render(request,'home.html')

def analysis(request):
    return render(request,'analysis.html')

def result(request):
    data = []
    if request.method=="POST":
        temperature=request.POST['temperature']
        humidity=request.POST['humidity']
        ph=request.POST['ph']
        rainfall=request.POST['rainfall']
        algorithm=request.POST['algorithm']
        data.append(temperature)
        data.append(humidity)
        data.append(ph)
        data.append(rainfall)
        model = joblib.load('RFCCYP.sav')
        prediction = int(model.predict([data]))
        output = types[prediction]
        number = CROP_NAME[output]
        CROPNAME = datacrop["CROPNAME"][number]
        mintime = datacrop["mintime"][number]
        maxtime = datacrop["maxtime"][number]
        PESTICIDES = datacrop["PESTICIDES"][number]
        minwater = datacrop["minwater"][number]
        maxwater = datacrop["maxwater"][number]
        SEASON = datacrop["SEASON"][number]
        CARE_TAKE = datacrop["CARE_TAKE"][number]
        REGION = datacrop["REGION"][number]



    if algorithm == '1':
        model = joblib.load('RFCCYP.sav')
        Algorithm = "Random Forest Classifier @Accuracy 95%"
    elif algorithm == '2':
        model = joblib.load('DecisionTreeCYP.sav')
        Algorithm = "Decision Tree Regressor @Accuracy 90%"
    elif algorithm == '3':
        model = joblib.load('KNNCYP.sav')
        Algorithm = "K-Nearest NeighBours Classifier @Accuracy 85%"
    else:
        pass
    prediction = int(model.predict([data]))
    output = types[prediction]
    number = CROP_NAME[output]
    CROPNAME = datacrop["CROPNAME"][number]
    mintime = datacrop["mintime"][number]
    maxtime = datacrop["maxtime"][number]
    PESTICIDES = datacrop["PESTICIDES"][number]
    minwater = datacrop["minwater"][number]
    maxwater = datacrop["maxwater"][number]
    SEASON = datacrop["SEASON"][number]
    CARE_TAKE = datacrop["CARE_TAKE"][number]
    REGION = datacrop["REGION"][number]
    #return render(request,"result.html",{'output':output,'number':number})
    return render(request,"result.html",{'CROPNAME':CROPNAME,'mintime':mintime,'maxtime':maxtime,'PESTICIDES':PESTICIDES,'minwater':minwater,'maxwater':maxwater,'SEASON':SEASON,'CARE_TAKE':CARE_TAKE,'REGION':REGION,'number':number,'Algorithm':Algorithm})