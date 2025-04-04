from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# aqui vai ser criado o banco de dados e seus campos para ser inicializados
def init_db():
    with sqlite3.connect("database.db") as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS LIVROS (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                categoria TEXT NOT NULL,
                autor TEXT NOT NULL,
                imagem_url TEXT NOT NULL
                )''')
        print("Banco de dados está criado!")

init_db()

# aqui será a principal rota do programa
@app.route('/')
def home():
    return "Bem-vindo à API de Livros! Doe e descubra novas histórias!"

@app.route('/doar', methods=['POST'])
def doar_livro():

    data = request.get_json()

    titulo = data.get('titulo')
    categoria = data.get('categoria')
    autor = data.get('autor')
    imagem_url = data.get('imagem_url')

    if not all([titulo, categoria, autor, imagem_url]):
        return jsonify({"erro": "Todos os campos são obrigatórios"}), 400
    
    with sqlite3.connect("database.db") as conn:
        conn.execute('''
            INSERT INTO LIVROS (titulo, categoria, autor, imagem_url)
            VALUES (?, ?, ?, ?)
        ''', (data['titulo'], data['categoria'], data['autor'], data['imagem_url']))
        
        conn.commit()
    
    return jsonify({"mensagem": "Livro cadastrado com sucesso!"}), 201

#aqui será onde os livros serão consultados
@app.route('/livros', methods=['GET'])
def listar_livros():
    with sqlite3.connect("database.db") as conn:
        livros = conn.execute("SELECT * FROM livros").fetchall()

        livros_formatados = []

        for livro in livros:
            dicionario_livros = {
                "id": livro[0],
                "titulo": livro[1],
                "categoria": livro[2],
                "autor": livro[3],
                "imagem_url": livro[4]

            }
            livros_formatados.append(dicionario_livros)
    
    return jsonify(livros_formatados)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Render fornece essa variável automaticamente
    app.run(host='0.0.0.0', port=port)