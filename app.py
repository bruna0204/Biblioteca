from flask_pydantic_spec import FlaskPydanticSpec
import sqlalchemy
from flask import Flask, render_template, request, redirect, url_for, flash,jsonify
from sqlalchemy import select, func, desc
from sqlalchemy.exc import SQLAlchemyError

from models import Usuario, Livro, Emprestimo, local_session
from sqlalchemy import func

app = Flask(__name__)
spec = FlaskPydanticSpec('flask',
                          title='First API - SENAI',
                          version='1.0.0',)
spec.register(app)

 # corrigir

@app.route('/cadastro_usuario', methods=["POST"])
def criar_usuario():
    """
    API para cadastrar o usuario

    ### Resposta (JSON):
    '''json{
        "status": "sucesso",
        "mensagem":"Usuario criado com sucesso",
        "id": post.id_usuario,
        "nome": informacoes["nome"],
        "cpf": informacoes["CPF"],
        "endereco": informacoes["endereco"]
        }

    :return: cadastra o usuario
    """
    db_session = local_session()
    try:
        informacoes = request.get_json()
        print(informacoes)
        if not "nome" in informacoes or not "CPF" in informacoes or not "endereco" in informacoes:
            return jsonify({'status': 'erro','mensagem': 'Obrigatorio Nome, CPF e endereco'}),400

        if informacoes["endereco"] == "" or informacoes["nome"] == "" or informacoes["CPF"] == "":
            return jsonify({'status': 'erro', 'mensagem': 'Erro preencha os espaços'}),400
        #if existe_cpf:
         #   return jsonify({'status': "erro", 'mensagem': 'usuario ja existente'})

        post = Usuario(Nome = informacoes["nome"],
                        CPF = informacoes["CPF"],
                        endereco = informacoes["endereco"]

                        )
        post.save(db_session),

        return jsonify(
            {
                "status": "sucesso",
                "mensagem":"Usuario criado com sucesso",
                "id": post.id_usuario,
                "nome": informacoes["nome"],
                "cpf": informacoes["CPF"],
                "endereco": informacoes["endereco"]
            }),201

    except SQLAlchemyError as e:
        return jsonify({'status': 'erro', 'mensagem': str(e)})
    finally:
        db_session.close()
#proteger
@app.route('/lista_usuario', methods=["GET"])
def listar_usuario():
    """
        API para listar o usuario

        ### Resposta (JSON):
        '''json
        {'usuarios': lista_usuario}


        :return: a lista ou a mensagem de erro
    """
    db_session = local_session()

    try:
        sql_usuario = select(Usuario)
        result = db_session.execute(sql_usuario).scalars()
        lista_usuario = []
        for usuario in result:
            lista_usuario.append(usuario.serialize_usuarios())
        return jsonify({'usuarios': lista_usuario})
    except SQLAlchemyError as e:
        return jsonify({'status': 'erro', 'mensagem': str(e)})
    finally:
        db_session.close()

#proteger
@app.route('/atualizar_usuario/<int:id_usuario>', methods=["PUT"])
def atualizar_usuario(id_usuario):
    """
    API para atualizar o livro
    ### Resposta (JSON):
    jsonify({'status': 'sucesso'})

    :param id_usuario: id do usuario que vai ser atualizado para assim localizado
    :return: atualiza o usuario
    """
    db_session = local_session()

    try:
        usuario = db_session.execute(select(Usuario).where(Usuario.id_usuario == id_usuario)).scalar()
        if usuario is None:
            return jsonify({"status": "erro", "mensagem": "usuario não encontrado"})

        dados_usuario = request.get_json()

        usuario.Nome = dados_usuario["nome"]
        usuario.CPF = dados_usuario["CPF"]
        usuario.endereco = dados_usuario["endereco"]
        usuario.save(db_session)

        return jsonify({'status': 'sucesso'})
    except SQLAlchemyError as e:
        return jsonify({'status': 'erro', 'mensagem': str(e)})
    finally:
        db_session.close()




@app.route('/cadastrar_emprestimo', methods=["POST"])
def criar_emprestimo():
    """
        API para cadastrar o emprestimo
        verifica se os campos estão vazios
        verifia se existe o id do usuario e do livro
        e verifica se o livro ja esta emprestado

        ### Resposta (JSON):
        '''json{
            "status": "sucesso",
            "mensagem":"Emprestimo criado com sucesso",
            "data_de_emprestimo": informacoes["data_de_emprestimo"],
            "data_de_devolucao": informacoes["data_de_devolucao"],
            "id_livro": informacoes["id_livro"],
            "id_usuario": informacoes["id_usuario"]
            }

        :return: o cadastro do emprestimo dos livros
        """
    db_session = local_session()

    try:
        informacoes = request.get_json()

        print("dados :",informacoes)
        livro = db_session.execute(select(Livro).where(Livro.id_livro == informacoes["id_livro"])).scalar()
        usuario = db_session.execute(select(Usuario).where(Usuario.id_usuario == informacoes["id_usuario"])).scalar()
        print("usuarios :",usuario)
        print("livro :",livro)

        if not livro:
            print("controle")
            if not usuario:
                return jsonify({"status": "erro", "mensagem": "usuario nem livro encontrado"})
            else:
                return jsonify({"status": "erro", "mensagem": "livro não encontrado"})
        if not usuario:
            return jsonify({"status": "erro", "mensagem": "usuario não encontrado"})

        emprestimo_existente = db_session.execute(
            select(Emprestimo).where(
                (Emprestimo.id_livro == informacoes["id_livro"]) &
                (Emprestimo.id_usuario == informacoes["id_usuario"])
            )
        ).scalar()

        if emprestimo_existente:
            return jsonify({"status": "erro", "mensagem": "emprestimo existente"})



        if not "data_de_emprestimo" in informacoes or not "data_de_devolucao" or not "id_livro" in informacoes or not "id_usuario" in informacoes:
            return jsonify({'status': 'erro','mensagem': 'campos obrigatorios'}),400

        if informacoes["data_de_emprestimo"] == "" or informacoes["data_de_devolucao"] == "" or informacoes["id_livro"] == "" or informacoes["id_usuario"] == "":
            return jsonify({'status': 'erro', 'mensagem': 'Erro preencha os espaços'}),400


        post = Emprestimo(data_de_emprestimo = informacoes["data_de_emprestimo"],
                        data_de_devolucao = informacoes["data_de_devolucao"],
                        id_livro = informacoes["id_livro"],
                        id_usuario= informacoes["id_usuario"]
                        )
        post.save(db_session)



        return jsonify(
            {
                "status": "sucesso",
                "mensagem":"Emprestimo criado com sucesso",
                "data_de_emprestimo": informacoes["data_de_emprestimo"],
                "data_de_devolucao": informacoes["data_de_devolucao"],
                "id_livro": informacoes["id_livro"],
                "id_usuario": informacoes["id_usuario"]
            }
        ),201
    except SQLAlchemyError as e:
        return jsonify({'status': 'erro', 'mensagem': str(e)})
    finally:
        db_session.close()


@app.route('/lista_emprestimo', methods=["GET"])
def listar_emprestimo():
    """
           API para listar o emprestimo

           ### Resposta (JSON):
           '''json
           {'emprestimo': lista_emprestimo}


           :return: a lista ou a mensagem de erro
    """
    db_session = local_session()

    try:
        sql_emprestimo = select(Emprestimo)
        result = db_session.execute(sql_emprestimo).scalars()
        lista_emprestimo = []
        for emprestimo in result:
            lista_emprestimo.append(emprestimo.serialize_emprestimo())
        return jsonify({'emprestimo': lista_emprestimo})
    except SQLAlchemyError as e:
        return jsonify({'status': 'erro', 'mensagem': str(e)})
    finally:
        db_session.close()

#proteger
@app.route('/atualizar_emprestimo/<int:id_emprestimo>', methods=["PUT"])
def atualizar_emprestimo(id_emprestimo):
    """
    API para atualizar o livro
    ### Resposta (JSON):
    jsonify({'status': 'sucesso'})

    :param id_emprestimo: id do emprestimo que vai ser atualizado para assim localizado
    :return: atualiza o emprestimo
    """
    db_session = local_session()

    try:
        emprestimo = db_session.execute(select(Emprestimo).where(Emprestimo.id_emprestimo == id_emprestimo)).scalar()
        if emprestimo is None:
            return jsonify({"status": "erro", "mensagem": "emprestimo não encontrado"})

        dados_emprestimo = request.get_json()

        emprestimo.data_de_emprestimo = dados_emprestimo["data_de_emprestimo"]
        emprestimo.data_de_devolucao = dados_emprestimo["data_de_devolucao"]
        emprestimo.id_livro = dados_emprestimo["id_livro"]
        emprestimo.id_usuario = dados_emprestimo["id_usuario"]

        emprestimo.save(db_session)

        return jsonify({'status': 'sucesso'})
    except SQLAlchemyError as e:
        return jsonify({'status': 'erro', 'mensagem': str(e)})
    finally:
        db_session.close()


#proteger
@app.route('/cadastro_livro', methods=["POST"])
def criar_livro():
    """
           API para cadastrar o livro

           ### Resposta (JSON):
           '''json{
               "status": "sucesso",
                "mensagem":"livro- criado com sucesso",
                "id": post.id_livro,
                "titulo": informacoes["titulo"],
                "autor": informacoes["autor"],
                "ISBN": informacoes["ISBN"],
                "resumo": informacoes["resumo"]
               }

           :return: o cadastro do livro
           """
    db_session = local_session()

    try:
        informacoes = request.get_json()
        # relacao = db_session.execute(select(Livro).where(Livro.id_livro == informacoes["id_livro"])).scalar()
        print(informacoes)
        if not "titulo" in informacoes or not "autor" in informacoes or not "ISBN" in informacoes or not "resumo" in informacoes:
            return jsonify({'status': 'erro','mensagem': 'Obrigatorio Nome, CPF e endereco'}),400

        if informacoes["titulo"] == "" or informacoes["autor"] == "" or informacoes["ISBN"] == "" or informacoes["resumo"] == "":
            return jsonify({'status': 'erro', 'mensagem': 'Erro preencha os espaços'}),400

        post = Livro(titulo = informacoes["titulo"],
                        autor = informacoes["autor"],
                        ISBN = informacoes["ISBN"],
                        resumo = informacoes["resumo"]
                        )
        post.save(db_session)

        return jsonify(
            {
                "status": "sucesso",
                "mensagem":"livro- criado com sucesso",
            }
        ),201
    except SQLAlchemyError as e:
        return jsonify({'status': 'erro', 'mensagem': str(e)}),400
    finally:
        db_session.close()

#proteger
@app.route('/lista_livro', methods=["GET"])
def listar_livros():
    """
           API para listar os livros

           ### Resposta (JSON):
           '''json
           {'livros': lista_livros}

           :return: a lista ou a mensagem de erro
    """
    db_session = local_session()

    try:
        sql_livro = select(Livro)
        result = db_session.execute(sql_livro).scalars()
        lista_livro = []
        for livro in result:
            lista_livro.append(livro.serialize_livro())
        return jsonify({'livros': lista_livro})
    except SQLAlchemyError as e:
        return jsonify({'status': 'erro', 'mensagem': str(e)}),400
    finally:
        db_session.close()

#proteger
@app.route('/atualizar_livro/<int:id_livro>', methods=["PUT"])
def atualizar_livro(id_livro):
    """
    API para atualizar o livro
    ### Resposta (JSON):
    jsonify({'status': 'sucesso'})

    :param id_livro: id do livro que vai ser atualizado para assim localizado
    :return: atualiza o livro
    """
    db_session = local_session()

    try:
        livro = db_session.execute(select(Livro).where(Livro.id_livro == id_livro)).scalar()
        if livro is None:
            return jsonify({"status": "erro", "mensagem": "livro não encontrado"}),404

        dados_livro = request.get_json()


        livro.titulo = dados_livro["titulo"]
        livro.autor = dados_livro["autor"]
        livro.ISBN = dados_livro["ISBN"]
        livro.resumo = dados_livro["resumo"]

        livro.save(db_session)

        return jsonify({'status': 'sucesso'})
    except SQLAlchemyError as e:
        return jsonify({'status': 'erro', 'mensagem': str(e)})

    finally:
        db_session.close()


@app.route('/mostrar_livro/<id_livro>', methods=["GET"])
def mostrar_livro(id_livro):
    """
           API para verificar um livro.

           ## Endpoint:
            /get_livro/<int:id>

            ##Parâmetros:
            "id" **Id do livro**

           ## Respostas (JSON):
           ```json

        {
            "id":,
            "titulo":
            "autor",
            "isbn":,
            "resumo",
        }

        ## Erros possíveis (JSON):
            "Não foi possível listar os dados do livro ***400
            Bad Request***:
                ```json
           """
    db_session = local_session()

    try:
        livro = db_session.execute(select(Livro).where(Livro.id_livro == id_livro)).scalar()

        if not livro:
            return jsonify({
                "error": "Livro não encontrado!"
            }), 400

        else:
            return jsonify({
                "id_livro": livro.id_livro,
                "titulo": livro.titulo,
                "autor": livro.autor,
                "ISBN": livro.ISBN,
                "resumo": livro.resumo
            }), 200

    except ValueError:
        return jsonify({
            "error": "Não foi possívl listar os dados do livro"
        }), 400
    except Exception as e:
        return jsonify({"erro": str(e)}), 400
    finally:
        db_session.close()



@app.route('/mostrar_user/<id_usuario>', methods=["GET"])
def mostrar_user(id_usuario):
    """
           API para verificar um livro.

           ## Endpoint:
            /get_livro/<int:id>

            ##Parâmetros:
            "id" **Id do livro**

           ## Respostas (JSON):
           ```json

        {
            "id":,
            "titulo":
            "autor",
            "isbn":,
            "resumo",
        }

        ## Erros possíveis (JSON):
            "Não foi possível listar os dados do livro ***400
            Bad Request***:
                ```json
           """
    db_session = local_session()

    try:
        usuario = db_session.execute(select(Usuario).where(Usuario.id_usuario == id_usuario)).scalar()

        if not usuario:
            return jsonify({
                "error": "user não encontrado!"
            }), 400

        else:
            return jsonify({
                "id_usuario": usuario.id_usuario,
                'CPF': usuario.CPF,
                'Nome': usuario.Nome,
                'endereco': usuario.endereco,
            }), 200

    except ValueError:
        return jsonify({
            "error": "Não foi possível listar os dados do user"
        }), 400
    except Exception as e:
        return jsonify({"erro": str(e)}), 400
    finally:
        db_session.close()




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)