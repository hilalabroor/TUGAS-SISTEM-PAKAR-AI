from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Knowledge base for rice diseases and their symptoms
DISEASES = {
    "Hawar Daun Bakteri": {
        "symptoms": ["Daun menguning", "Bercak coklat pada daun", "Daun mengering dari ujung"],
        "solution": "Gunakan bakterisida berbahan aktif streptomycin atau oxytetracycline. Lakukan rotasi tanaman dan hindari kelembaban berlebihan."
    },
    "Blas": {
        "symptoms": ["Bercak belah ketupat pada daun", "Daun menguning", "Malai padi hampa"],
        "solution": "Gunakan fungisida sistemik seperti tricyclazole atau isoprothiolane. Gunakan varietas tahan dan hindari pemupukan N berlebihan."
    },
    "Tungro": {
        "symptoms": ["Daun menguning oranye", "Pertumbuhan terhambat", "Daun menggulung"],
        "solution": "Kendalikan vektor dengan insektisida. Gunakan varietas tahan seperti Inpari 7 dan Inpari 9. Lakukan penanaman serempak."
    }
}

# List of all symptoms (unique)
ALL_SYMPTOMS = sorted(list(set(symptom for disease in DISEASES.values() for symptom in disease["symptoms"])))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diagnosa', methods=['GET', 'POST'])
def diagnosa():
    if request.method == 'POST':
        selected_symptoms = request.form.getlist('symptoms')
        results = []
        
        # Simple forward chaining
        for disease, data in DISEASES.items():
            matched_symptoms = [s for s in selected_symptoms if s in data["symptoms"]]
            if len(matched_symptoms) > 0:
                match_percentage = (len(matched_symptoms) / len(data["symptoms"])) * 100
                results.append({
                    'name': disease,
                    'match_percentage': round(match_percentage, 2),
                    'solution': data['solution']
                })
        
        # Sort by match percentage (highest first)
        results.sort(key=lambda x: x['match_percentage'], reverse=True)
        
        return render_template('result.html', results=results)
    
    return render_template('diagnosa.html', symptoms=ALL_SYMPTOMS)

@app.route('/tentang')
def tentang():
    return render_template('tentang.html')

if __name__ == '__main__':
    app.run(debug=True)
