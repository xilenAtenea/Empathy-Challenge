import re
import unidecode
import unicodedata
import pandas as pd
import csv
import io

class DataPreprocessor:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.original_columns = df.columns.tolist()
        self.column_mapping = {}

    def _clean_column_name(self, name: str) -> str:
        original = str(name)
        name = unidecode.unidecode(original)
        name = re.sub(r'(?<=[a-z])(?=[A-Z])', '_', name)
        name = re.sub(r'(?<=[A-Z])(?=[A-Z][a-z])', '_', name)
        name = name.lower()
        name = re.sub(r"[\"']", "", name)
        name = re.sub(r"[^a-z0-9]+", "_", name)
        name = re.sub(r"_+", "_", name)
        name = name.strip("_")
        self.column_mapping[original] = name
        return name

    def clean_column_names(self):
        cleaned_names = [self._clean_column_name(col) for col in self.df.columns]
        self.df.columns = cleaned_names

        manual_rename = {
            "signos_vitales_im_cinterpretacion": "signos_vitales_imc_interpretacion",
            "tantefumar": "tiempo_ante_fumar",
            "tabstifumar": "tiempo_abstinencia_fumar",
            "tbeber": "tiempo_beber",
            "tabstialcohol": "tiempo_abstinencia_alcohol",
            "td_examen": "tipo_examen",
            "dx1_examen": "diagnostico_1",
            "dx2_examen": "diagnostico_2",
            "dx3_examen": "diagnostico_3"
        }
        self.df.rename(columns=manual_rename, inplace=True)
        self.column_mapping.update(manual_rename)

        return self.df
    
    def get_column_mapping(self):
        # Devuelve el mapeo original -> limpio. Revisar cómo quedaron las columnas.
        return self.column_mapping
    
    def get_null_summary(self):
        null_summary = self.df.isnull().sum().sort_values(ascending=False)
        null_summary = null_summary[null_summary > 0]
        return null_summary
        
    def detect_malformed_rows(self, null_threshold=0.8):
        null_rows_threshold = int(len(self.df.columns) * null_threshold)
        null_per_row = self.df.isnull().sum(axis=1)
        return self.df[null_per_row >= null_rows_threshold].index

    def fix_malformed_rows(self, null_threshold=0.8):
        malformed_rows = self.detect_malformed_rows(null_threshold)
        print(f"Filas corregidas: {len(malformed_rows)}")

        for idx in malformed_rows:
            raw_text = str(self.df.iloc[idx, 0])

            fixed_values = next(csv.reader(io.StringIO(raw_text))) # con csv porque hay un valor que tiene una coma en medio del string (profesion) y si se hace split por coma obtendré un valor extra que no va

            print(f"Fila {idx} corregida:", fixed_values)
            print(type(fixed_values))
            print(len(fixed_values), len(self.df.columns))

            if len(fixed_values) == len(self.df.columns):
                self.df.loc[idx, :] = pd.Series(fixed_values, index=self.df.columns)

        return self.df

    def convert_column_types(self):
        date_cols = ["fecha_nacimiento", "fecha_de_examen"]
        for col in date_cols:
            if col in self.df.columns:
                self.df[col] = pd.to_datetime(self.df[col], errors="coerce")

        boolean_cols = [
            "enfermedades_del_ojo_y_sus_anexos", "sintomas",
            "signos_y_hallazgos_anormales_clinicos_y_de_laboratorio",
            "no_clasificados_en_otra_parte",
            "enfermedades_del_sistema_osteomuscular_y_del_tejido_conectivo",
            "enfermedades_endocrinas", "fuma", "bebealcohol", "ante_alcohol",
            "actifisica", "siesta"
        ]
        for col in boolean_cols:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(self.df[col], errors="coerce")
                self.df[col] = self.df[col].map(lambda x: True if x == 1 else (False if x == 0 else pd.NA)).astype("boolean")

        numeric_cols = [
            "edad", "ndependientes", "horas_sueno", "duracion_siesta",
            "signos_vitales_tensionarterialsistolica", "signos_vitales_tensionarterialdiastolica",
            "signos_vitales_pulso", "signos_vitales_frecuenciacardiaca", "signos_vitales_frecuenciarespiratoria",
            "signos_vitales_talla", "signos_vitales_peso", "signos_vitales_imc",
            "tiempo_ante_fumar", "tiempo_abstinencia_fumar",
            "tiempo_beber", "tiempo_abstinencia_alcohol",
            "tact_fisica", "atenciones", "dias_perdidos"
        ]
        for col in numeric_cols:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(self.df[col], errors="coerce")

        categorical_cols = [
            "genero", "grupo_etareo", "sede", "cedula", "hemo", "estado_civil", "escolaridad",
            "profesion", "estrato", "area",  "t_fumar", "ante_fumar",
            "tipo_actifisica", "tipo_examen",
            "signos_vitales_dominancia", "signos_vitales_contextura",
            "signos_vitales_tensionarterialsistolica_interpretacion",
            "signos_vitales_tensionarterialdiastolica_interpretacion",
            "signos_vitales_interpretacionmedico", "signos_vitales_imc_interpretacion",
            "diagnostico_1", "diagnostico_2", "diagnostico_3", "frec_actifisica", "frec_alcohol"
        ]
        for col in categorical_cols:
            if col in self.df.columns:
                self.df[col] = self.df[col].astype("category")

        print("Conversión completada")
        return self.df
    
    def assign_age_group(self):
        def calculate_age_group(edad):
            if pd.isnull(edad):
                return "Unknown"
            elif edad < 20:
                return "0-19"
            elif edad < 30:
                return "20-29"
            elif edad < 40:
                return "30-39"
            elif edad < 50:
                return "40-49"
            elif edad < 60:
                return "50-59"
            else:
                return "60+"

        self.df["grupo_etareo"] = self.df["edad"].apply(calculate_age_group)
        return self.df
    
    def drop_uninformative_columns(self, drop_manual=None):
        cols_to_drop = []

        all_nan = self.df.columns[self.df.isnull().all()].tolist() # Columnas 100% NaN
        cols_to_drop.extend(all_nan)

        if drop_manual:
            cols_to_drop.extend(drop_manual)

        self.df.drop(columns=cols_to_drop, inplace=True)

        print(f"Columnas eliminadas: {cols_to_drop}")
        return self.df
    
    def normalize_text_columns(self, columns=None):
        if columns is None:
            columns = self.df.select_dtypes(include=["object", "category"]).columns

        for col in columns:
            self.df[col] = (
                self.df[col]
                .astype(str)
                .apply(lambda x: unicodedata.normalize("NFKD", x).encode("ascii", "ignore").decode("utf-8"))
                .str.lower()
                .str.strip()
                .replace("nan", pd.NA)
            )
            print(f"Normalized '{col}'")

        if "sede" in self.df.columns:
            self.df["sede"] = self.df["sede"].replace("bogot", "bogota")
    
        return self.df

    
    def run_all(self):
        self.clean_column_names()
        self.drop_uninformative_columns()
        self.fix_malformed_rows()
        # self.drop_uninformative_columns(drop_manual=["frec_alcohol", "frec_actifisica"])
        self.convert_column_types()
        self.assign_age_group()
        self.normalize_text_columns()

        return self.df
