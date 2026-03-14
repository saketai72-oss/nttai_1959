from flask import Flask, render_template, request, json
from cipher.caesar import CaesarCipher
from cipher.vigenere import VigenereCipher
from cipher.playfair import PlayFairCipher
app = Flask(__name__)

def clean_playfair_key(key_str):
    """Clean key for Playfair: remove non-alpha, spaces, J->I, upper."""
    cleaned = ''.join(c for c in key_str.upper().replace('J', 'I') if c.isalpha())
    return cleaned

#router routes for home page
@app.route("/")
def home():
    return render_template('index.html')

#router routes for caesar cypher
@app.route("/caesar")
def caesar():
    return render_template('caesar.html')

@app.route("/caesar/encrypt", methods=['POST'])
def caesar_encrypt():
    text = request.form['inputPlainText']
    key = int(request.form['inputKeyPlain'])
    Caesar = CaesarCipher()
    encrypted_text = Caesar.encrypt_text(text, key)
    return render_template('caesar.html', 
                           action='encrypt', 
                           text=text, 
                           key=key, 
                           result=encrypted_text)

@app.route("/caesar/decrypt", methods=['POST'])
def caesar_decrypt():
    text = request.form['inputCipherText']
    key = int(request.form['inputKeyCipher'])
    Caesar = CaesarCipher()
    decrypted_text = Caesar.decrypt_text(text, key)
    return render_template('caesar.html', 
                           action='decrypt', 
                           text=text, 
                           key=key, 
                           result=decrypted_text)

#router routes for vigenere cypher
@app.route("/vigenere")
def vigenere():
    return render_template('vigenere.html')

@app.route("/vigenere/encrypt", methods=['POST'])
def vigenere_encrypt():
    text = request.form['inputPlainText']
    key = request.form['inputKeyPlain']
    vigenere = VigenereCipher()
    encrypted_text = vigenere.vigenere_encrypt(text, key)
    return render_template('vigenere.html', 
                           action='encrypt', 
                           text=text, 
                           key=key, 
                           result=encrypted_text)

@app.route("/vigenere/decrypt", methods=['POST'])
def vigenere_decrypt():
    text = request.form['inputCipherText']
    key = request.form['inputKeyCipher']
    vigenere = VigenereCipher()
    decrypted_text = vigenere.vigenere_decrypt(text, key)
    return render_template('vigenere.html', 
                           action='decrypt', 
                           text=text, 
                           key=key, 
                           result=decrypted_text)



#router routes for playfair cypher
@app.route("/playfair")
def playfair():
    return render_template('playfair.html')

@app.route("/playfair/create_playfair_matrix", methods=['POST'])
def playfair_create_matrix_route():
    raw_key = request.form['inputKeyMatrix']
    key = clean_playfair_key(raw_key)
    playfair = PlayFairCipher()
    matrix = playfair.create_playfair_matrix(key)
    # Format matrix nicely as 5x5 grid
    matrix_str = '\n'.join([' '.join(row) for row in matrix])
    return render_template('playfair.html', 
                           action='create_matrix', 
                           key=raw_key,
                           cleaned_key=key,
                           matrix=matrix_str)
    
@app.route("/playfair/generate_key", methods=['POST'])
def playfair_generate_key_route():
    keyword = request.form.get('inputKeyword', '').upper()
    keyword = keyword.replace('J', 'I')
    keyword = ''.join(filter(str.isalpha, keyword))
    
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    result_key = []
    for char in keyword + alphabet:
        if char not in result_key:
            result_key.append(char)
            
    generated_key = ''.join(result_key)
    
    return render_template('playfair.html', 
                           action='generate_key', 
                           key=generated_key)
    
@app.route("/playfair/encrypt", methods=['POST'])
def playfair_encrypt():
    text = request.form['inputPlainText']
    raw_key = request.form['inputKeyPlain']
    key = clean_playfair_key(raw_key)
    playfair = PlayFairCipher()
    matrix = playfair.create_playfair_matrix(key)
    encrypted_text = playfair.playfair_encrypt(text, matrix)
    return render_template('playfair.html', 
                           action='encrypt', 
                           text=text, 
                           key=raw_key,
                           cleaned_key=key,
                           result=encrypted_text)

@app.route("/playfair/decrypt", methods=['POST'])
def playfair_decrypt():
    text = request.form['inputCipherText']
    raw_key = request.form['inputKeyCipher']
    key = clean_playfair_key(raw_key)
    playfair = PlayFairCipher()
    matrix = playfair.create_playfair_matrix(key)
    decrypted_text = playfair.playfair_decrypt(text, matrix)
    return render_template('playfair.html', 
                           action='decrypt', 
                           text=text, 
                           key=raw_key,
                           cleaned_key=key,
                           result=decrypted_text)
#main function
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
