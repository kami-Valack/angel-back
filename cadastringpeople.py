import pymysql

try: 
    cnx = pymysql.connect(
        user="root",
        password="YiQlVlvJsOFXPIYSDGTYTxndxArhwNSc",
        host="hopper.proxy.rlwy.net",
        database="railway",
        port=58780
    )
    cursor = cnx.cursor()

    name=str(input("Insira o seu nome: "))
    date=str(input("Insira a sua data de nasimento (ano-mes-dia): "))
    sex=str(input("Qual e o seu sexo? (F/M): "))
    peso=float(input("Digite o seu peso: "))
    height=float(input("Digite a sua  altura: "))
    naction=str(input("Digite a sua nacionalidade: "))
    number=int(input("Digite o seu numero: "))
    prof=str(input("Qual a sua profissao? "))
    if sex != "F" or "M":
        print ("Opcao invalida!")
        sex=str(input("Qual e o seu sexo? (F/M): "))
    if height > 2.99:
        print("Opcao invalida!")
        height=int(input("Digite a sua  altura: "))
    



    query_Insert = (f"""INSERT INTO `novo` 
                    (`id`, `nome`, `data`, `sexo`, `peso`, `altura`, `nacao`, `numero`, `profissao`)
                    VALUES 
                    (NULL, '{name}', '{date}', '{sex}', '{peso}', '{height}', '{naction}', '{number}', '{prof}');""")
    
    cursor.execute(query_Insert)
    cnx.commit()
    NumeroRegistro=str(input("Digite o numero do resgistro que queres encontrar: "))
    
    query_select=(f"SELECT * FROM novo WHERE id = {NumeroRegistro} " )
    cursor.execute(query_select)

    for row in cursor:
        print  (row)

except mysql.connector.Error as error:
    print (f"Error: {error}")

finally:
    if "cursor" in locals() and cursor is not None:
        cursor.close()
    if "cnx" in locals() and cnx is not None:
        cnx.close()
print ("Voce foi cadastrado!")