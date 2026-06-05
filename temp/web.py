import streamlit as st
import datetime

st.title("Pet Insurance Application Form")

st.divider()

st.header("Policyholder")

ph_name = st.text_input("Name")

st.write("Date of Birth")
col1, col2, col3 = st.columns(3)
current_year = datetime.date.today().year

ph_day = col1.selectbox("Day", list(range(1, 32)), index=None, placeholder="Select Day")
ph_month = col2.selectbox("Month", list(range(1, 13)), index=None, placeholder="Select Month")
ph_year = col3.selectbox("Year", list(range(current_year, 1900, -1)), index=None, placeholder="Select Year")

if ph_year is not None:
    if (current_year - ph_year) < 18:
        st.error("Policyholder must be above 18 yrs old")
        st.stop()

ph_phone = st.text_input("Contact Phone Number")
ph_address = st.text_input("Address")

st.divider()

st.header("Insured Pet")

pet_name = st.text_input("Pet's Name")

st.write("Pet's Date of Birth")
col1, col2 = st.columns(2)

months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]

with col1:
    selected_month_name = st.selectbox(
        "Month", options=months, index=None, placeholder="Month"
    )

with col2:
    current_year = datetime.datetime.now().year
    years = list(range(current_year, current_year - 25, -1))
    selected_year = st.selectbox(
        "Year", options=years, index=None, placeholder="Year"
    )

# Convert to actual datetime.date object
if selected_month_name and selected_year:
    # Get the 1-indexed month number (January = 1, February = 2, etc.)
    month_number = months.index(selected_month_name) + 1

    # Create the datetime object defaulting to the 1st of the month
    pet_dob = datetime.date(year=selected_year, month=month_number, day=1)

pet_type = st.selectbox("Pet's Type", ["", "Dog", "Cat"])
breed_list = []

if pet_type != "":
    if pet_type == "Dog":
        breed_list = ["", "Mixed Breed", "Golden Retriever", "Poodle", "Other (See Annex 1)", "Banned Breeds (See Annex 1)"]
    else:
        breed_list = ["", "Mixed Breed", "Persian", "Shorthair", "Other (See Annex 1)"]

    pet_breed = st.selectbox("Pet's Breed", breed_list)

    # Fixed: Changed Annex 2 to Annex 1
    if pet_breed == "Banned Breeds (See Annex 1)":
        st.error("This breed is not covered under the policy.")
        st.stop()
    elif pet_breed == "Other (See Annex 1)":
        st.warning("Please input the breed, input unknow if you are not sure")
    

pet_sex = st.selectbox("Pet's Sex", ["", "Male", "Female"])


pet_sterilization = st.selectbox("Pet's Sterilization Status", ["", "Sterilized", "Not Sterilized"])

pet_microchip = st.selectbox("Pet's Microchip Status", ["","Implanted", "Not Implanted"])
if pet_microchip == "Implanted":
    microchip_number = st.text_input("Microchip Number")

    
pet_characteristics = st.text_area("Pet's Characteristics", max_chars=250, help="Max 250 characters (Max 40 for Chinese characters)")

pet_photo = st.file_uploader("Pet's Recent Photo", type=['png', 'jpg', 'jpeg'])

st.subheader("Medical History")

med_surgery = st.selectbox("Ever undergone any surgical procedures or biopsies?", ["No", "Yes"])
if med_surgery == "Yes":
    st.file_uploader("Please Upload Medical History (Surgery/Biopsy)")

med_ongoing = st.selectbox("Currently receiving medication, or ongoing veterinary care?", ["No", "Yes"])
if med_ongoing == "Yes":
    st.file_uploader("Please Upload Medical History (Medication/Care)")

med_congenital = st.selectbox("Been diagnosed any congenital or hereditary conditions?", ["No", "Yes"])
if med_congenital == "Yes":
    st.error("Please contact FM for more information.")
    st.stop()

med_chronic = st.selectbox("Have any chronic or recurring conditions?", ["No", "Yes"])
if med_chronic == "Yes":
    st.file_uploader("Please Upload Medical History (Chronic Conditions)")

med_accident = st.selectbox("Ever been involved in an accident resulting in injury to a person or another animal?", ["No", "Yes"])
if med_accident == "Yes":
    st.error("Please contact FM for more information.")
    st.stop()

st.divider()

st.header("Period of Insurance")

policy_start_date = st.date_input("Policy Start Date", value=datetime.date.today())

if policy_start_date is not None and pet_dob is not None:
    
    # 1. Calculate total months difference
    total_months = (policy_start_date.year - pet_dob.year) * 12 + (policy_start_date.month - pet_dob.month)
    
    # Adjust if the specific day of the month hasn't been reached yet
    if policy_start_date.day < pet_dob.day:
        total_months -= 1
        
    # 2. Convert to fractional years (e.g., 6 months = 0.5 years)
    age_in_years = total_months / 12.0
    
    # 3. Get cleanly broken down years and months for display
    display_years = total_months // 12
    display_months = total_months % 12

    # Visual confirmation for the user (Optional)
    if age_in_years >= 0:
        st.info(f"Calculated Pet Age at Start Date: {display_years} years and {display_months} months ({age_in_years:.2f} years)")
    
    # 4. Rejection Logic based on your rule (< 0.5 or > 8)
    if age_in_years < 0.5 or age_in_years > 8:
        st.error("Application Blocked: Pet must be between 6 months (0.5 years) and 8 years old at the policy start date.")
        st.stop()

st.divider()

st.header("Plan Type")

plan_type = st.selectbox("Select Plan", ["", "Pet 1", "Pet 2", "Pet 3", "Pet Premium"])

if plan_type == "Pet Premium":
    st.file_uploader("Please upload health check-up report")

if plan_type != "":
    st.caption("Monthly Premium: xxx")

st.divider()
st.button("Submit Application")