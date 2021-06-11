import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("/Projeto Faculdade/Final.csv", header=None, index_col=0)
columns = ["nomeanimal", "estado", "idade", "nomeescola", "senhafinal", "loginfinal", "renda",
           "trabalho", "sexo", "imc", "cep", "email", "user"]
df.columns = columns
df_describe = df.describe()
df_describe.drop(['senhafinal'], axis=1, inplace=True)
print(df_describe)

# plt.subplot(3, 3, 1)
plt.title('Histograma de idades')
plt.hist(df['idade'])
plt.vlines(df['idade'].mean(), 0, len(df) / 2, colors='red', label='idade média')
plt.grid()
plt.legend()
plt.show()
# plt.subplot(2, 1, 1)
plt.title('Histograma de renda')
plt.hist(df['renda'])
plt.vlines(df['renda'].mean(), 0, len(df) / 2, colors='red', label='renda média')
plt.grid()
plt.legend()
plt.show()
# plt.subplot(1, 3, 1)
plt.title('Histograma de Indice de Massa Corporal')
plt.hist(df['imc'])
plt.vlines(df['imc'].mean(), 0, len(df) / 2, colors='red', label='IMC médio')
plt.grid()
plt.legend()
plt.tight_layout()
plt.show()

homens = len(df[df['sexo'] == 'M'])
mulheres = len(df[df['sexo'] == 'F'])

plt.title('Sexo dos usuários')
plt.pie([homens, mulheres], labels=['Homens', 'Mulheres'], autopct='%1.0f%%')
plt.show()
