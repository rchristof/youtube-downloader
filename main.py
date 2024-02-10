import streamlit as st
from pytube import YouTube, Playlist
import os
import string
import shutil
import zipfile
import time

# Função para baixar um vídeo do YouTube


def baixar_video(url, pasta_destino):
    try:
        if 'playlist' in url:
            playlist = Playlist(url)

            # Criar uma pasta para a playlist
            nome_pasta_playlist = os.path.join(pasta_destino, playlist.title)
            os.makedirs(nome_pasta_playlist, exist_ok=True)

            for video in playlist.videos:
                nome_arquivo = ''.join(
                    c for c in video.title if c in string.ascii_letters + string.digits + ' -_.') + ".mp4"
                video.streams.get_highest_resolution().download(
                    output_path=nome_pasta_playlist, filename=nome_arquivo)
            st.success(
                f"Todos os vídeos da playlist '{playlist.title}' foram baixados com sucesso!")
        else:
            yt = YouTube(url)
            video = yt.streams.get_highest_resolution()
            nome_arquivo = ''.join(
                c for c in yt.title if c in string.ascii_letters + string.digits + ' -_.') + ".mp4"
            video.download(output_path=pasta_destino, filename=nome_arquivo)
            st.success(f"Vídeo '{yt.title}' baixado com sucesso!")
    except Exception as e:
        st.error(f"Ocorreu um erro durante o download: {str(e)}")


# Configuração da página do Streamlit
st.title("Baixar Vídeos do YouTube")

# Entrada das URLs dos vídeos
st.write("Insira as URLs dos vídeos do YouTube separadas por quebras de linha:")
urls = st.text_area("URLs dos vídeos", height=200)

# Botão para iniciar o download dos vídeos
if st.button("Baixar Vídeos"):
    if urls.strip() == "":
        st.warning("Por favor, insira as URLs dos vídeos.")
    else:
        # Criar uma pasta temporária para armazenar os arquivos
        pasta_temporaria = "videos_temporarios"
        os.makedirs(pasta_temporaria, exist_ok=True)

        # Divide as URLs em uma lista
        lista_urls = urls.strip().split('\n')

        # Mostrar a fila de downloads dentro de um expander
        with st.expander("Fila de Downloads"):
            for url in lista_urls:
                if 'playlist' in url:
                    st.write(f"Playlist: {Playlist(url).title}")
                else:
                    try:
                        st.write(f"Vídeo: {YouTube(url).title}")
                    except:
                        st.write(f"URL: {url}")
                with st.spinner(text="Baixando..."):
                    baixar_video(url, pasta_temporaria)

        # Compactar os arquivos em um arquivo zip
        with zipfile.ZipFile('videos.zip', 'w') as zipf:
            for root, dirs, files in os.walk(pasta_temporaria):
                for file in files:
                    zipf.write(os.path.join(root, file), os.path.relpath(
                        os.path.join(root, file), pasta_temporaria))

        st.success(
            "Todos os vídeos foram baixados e compactados em 'videos.zip'.")

        # Remover a pasta temporária
        shutil.rmtree(pasta_temporaria)
