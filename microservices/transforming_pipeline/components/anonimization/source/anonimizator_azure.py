import os
import pandas as pd
from dotenv import load_dotenv
from openai import AzureOpenAI
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

class AnonimizatorAzure:
    """
    This class is used to anonymize a parquet file using 
    the Azure OpenAI API in parallel using gpt-4.1-mini model.

    Attributes:     
        subscription_key (str): Azure OpenAI API key
        api_version (str): Azure OpenAI API version
        azure_endpoint (str): Azure OpenAI API endpoint
        azure_model_deployment (str): Azure OpenAI API model deployment
        client (AzureOpenAI): Azure OpenAI API client
        script_dir (str): Script directory where the script is located 
        data_dir (str): Data directory where the input .parquet file is located
        input_file (str): Input .parquet file
        input_filename (str): Input filename of the input .parquet file
        output_filename (str): Output filename of the anonimized .parquet file
        output_file (str): Output .parquet anonimized file 
        df (pd.DataFrame): DataFrame converted from the input .parquet file
        SYSTEM_PROMPT (str): System prompt for the LLM
    """
    def __init__(self):
        load_dotenv()
        self.subscription_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.api_version = os.getenv("AZURE_OPENAI_VERSION")
        self.azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.azure_model_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
        
        #----------------------- TODO: change to the correct .parquet input file path ------------------------
        self.script_dir = os.path.dirname(os.path.abspath(__file__)) # TODO: 
        self.data_dir = os.path.join(self.script_dir, "..", "data") # TODO: 
        self.input_file = os.path.join(self.data_dir, "docgen-unofficial-docgen-test_part_0.parquet") # TODO: 
        self.input_filename = os.path.basename(self.input_file) # TODO: 
        self.output_filename = self.input_filename.replace(".parquet", "_anonimized.parquet") # TODO: 
        self.output_file = os.path.join(self.data_dir, self.output_filename) # TODO: 
        self.df = pd.read_parquet(self.input_file) # TODO: 
        #-----------------------------------------------------------------------------------------------------
        self.SYSTEM_PROMPT = (
            """
            You are a data anonymization assistant. 
            
            When given any text (including code, logs, documents, emails, 
            or any unstructured content), 
            
            identify and replace all personal information (PII) such as names, emails, 
            phone numbers, addresses, as well as any API keys, access tokens, secrets, passwords, and credentials 
            with a clear generic placeholder. 

            Use tags like: 
            <PERSON>, <EMAIL>, <PHONE_NUMBER>, <ADDRESS>, <API_KEY>, 
            <TOKEN>, <PASSWORD> as appropriate. 

            Do not change anything else in the text. Do not add comments, explanations, 
            or output formatting. 
            
            Only return the anonymized version of the text.
            """
        )

    def llm_parquet_anonimizer(self, text: str) -> str:
        """
        Anonymizes a given text using the Azure OpenAI API model gpt-4o-mini.

        Args:
            text (str): The text to anonymize with pii information 
            and api keys/tokens/secrets/passwords/etc.

        Returns:
            text (str): The anonymized text without pii information 
            and api keys/tokens/secrets/passwords/etc.
        """
        messages = [
            {"role": "system", "content": self.SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ]
        
        client = AzureOpenAI(
        api_version=self.api_version,
        azure_endpoint=self.azure_endpoint,
        api_key=self.subscription_key,
        )           

        response = client.chat.completions.create(
            model=self.azure_model_deployment,
            temperature=0,
            messages=messages,
        )
        return response.choices[0].message.content.strip()

    def parallel_anonimization(self, df: pd.DataFrame) -> None:
        """
        Anonymize a parquet file using the Azure OpenAI API.

        Args:
            df (pd.DataFrame): The DataFrame containing the data from the file parquet to anonymize

        Returns:
            None
        """
        #---- Test -----
        test_row = {"name": ".env", "content": "api_key=akd1239u8190ue101jodjakn1090123098dyq"}
        df = pd.concat([pd.DataFrame([test_row]), df], ignore_index=True)
        #---------------
        
        texts = df["content"].tolist()
        max_workers = 16 
        results = [None] * len(texts)

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_idx = {executor.submit(self.llm_parquet_anonimizer, text): idx for idx, text in enumerate(texts)}

            for future in tqdm(as_completed(future_to_idx), total=len(future_to_idx), desc="Anonimizing files ..."):
                idx = future_to_idx[future]

                try:
                    result = future.result()

                except Exception as exc:
                    print(f"Error in the row {idx}: {exc}")
                    result = texts[idx] 
                    continue 
                results[idx] = result

        df["content"] = results
        # df.to_parquet(self.output_file, index=False) # TODO: where to save?

        return df

if __name__ == "__main__":
    anonimizator = AnonimizatorAzure()
    anonimizator.parallel_anonimization(anonimizator.df)





