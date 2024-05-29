from pytube import YouTube
import pandas as pd
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive


# Variables excel
file_path = 'enlaces_videos/enlaces.xlsx'
sheet_name = 'Hoja1'
column_name = 'Videos'

# Credenciales google drive
directorio_credenciales = 'credentials_module.json'
id_folder =  '1DGvrvJFJsnqecNwjGiOl5NhDNmfPRMZ2' 

# Iniciar sesion en drive
def login():
    GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = directorio_credenciales
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(directorio_credenciales)
    
    if gauth.credentials is None:
        gauth.LocalWebserverAuth(port_numbers=[8092])
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()
        
    gauth.SaveCredentialsFile(directorio_credenciales)
    credenciales = GoogleDrive(gauth)
    return credenciales

# Subir un archivo a drive
def upload_file(path_file, id_folder):
    credenciales = login()
    file = credenciales.CreateFile({'parents': [{"kind": "drive#fileLink",\
                                                'id': id_folder}]})
    file['title'] = path_file.split("/")[-1]
    file.SetContentFile(file_path)
    file.Upload()
    
def main():
    # Leer los links del excel
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    column_data = df[column_name]
    videos = column_data.values
    
    # Descarga de videos de youtube y subida a drive
    for link_video in videos:
        yt = YouTube(link_video)
        video = yt.streams.get_highest_resolution()
        video.download('./YT')
        upload_file(f'YT/{video.title}.mp4', id_folder)
        
if __name__ == '__main__':
    main()