# Importamos las librerias 
import cv2
import mediapipe as mp
import serial

#Configuracion del puerto serial 
#La velocidad de comunicacion y tiempo de respuesta tienen que ser los mismos en arduino IDE
com = serial.Serial("COM3", 9600, write_timeout= 5)
#Variables que se mandan por el puerto serial
d = 'd' #Derecha
i = 'i' #Izquierda
p = 'p' #Parar
marca = 0

#Detector de rostros por la libreria mediapipe
detector = mp.solutions.face_detection
dibujo = mp.solutions.drawing_utils

#Declaramos la camara que usamos
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)


# Funcion Mouse 
def mouse(evento, xm, ym, bandera, param):
    global xmo, ymo, marca
    # Conseguir las coordenadas de la ventana de la camara
    if evento == cv2.EVENT_LBUTTONDOWN:
        xmo = xm
        ymo = ym
        marca = 1
        print(xmo, ymo)



# Parametros para la deteccion de rostro 
with detector.FaceDetection(min_detection_confidence=0.75, model_selection=0) as rostros:
    while True:

        # Lectura de fps
        ret, frame = cap.read()

        #  El servo nos ve de frente y por eso necesitamos el efecto espejo
        frame = cv2.flip(frame,1)

        # por las librerias necesitamos cambiar el orden de color BGR -> RGB
        #opencv -> BGR
        #mediapipe ->RGB
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        #  los rostros
        resultado = rostros.process(rgb)

        # Creamos listas
        listacentro = []
        click = []
        listarostro = []


        #  Si hay rostros entra a la sentencia IF
        if resultado.detections is not None:
            for rostro in resultado.detections:
                dibujo.draw_detection(frame, rostro, dibujo.DrawingSpec(color=(0,255,0),))

                for id, puntos in enumerate(resultado.detections):
                    # Mostramos toda la informacion
                    print("Puntos: ", resultado.detections)

                    #  el ancho y el alto del frame
                    al, an, c = frame.shape

                    #  el medio de la pantalla
                    centro = int(an / 2)

                    # Extraemos las coordenadas X e Y min
                    #Esquina superir izquierda del rostro
                    x = puntos.location_data.relative_bounding_box.xmin
                    y = puntos.location_data.relative_bounding_box.ymin

                    # Extraemos el ancho y el alto de la hitbox del rostro
                    ancho = puntos.location_data.relative_bounding_box.width
                    alto = puntos.location_data.relative_bounding_box.height

                    # Pasamos X e Y a coordenadas en pixeles
                    x, y = int(x * an), int(y * al)
                    #print("X, Y: ", x, y)

                    # Pasamos el ancho y el alto a pixeles
                    x1, y1 = int(ancho * an), int(alto * al)
                    xf, yf = x + x1, y + y1

                    # Extraemos el punto central
                    cx = (x + (x + x1)) // 2
                    cy = (y + (y + y1)) // 2

                    listacentro.append([id, cx, cy])
                    listarostro.append([x, y, x1, y1])

                    # Mostrar un punto en el centro
                    cv2.circle(frame, (cx, cy), 3, (0, 0, 255), cv2.FILLED)
                    cv2.line(frame, (cx, 0), (cx, 480), (0, 0, 255), 2)

                    cv2.namedWindow('CamaraTracker')
                    cv2.setMouseCallback('CamaraTracker', mouse)

                    # Marca
                    if marca == 1:
                        # SI estamos dentro de las coordenadas
                        if x < xmo < xf and y < ymo < yf:

                            # Dibujamos el click
                            cv2.circle(frame, (xmo, ymo), 20, (0, 255, 0), 2)
                            cv2.rectangle(frame, (x, y), (xf, yf), (255, 255, 0),3)  
                            # Dibujamos el rectangulo
                            cv2.putText(frame, str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)
                            xmo = cx
                            ymo = cy

                            print(resultado.detections[id])

                            # Condiciones para mover el servo
                            if xmo < centro - 50:
                                # Movemos hacia la izquierda
                                print("Izquierda")
                                com.write(i.encode('ascii'))
                            elif xmo > centro + 50:
                                # Movemos hacia la derecha
                                print("Derecha")
                                com.write(d.encode('ascii'))
                            elif xmo == centro:
                                # Paramos el servo
                                print("Centro")
                                com.write(p.encode('ascii'))


        cv2.imshow('CamaraTracker', frame)

        t = cv2.waitKey(1)
        if t == 27:
            break
cap.release()
cv2.destroyAllWindows()