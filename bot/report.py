import json
import pandas as pd
from io import BytesIO
from typing import Any, List
from repository.models import DietRegister
class Report(object):
    def __init__(self, diet_history: List[DietRegister]) -> None:
        self.diet_history = diet_history

    def mark_down(self) -> str:
        if not self.diet_history:
            return "📉 Nenhum registro de dieta encontrado para o período especificado."

        def format_item(item):
            # Formatação dos valores com duas casas decimais
            return (f"  - {item.product}: {item.grams:.2f}g | {item.calories:.2f}kcal | "
                    f"{item.carbohydrates:.2f}g | {item.fats:.2f}g | {item.proteins:.2f}g\n")

        res = ["📅 **Relatório de Dieta**\n"]
        total_calories = total_carbs = total_fats = total_proteins = 0

        for di in self.diet_history:
            header = f"🍽️ **{di.description}** - _{di.created_at.strftime('%d/%m/%Y %H:%M')}_\n"
            items_details = [format_item(item) for item in di.items]
            day_totals = {
                'calories': sum(item.calories for item in di.items),
                'carbs': sum(item.carbohydrates for item in di.items),
                'fats': sum(item.fats for item in di.items),
                'proteins': sum(item.proteins for item in di.items)
            }
            total_calories += day_totals['calories']
            total_carbs += day_totals['carbs']
            total_fats += day_totals['fats']
            total_proteins += day_totals['proteins']

            # Formatação dos totais diários com duas casas decimais
            totals_line = (f"    🔹 Totais: 🍔 {day_totals['calories']:.2f}kcal, "
                        f"🥖 {day_totals['carbs']:.2f}g, 🧈 {day_totals['fats']:.2f}g, 🍗 {day_totals['proteins']:.2f}g\n")
            res.append(header + "".join(items_details) + totals_line + "\n")

        # Formatação dos totais gerais com duas casas decimais
        grand_totals = (f"🔥 **Totais Gerais**: 🍔 {total_calories:.2f}kcal, "
                        f"🥖 {total_carbs:.2f}g, 🧈 {total_fats:.2f}g, 🍗 {total_proteins:.2f}g\n")
        res.append(grand_totals)

        return "".join(res)

        
    def to_excel(self) -> BytesIO:
        data = []
        for register in self.diet_history:
            for item in register.items:
                data.append({
                    "Descrição": register.description,
                    "Produto": item.product,
                    "Gramas": item.grams,
                    "Calorias": item.calories,
                    "Carboidratos": item.carbohydrates,
                    "Gorduras": item.fats,
                    "Proteínas": item.proteins,
                    "Data registro": register.created_at.strftime('%d/%m/%Y %H:%M')
                })
        
        df = pd.DataFrame(data)
        excel_file = BytesIO()
        with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Histórico de dieta')
        excel_file.seek(0)
        return excel_file      
    
    def to_json(self) -> str:
        data = []
        for register in self.diet_history:
            data.append(register.to_dict_plain())
        json_text = json.dumps(data, ensure_ascii=False, indent=2)
        res = f"Aqui está o JSON:\n```\n{json_text}\n```\nVocê pode devolver um registro específico aqui e solicitar sua alteração, se assim desejar."
        return res