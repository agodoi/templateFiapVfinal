import oracledb

def conectar():
    try:
        dsn = "oracle.fiap.com.br:1521/ORCL"
        conn = oracledb.connect(
            user="admin",
            password="191107",
            dsn=dsn
        )
        print("Conexão realizada com sucesso!")
        return conn
    except Exception as e:
        print("Erro ao conectar ao Oracle:", e)
        return None