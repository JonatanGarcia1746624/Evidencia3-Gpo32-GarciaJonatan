import datetime
import sys
import sqlite3
from sqlite3 import Error

try:
    with sqlite3.connect("VentasCosmeticos.db") as conn:
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTs VENTA (Folio INTEGER PRIMARY KEY, FecVenta TEXT NOT NULL);")
        c.execute("""CREATE TABLE IF NOT EXISTS VENTA_DETALLE       
                     (Desc TEXT NOT NULL, \
                     CantArticulo INT NOT NULL, \
                     Precio REAL NOT NULL, \
                     Folio INTEGER NOT NULL, \
                     FOREIGN KEY(Folio) REFERENCES VENTA(Folio) \
                     );""")
except Error as e:
    print(e)
except Exception:
    print(f'SE PRODUJO EL SIGUIENTE ERROR: {sys.exc_info()[0]}')


salida = int(0)
while salida == int(0):
    print("\n")
    print("*"*90)
    print("*"*90)
    print(f'\nBASE DE DATOS "COSMETICOS LAS PRIMAS"')
    print(f'1.REGISTRAR UNA VENTA')
    print(f'2.CONSULTAR UNA VENTA')
    print(f'3.OBTENER UN REPORTE DE VENTAS PARA UNA FECHA ESPECIFICA')
    print(f'4.SALIR')
    op = input("OPCIÓN:")
    
    print()

    if op == "1":
        print("DIGITE EL NUMERO DE FOLIO DE VENTA")
        print("SI DIGITA UN FOLIO YA EXISTENTE NO SE REGISTRARA")
        print("EL SISTEMA MARCARA ERROR Y VOLVERA AL MENU")
        Folio = int(input("FOLIO: "))
        Fecha = str(datetime.date.today())
        
        try:
            with sqlite3.connect("VentasCosmeticos.db") as conn:
                mi_cursor = conn.cursor()
                mi_cursor.execute("SELECT * FROM VENTA")
                folios = mi_cursor.fetchall()
                sal = int(0)
                for folio, Fecha in folios:
                    if folio == Folio:
                        print("-----------------------")
                        print(f'\nFOLIO YA EXISTENTE\n')
                        print("-----------------------")
                        print(f'\nVERIFIQUE EL FOLIO\n')
                        print("-----------------------")
                        print(f'\nPROGRAMA TERMINADO')
                        sal = int(1)
        except Error as e:
            print(e)
        except Exception:
            print(f'SE PRODUJO EL SIGUIENTE ERROR: {sys.exc_info()[0]}')
        
        if sal == int(1):
            break
        
        try:
            with sqlite3.connect("VentasCosmeticos.db") as conn:
                mi_cursor = conn.cursor()
                valores = {"Folio":Folio, "FecVenta":Fecha}        
                mi_cursor.execute("INSERT INTO VENTA VALUES(:Folio,:FecVenta)", valores)
        except Error as e:
            print(e)
        except Exception:
            print(f'SE PRODUJO EL SIGUIENTE ERROR: {sys.exc_info()[0]}')
        
        
        
        salida2 = int(0)
        while salida2 == int(0):
            try:
                with sqlite3.connect("VentasCosmeticos.db") as conn:
                    print("\n")
                    print("*"*80)
                    print("*"*80)
                    mi_cursor = conn.cursor()
                    print("\nAGREGAR ARTICULO")
                    Descripcion = str(input("\nDESCRIPCIÓN DEL ARTICULO: "))
                    Cantidad = int(input("CANTIDAD: "))
                    Precio = float(input("PRECIO DEL ARTICULO: "))
                    valores = {"Desc":Descripcion, "CantArticulo":Cantidad, "Precio":Precio, "Folio":Folio}
                    mi_cursor.execute("INSERT INTO VENTA_DETALLE VALUES(:Desc,:CantArticulo,:Precio,:Folio)", valores)
                 
                    print("\nAGREGAR OTRO ARTICULO SI[0], NO[1]")
                    agregarOP = int(input("OPCIÓN: "))
                    salida2 = agregarOP
            except Error as e:
                print(e)
            except Exception:
                print(f'SE PRODUJO EL SIGUIENTE ERROR: {sys.exc_info()[0]}')
            
            
        try:
            with sqlite3.connect("VentasCosmeticos.db") as conn:
                mi_cursor = conn.cursor()
                mi_cursor.execute("SELECT * FROM VENTA_DETALLE WHERE Folio == ?",(Folio,))
                venta = mi_cursor.fetchall()
                
                print("\n")
                print("*"*80)
                print("*"*80)
                print("\n***VENTA REGISTRADA CON EXITO***")
                print(f'\nFECHA DE VENTA: {Fecha}')
                subtotal = 0
                for Desc, Cant, Price, Fol  in venta:
                    print()
                    print(f'DESCRIPCIÓN DEL ARTICULO: {Desc}')
                    print(f'CANTIDAD: {Cant}')
                    print(f'PRECIO UNITARIO: {Price}')
                    print(f'IMPORTE: {Cant * Price}')
                    subtotal += Cant * Price
                print()
                print(f'SUBTOTAL: {subtotal}')
                print(f'IVA(16%): {subtotal * 0.16}')
                print(f'TOTAL: {(subtotal) + (subtotal * 0.16)} ')
        except Error as e:
            print(e)
        except Exception:
            print(f'SE PRODUJO EL SIGUIENTE ERROR: {sys.exc_info()[0]}')
   
   
    else:
        if op == "2":
            print(f'\nCONSULTAR UNA VENTA')
            print(f'INGRESE EL FOLIO DE LA VENTA QUE DESEA CONSULTAR')
            num_Venta = int(input("Numero de Folio: "))
            
            try:
                with sqlite3.connect("VentasCosmeticos.db") as conn:
                    print("\n")
                    print("*"*80)
                    print("*"*80)
                    mi_cursor = conn.cursor()
                    mi_cursor.execute("SELECT * FROM VENTA_DETALLE WHERE Folio == ?",(num_Venta,))
                    venta = mi_cursor.fetchall()
                    mi_cursor.execute("SELECT FecVenta FROM VENTA WHERE Folio == ?",(num_Venta,))
                    Fecha = mi_cursor.fetchall()
            except Error as e:
                print(e)
            
            except Exception:
                print(f'SE PRODUJO EL SIGUIENTE ERROR: {sys.exc_info()[0]}')
        
            
            if len(venta) == 0:
                print("*"*80)
                print("*"*80)
                print("\n¡¡¡VENTA NO ENCONTRADA FAVOR DE VERIFICAR EL DATO!!!")
            
            else:
                print("\n")
                print("*"*80)
                print("*"*80)
                print("\n***VENTA ENCONTRADA***")
                print(f'\nFECHA DE VENTA: {Fecha[0][0]}')
                subtotal = 0
                for Desc, Cant, Price, Fol  in venta:
                    print()
                    print(f'DESCRIPCIÓN DEL ARTICULO: {Desc}')
                    print(f'CANTIDAD: {Cant}')
                    print(f'PRECIO UNITARIO: {Price}')
                    print(f'IMPORTE: {Cant * Price}')
                    subtotal += Cant * Price
                print()
                print(f'SUBTOTAL: {subtotal}')
                print(f'IVA(16%): {subtotal * 0.16}')
                print(f'TOTAL: {(subtotal) + (subtotal * 0.16)} ')
        
        
        else:
            if op == "3":
                print(f'\n***INGRESE UNA FECHA PARA IMPRIMIR TODAS LAS VENTAS DE ESA FECHA***')
                print(f'¡PORFAVOR DIGITE LA FECHA EN EL SIGUIENTE FORMATO! (AÑO-MES-DÍA)')
                print(f'EJEMPLO:2008-07-23')
                fec = input("FECHA: ")
                try:
                    with sqlite3.connect("VentasCosmeticos.db") as conn:
                        print("\n")
                        print("*"*90)
                        print("*"*90)
                        mi_cursor = conn.cursor()
                        mi_cursor.execute("""SELECT VD.Folio, V.FecVenta, VD.Desc, VD.CantArticulo, VD.Precio \
                                             FROM VENTA_DETALLE VD  \
                                             INNER JOIN VENTA V ON V.Folio = VD.Folio \
                                             WHERE V.FecVenta == ?""", (fec,))
                        venta = mi_cursor.fetchall()
                        if len(venta) == 0:
                            print("*"*80)
                            print("*"*80)
                            print("\n¡¡¡VENTA NO ENCONTRADA FAVOR DE VERIFICAR EL DATO!!!")
                        else:
                            print(f'\nFOLIO\t \tFECHA\t \tDESCRIPCIÓN\t \tCANTIDAD\t \tPRECIO')
                            for Fol, Fec, Desc, Cant, Price in venta:
                                print(f'{Fol}\t\t{Fec}\t{Desc}\t\t{Cant}\t\t\t{Price}')

                except Error as e:
                    print(e)
            
                except Exception:
                    print(f'SE PRODUJO EL SIGUIENTE ERROR: {sys.exc_info()[0]}')
            
            else: 
                if op == "4":
                    print("*"*80)
                    print("---PROGRAMA TERMINADO---")
                    break