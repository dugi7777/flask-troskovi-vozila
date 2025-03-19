from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

def izracunaj_troskove(kilometraza, potrosnja, cijena_goriva, rata_kredita, osiguranje, servis, porez):
    trosak_goriva = kilometraza * (potrosnja / 100) * cijena_goriva
    godisnja_rata = rata_kredita * 12
    ukupni_trosak = godisnja_rata + trosak_goriva + osiguranje + servis + porez
    tjedni_trosak = ukupni_trosak / 52
    trosak_po_km = ukupni_trosak / kilometraza
    
    # Generiranje grafikona
    kategorije = ["Rata Kredita", "Gorivo", "Osiguranje", "Servis", "Porez"]
    vrijednosti = [godisnja_rata, trosak_goriva, osiguranje, servis, porez]
    plt.figure(figsize=(6,6))
    plt.pie(vrijednosti, labels=kategorije, autopct="%1.1f%%", startangle=140, colors=["#ff9999","#66b3ff","#99ff99","#ffcc99","#c2c2f0"])
    plt.title("Raspodjela godišnjih troškova vozila")
    
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    
    return ukupni_trosak, tjedni_trosak, trosak_po_km, plot_url

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        try:
            kilometraza = float(request.form['kilometraza'])
            potrosnja = float(request.form['potrosnja'])
            cijena_goriva = float(request.form['cijena_goriva'])
            rata_kredita = float(request.form['rata_kredita'])
            osiguranje = float(request.form['osiguranje'])
            servis = float(request.form['servis'])
            porez = float(request.form['porez'])
            
            ukupni_trosak, tjedni_trosak, trosak_po_km, plot_url = izracunaj_troskove(
                kilometraza, potrosnja, cijena_goriva, rata_kredita, osiguranje, servis, porez)
            
            return render_template('index.html', rezultat=True, ukupni_trosak=ukupni_trosak,
                                   tjedni_trosak=tjedni_trosak, trosak_po_km=trosak_po_km, plot_url=plot_url)
        except ValueError:
            return render_template('index.html', greska="Molimo unesite ispravne brojčane vrijednosti.")
    
    return render_template('index.html', rezultat=False)

if __name__ == '__main__':
    app.run(debug=True)

# HTML (templates/index.html)
html_content = '''
<!DOCTYPE html>
<html lang="hr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kalkulator troškova vozila</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
</head>
<body>
    <div class="container">
        <h1>Kalkulator troškova vozila</h1>
        <form method="POST">
            <label>Godišnja kilometraža:</label>
            <input type="text" name="kilometraza" required>
            <label>Potrošnja (L/100km):</label>
            <input type="text" name="potrosnja" required>
            <label>Trenutna cijena goriva po litri (€):</label>
            <input type="text" name="cijena_goriva" required>
            <label>Mjesečna rata kredita (€):</label>
            <input type="text" name="rata_kredita" required>
            <label>Godišnja cijena osiguranja (€):</label>
            <input type="text" name="osiguranje" required>
            <label>Godišnja cijena servisa (€):</label>
            <input type="text" name="servis" required>
            <label>Godišnji porez (€):</label>
            <input type="text" name="porez" required>
            <button type="submit">Izračunaj</button>
        </form>
        {% if rezultat %}
            <h2>Rezultati</h2>
            <p>Ukupni godišnji trošak: {{ ukupni_trosak }} €</p>
            <p>Tjedni trošak: {{ tjedni_trosak }} €</p>
            <p>Trošak po kilometru: {{ trosak_po_km }} €/km</p>
            <img src="data:image/png;base64,{{ plot_url }}" alt="Grafikon">
        {% endif %}
        {% if greska %}
            <p class="error">{{ greska }}</p>
        {% endif %}
    </div>
</body>
</html>
'''

# CSS (static/styles.css)
css_content = '''
body {
    font-family: Arial, sans-serif;
    background-color: #f4f4f4;
    text-align: center;
}
.container {
    width: 50%;
    margin: auto;
    background: white;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0px 0px 10px 0px #0000001a;
}
input, button {
    width: 90%;
    padding: 10px;
    margin: 10px 0;
    border: 1px solid #ccc;
    border-radius: 5px;
}
button {
    background-color: #28a745;
    color: white;
    font-size: 16px;
    border: none;
    cursor: pointer;
}
button:hover {
    background-color: #218838;
}
.error {
    color: red;
    font-weight: bold;
}
'''

# Spremanje HTML i CSS datoteka
with open("templates/index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

with open("static/styles.css", "w", encoding="utf-8") as f:
    f.write(css_content)
