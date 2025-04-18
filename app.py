import streamlit as st
import pickle
import os
from streamlit_option_menu import option_menu
import plotly.graph_objects as go
from fpdf import FPDF
import base64

st.set_page_config(page_title="Multiple Disease Prediction", layout="wide", page_icon="🧬")

# Load models
working_dir = os.path.dirname(os.path.abspath(__file__))
diabetes_model = pickle.load(open(f'{working_dir}/saved_models/diabetes.pkl','rb'))
heart_disease_model = pickle.load(open(f'{working_dir}/saved_models/heart.pkl','rb'))
kidney_disease_model = pickle.load(open(f'{working_dir}/saved_models/kidney.pkl','rb'))

# Sidebar menu
with st.sidebar:
    selected = option_menu("Multiple Disease Prediction", 
                ['Diabetes Prediction', 'Heart Disease Prediction', 'Kidney Disease Prediction'],
                menu_icon='hospital-fill', 
                icons=['activity','heart', 'person'], 
                default_index=0)

def generate_pdf(title, result, confidence):
    # Remove emojis and non-latin characters
    result_clean = result.encode('ascii', 'ignore').decode()
    title_clean = title.encode('ascii', 'ignore').decode()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=16)
    pdf.cell(200, 10, txt=title_clean, ln=1, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Result: {result_clean}", ln=2)
    pdf.cell(200, 10, txt=f"Model Confidence: {confidence:.2f}%", ln=3)

    pdf_path = "prediction_report.pdf"
    pdf.output(pdf_path)
    return pdf_path

# -----------------------------------
# Diabetes Prediction
# -----------------------------------
if selected == 'Diabetes Prediction':
    st.title("🧬 Diabetes Prediction ")

    col1, col2, col3 = st.columns(3)

    with col1:
        Pregnancies = st.number_input("Number of Pregnancies", min_value=0)
    with col2:
        Glucose = st.number_input("Glucose Level", min_value=0)
    with col3:
        BloodPressure = st.number_input("Blood Pressure", min_value=0)
    with col1:
        SkinThickness = st.number_input("Skin Thickness", min_value=0)
    with col2:
        Insulin = st.number_input("Insulin", min_value=0)
    with col3:
        BMI = st.number_input("BMI", min_value=0.000, step=0.001, format="%.3f")
    with col1:
            DiabetesPedigreeFunction = st.number_input(
                "Diabetes Pedigree Function", 
                min_value=0.000, 
                step=0.001, 
                format="%.3f"
        )

    with col2:
        Age = st.number_input("Age", min_value=0)

    if st.button("🔍 Diabetes Test Result"):
        NewBMI_Overweight = NewBMI_Underweight = NewBMI_Obesity_1 = NewBMI_Obesity_2 = NewBMI_Obesity_3 = 0
        NewInsulinScore_Normal = NewGlucose_Low = NewGlucose_Normal = NewGlucose_Overweight = NewGlucose_Secret = 0

        if BMI <= 18.5:
            NewBMI_Underweight = 1
        elif 24.9 < BMI <= 29.9:
            NewBMI_Overweight = 1
        elif 29.9 < BMI <= 34.9:
            NewBMI_Obesity_1 = 1
        elif 34.9 < BMI <= 39.9:
            NewBMI_Obesity_2 = 1
        elif BMI > 39.9:
            NewBMI_Obesity_3 = 1

        if 16 <= Insulin <= 166:
            NewInsulinScore_Normal = 1

        if Glucose <= 70:
            NewGlucose_Low = 1
        elif 70 < Glucose <= 99:
            NewGlucose_Normal = 1
        elif 99 < Glucose <= 126:
            NewGlucose_Overweight = 1
        elif Glucose > 126:
            NewGlucose_Secret = 1

        user_input = [Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin,
                      BMI, DiabetesPedigreeFunction, Age, NewBMI_Underweight,
                      NewBMI_Overweight, NewBMI_Obesity_1, NewBMI_Obesity_2, NewBMI_Obesity_3,
                      NewInsulinScore_Normal, NewGlucose_Low, NewGlucose_Normal,
                      NewGlucose_Overweight, NewGlucose_Secret]

        prediction = diabetes_model.predict([user_input])
        probability = diabetes_model.predict_proba([user_input])[0]

        if prediction[0] == 1:
            result = "⚠️ The person **has diabetes**"
            confidence = probability[1] * 100
            st.warning(result)
        else:
            result = "✅ The person **does not have diabetes**"
            confidence = probability[0] * 100
            st.success(result)

        st.info(f"🧪 Model Confidence: {confidence:.2f}%")

        pdf_path = generate_pdf("Diabetes Prediction Report", result, confidence)
        with open(pdf_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
            href = f'<a href="data:application/pdf;base64,{base64_pdf}" download="diabetes_report.pdf">📄 Download Report as PDF</a>'
            st.markdown(href, unsafe_allow_html=True)

# Heart Disease Prediction
# -----------------------------------
if selected == 'Heart Disease Prediction':
    st.title("❤️ Heart Disease Prediction ")

    col1, col2, col3  = st.columns(3)

    with col1:
        age = st.number_input("Age", min_value=0)
    with col2:
        sex = st.number_input("Sex (1 = male, 0 = female)", min_value=0, max_value=1)
    with col3:
        cp = st.number_input("Chest Pain Type (0–3)", min_value=0, max_value=3)
    with col1:
        trestbps = st.number_input("Resting Blood Pressure", min_value=0)
    with col2:
        chol = st.number_input("Cholesterol (mg/dl)", min_value=0)
    with col3:
        fbs = st.number_input("Fasting Blood Sugar > 120 mg/dl (1 = true; 0 = false)", min_value=0, max_value=1)
    with col1:
        restecg = st.number_input("Resting ECG Results (0–2)", min_value=0, max_value=2)
    with col2:
        thalach = st.number_input("Max Heart Rate Achieved", min_value=0)
    with col3:
        exang = st.number_input("Exercise Induced Angina (1 = yes; 0 = no)", min_value=0, max_value=1)
    with col1:
        oldpeak = st.number_input("ST Depression", min_value=0.0)
    with col2:
        slope = st.number_input("Slope (0–2)", min_value=0, max_value=2)
    with col3:
        ca = st.number_input("Number of Major Vessels (0–3)", min_value=0, max_value=3)
    with col1:
        thal = st.number_input("Thal (0 = normal; 1 = fixed defect; 2 = reversible)", min_value=0, max_value=2)

    heart_disease_result = ""

    if st.button("🔍 Heart Disease Test Result"):
        user_input = [age, sex, cp, trestbps, chol, fbs, restecg,
                      thalach, exang, oldpeak, slope, ca, thal]

        prediction = heart_disease_model.predict([user_input])
        probability = heart_disease_model.predict_proba([user_input])[0]

        if prediction[0] == 1:
            result = "⚠️ This person **has heart disease**"
            st.warning(result)
            confidence = probability[1]*100
            st.markdown("💡 **Advice**: Immediate medical consultation is recommended.")
        else:
            result = "✅ This person **does not have heart disease**"
            st.success(result)
            confidence = probability[1]*100
        st.info(f"🧪 Model Confidence: {confidence:.2f}%")
        
        pdf_path = generate_pdf("Heart Prediction Report", result, confidence)
        with open(pdf_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
            href = f'<a href="data:application/pdf;base64,{base64_pdf}" download="diabetes_report.pdf">📄 Download Report as PDF</a>'
            st.markdown(href, unsafe_allow_html=True)

# -----------------------------------
# Kidney Disease Prediction
# -----------------------------------
if selected == 'Kidney Disease Prediction':
    st.title("🩺 Kidney Disease Prediction Using Machine Learning")

    fields = {
        "Age": 0, "Blood Pressure": 0, "Specific Gravity": 1.0, "Albumin": 0, "Sugar": 0,
        "Red Blood Cell": 0, "Pus Cell": 0, "Pus Cell Clumps": 0, "Bacteria": 0,
        "Blood Glucose Random": 0, "Blood Urea": 0, "Serum Creatinine": 0,
        "Sodium": 0, "Potassium": 0, "Haemoglobin": 0, "Packed Cell Volume": 0,
        "White Blood Cell Count": 0, "Red Blood Cell Count": 0, "Hypertension": 0,
        "Diabetes Mellitus": 0, "Coronary Artery Disease": 0, "Appetite": 0,
        "Peda Edema": 0, "Aanemia": 0
    }

    col_list = list(st.columns(5))
    input_values = []

    for i, (label, default_val) in enumerate(fields.items()):
        with col_list[i % 5]:
            val = st.number_input(label, value=float(default_val))
            input_values.append(val)

    kindey_diagnosis = ''

    if st.button("🔍 Kidney Test Result"):
        prediction = kidney_disease_model.predict([input_values])
        probability = kidney_disease_model.predict_proba([input_values])[0]

        if prediction[0] == 1:
            result = "⚠️ The person **has kidney disease**"
            st.warning(result)
            confidence = probability[1]*100
            st.markdown("💡 **Advice**: Consult a nephrologist and consider dietary adjustments.")
        else:
            result = "✅ The person **does not have kidney disease**"
            st.success(result)
            confidence = probability[1]*100
        st.info(f"🧪 Model Confidence: {confidence:.2f}%")
        
        pdf_path = generate_pdf("Kidney Prediction Report", result, confidence)
        with open(pdf_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
            href = f'<a href="data:application/pdf;base64,{base64_pdf}" download="diabetes_report.pdf">📄 Download Report as PDF</a>'
            st.markdown(href, unsafe_allow_html=True)