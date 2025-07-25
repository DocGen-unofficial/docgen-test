import os
from typing import Any
import pandas as pd
from openai import AzureOpenAI
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed
from .utils.prompt import SYSTEM_PROMPT

class CodeExplainer:
    """
    A class that manages interaction with Azure OpenAI to transform Python code
    into detailed natural language explanations, replacing the content of a DataFrame.
    """

    def __init__(self, system_prompt: str = SYSTEM_PROMPT, max_workers: int = 16) -> None:
        load_dotenv()
        self.client = AzureOpenAI(
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        )
        self.model = os.getenv("AZURE_OPENAI_DEPLOYMENT")
        self.system_prompt = system_prompt
        self.max_workers = max_workers

    def explain_code(self, code: str) -> str:
        """
        Sends a code string to the LLM and retrieves the explanation.
        """
        response = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": code},
            ],
            temperature=0,
            model=self.model
        )
        return response.choices[0].message.content

    def _process_row(self, row: pd.Series) -> str:
        print(f"Explaining: {row['name']}")
        return self.explain_code(row["content"])

    def explain_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Iterates over a DataFrame with columns 'name' and 'content', replacing
        'content' with its explanation using parallel processing.
        """
        explained_contents = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(self._process_row, row): idx
                for idx, row in df.iterrows()
            }
            for future in as_completed(futures):
                explained_contents.append(future.result())
        return pd.DataFrame({"name": df["name"], "content": explained_contents})
