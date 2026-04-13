import logging
import azure.functions as func

def main(myblob: func.InputStream):
    logging.info(f"Nouveau fichier uploadé : {myblob.name} ({myblob.length} octets)")
    # Traitement à implémenter : extraction de texte, génération de miniature, etc.
