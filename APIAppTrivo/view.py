from flask import Flask, jsonify, request, session
from main import app, db
from models import Usuario, Receita, Despesa
from flask_bcrypt import generate_password_hash, check_password_hash

@app.route('/despesa', methods=['GET'])
def get_despesa():
    if 'id_usuario' in session:
        despesas = Despesa.query.all()
        despesas_dic = []
        for despesa in despesas:
            despesa_dic = {
                'id_despesa' : despesa.id_despesa,
                'data_emissao' : despesa.data_emissao,
                'valor' : despesa.valor,
                'nome_despesa' : despesa.nome_despesa,
                'id_usuario' : despesa.id_usuario
            }
            despesas_dic.append(despesa_dic)

        return jsonify(
            mensagem='Lista de Despesas',
            despesas = despesas_dic
        )
    else:
        return jsonify({'mensagem': 'Requer Autorização'})

@app.route('/despesa', methods=['POST'])
def post_despesa():
    if 'id_usuario' in session:
        despesa = request.json

        nova_despesa = Despesa(
            id_despesa = despesa.get('id_despesa'),
            data_emissao = despesa.get('data_emissao'),
            valor = despesa.get('valor'),
            descricao = despesa.get('descricao'),
            nome_despesa = despesa.get('nome_despesa'),
            id_usuario = despesa.get('id_usuario')
        )

        db.session.add(nova_despesa)
        db.session.commit()

        return jsonify(
            mensagem='Despesa cadastrada com sucesso',
            despesa = {
                'id_despesa': nova_despesa.id_despesa,
                'data_emissao': nova_despesa.data_emissao,
                'valor': nova_despesa.valor,
                'descricao': nova_despesa.descricao,
                'nome_despesa': nova_despesa.nome_despesa,
                'id_usuario': nova_despesa.id_usuario
            }
        )
    else:
        return jsonify({'mensagem': 'Requer Autorização'})

@app.route('/receita', methods=['GET'])
def get_receita():
    if 'id_usuario' in session:
        receitas = Receita.query.all()
        receitas_dic = []
        for receita in receitas:
            receita_dic = {
                'id_receita' : receita.id_receita,
                'data_emissao' : receita.data_emissao,
                'valor' : receita.valor,
                'descricao' : receita.descricao,
                'nome_receita' : receita.nome_receita,
                'id_usuario' : receita.id_usuario
            }
            receitas_dic.append(receita_dic)

        return jsonify(
            mensagem='Lista de Receitas',
            receitas = receitas_dic
        )
    else:
        return jsonify({'mensagem': 'Requer Autorização'})

@app.route('/receita', methods=['POST'])
def post_receita():
    if 'id_usuario' in session:
        receita = request.json

        nova_receita = Receita(
            id_receita = receita.get('id_receita'),
            data_emissao = receita.get('data_emissao'),
            valor = receita.get('valor'),
            descricao = receita.get('descricao'),
            nome_receita = receita.get('nome_receita'),
            id_usuario = receita.get('id_usuario')
        )

        db.session.add(nova_receita)
        db.session.commit()

        return jsonify(
            mensagem='Receita cadastrada com sucesso',
            receita = {
                'id_receita': nova_receita.id_receita,
                'data_emissao': nova_receita.data_emissao,
                'valor': nova_receita.valor,
                'descricao': nova_receita.descricao,
                'nome_receita': nova_receita.nome_receita,
                'id_usuario': nova_receita.id_usuario
            }
        )
    else:
        return jsonify({'mensagem': 'Requer Autorização'})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    senha = data.get('senha')

    # Consulta o usuário no banco de dados pelo email fornecido
    usuarios = Usuario.query.filter_by(email=email).first()
    senha = check_password_hash(usuarios.senha, senha)
    # Verifica se o e-mail está cadastrado e se a senha está correta
    if usuarios and senha:
        # Salva o email do usuário na sessão
        session['id_usuario'] = usuarios.id_usuario
        return jsonify({'mensagem': 'Login com sucesso'}), 200
    else:
        # Se as credenciais estiverem incorretas, retorna uma mensagem de erro
        return jsonify({'mensagem': 'Email ou senha inválido'})

@app.route('/CriarUser', methods=['POST'])
def criar():
    data =  request.json
    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')

    valori = Usuario.query.filter_by(nome=nome, email=email, senha=senha).first()
    if valori:
        return jsonify({'mensagem': 'Usuário ja existente'})

    else:
        senha_hash = generate_password_hash(senha).decode('utf-8')
        novo_usuario = Usuario(nome=nome, email=email, senha=senha_hash)
        db.session.add(novo_usuario)
        db.session.commit()
        return jsonify({'mensagem': 'Usuário cadastrado com sucesso'})

@app.route('/logout', methods=['POST'])
def logout():
    # Remove o email da sessão, efetivamente fazendo logout
    session.pop('id_usuario', None)
    return jsonify({'mensagem': 'Logout bem Sucedido'})

@app.route('/despesa/<int:id_despesa>', methods=['PUT'])
def put_despesa(id_despesa):
    # Verifica se o usuário está autenticado
    if 'id_usuario' in session:
        # Obtém a despesa pelo ID fornecido
        despesa = Despesa.query.get(id_despesa)

        if despesa:
            # Atualiza os dados da despesa com base nos dados enviados
            data = request.json
            despesa.data_emissao = data.get('data_emissao', despesa.data_emissao)
            despesa.valor = data.get('valor', despesa.valor)
            despesa.descricao = data.get('descricao', despesa.descricao)
            despesa.nome_despesa = data.get('nome_despesa', despesa.nome_despesa)

            # Salva as mudanças no banco de dados
            db.session.commit()

            return jsonify(
                mensagem='Despesa atualizada com sucesso',
                despesa={
                    'id_despesa': despesa.id_despesa,
                    'data_emissao': despesa.data_emissao,
                    'valor': despesa.valor,
                    'descricao': despesa.descricao,
                    'nome_despesa': despesa.nome_despesa,
                    'id_usuario': despesa.id_usuario
                }
            )

        else:
            return jsonify({'mensagem': 'Despesa não encontrada'})
    else:
        return jsonify({'mensagem': 'Requer Autorização'})

@app.route('/despesa/<int:id_despesa>', methods=['DELETE'])
def delete_despesa(id_despesa):
    # Verifica se o usuário está autenticado
    if 'id_usuario' in session:
        # Obtém a despesa pelo ID fornecido
        despesa = Despesa.query.get(id_despesa)

        if despesa:
            # Remove a despesa do banco de dados
            db.session.delete(despesa)
            db.session.commit()

            return jsonify({'mensagem': 'Despesa excluída com sucesso'})
        else:
            return jsonify({'mensagem': 'Despesa não encontrada'})
    else:
        return jsonify({'mensagem': 'Requer Autorização'})

@app.route('/receita/<int:id_receita>', methods=['PUT'])
def put_receita(id_receita):
    # Verifica se o usuário está autenticado
    if 'id_usuario' in session:
        # Obtém a receita pelo ID fornecido
        receita = Receita.query.get(id_receita)

        if receita:
            # Atualiza os dados da receita com base nos dados enviados
            data = request.json
            receita.data_emissao = data.get('data_emissao', receita.data_emissao)
            receita.valor = data.get('valor', receita.valor)
            receita.descricao = data.get('descricao', receita.descricao)
            receita.nome_receita = data.get('nome_receita', receita.nome_receita)

            # Salva as mudanças no banco de dados
            db.session.commit()

            return jsonify(
                mensagem='Receita atualizada com sucesso',
                receita={
                    'id_receita': receita.id_receita,
                    'data_emissao': receita.data_emissao,
                    'valor': receita.valor,
                    'descricao': receita.descricao,
                    'nome_receita': receita.nome_receita,
                    'id_usuario': receita.id_usuario
                }
            )

        else:
            return jsonify({'mensagem': 'Receita não encontrada'})
    else:
        return jsonify({'mensagem': 'Requer Autorização'})

@app.route('/receita/<int:id_receita>', methods=['DELETE'])
def delete_receita(id_receita):
    # Verifica se o usuário está autenticado
    if 'id_usuario' in session:
        # Obtém a receita pelo ID fornecido
        receita = Receita.query.get(id_receita)

        if receita:
            # Remove a receita do banco de dados
            db.session.delete(receita)
            db.session.commit()

            return jsonify({'mensagem': 'Receita excluída com sucesso'})
        else:
            return jsonify({'mensagem': 'Receita não encontrada'})
    else:
        return jsonify({'mensagem': 'Requer Autorização'})