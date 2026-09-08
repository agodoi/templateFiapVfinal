from conectar_bd import conectar

def inserir_simulacao(
    id_simulacao,
    area_m2,
    metodo_colheita,
    lucro,
    gastos,
    peso_total,
    peso_perdido_ton,
    peso_perdido_rs,
    coef_correlacao
):
    conn = conectar()

    if conn:
        try:
            cursor = conn.cursor()

            sql = """
                INSERT INTO SIMULACAO_COLHEITA (
                    ID_SIMULACAO,
                    AREA_M2,
                    METODO_COLHEITA,
                    LUCRO,
                    GASTOS,
                    PESO_TOTAL,
                    PESO_PERDIDO_TON,
                    PESO_PERDIDO_RS,
                    COEF_CORRELACAO
                )
                VALUES (
                    :1, :2, :3, :4, :5, :6, :7, :8, :9
                )
            """

            cursor.execute(sql, (
                id_simulacao,
                area_m2,
                metodo_colheita,
                lucro,
                gastos,
                peso_total,
                peso_perdido_ton,
                peso_perdido_rs,
                coef_correlacao
            ))

            conn.commit()
            print("Simulação inserida com sucesso.")

        except Exception as e:
            print("Erro ao inserir:", e)

        finally:
            cursor.close()
            conn.close()