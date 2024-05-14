import pandas as pd

new_csv = pd.read_csv("UsuariosCadastrados.csv")

print(new_csv["NOME"])