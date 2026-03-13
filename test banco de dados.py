import pymysql

try:
    # Establish a connection to the database
    cnx = pymysql.connect(
        user='root',
        password='YiQlVlvJsOFXPIYSDGTYTxndxArhwNSc',
        host='hopper.proxy.rlwy.net',
        database='railway',
        port=58780
    )

    # Create a cursor object to interact with the database
    cursor = cnx.cursor()
    
    nome=str(input("Digite o seu nome: "))
    nascimento=str(input("Insira a sua data Padrao(ano-mes-dia): "))
    sexo=str(input("Digite o seu sexo (M/F): "))
    peso=float(input("Digite o seu peso: "))
    altura=float(input("Digite a sua altura: "))
    nacionalidade=str(input("Digite a sua nacionaliade: "))

    # Execute an SQL query
    query_Insert = (f"""
                    INSERT INTO `pessoas` 
                    (`id`, `nome`, `nascimento`, `sexo`, `peso`, `altura`, `nacionalidade`)
                    VALUES (NULL, '{nome}', '{nascimento}', '{sexo}', '{peso}', '{altura}', '{nacionalidade}');
                    """)
    cursor.execute(query_Insert)
    cnx.commit()

    query_select=("SELECT * FROM pessoas")
    cursor.execute(query_select)
    # Fetch and print the results
    for row in cursor:
        print(row)

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    # Close the cursor and connection
    if 'cursor' in locals() and cursor is not None:
        cursor.close()
    if 'cnx' in locals() and cnx is not None:
        cnx.close()
