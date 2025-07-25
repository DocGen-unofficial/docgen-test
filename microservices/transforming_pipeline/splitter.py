import pandas as pd
from components.python_to_text_conversion.filtering.source.cleaner_comments import cleaner
from components.md_to_txt.source.converter import FileConverter
from components.cleaning_and_transformation.source.text_cleaner import TextCleaner
from components.python_to_text_conversion.llm_explainer.source.python_explainer import CodeExplainer
import asyncio
import json

json_path = "C:\\desktopnoonedrive\\docgenofficial\\AIDocGen\\microservices\\transforming_pipeline\\pipeline_extensions.json"
input_path = "C:\\desktopnoonedrive\\docgenofficial\\AIDocGen\\docgen-unofficial-docgen-test_part_0.parquet"

with open(json_path, "r", encoding="utf-8") as f:
    EXTENSIONS = json.load(f)


class ManageTransforming():
    def __init__(self, input_path: str, keep_comments: bool):
        self.input_path, self.keep_comments = input_path, keep_comments
        self.__read_parquet()
        self.__run()

    def __read_parquet(self):
        self.df = pd.read_parquet(self.input_path)

    def __filter_extension(self, extensions) -> pd.DataFrame:
        """
        Filter the DataFrame for the specified extensions.
        """
        mask = self.df['name'].apply(lambda x: any(str(x).endswith(ext) for ext in extensions))
        return self.df[mask]

    def __run(self):
        """
        Avvia la pipeline per i tipi di file specificati.
        """
        for key, value in EXTENSIONS.items():
            if key == 'file_converter':
                self.df_files_to_txt = asyncio.run(FileConverter(self.__filter_extension(value), value).file_to_text())
            elif key == 'python_to_text':
                self.df_py_to_txt = self.__filter_extension(value)
                if not self.keep_comments:
                    self.df_py_to_txt['content'] = cleaner(self.df_py_to_txt['content'])
                    self.df_py_to_txt = CodeExplainer().explain_dataframe(self.df_py_to_txt)
            elif key == 'text_cleaner':
                self.df3 = self.__filter_extension(value)
                self.df_text_cleaner = TextCleaner(self.df3).save_cleaned_df()
            else:
                pass

    def final_df(self) -> pd.DataFrame:
        return  pd.concat([self.df_files_to_txt, self.df_py_to_txt, self.df_text_cleaner]).reset_index(drop=True)

df = ManageTransforming(input_path, False).final_df()
df.to_parquet("C:\\desktopnoonedrive\\docgenofficial\\AIDocGen\\trans_pipeline_output.parquet", index=False)
print(df)