import pandas as pd
from io import BytesIO

class ReportGenerator:
    @staticmethod
    def generate_excel(db):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df = pd.DataFrame([{"name": "test"}])
            df.to_excel(writer, sheet_name="Sites")
        output.seek(0)
        return output
