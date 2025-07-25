import streamlit as st
import requests
import time

class FrontEnd():
    def __init__(self):
        st.set_page_config(
            page_title="DocGen",
            page_icon="🤖",
        )
        st.title("Document Generation")
        st.sidebar.success("Settings")
        self.__add_select_box()
        self.__add_description()
        self.__add_form()

    def __add_select_box(self):
        self.option = st.sidebar.selectbox( 
            "Keep comments",
            ['Yes', 'No']
        )
    
    def __add_description(self):
        st.markdown(
            """
            DocGen è un'applicazione che ti consente di generare documentazione funzionale e tecnica incollando semplicemente l'URL di un repository pubblico o privato.
            """
        )
    
    def __add_form(self):
        with st.form("login_form"):
            self.url_repository = st.text_input("Link Repository")
            self.token = st.text_input("Token", type="password")
            submit = st.form_submit_button("Genera")

        if submit:
            if self.url_repository:
                st.success("Start!")
                self.__pipeline()
            else:
                st.error("You must fill in the required fields.")

    def __pipeline(self):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        total_steps = 3
        
        try:
            status_text.text("Step 1/3: Downloading repository...")
            progress_bar.progress(1/total_steps)
            
            response = requests.post("http://localhost:5001/v1/download_repository", 
                                 json={'repository': self.url_repository, 'token': self.token})
            
            if "Repository successfully cloned." != response.json()['message']:
                status_text.error(f"Errore Step 1: {response.json()['message']}")
                progress_bar.empty()
                return 
            
            status_text.text("Step 1/3: Repository scaricato con successo ✓")
            time.sleep(0.5) 
            
            status_text.text("Step 2/3: Uploading repository...")
            progress_bar.progress(2/total_steps)
            
            response = requests.post("http://localhost:5002/v2/repo/upload", 
                                    params={"repo_path": response.json()["path"]})
            
            if response.json()["status"] == "error":
                status_text.error(f"Errore Step 2: {response.json()['error']}")
                progress_bar.empty()
                return 
            
            container: str = response.json()["container_name"]
            status_text.text("Step 2/3: Upload completato con successo ✓")
            time.sleep(0.5)
            
            status_text.text("Step 3/3: Transforming to parquet...")
            progress_bar.progress(3/total_steps)
            
            response = requests.post("http://localhost:5003/v3/transform-container-to-parquet",
                                    json={'container_name': container, 'single_parquet': True})
            
            progress_bar.progress(1.0)
            
            st.info(f"Messaggio: {response.json()['message']}")
            st.info(f"Percorso Parquet: {response.json()['parquet_path']}")
            
        except requests.exceptions.RequestException as e:
            status_text.error(f"Errore di connessione: {str(e)}")
            progress_bar.empty()
        except KeyError as e:
            status_text.error(f"Errore nella risposta del server: chiave mancante {str(e)}")
            progress_bar.empty()
        except Exception as e:
            status_text.error(f"Errore imprevisto: {str(e)}")
            progress_bar.empty()

if __name__ == "__main__":
    FrontEnd()