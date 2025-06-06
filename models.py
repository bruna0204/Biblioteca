from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, declarative_base
#configuração base de dados
engine = create_engine('sqlite:///controle_estoque.sqlite3') #nome do banco
# db_session = scoped_session(sessionmaker(bind=engine)) - atualizado
local_session = sessionmaker(bind=engine)


#modo declarativo
Base = declarative_base()
# Base.query = db_session.query_property()


#Pessoas que tem atividade
class Usuario(Base):
    __tablename__ = 'tab_usuarios'
    id_usuario = Column(Integer, primary_key=True)
    Nome = Column(String(30), nullable=False, index=True )
    endereco = Column(String(70), nullable=False, index=True) #string o tamanho dele
    CPF = Column(Integer, nullable=False, index=True, unique=True) #string o tamanho dele


    def __repr__(self):
        return '<Funcionario: {} {} {} {}>' .format(self.id_usuario, self.CPF, self.Nome, self.endereco, )


    def save(self, db_session):
        try:
            db_session.add(self)
            db_session.commit()
        except SQLAlchemyError as e:
            db_session.rollback()
            raise

#função para deletar
    def delete(self, db_session):
        try:
            db_session.delete(self)
            db_session.commit()
        except SQLAlchemyError as e:
            db_session.rollback()
            raise

    def serialize_usuarios(self):
        dados_usuario = {
            'id_usuarios': self.id_usuario,
            'CPF': self.CPF,
            'Nome': self.Nome,
            'endereco': self.endereco,
        }
        return dados_usuario



class Livro(Base):
    __tablename__ = 'tab_livros'
    id_livro = Column(Integer, primary_key=True)
    titulo = Column(String(70), nullable=False, index=True)
    autor = Column(String(70), nullable=False, index=True)
    ISBN = Column(Integer, nullable=False, index=True)
    resumo = Column(String(100), nullable=False, index=True)

    def __repr__(self):
        return '<Livros: {} {} {} {}>' .format(self.id_livro, self.titulo, self.ISBN, self.resumo, self.autor)

#função para salvar no banco

    def save(self, db_session):
        try:
            db_session.add(self)#seção de acesso
            db_session.commit() #salva a informação
        except SQLAlchemyError as e:
            db_session.rollback()
            raise

#função para deletar
    def delete(self, db_session):
        try:
            db_session.delete(self)#deletar
            db_session.commit()# salvar
        except SQLAlchemyError as e:
            db_session.rollback()
            raise

    def serialize_livro(self):
        dados_livros = {
            'id_livro': self.id_livro,
            'titulo': self.titulo,
            'autor': self.autor,
            'resumo': self.resumo,
            'ISBN': self.ISBN,
        }
        return dados_livros






class Emprestimo(Base):
    __tablename__ = 'TAB_EMPRESTIMO' #nome da tabela
    id_emprestimo = Column(Integer, primary_key=True) #chave primaria (unico) integer = tipo de dado
    data_de_emprestimo = Column(String(20), nullable=False, index=True) #nullable tem que obrigatoriamente preencher o espaço
    data_de_devolucao = Column(String(27), nullable=False, index=True)# index pesquisa
    id_usuario = Column(Integer, ForeignKey('tab_usuarios.id_usuario'), nullable=False)#string o tamanho dele
    usuario = relationship('Usuario')
    id_livro = Column(Integer, ForeignKey('tab_livros.id_livro'), nullable=False)
    produto = relationship('Livro')
    #colum = coluna

    def __repr__(self):
        return '<Emprestimo: {} {} {} {} {}>' .format(self.id_emprestimo, self.data_de_emprestimo, self.data_de_devolucao, self.id_livro, self.id_usuario)#self ele chama ele mesmo

#função para salvar no banco

    def save(self, db_session):
        try:
            db_session.add(self)#seção de acesso
            db_session.commit() #salva a informação
        except SQLAlchemyError as e:
            db_session.rollback()
            raise

#função para deletar
    def delete(self, db_session):
        try:
            db_session.delete(self)#deletar
            db_session.commit()# salvar
        except SQLAlchemyError as e:
            db_session.rollback()
            raise


    def serialize_emprestimo(self):
        dados_emprestimo = {
            'id_emprestimo': self.id_emprestimo,
            'data_de_emprestimo': self.data_de_emprestimo,
            'data_de_devolucao': self.data_de_devolucao,
            'id_usuario': self.id_usuario,
            'id_livro': self.id_livro,

        }
        return dados_emprestimo


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    init_db()