import streamlit as st
import pandas as pd
import plotly.py as px
import pymongo


#TO GET CLUSTER
client = pymongo.MongoClient ('mongodb+srv://admin:Difficultpassword12345@cluster0.aaics2h.mongodb.net/?retryWrites=true&w=majority')
# client = pymongo.MongoClient (st.secrets[])

#TO GET DATABASE. CLUSTER.DB IS THE SYNTAX
db = client.test

unwanted_domains = ["gmail", "vsnl", "yahoo", "hotmail", "rediffmail", "rediff", "aol", "msn", "live", "outlook", "ymail", "mail", "indiatimes", "rocketmail", "zoho", "yandex", "inbox", "protonmail", "gmx"]
Company_names = ['De Penning & De Penning','Remfry & Sagar','KNS Partners','Lakshmi Kumaran Sridhan','LS Davar','Anand & Anand','D.P. Ahuja & Co.','LexOrbis','Patent India','Kan and Krishme','RK Dewan','Khurana & Khurana','Krishna & Shashtri','Sna-IP','IP Attorneys','HK Acharya and Company','RAHUL CHAUDHRY & PARTNERS','CSIR-NISCAIR','Groser & Groser','CHANDRAKANT M JOSHI','khuranaandkhuran','Philips','Signify','Cantwell & Co','IP India ASA','GE','AMS Shardul', 'IPHorizons']
domains = ['depenning','remfry','knspartners','lakshmisri','lsdavar','anandandanand','dpahuja','lexorbis','patentindia','kankrishme','rkdewanmail','khuranaandkhurana','krishnaandsaurastri','sna/ip','iprattorneys','hkindia','rahulchaudhry','niscair.res','groserandgroser','cmjoshi','khuranaandkhuran','philips','signify','cantwellandco','ipindiaasa','ge','amsshardul', 'iphorizons']
dict = {}
for i in range(len(Company_names)):
    dict[Company_names[i]] = domains[i]

    


def login():
    st.write("New here? Sign up")

    if st.button("Signup"):
        st.session_state.register=True
        st.experimental_rerun()

    st.header("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type='password')
    if st.button("Submit"):
        if email and password:

            user=db.users
            foundUser=user.find_one({ "email": email })

            if foundUser:
                st.session_state.loggedin=True
                st.experimental_rerun()
            
            else:
                st.error("User does not exist")
        else:
            st.error("One or more of the fields are missing")

def register():
    st.write("Have an account? Login")

    if st.button("Login"):
        st.session_state.register=False
        st.experimental_rerun()
    st.header("Register")
    firstname = st.text_input("First name")
    lastname = st.text_input("Last name")
    email = st.text_input("Email")
    # country_codes = {+91 : "India", +1 : "USA", +44 : "UK", +61 : "Australia"}
    # for country in pycountry.countries:
    #     try:
    #         country_calling_code = "+" + pycountry.phonenumbers.country_code_for_region(country.alpha_2)
    #     except:
    #         country_calling_code = ""
    #     country_codes[country_calling_code] = country.name

    #     selected_country_code = st.selectbox("Select Country Code", list(country_codes.keys()))
    #     phone_number = st.text_input("Enter Phone Number")


    password = st.text_input("Password", type='password')
    confirm_password = st.text_input("Confirm Password", type='password')
    mobile_number = st.text_input("Mobile number")

    if st.button("Submit"):
        if password == confirm_password:
            st.success("Successfully registered.")
            user=db.users
            userDocument = {
            "email": email,
            "firstname": firstname,
            "lastname": lastname,
            "mobilenum":mobile_number,
            "password":password,
            # "premium":premium
            }
            user.insert_one(userDocument)
            st.session_state.register=False
            st.experimental_rerun()
        else:
            st.error("Password and Confirm Password do not match.")

def showgraphs():
    if st.button("Logout"):
        st.session_state.register=False
        st.session_state.loggedin=False
        st.experimental_rerun()

    #TO GET COLLECTION
    patents=db.patents


    #TO FETCH DATA FROM COLLECTION
    data=patents.find()

    #FUNCTION TO REMOVE UNWNAETED DOMAINS
    # def remove_unwanted_domains(domain):
    #     if 'gmail' in domain or 'vsnl' in domain or 'yahoo' in domain or 'hotmail' in domain or 'rediffmail' in domain or 'rediff' in domain or 'aol' in domain or 'msn' in domain or 'live' in domain or 'outlook' in domain or 'ymail' in domain or 'mail' in domain or 'indiatimes' in domain or 'rocketmail' in domain or 'zoho' in domain or 'yandex' in domain or 'inbox' in domain or 'protonmail' in domain or 'gmx' in domain:
    #         return None
    #     else:
    #         return domain

    #Function to extract unique domain names and their counts
    def get_patent_agent(df):
        # Create a set to store unique domain names
        unique_domains = set()
            # Loop through each row in the DataFrame
        for _, row in df.iterrows():
            # Combine all email columns into one list
            emails = []
            for column in ["Email", "AdditionEmail", "UpdatedEmail"]:
                # Split the cell into a list of emails using the "," delimiter
                if isinstance(row[column], str):
                    # Convert email addresses to lowercase before adding them to the list
                    emails += [email.lower() for email in row[column].split(",")]
            # Create a set to store unique domains for this row
            row_domains = set()
            # Loop through each email in the list
            for email in emails:
                # Split the email into username and domain
                if "@" in email:
                    try:
                        username, domain = email.strip().split("@")
                        # Split the domain on the last dot and take the first part
                        domain = domain.rsplit(".", 1)[0]
                    except ValueError:
                        # Skip any email addresses that do not contain exactly one "@" symbol
                        continue
                    # Add the domain to the set of unique domains for this row
                    row_domains.add(domain)
            # Add the unique domains for this row to the set of all unique domains
            unique_domains.update(row_domains)

        # Create a dictionary to store the count of each unique domain name
        domain_counts = {domain: 0 for domain in unique_domains}

        # Loop through each row in the DataFrame again
        for _, row in df.iterrows():
            # Combine all email columns into one list
            emails = []
            for column in ["Email", "AdditionEmail", "UpdatedEmail"]:
                # Split the cell into a list of emails using the "," delimiter
                if isinstance(row[column], str):
                    # Convert email addresses to lowercase before adding them to the list
                    emails += [email.lower() for email in row[column].split(",")]
            # Create a set to store unique domains for this row
            row_domains = set()
            # Loop through each email in the list
            for email in emails:
                # Split the email into username and domain
                if "@" in email:
                    try:
                        username, domain = email.strip().split("@")
                        # Split the domain on the last dot and take the first part
                        domain = domain.rsplit(".", 1)[0]
                    except ValueError:
                        # Skip any email addresses that do not contain exactly one "@" symbol
                        continue
                    # Add the domain to the set of unique domains for this row
                    row_domains.add(domain)
            # Loop over the unique domains for this row
            for domain in row_domains:
                # Remove unwanted domains
                # domain = remove_unwanted_domains(domain)
                # If the domain is not None, add it to the dictionary of domain counts
                # if domain is not None:
                domain_counts[domain] = domain_counts.get(domain, 0) + 1

        # Convert the domain_counts dictionary to a DataFrame with two columns
        df_domains = pd.DataFrame(list(domain_counts.items()), columns=["Domain", "Count"])
        df_domains = df_domains.sort_values(by="Count", ascending=False)
        return df_domains


        # Check if the domain contains 'gmail' or 'vsnl', and return None if it does.
        
        # Otherwise, return the domain unchanged.   


    # x = [d['ApplicationNumber'] for d in data]
    # y = [d['ApplicationType'] for d in data]


    st.title("Patent Database (Alpha)")

    # CONVERT DATA IN JSON FORMAT TO PANDAS DATAFRAME
    df= pd.DataFrame(data)

    # df = px.data.tips()
    foi=("NO SUBJECT","")
    df = df[df['AppropriateOffice'] != "///"]


    patentNumber=st.number_input("Patent Number", value=0)

    applicationNumber=st.text_input("Application Number")

    officeLocation = st.selectbox(
        'Appropriate Office',
        (None,'MUMBAI', 'DELHI', 'KOLKATA', 'CHENNAI'), index=0)

    fieldOfInvention = st.selectbox(
        'Field Of Invention',
        (None,'PHYSICS', 'PHARMACEUTICALS', 'MECHANICAL ENGINEERING', 'TEXTILE', 'COMPUTER SCIENCE', 'BIOTECHNOLOGY', 'CHEMICAL', 'BIOMEDICAL ENGINEERING', 'GENERAL ENGINEERING', 'ELECTRICAL', 'POLYMER TECHNOLOGY', 'COMMUNICATION', 'METALLURGY','AGROCHEMICALS', 'AGRICULTURE ENGINEERING', 'MICRO BIOLOGY', 'BIO/CHEMISTRY', 'CIVIL', 'DRUG','ELECTRONICS', 'FOOD', 'TRADITIONAL KNOWLEDGE'), index=0)

    typeOfApplication = st.selectbox(
        'Patent Application Type',
        (None,'PCT NATIONAL PHASE APPLICATION', 'CONVENTIONAL APPLICATION', 'ORDINARY APPLICATION', 'DIVISIONAL PCT NATIONAL PHASE APPLICATION'), index=0)

    patentAgent = st.selectbox(
        'Patent Agent',
        (None,'De Penning & De Penning','Remfry & Sagar','KNS Partners','Lakshmi Kumaran Sridhan','LS Davar','Anand & Anand','D.P. Ahuja & Co.','LexOrbis','Patent India','Kan and Krishme','RK Dewan','Khurana & Khurana','Krishna & Shashtri','Sna-IP','IP Attorneys','HK Acharya and Company','RAHUL CHAUDHRY & PARTNERS','CSIR-NISCAIR','Groser & Groser','CHANDRAKANT M JOSHI','khuranaandkhuran','Philips','Signify','Cantwell & Co','IP India ASA','GE','AMS Shardul', 'IPHorizons'), index=0)

    granteeAddress=st.text_input("Grantee Address")

    grantTitle=st.text_input("Grant Title")

    applicantName=st.text_input("Applicant Name")

    #to read an csv file and map the data to create a dcitionary and add it to a dataframe
    # df = pd.read_csv('patent-agents\patents1.csv')
    

    #date=st.date_input("Date", value=)

    if(patentNumber):
        df = df[df['PatentNumber'] == patentNumber]

    if(applicationNumber):
        df = df[df['ApplicationNumber'] == applicationNumber]

    if(fieldOfInvention):
        # df = df[df['FieldOfInvention'].notna()]
        df = df[df['FieldOfInvention'] == fieldOfInvention]

    df.loc[df['FieldOfInvention'].isin(foi),"FieldOfInvention" ] = "Others"

    if(officeLocation):
        df = df[df['AppropriateOffice'] == officeLocation]

    if(typeOfApplication):
        df = df[df['ApplicationType'] == typeOfApplication]

    if(granteeAddress):
        df = df[df['GranteeAddress'].str.contains(granteeAddress,case=False,na=False)]

    if(grantTitle):
        df = df[df['GrantTitle'].str.contains(grantTitle,case=False,na=False)]

    if(patentAgent):
        patentAgent = dict[patentAgent]
        melted_df = pd.melt(df, value_vars=['Email', 'AdditionEmail', 'UpdatedEmail'], var_name='Column', value_name='Emails')
        df = df[melted_df['Emails'].str.contains(patentAgent,case=False,na=False)]
        # rows=df.shape[0]
        # st.header("Number of Filtered Patents:"+str(rows))
        # st.dataframe(df)

    if(applicantName):
        df = df[df['ApplicantName'].str.contains(applicantName,case=False,na=False)]


    #TO EXCLUDE ROWS WHERE CITY WAS ///

    rows=df.shape[0]
    st.header("Number of Filtered Patents:"+str(rows))


    st.dataframe(df)

    if(patentNumber == 0 and applicationNumber==""):


        if(fieldOfInvention==None):
            counts = df['FieldOfInvention'].value_counts()
            counts_df = pd.DataFrame({'FieldOfInvention': counts.index, 'Count': counts.values})

            figFieldOfInvention = px.pie(counts_df, names='FieldOfInvention', values='Count', custom_data=['FieldOfInvention', 'Count'])
            figFieldOfInvention.update_traces(hoverinfo='label+value+percent', textinfo='percent')

            figFieldOfInvention.update_traces(hovertemplate='%{customdata[0]}')

            st.subheader('Field Of Invention')
            st.plotly_chart(figFieldOfInvention)

        if(officeLocation==None):
            # figAppropriateOffice = px.pie(df, names='AppropriateOffice')
            # st.plotly_chart(figAppropriateOffice)

            counts = df['AppropriateOffice'].value_counts()
            counts_df = pd.DataFrame({'AppropriateOffice': counts.index, 'Count': counts.values})

            figAppropriateOffice = px.pie(counts_df, names='AppropriateOffice', values='Count', custom_data=['AppropriateOffice', 'Count'])
            figAppropriateOffice.update_traces(hoverinfo='label+value+percent', textinfo='percent')
            figAppropriateOffice.update_traces(hovertemplate='%{customdata[0]}')

            st.subheader('Appropriate Office')
            st.plotly_chart(figAppropriateOffice)

        if(typeOfApplication==None):
            # figTypeOfApplication = px.pie(df, names='ApplicationType')
            # st.plotly_chart(figTypeOfApplication)
            counts = df['ApplicationType'].value_counts()
            counts_df = pd.DataFrame({'ApplicationType': counts.index, 'Count': counts.values})

            figApplicationType = px.pie(counts_df, names='ApplicationType', values='Count', custom_data=['ApplicationType', 'Count'])
            figApplicationType.update_traces(hoverinfo='label+value+percent', textinfo='percent')

            figApplicationType.update_traces(hovertemplate='%{customdata[0]}')
            
            st.subheader('Type Of Application')
            st.plotly_chart(figApplicationType)
        
        if(patentAgent==None):
            # df = pd.json_normalize(data)
            patentAgent_df = get_patent_agent(df)
            other_agents = patentAgent_df[(patentAgent_df['Count'] < 0.005*patentAgent_df['Count'].sum()) | patentAgent_df['Domain'].isin(unwanted_domains)]
            patentAgent_df = patentAgent_df.drop(other_agents.index)
           #patentAgent_df = patentAgent_df.append({'Domain': 'Others', 'Count': other_agents['Count'].sum()}, ignore_index=True)

            new_df = pd.DataFrame({'Domain': ['Others'], 'Count': [other_agents['Count'].sum()]})
            patentAgent_df = pd.concat([patentAgent_df, new_df], ignore_index=True)


            figPatentAgent = px.pie(patentAgent_df, names='Domain', values='Count', custom_data=['Domain', 'Count'])
            figPatentAgent.update_traces(hoverinfo='label+value+percent', textinfo='percent')
            figPatentAgent.update_traces(hovertemplate='%{customdata[0]}')

            st.subheader('Patent Agent')
            st.plotly_chart(figPatentAgent)

            figOtherPatentAgent = px.pie(other_agents, names='Domain', values='Count', custom_data=['Domain', 'Count'])
            figOtherPatentAgent.update_traces(hoverinfo='label+value+percent', textinfo='percent')
            figOtherPatentAgent.update_traces(hovertemplate='%{customdata[0]}')
            
            st.subheader('Other Patent Agent')
            st.plotly_chart(figOtherPatentAgent)
    else:
        st.json(df.iloc[0].to_dict())



if 'loggedin' not in st.session_state or st.session_state.loggedin==False:
    if 'register' in st.session_state and st.session_state.register==True:
        register()
    else:
        login()
else:
    showgraphs()

# De Penning & De Penning
