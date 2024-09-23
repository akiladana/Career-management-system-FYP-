from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import requests
import mysql.connector
from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest

import spacy
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import gitusername_dataset, gitreponame_dataset, gitrepodetail_dataset

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import numpy as np


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render(request, 'index.html')


@csrf_exempt
def ranking_List(request):
    result = None
    if request.method == 'POST':
        category = request.POST.get('option')
        result = process_option(category)
    
    return render(request, 'rankingList.html', {'result': result})
        
def selectOption(request):
    datalist=[]
    newrowdata = []
    if request.method == 'POST':
        input_data = {key: value for key, value in request.POST.items() if key.startswith('input_')}
        if len(input_data.values())==0:
            return redirect('selectOption')
        datalist.append(input_data.values())
        
        rowdata = row_data(input_data)
        newrowdata = rankingNewList(rowdata)
        
    
    return render(request, 'selectOption.html',{'result':newrowdata})
        

def row_data(datalist):
    db_config = {
        "host": "127.0.0.1",
        "user": "root",
        "password": "Akila@123",
        "database": "test_d"
    }

    conn = mysql.connector.connect(**db_config)

    cursor = conn.cursor()
    cursor.execute("SELECT repositories, stars_count, forks_count, issues_count, pull_requests, contributors, topics FROM githubdataset")
    results  = cursor.fetchall()
    
    
        
    updtesdList=[]
    for data in datalist.values():
        data = data.lower()
        for row in results:
            if row[0] == data:
                updtesdList.append(row)
        # if gitusername_dataset.objects.filter(gitusername=data).exists():
    #     for row in results:
    #         if row[0] == data:
    #             updtesdList.append(row)
    # print(updtesdList)
    return updtesdList
            
    
def rankingNewList(name):

    db_config = {
        "host": "127.0.0.1",
        "user": "root",
        "password": "Akila@123",
        "database": "test_d"
    }

    conn = mysql.connector.connect(**db_config)

    cursor = conn.cursor()

    cursor.execute(
        "SELECT repositories, stars_count, forks_count, issues_count, pull_requests, contributors, topics FROM githubdataset")
    column_names = [i[0] for i in cursor.description]

    uresults = cursor.fetchall()

    score_s = []

    id_r = 0
    results = name
    # for row in name:
    #     for row in uresults:
    #         if row[0]==name:
    #             results.append(row)
    print(name)
    for row in results:
        sample_data = [{
            'Username': row[0],
            'Stars': row[1],
            'Forks': row[2],
            'Issues': row[3],
            'Pull Requests': row[4],
            'Contributors': row[5]
        }
        ]
        id_r = id_r + 1
        weights = {
            'Stars': 0.3,
            'Forks': 0.2,
            'Issues': 0.2,
            'Pull Requests': 0.15,
            'Contributors': 0.15
        }
        for user_data in sample_data:
            score = sum(user_data[metric] * weights[metric]
                        for metric in weights)
            user_data['Score'] = format(score, ".3f")
            score_s.append(score)

    data = pd.DataFrame(results, columns=column_names)
    data['Score'] = score_s

    X = data[['stars_count', 'forks_count',
              'issues_count', 'pull_requests', 'contributors']]
    y = data['Score']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)

    data['Predicted Score'] = model.predict(X)
    sorted_data = data.sort_values(by='Predicted Score', ascending=False)
    nuser = []
    ranked_usernames = []
    r = 0
    for idx, (_, row) in enumerate(sorted_data.iterrows(), start=1):
        usernames = row['repositories']
        try:
            parts = break_sentence_on_slash(usernames)
            username = parts[0]
            if len(parts) > 1:
                reponame = parts[1]
        except ValueError as e:
            print(e)

        if username not in nuser:
            nuser.append(username)
            r = r+1
            ranked_usernames.append(
                {'rank': r, 'username': username, 'reponame': reponame})
        if idx == 50:
            break
        
    return ranked_usernames

    # , {'ranked_usernames': ranked_usernames}
   
        
def process_option(category):

    if category == 'option1':
        name = 'Web Development'
        name2 = rankingD(name)
        return name2
    if category == 'option2':
        name = "Machine Learning"
        name2 = rankingD(name)
        return name2
    if category == 'option3':
        name = "UI-UX Development"
        name2 = rankingD(name)
        return name2
    if category == 'option4':
        name = "Mobile App Development"
        name2 = rankingD(name)
        return name2
    if category == 'option5':
        name = "IoT (Internet of Things)"
        name2 = rankingD(name)
        return name2
    if category == 'option6':
        name = "Blockchain Technology"
        name2 = rankingD(name)
        return name2
    if category == 'option7':
        name = "Cybersecurity"
        name2 = rankingD(name)
        return name2
    if category == 'option8':
        name = "Cloud Computing"
        name2 = rankingD(name)
        return name2

    # return render(request, 'rankingList.html')
# {'ranked_usernames': ranked_usernames}

    # datalist = []
    # if request.method == 'POST':
    #     # Get all inputs dynamically
    #     input_data = {key: value for key, value in request.POST.items() if key.startswith('input_')}
    #     datalist.append(input_data.values())

    #     for data in input_data.values():
    #         print(data)


def rankingD(name):

    db_config = {
        "host": "127.0.0.1",
        "user": "root",
        "password": "Akila@123",
        "database": "test_d"
    }

    conn = mysql.connector.connect(**db_config)

    cursor = conn.cursor()

    cursor.execute(
        "SELECT repositories, stars_count, forks_count, issues_count, pull_requests, contributors, topics FROM githubdataset")
    column_names = [i[0] for i in cursor.description]

    uresults = cursor.fetchall()

    score_s = []

    id_r = 0
    results = []
    for row in uresults:
        if row[6]==name:
            results.append(row)
    
    for row in results:
        sample_data = [{
            'Username': row[0],
            'Stars': row[1],
            'Forks': row[2],
            'Issues': row[3],
            'Pull Requests': row[4],
            'Contributors': row[5]
        }
        ]
        id_r = id_r + 1
        weights = {
            'Stars': 0.3,
            'Forks': 0.2,
            'Issues': 0.2,
            'Pull Requests': 0.15,
            'Contributors': 0.15
        }
        for user_data in sample_data:
            score = sum(user_data[metric] * weights[metric]
                        for metric in weights)
            user_data['Score'] = format(score, ".3f")
            score_s.append(score)

    data = pd.DataFrame(results, columns=column_names)
    data['Score'] = score_s

    X = data[['stars_count', 'forks_count',
              'issues_count', 'pull_requests', 'contributors']]
    y = data['Score']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)

    data['Predicted Score'] = model.predict(X)
    sorted_data = data.sort_values(by='Predicted Score', ascending=False)
    nuser = []
    ranked_usernames = []
    r = 0
    for idx, (_, row) in enumerate(sorted_data.iterrows(), start=1):
        usernames = row['repositories']
        try:
            parts=break_sentence_on_slash(usernames)
            username = parts[0]
            if len(parts)> 1:
                reponame = parts[1]
        except ValueError as e:
            print(e)
        
        if username not in nuser:
            nuser.append(username)
            r=r+1
            ranked_usernames.append({'rank': r, 'username': username,'reponame':reponame})
        if idx == 50:
            break


    return ranked_usernames


# def index(request):
#     return render(request, 'myapp/index.html', {'user_data': user_data})
user_data = {'name': 'antonmedv/countdown',
             'email': 'john@example.com'}
# Add more users as needed


def get_user_info(request, username):
    user_info = user_data
    print(user_info)
    return JsonResponse(user_info)

    # return render(request, 'mainb.html')


def break_sentence_on_slash(sentence):

    if not sentence:
        raise ValueError("Sentence cannot be empty.")

    parts = sentence.split('/', 1)  # Split at most once on '/'
    return parts


def signup(request):

    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if email is None:
            print(username)
            return redirect('signup')

        if User.objects.filter(username=username):
            messages.error(request, "Username already exist!")
            return redirect('signup')

        if User.objects.filter(email=email):
            messages.info(request, email)
            return redirect('signup')

        if pass1 != pass2:
            messages.error(request, "Password didn't match!")

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()

        messages.success(request, "Your account has been successfully created")

        return redirect('index')

    return render(request, 'signup.html')


def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']

        if username is None:
            return redirect(index)

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            return redirect("mainFront")
        else:
            messages.error(request, "Bad Credentials!")
            return redirect('index')

    return render(request, 'index')


def mainFront(request):

    return render(request, 'main.html')


def suggestion_List(request):
    listS = []

    if request.method == "POST":
        suggestionTopic = str(request.POST['suggestionTopic'])

        if not suggestionTopic.strip():
            return redirect("suggestionList")

        if suggestionTopic is not None:
            specTopic = topicSelection(suggestionTopic)
            print("sugest topic in return", specTopic)

            db_config = {
                "host": "127.0.0.1",
                "user": "root",
                "password": "Akila@123",
                "database": "test_d"
            }

            conn = mysql.connector.connect(**db_config)

            cursor = conn.cursor()

            cursor.execute("SELECT repositories, topics FROM githubdataset")
            column_names = [i[0] for i in cursor.description]

            results = cursor.fetchall()
            for row in results:
                reponames = row[0]
                stopic = row[1]
                if stopic == specTopic:
                    try:
                        parts=break_sentence_on_slash(reponames)
                        username = parts[0]
                        if len(parts)> 1:
                            reponame = parts[1]
                    except ValueError as e:
                        print(e)
                    listS.append(username)
                    
        
    return render(request, 'suggestionList.html', {'listS': listS})


def topicSelection(suggestionTopic):
    topics = [
        "Web Development",
        "Machine Learning",
        "UI-UX Development",
        "Mobile App Development",
        "IoT (Internet of Things)",
        "Blockchain Technology",
        "Cybersecurity",
        "Cloud Computing",
    ]

    data = {
        "Web Development": [
            "I'm a front-end developer who specializes in creating responsive web designs and user interfaces.",
            "My expertise in UX design ensures that users have a seamless and enjoyable experience on websites.",
            "I've implemented responsive web design principles to ensure websites look great on all devices.",
            "As a back-end developer, I focus on building server-side logic and database management.",
            "Creating RESTful APIs is a key part of my back-end development work.",
            "I specialize in server administration, ensuring the reliable and secure operation of web applications.",
            "I've developed full-stack web applications, from the front-end to the back-end.",
            "Web security is a top priority in my work, and I implement measures to protect against common threats.",
            "I've customized and extended content management systems (CMS) to meet specific website requirements.",
            "My e-commerce development experience includes building online stores and integrating payment gateways.",
            "I'm committed to web accessibility and ensure that websites I develop comply with WCAG standards.",
            "Web performance optimization is crucial in my work to provide a fast and efficient user experience.",
            "I conduct rigorous testing to identify and resolve issues, ensuring high-quality web applications.",
            "I've built progressive web apps (PWAs) that provide offline capabilities and app-like experiences.",
            "Single Page Applications (SPAs) are a specialty of mine, using frameworks like React to create dynamic web apps.",
            "I incorporate DevOps practices for automated deployment and continuous integration in web development.",
            "Web frameworks like Angular and Express.js are at the core of my development projects.",
            "I have a background in web design, focusing on graphic design, typography, and visual aesthetics.",
            "Web analytics and SEO are integral to my work, optimizing websites for search engines and tracking performance.",
        ],
        "Machine Learning": [
            "I specialize in supervised learning, working on classification and regression tasks.",
            "Unsupervised learning is a key focus of my work, including clustering and dimensionality reduction.",
            "Semi-supervised learning is valuable in scenarios where labeled data is limited, and I use it effectively.",
            "Reinforcement learning is a fascinating area I explore, training agents to make autonomous decisions.",
            "Deep learning is my expertise, with experience in Convolutional Neural Networks (CNNs), Recurrent Neural Networks (RNNs), and NLP.",
            "I work on computer vision projects, training models to recognize objects and patterns in images and videos.",
            "Natural Language Processing (NLP) is central to my work, and I develop models for text analysis and generation.",
            "Time series analysis is a crucial part of my work, with applications in finance, forecasting, and more.",
            "Anomaly detection is important in various industries, and I build models to identify irregular patterns in data.",
            "I'm experienced in developing recommendation systems, providing personalized content or product suggestions.",
            "Ensemble learning is a powerful technique I use, combining multiple models to improve predictions.",
            "Transfer learning is part of my workflow, reusing pre-trained models to accelerate training on new tasks.",
            "AutoML (Automated Machine Learning) is integral to my work, streamlining the ML process for efficiency.",
            "Explainable AI (XAI) is a focus in my projects, ensuring that models can provide interpretable results.",
            "I address fairness and bias in machine learning models, striving for equitable and unbiased predictions.",
            "Federated learning is an exciting area I explore, developing models that can learn from decentralized data sources.",
            "MLOps is part of my workflow, managing and deploying machine learning models in production environments.",
            "Quantum machine learning is a fascinating frontier I investigate, leveraging quantum computing for ML tasks.",
            "Causal inference is an important aspect of my work, allowing me to understand cause-and-effect relationships in data.",
            "Interpretable machine learning is a priority, and I develop models that offer transparency and explanations.",
            "Bayesian machine learning is part of my skill set, using probabilistic methods for modeling and inference.",
            "Meta-learning is a focus in my research, enabling models to learn how to learn from diverse tasks.",
            "I specialize in handling imbalanced data and anomaly detection, developing models for these challenging scenarios.",
            "Ethical AI and responsible AI are essential considerations in my work, addressing the societal and ethical implications of ML.",
            "Robotic Process Automation (RPA) is an area where I apply machine learning to automate repetitive tasks in various industries.",
            "I specialize in image processing using machine learning techniques to analyze and enhance images.",
            "Computer vision and object recognition are key aspects of my work, allowing machines to 'see' and understand images.",
            "I've developed image classification models for tasks like identifying objects in photographs.",
            "Image segmentation is a critical component of my projects, separating images into meaningful parts or regions.",
            "My work includes facial recognition and emotion detection, enabling applications in security and user experience.",
            "I use deep learning models, such as convolutional neural networks (CNNs), for image analysis and feature extraction.",
            "Medical image analysis is an area of expertise, aiding in disease diagnosis and treatment planning.",
            "I work on image generation tasks, using generative adversarial networks (GANs) to create synthetic images.",
            "Image-based anomaly detection is an important application in quality control and surveillance.",
            "I'm involved in satellite image analysis for tasks like land use classification and disaster monitoring.",
        ],

        "UI-UX Development": [
            "I specialize in visual UI design, creating captivating interfaces with a focus on aesthetics and branding.",
            "Interactive UI design is my forte, making user interfaces engaging and responsive to user interactions.",
            "I'm experienced in responsive design, ensuring that websites and applications work seamlessly on all devices.",
            "Mobile app UI design is a key focus, and I create user-friendly interfaces for both iOS and Android platforms.",
            "I'm skilled in web UI design, crafting user interfaces for websites and online platforms.",
            "Software UI design is my specialty, creating intuitive interfaces for desktop applications and enterprise software.",
            "Game UI design is an area of expertise, crafting user interfaces for video games with engaging menus and HUDs.",
            "User research is an essential part of my UX design process, gaining insights through interviews and usability testing.",
            "I focus on information architecture, organizing content to create logical and user-friendly experiences.",
            "Wireframing and prototyping are integral to my process, visualizing and testing UI designs before development.",
            "Interaction design is a key component, defining how users navigate and interact with the interface.",
            "I've developed user personas to represent and design for target user groups.",
            "Usability evaluation is a crucial step, identifying and addressing issues to enhance the user experience.",
            "Accessibility design is a priority, ensuring that interfaces are usable by individuals with disabilities.",
            "User flow design is integral to my work, mapping out user journeys and pathways through an application or website.",
            "Service design is an area of focus, considering the entire user experience and service interactions.",
            "Gamification is part of my expertise, adding game elements to non-gaming applications to boost engagement.",
            "I specialize in e-commerce UX design, creating seamless shopping experiences on websites and apps.",
            "Voice User Interface (VUI) design is my strength, designing voice-activated interfaces for various devices.",
            "I've worked on AR and VR UX design, crafting immersive experiences for augmented and virtual reality applications.",
            "Cross-platform UX design is essential in my projects, ensuring a consistent user experience across different platforms.",
            "Emotional design is a key aspect of my work, creating interfaces that evoke specific emotions and aesthetics.",
            "Internationalization and localization are integral to my work, adapting designs for diverse regions and languages.",
            "Ethical and inclusive design principles are at the core of my process, ensuring ethical and inclusive experiences for all users.",
        ],
        "Mobile App Development": [
            "I specialize in iOS development, creating mobile apps for Apple's iOS platform.",
            "Android development is my expertise, focusing on building mobile applications for the Android operating system.",
            "I'm skilled in cross-platform development, developing apps that run on both iOS and Android using frameworks like React Native.",
            "Native app development is a key focus, building apps using platform-specific languages and tools like Swift and Kotlin.",
            "I specialize in hybrid app development, creating apps using web technologies and packaging them for mobile using frameworks like Apache Cordova.",
            "Mobile game development is my forte, creating engaging and interactive games for both iOS and Android platforms.",
            "I'm experienced in mobile web development, designing and developing web-based applications optimized for mobile browsers.",
            "Augmented reality (AR) app development is an area of expertise, building apps that use AR technology to enhance the real world.",
            "I create immersive virtual reality (VR) experiences for mobile devices using VR headsets.",
            "Wearable app development is a key focus, developing apps for smartwatches and fitness trackers.",
            "I specialize in IoT app development, creating apps that interact with and control Internet of Things (IoT) devices.",
            "Location-based app development is integral to my work, using GPS and location data to provide location-specific information and services.",
            "Health and fitness app development is a priority, creating apps that monitor and analyze health and fitness data.",
            "I'm skilled in e-commerce app development, focusing on mobile shopping apps that provide a seamless buying experience.",
            "Social media app development is my expertise, creating social networking and communication apps for user interaction.",
            "I specialize in enterprise app development, developing mobile apps that enhance business productivity and operations.",
            "Gaming app development is a key focus, creating games for mobile devices, including casual, simulation, and action games.",
            "Educational app development is an area of expertise, creating apps for learning, training, and skill development.",
            "Media and entertainment app development is integral to my work, building apps for streaming, video, music, and interactive entertainment.",
            "Security and privacy in mobile development is a priority, ensuring the security and privacy of mobile apps and user data.",
            "I specialize in mobile app testing, focusing on quality assurance and testing to identify and address issues.",
            "Mobile app performance optimization is a key part of my work, enhancing app speed and performance for an improved user experience.",
            "Monetization strategies are essential in my projects, including in-app purchases and advertisements to generate revenue from mobile apps.",
            "I'm involved in mobile app marketing, promoting and marketing apps to reach a wider audience and increase downloads.",
            "Mobile app analytics is integral to my work, monitoring app usage and user behavior to make data-driven decisions for app improvement.",
        ],

        "IoT (Internet of Things)": [
            "I specialize in IoT device development, designing and building sensors and microcontrollers for various applications.",
            "IoT connectivity is a key focus of my work, using communication protocols like Wi-Fi, Bluetooth, and cellular networks to connect devices.",
            "IoT data analytics is a crucial aspect of my projects, where I analyze the data generated by IoT devices to extract valuable insights.",
            "IoT security is a top priority in my work, ensuring the protection of IoT devices and the data they transmit.",
            "I utilize IoT cloud platforms such as AWS IoT and Azure IoT to store and process data from IoT devices.",
            "IoT edge computing is integral to my projects, processing data locally on IoT devices to reduce latency and dependence on cloud services.",
            "I specialize in Industrial IoT (IIoT), applying IoT technology to industrial settings to enhance efficiency and automation.",
            "Smart cities are a focus in my work, using IoT to improve urban infrastructure and services, such as traffic management and waste disposal.",
            "Agricultural IoT is an area of expertise, where I use IoT for precision agriculture, including soil and weather monitoring.",
            "IoT in healthcare is a key focus, involving remote patient monitoring and wearable medical devices.",
            "I work on IoT solutions for retail, improving customer experiences and optimizing inventory management using IoT technology.",
            "IoT in energy and utilities is integral to my work, monitoring and optimizing energy consumption and distribution.",
            "Smart homes and IoT automation are areas of specialization, enhancing household appliances, security systems, and climate control.",
            "IoT in transportation is a priority, enhancing transportation systems with features like real-time tracking and autonomous vehicles.",
            "Environmental monitoring using IoT technology is integral to my work, tracking and mitigating environmental issues like air quality and pollution.",
            "IoT in logistics and supply chain management is a key area of expertise, improving supply chain visibility and efficiency through tracking and monitoring.",
            "I'm involved in wildlife conservation using IoT technology, tracking and protecting endangered species with innovative solutions.",
            "I specialize in integrating IoT with artificial intelligence (AI), combining IoT data with AI for autonomous decision-making and predictive analytics.",
            "Blockchain and IoT integration is a focus in my work, enhancing security and trust in IoT networks using blockchain technology.",
            "Low-Power Wide Area Network (LPWAN) IoT is a key area of expertise, implementing long-range, low-power IoT communication technologies for extended coverage.",
            "IoT standardization is a priority, participating in global efforts to develop standards for IoT device interoperability.",
        ],
        "Blockchain Technology": [
            "I specialize in cryptocurrencies, including Bitcoin and Ethereum, and their use in decentralized finance (DeFi).",
            "Smart contracts are my expertise, designing and implementing self-executing contracts with predefined rules on blockchain networks.",
            "Blockchain development is a key focus of my work, involving the creation of public, private, and consortium blockchains.",
            "Blockchain security is a top priority in my projects, ensuring the protection and integrity of blockchain networks and transactions.",
            "I'm skilled in developing decentralized applications (DApps) that run on blockchain networks and provide various decentralized services.",
            "Blockchain consensus mechanisms are integral to my work, researching and implementing algorithms like Proof of Work (PoW) and Proof of Stake (PoS).",
            "Tokenization is an area of expertise, creating and managing digital assets and tokens on blockchain networks.",
            "I've been involved in initial coin offerings (ICOs) and token sales, launching and managing fundraising campaigns using blockchain-based tokens.",
            "Blockchain interoperability is a priority, developing solutions to enable different blockchains to communicate and interact.",
            "Integrating blockchain technology into existing systems and processes is a key aspect of my work.",
            "I specialize in blockchain governance, establishing rules and decision-making processes for blockchain networks and communities.",
            "Supply chain and logistics blockchain solutions are integral to my work, providing transparent and secure tracking of goods and shipments.",
            "Identity management on the blockchain is a focus area, creating secure and decentralized solutions for identity verification.",
            "Storing and securing healthcare and medical records on blockchain networks is a key aspect of my expertise.",
            "Real estate and property records on the blockchain are a priority, ensuring secure and transparent property transactions and record-keeping.",
            "I provide blockchain-based notarization and legal services, enhancing trust and security in legal processes.",
            "Blockchain consulting is an important part of my work, offering advisory and consulting services to organizations exploring blockchain technology.",
            "I specialize in blockchain education and training, providing resources and courses to educate individuals and organizations about blockchain technology.",
            "Blockchain research and development is integral to my work, conducting research to advance the capabilities and applications of blockchain.",
            "I assist organizations in adhering to blockchain-related regulations and compliance requirements, ensuring adherence to legal standards.",
            "I leverage blockchain technology for social impact, addressing humanitarian and social challenges through blockchain solutions.",
            "Using blockchain for cross-border payments and remittances is a key focus, offering cost-effective and efficient money transfer solutions.",
            "Integrating blockchain in gaming is my expertise, including in-game assets, digital collectibles, and decentralized gaming ecosystems.",
            "Non-fungible tokens (NFTs) are an area of specialization, creating and trading unique digital assets used in art, collectibles, and gaming.",
            "I'm involved in DeFi (Decentralized Finance), creating and using blockchain-based financial services like lending, borrowing, and trading.",
        ],
        "Cybersecurity": [
            "I specialize in network security, protecting computer networks and data transmission from cyber threats.",
            "Information security is my focus, ensuring the confidentiality, integrity, and availability of sensitive data.",
            "Endpoint security is a priority, protecting individual devices from cyber threats, including computers, smartphones, and IoT devices.",
            "I ensure cloud security, securing data and applications hosted on cloud platforms and ensuring compliance with cloud security standards.",
            "Application security is a key area of expertise, identifying and addressing vulnerabilities in software applications to prevent exploitation by attackers.",
            "I specialize in identity and access management (IAM), managing user identities, permissions, and access to resources within organizations.",
            "Incident response and forensics are integral to my work, preparing for and responding to cybersecurity incidents and conducting digital forensics investigations.",
            "Security assessment and testing is a focus area, assessing and testing systems and networks for vulnerabilities and weaknesses.",
            "I gather threat intelligence, analyzing information about potential cyber threats and attackers.",
            "Security policy and compliance are a priority, developing and enforcing security policies and ensuring compliance with industry standards and regulations.",
            "I specialize in cryptography, applying cryptographic techniques to protect data and communications.",
            "Vulnerability management is a key focus, identifying, prioritizing, and mitigating vulnerabilities in systems and applications.",
            "Security operations center (SOC) operations are integral to my work, operating and monitoring a SOC to detect and respond to security incidents.",
            "Wireless security is a focus area, securing wireless networks and devices to prevent unauthorized access and data breaches.",
            "I educate and train users to recognize and avoid social engineering attacks and phishing scams, preventing cyber threats.",
            "Internet of Things (IoT) security is a priority, securing IoT devices and networks to prevent IoT-related cyber threats.",
            "Industrial control systems (ICS) security is a key area of expertise, protecting critical infrastructure systems and industrial control systems from cyberattacks.",
            "I ensure the security of mobile devices, mobile apps, and mobile data, addressing mobile device security challenges.",
            "Secure DevOps is an area of specialization, integrating security practices into the DevOps process to ensure secure software development and deployment.",
            "I leverage artificial intelligence (AI) and machine learning for threat detection and security analytics, using AI in cybersecurity.",
            "Blockchain security is a priority, ensuring the security of blockchain networks and transactions.",
            "I safeguard the security and integrity of election and voting systems, addressing election and voting system security challenges.",
            "Critical infrastructure security is integral to my work, protecting critical infrastructure such as power grids, water supply, and transportation systems from cyber threats.",
            "I educate individuals and organizations about cybersecurity best practices and threats, enhancing cybersecurity awareness and training.",
            "I conduct red teaming and penetration testing, identifying vulnerabilities and weaknesses in systems through ethical hacking tests.",
        ],
        "Cloud Computing": [
            "I specialize in Infrastructure as a Service (IaaS), managing and provisioning virtualized computing resources in the cloud.",
            "Platform as a Service (PaaS) is my focus, developing and deploying applications without managing underlying infrastructure.",
            "I work with Software as a Service (SaaS), providing software applications over the internet on a subscription basis.",
            "I have experience with public clouds, utilizing services provided by third-party cloud providers over the internet.",
            "Private clouds are an area of expertise, involving cloud infrastructure exclusively for a single organization's use.",
            "Hybrid cloud solutions are a priority, combining public and private cloud resources for flexibility and scalability.",
            "I specialize in cloud-native architecture, designing applications for cloud environments with microservices and containers.",
            "Serverless computing is a focus area, running code without managing servers, using platforms like AWS Lambda and Azure Functions.",
            "I work on cloud security and compliance, ensuring data security, encryption, and regulatory compliance.",
            "Cloud migration and deployment strategies are a key area of expertise, including moving on-premises systems to the cloud.",
            "I have experience in multi-cloud and cross-cloud deployment, optimizing resources and ensuring redundancy.",
            "Cloud storage solutions are a priority, including object storage, file storage, data backup, archiving, and disaster recovery.",
            "Cloud networking is a focus, involving virtual networks, subnets, security groups, and content delivery networks (CDNs).",
            "I specialize in server and resource management, managing virtual machines and server instances in the cloud.",
            "Auto-scaling and load balancing are integral to my work for resource optimization in the cloud.",
            "Cost management and billing are a key area of expertise, including monitoring and controlling cloud costs and cost allocation in multi-cloud environments.",
            "Container orchestration, especially with Kubernetes, is a focus area for managing containerized applications.",
            "I work with cloud monitoring and management tools, utilizing them for performance monitoring, log analysis, and resource management.",
            "Automation and orchestration platforms are a priority for managing cloud resources efficiently.",
            "I specialize in serverless and Function-as-a-Service (FaaS), building and deploying serverless applications using cloud providers' services.",
            "Cloud governance and compliance are a focus, establishing policies and best practices for cloud usage and ensuring compliance with industry standards and regulations.",
            "I have experience with edge computing, extending cloud computing to the edge of the network for low-latency processing.",
            "I integrate cloud resources into DevOps practices for continuous integration and delivery (CI/CD) in cloud DevOps.",
            "Leveraging cloud services for AI and machine learning model training and deployment is an area of specialization.",
            "Managed database services like AWS RDS and Azure SQL Database are a priority in my work.",
            "I work with NoSQL databases and big data solutions in the cloud, handling large datasets and big data analytics.",
            "Cloud platforms for managing IoT device data and analytics are a key focus, combining IoT and cloud technologies.",
            "Serverless computing is an area of expertise, developing and deploying applications without managing servers using platforms like AWS Lambda and Azure Functions.",
            "Integrating blockchain technology into cloud-based solutions is a priority, ensuring the security and trust of blockchain networks in the cloud.",
        ],
    }

    labeled_data = []
    for topic, sentences in data.items():
        for sentence in sentences:
            labeled_data.append((sentence, topic))

    sentences, labels = zip(*labeled_data)
    X_train, X_test, y_train, y_test = train_test_split(
        sentences, labels, test_size=0.2)

    def preprocess_text(text):

        return text.lower().strip()

    X_train_processed = [preprocess_text(text) for text in X_train]
    X_test_processed = [preprocess_text(text) for text in X_test]

    vectorizer = TfidfVectorizer()
    X_train_features = vectorizer.fit_transform(X_train_processed)
    X_test_features = vectorizer.transform(X_test_processed)

    model = SVC()
    model.fit(X_train_features, y_train)

    y_pred = model.predict(X_test_features)

    def identify_topic(sentence):
        sentence_processed = preprocess_text(sentence)
        sentence_features = vectorizer.transform([sentence_processed])
        predicted_topic = model.predict(sentence_features)[0]
        return predicted_topic

    sample_sentence = suggestionTopic
    predicted_topic = identify_topic(sample_sentence)
    # print(f"Predicted Topic: {predicted_topic}")
    return predicted_topic


def gitdetail(request):
    if request.method == 'POST':
        gitusername = request.POST.get('gitusername')

        username = getusername(request)

        if gitusername is None:
            return redirect('gitdetail')

        if gitusername_dataset.objects.filter(username=username).exists():
            return redirect('gitdetail')
        else:
            users = gitusername_dataset(
                username=username, gitusername=gitusername)
            users.save()
            get_github_repositories(gitusername)

    return render(request, 'gitdetail.html')


def getusername(request):
    username = request.user.username
    return username


def get_github_repositories(username):
    url = f'https://api.github.com/users/{username}/repos'

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx HTTP status codes
        repositories = response.json()

        # Extract and print repository names
        repo_names = [repo['name'] for repo in repositories]
        print(f"Repositories for {username}:")
        for repo_name in repo_names:
            print(repo_name)
            users = gitreponame_dataset(
                username=username, repositories=repo_name)
            users.save()
            get_repo_details(repo_name)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching repositories: {e}")


def get_repo_details(request):
    username = getusername(request)
    response = requests.get(f"https://api.github.com/repos/{username}")
    if response.status_code == 200:
        repositories = response.json()
        print(repositories)


def myprofile(request):
    usernamee = extract_data(request)
    name = extract_name(request)

    # user_data = gitreponame_dataset.objects.get(username=username)
    # for row in user_data:
    #     print(row)
    users = gitreponame_dataset.objects.filter(username__isnull=False)

    git_reponames = []
    for user in users:
        if usernamee == user.username:
            git_reponames.append(
                user.repositories) if user.repositories else None

    # context = {'repos': repos}
    # username ={'username': username}
    return render(request, 'myprofile.html', {'git_reponames': git_reponames, 'username': usernamee, 'name': name})


def extract_data(request):
    username = getusername(request)
    try:
        # Fetch the user object based on username
        user = gitusername_dataset.objects.get(username=username)
        gitusername = user.gitusername
    except gitusername_dataset.DoesNotExist:
        gitusername = None
    return (gitusername)


def extract_name(request):
    username = getusername(request)
    try:
        # Fetch the user object based on username
        user = User.objects.get(username=username)
        name1 = user.first_name
        name2 = user.last_name
    except User.DoesNotExist:
        name1 = None
        name2 = None
    fname = name1.upper()+" " + name2.upper()
    return (fname)


# def jobposting(request):
#     return render(request, 'jobposting.html')

from .models import Job, JobForm

def create_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('jobposting')
    else:
        form = JobForm()
    return render(request, 'create_job.html', {'form': form})

def jobposting(request):
    jobs = Job.objects.all()
    return render(request, 'jobposting.html', {'jobs': jobs})

def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if request.method == 'POST':
        job.delete()
        return redirect('jobposting')
    return render(request, 'confirm_delete.html', {'job': job})

def testJb(request):
    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('jobposting')
    else:
        form = JobForm()
    return render (request, 'testJb.html', {'form': form})