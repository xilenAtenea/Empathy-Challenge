import pandas as pd

class FeatureEngineer:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def create_is_over_50(self):
        self.df["es_mayor_50"] = self.df["edad"].apply(lambda x: 1 if pd.notna(x) and x > 50 else 0)
        return self.df

    def create_has_diagnosis(self):
        diag_cols = ["diagnostico_1", "diagnostico_2", "diagnostico_3"]
        self.df["tiene_diagnosticos"] = self.df[diag_cols].apply(
            lambda row: any(val.lower() != "unknown" for val in row if pd.notna(val)), axis=1).astype(int)
        return self.df

    def create_multiple_diagnoses(self):
        diag_cols = ["diagnostico_1", "diagnostico_2", "diagnostico_3"]
        self.df["multiples_diagnosticos"] = self.df[diag_cols].apply(
            lambda row: sum(val.lower() != "unknown" for val in row if pd.notna(val)) > 1, axis=1).astype(int)
        return self.df

    def create_work_disease_risk(self):
        cols = [
            "enfermedades_del_ojo_y_sus_anexos",
            "signos_y_hallazgos_anormales_clinicos_y_de_laboratorio",
            "enfermedades_del_sistema_osteomuscular_y_del_tejido_conectivo"
        ]
        self.df["riesgo_enfermedades_laborales"] = self.df[cols].any(axis=1).astype(int)
        return self.df

    def create_high_absence(self):
        self.df["dias_perdidos_alto"] = self.df["dias_perdidos"].apply(
            lambda x: 1 if pd.notna(x) and x > 10 else 0)
        return self.df

    def create_main_diagnosis_group(self):
        def extract_group(code):
            if pd.isna(code) or code.lower() == "unknown":
                return "NA"
            return str(code).strip().upper()[0]

        self.df["diagnostico_principal_categoria"] = self.df["diagnostico_1"].apply(extract_group)
        return self.df

    def run_all(self):
        self.create_is_over_50()
        self.create_has_diagnosis()
        self.create_multiple_diagnoses()
        self.create_work_disease_risk()
        self.create_high_absence()
        self.create_main_diagnosis_group()
        return self.df