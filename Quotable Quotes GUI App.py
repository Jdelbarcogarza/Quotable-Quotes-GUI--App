'''
Este es mi primer intento de hacer una GUI App mientras trabajo con una API.
Esta es una App que te da Quotes inspiracionales de diferentes maneras provenientes de la API.
El endpoint es "http://staging.quotable.io/"
Se utilizrá la librería tkinter para crar la GUI.

El proceso de desarrollo fue primero crear la UI y acomodar todo como se debe para que sea una app
responsiva. Despúes se fue agregando la lógica a los botones para hacer que cambien de ventana 
y por último conectar el programa con la API.

Fecha de inicio de proyecto: 21/01/2021
'''
# Se importan las librerías que se utiizarán en le programa
import tkinter as tk
import requests
from time import sleep




def main():

    
    
    # creamos la pantalla del menú
    menuWindow = tk.Tk()

    # tamaño mínimo de la pantalla principal
    menuWindow.minsize(325,280)

    # declaramos todos los widgets de esa pantalla
    frm_Menu = tk.Frame(menuWindow)
    lbl_AppBanner = tk.Label(frm_Menu, text="Quotable Quotes")
    btn_RandomQuotes = tk.Button(frm_Menu, text="Random Quotes")
    btn_ListOfQuotes = tk.Button(frm_Menu, text="List of Quotes")
    btn_ListOfAuthors = tk.Button(frm_Menu, text="List of Authors")
    btn_GetAuthorByID = tk.Button(frm_Menu, text="Get Author by ID")
    
    # Queremos que los créditos estén separados de el menú funcional de la app
    frm_Credits = tk.Frame(menuWindow)
    lbl_AppAuthor = tk.Label(frm_Credits, text="App made by Jorge Del Barco")
    lbl_Credits = tk.Label(frm_Credits,text="Powered with the Quotable API \"http://staging.quotable.io/\" ")

    # con estas líneas permitimos que la pantalla y los elementos (widgets) que se encuentran adentro
    # de ella puedan cambiar de tamaño si se hace un resize de la pantalla
    menuWindow.rowconfigure(0, weight=1, minsize=20)
    menuWindow.columnconfigure(0,weight=1, minsize=20)
    
    # se agregan los widgets a la pantalla
    frm_Menu.grid(row=0, column=0, sticky="NEWS")
    lbl_AppBanner.grid(row=0, column=0, sticky="NEWS", columnspan=2)
    btn_RandomQuotes.grid(row=1, column=0, sticky="NEWS", padx=5, pady=10)
    btn_ListOfQuotes.grid(row=1, column=1, sticky="NEWS", padx=5, pady=10)
    btn_ListOfAuthors.grid(row=2, column=0, sticky="NEWS", padx=5, pady=10)
    btn_GetAuthorByID.grid(row=2, column=1, sticky="NEWS", padx=5, pady=10)

    # Estos widgets se encuentran en el frame de los créditos de la app. Están localizados abajo
    frm_Credits.grid(row=1, column=0, sticky="S")
    lbl_AppAuthor.grid(row=0, column=0, sticky="NEWS")
    lbl_Credits.grid(row=1, column=0, sticky="NEWS")
    

    # se configura el comportamiento de cada celda en el grid
    frm_Menu.rowconfigure(0, weight=2, minsize=15)
    frm_Menu.rowconfigure([1,2], weight=1, minsize=10)
    frm_Menu.columnconfigure([0,1], weight=1)

    '''
    A partir de este punto se le agrega funcionalidad a los botones del programa con event handlers.
    Cada botón abre una nueva ventana dedicada a cumplir con lo que dice el botón
    '''

    def RandomQuoteWindow(event):
        """
        Funcion que abre una ventana dedicada a generar una random quote tomando en cuenta
        los parámetros que el usuario puede poner. Se genera la quote con ayuda de la API
        """
        # se genera la ventana secundaria conectada a la ventana principal menuWindow
        window = tk.Toplevel(menuWindow)

        # Título de ventana
        window.title("Generate a random quote")

        # Se declara el tamaño mínimo de esta ventana
        window.minsize(620,250)

        # Se declra la funcionalidad de la ventana
        window.rowconfigure([0,1],weight=1)
        window.columnconfigure(0,weight=1)

        # Se declaran los widgets que se van a usar
        frm_Params = tk.Frame(window)
        lbl_MaxLength = tk.Label(frm_Params, text="Maximum amount of characters in quote:")
        entry_MaxLength = tk.Entry(frm_Params)
        lbl_MinLength = tk.Label(frm_Params, text="Minimum amount of characters is quote:")
        entry_MinLength = tk.Entry(frm_Params)
        lbl_Message = tk.Label(frm_Params, text="(Leave blank if parameters are not needed.)")

        # Se declara la ubicación de los widgets dentro del frame en su respectivas celdas
        frm_Params.grid(row=0, column=0, sticky="NEWS", padx=5, pady=5)
        lbl_MaxLength.grid(row=0, column=0, sticky="NEWS")
        entry_MaxLength.grid(row=0, column=1, sticky="NEWS")
        lbl_MinLength.grid(row=1, column=0, sticky="NEWS")
        entry_MinLength.grid(row=1, column=1, sticky="NEWS")
        lbl_Message.grid(row=2,column=0, columnspan=2, sticky="NEWS")


        # Est parte de la función declara los widgets que se encargan de mostrar los resultados del 
        # query hecha a la API 
        frm_QuoteDisplay = tk.LabelFrame(window)

        lbl_QuoteContent = tk.Label(
            frm_QuoteDisplay, 
            text="Your quote will appear here once you click the button below.",
            bg="white", relief=tk.RAISED, width=30, height=5)

        lbl_QuoteCategory = tk.Label(frm_QuoteDisplay, text="Quote Category: ")
        btn_GenerateQuote = tk.Button(frm_QuoteDisplay, text="Generate Quote")

        # Se colocan los widgets que muestran el resultdo de las queries
        frm_QuoteDisplay.grid(row=1, column=0, sticky="NEWS")
        lbl_QuoteCategory.grid(row=0, column=0, sticky="NEWS", pady=5)
        lbl_QuoteContent.grid(row=1, column=0, sticky="NEWS", padx=10)
        btn_GenerateQuote.grid(row=2, column=0, sticky="NEWS", pady=10, padx=150)

        # Se configura el comportaiento de los widgets en la ventana cuando se hace una cambio de 
        # tamaño de la misma

        frm_Params.grid_rowconfigure([0,1], weight=1)
        frm_Params.grid_columnconfigure([0,1], weight=1)

        # Aqui se quiere que las líneas del 2o frame crezcan
        frm_QuoteDisplay.grid_rowconfigure([0,1], weight=1)
        frm_QuoteDisplay.grid_rowconfigure(2, minsize=25)
        # Aqui solo se quiere que la columan 0 crezca, ya que en todo este 2o frame no hay 
        # otras columnas
        frm_QuoteDisplay.grid_columnconfigure(0, weight=1)

        ''' Lógica de la función'''

        def GenerateRandomQuote(event):
            """
            Función que se llama cuando se presiona el botón de generar una quote de manera
            aleatoria.
            """
            
            # Verificar si los entries tienen algo escrito
            

            # Se declara el diccionario que pasará los parámetros a la URL.
            payload = {"minLength":int(entry_MinLength.get()), "maxLength":int(entry_MaxLength.get())}

            # se hace un request a la API
            r = requests.get("http://staging.quotable.io/random", params=payload)

            # Se imprime la URL que se mandó y el estatus de la request (200 == OK)
            #print(r.url)
            #print(r.status_code)

            # se imprime en consola tambien la respuesta en formato json en la terminal.
            #print(r.text)

            # Se limpia el string antes de imprimirse, solo el primer tag se imprime
            category = r.json()["tags"]
            category = category[0]

            # Se imprime la categoría de la quote
            lbl_QuoteCategory["text"] = f'Quote Category: \"{category}\"'

            # Se modifica el string de texto para evitar que las quotes muy largas salgan de su 
            # label. 
            '''OJO: Se sabe que con 66 caracteres la línea ya casi se sale del label. Si se inserta
            un newline (/n) en la quote podemos poner quotes más largas.'''

            quote = r.json()["content"]
            

            '''
            # Hacemos el split de la quote con todos los espacios
            words = quote.split(" ")

            acum_quote_length = 0
            for item_index , items in enumerate(words):

                acum_quote_length = acum_quote_length + (len(items)+1)
                if (acum_quote_length >= 55):
                    words.insert(item_index,"/n")
                    break

            print(words)

            words = ' '.join(words)
            '''


            # se imprime el nombre del autor y el contenido de la quote en el widget que corresponde
            lbl_QuoteContent["text"] = f'\"{quote}\"\n-{r.json()["author"]}'


        # Event handler del botón generate quote

        btn_GenerateQuote.bind("<ButtonRelease>", GenerateRandomQuote)

        

    btn_RandomQuotes.bind("<ButtonRelease>", RandomQuoteWindow)    


    menuWindow.mainloop()

if __name__ == "__main__":
    main()
