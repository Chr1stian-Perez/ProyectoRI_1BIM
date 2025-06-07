# Sistema de Recuperación de Información - TREC CAR

Sistema de IR implementado en Python que utiliza el dataset TREC CAR car/v1.5/test200 con algoritmos TF-IDF y BM25.

## Características

- **Índice invertido** con procesamiento completo de texto
- **Algoritmos de recuperación**: TF-IDF con similitud coseno y BM25
- **Interfaz CLI** para consultas interactivas
- **Evaluación automática** con métricas estándar (Precision, Recall, MAP)
- **Dataset**: TREC CAR car/v1.5/test200


##Instrucciones para la instalación y uso

- **Primer paso:** Instalar los requisitos ir-datasets>=0.5.5; nltk>=3.8; numpy>=1.21.0; scikit-learn>=1.0.0; colorama; pyfiglet
                    con el comando pip install -r requirments.txt
- **Segundo paso**: Ejecutar el programa de interfaz principal del proyecto "proyecto.py"
- **Tercer paso**: En la interfaz CLI seleccionar la primera opción para descargar automomaticamente el corpus TREC CAR car/v1.5/test200
                    "5GB" pasa su posterior uso en la creción del indice invertido "el corpus solo se descarga la primera vez", el indice
                    invertido solo es necesario crearlo una vez, dado que este se almacne en la carpeta /data una vez creado
- **Cuarto paso**:  En la interfaz CLI seleccionar la segunda opción para realizar las consultas con terminos que el usurio desee,
                    se agrego la opción help para que el usuario tenga ayuda de como utilizar esta segunda opción
- **Quinto paso**:  En la interfaz CLI seleccionar la tercera opción para realizar el benchmarking del sitema de recuperación de    información automatico segun qrels del corpus
- **Sexto paso**:  En la interfaz CLI seleccionar la cuarta opción para salir